import asyncio
import os
import re
from typing import Any, TYPE_CHECKING
import zipfile

from CommonClient import gui_enabled, logger
from CommonClient import get_base_parser, handle_url_arg, server_loop
from MultiServer import mark_raw
from settings import Settings, get_settings
from Utils import async_start, get_intended_text, open_filename, tuplize_version

# Import Context and CommandProcessor from CommonClient when TrackerClient is not available, or for type checking
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext  # type: ignore
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as ClientCommandProcessor  # type: ignore
except ModuleNotFoundError:
    from CommonClient import CommonContext, ClientCommandProcessor
if TYPE_CHECKING:
    from CommonClient import CommonContext, ClientCommandProcessor

from .EnemyRando import EnemyRandoManager
from .Items import item_table, item_display_name_to_key
from .Options import HintResearchProjects
from .Proxy import run_proxy
from .Settings import X2WOTCSettings
from .Version import CLIENT_NAME, GAME_NAME, client_version, client_minimum_mod_version, client_minimum_world_version

from .mods import mods_data, mod_names


class X2WOTCCommandProcessor(ClientCommandProcessor):
    ctx: "X2WOTCContext"

    def _cmd_version(self) -> bool:
        """Print client version info"""
        self.output(f"Client version: {client_version}")
        self.output(f"Minimum world version: {client_minimum_world_version}")
        self.output(f"Minimum mod version: {client_minimum_mod_version}")

        if self.ctx.connected.is_set():
            world_version = self.ctx.slot_data["world_version"]
            self.output(f"Connected world version: {world_version}")
            self.output(f"Connected mod version: {self.ctx.mod_version}")
        else:
            self.output("Connect to a slot for more information.")

        return True

    def _cmd_proxy(self, port: str = "") -> bool:
        """Restart the proxy server at the specified port"""
        if port == "":
            self.output(f"Current proxy port: {self.ctx.proxy_port}")
            return False

        try:
            port = int(port)
        except ValueError:
            self.output("Invalid port number (not an integer).")
            return False

        if port < 0 or port > 65535:
            self.output("Port number out of range (0 to 65535).")
            return False

        self.ctx.proxy_port = port
        self.ctx.start_proxy()
        self.output("Config updated. Please restart your game if it is already running.")
        return True

    @mark_raw
    def _cmd_game_path(self, path: str = "") -> bool:
        """Set the game_path stored in host.yaml"""
        if path == "":
            self.output(self.ctx.settings["x2wotc_options"]["game_path"])
            self.ctx.settings.save()
            return False

        if self.ctx.connected.is_set():
            self.output("Cannot set game_path while connected to a slot.")
            return False

        if not os.path.isdir(path):
            self.output("Could not set game_path, invalid path given. Note that quotes should not be used.")
            return False

        self.ctx.settings["x2wotc_options"]["game_path"] = path
        self.ctx.settings.save()
        self.output("New game_path saved.")
        return True

    @mark_raw
    def _cmd_workshop_path(self, path: str = "") -> bool:
        """Set the workshop_path stored in host.yaml, you can most likely ignore this"""
        if path == "":
            self.output(self.ctx.settings["x2wotc_options"]["workshop_path"])
            self.ctx.settings.save()
            return False

        if self.ctx.connected.is_set():
            self.output("Cannot set workshop_path while connected to a slot.")
            return False

        if not os.path.isdir(path):
            self.output("Could not set workshop_path, invalid path given. Note that quotes should not be used.")
            return False

        self.ctx.settings["x2wotc_options"]["workshop_path"] = path
        self.ctx.settings.save()
        self.output("New workshop_path saved.")
        return True

    def _cmd_reset_paths(self) -> bool:
        """Reset game_path and workshop_path to their default values"""
        if self.ctx.connected.is_set():
            self.output("Cannot reset paths while connected to a slot.")
            return False

        self.ctx.settings["x2wotc_options"]["game_path"] = X2WOTCSettings.game_path
        self.ctx.settings["x2wotc_options"]["workshop_path"] = X2WOTCSettings.workshop_path
        self.ctx.settings.save()
        self.output("Reset game_path and workshop_path to default values:")
        self.output(X2WOTCSettings.game_path)
        self.output(X2WOTCSettings.workshop_path)
        return True

    def _cmd_mods(self) -> bool:
        """List all installed and active mods"""
        if mod_names:
            self.output("Installed mods:")
            for mod_name in mod_names:
                self.output(f"- {mod_name}")
        else:
            self.output("No installed mods found.")

        if self.ctx.active_mods:
            self.output("Active mods:")
            for mod_name in self.ctx.active_mods:
                self.output(f"- {mod_name}")

            missing_mods = [mod_name for mod_name in self.ctx.active_mods if mod_name not in mod_names]
            if missing_mods:
                self.output("These mods are active but not installed:")
                for mod_name in missing_mods:
                    self.output(f"- {mod_name}")
                self.output("Please use the same apworld that was used to generate the multiworld.")
        else:
            self.output("No active mods found.")

        return True

    def _cmd_install_mod(self) -> bool:
        """Install a mod"""
        mod_path = open_filename("Select mod file", [("x2wotc mod", [".py", ".zip"])])
        if not mod_path:
            self.output("No file selected.")
            return False

        apworld_path = f"{__file__.split(".apworld")[0]}.apworld"
        arcname = f"x2wotc/mods/{os.path.basename(mod_path)}"
        with zipfile.ZipFile(apworld_path, "a") as apworld_file:

            # If the mod is a .py file, add it directly to the archive
            if mod_path.endswith(".py"):
                apworld_file.write(mod_path, arcname=arcname)

            # If the mod is a .zip file, extract its contents and add them to the archive
            if mod_path.endswith(".zip"):
                with zipfile.ZipFile(mod_path, "r") as mod_zip_file:
                    for file_name in mod_zip_file.namelist():
                        arcname = f"x2wotc/mods/{file_name}"
                        with mod_zip_file.open(file_name) as file:
                            apworld_file.writestr(arcname, file.read())

        self.output("Mod installed. Please restart the client.")
        return True

    def _cmd_clear_mods(self) -> bool:
        """Uninstall all mods"""
        apworld_path = f"{__file__.split(".apworld")[0]}.apworld"
        temp_path = f"{apworld_path}.tmp"

        with zipfile.ZipFile(apworld_path, "r") as apworld_file:
            with zipfile.ZipFile(temp_path, "w") as temp_file:
                for file_name in apworld_file.namelist():
                    if not file_name.startswith("x2wotc/mods/") or file_name == "x2wotc/mods/__init__.py":
                        with apworld_file.open(file_name) as file:
                            temp_file.writestr(file_name, file.read())
        os.replace(temp_path, apworld_path)

        self.output("All mods uninstalled. Please restart the client.")
        return True

    @mark_raw
    def _cmd_stages(self, progressive_item: str = "") -> bool:
        """Print progressive item stages"""
        progressive_items = [
            item_data.display_name
            for item_data in item_table.values()
            if item_data.stages is not None
        ]

        if progressive_item == "":
            self.output("All progressive items:")
            for item_name in progressive_items:
                self.output(f"- {item_name}")
            return True

        result, usable, response = get_intended_text(progressive_item, progressive_items)
        if not usable:
            self.output(response)
            self.ctx.ui.last_autofillable_command = "/stages"
            return False

        item_key = item_display_name_to_key[result]
        stages = item_table[item_key].stages
        if not stages:
            self.output(f"No stages for progressive item '{result}'.")
            return True

        self.output(f"Stages for progressive item '{result}':")
        for stage in stages:
            stage_name = item_table[stage].display_name if stage in item_table else "Nothing"
            self.output(f"- {stage_name}")
        return True


class X2WOTCContext(CommonContext):
    command_processor = X2WOTCCommandProcessor
    game = GAME_NAME
    items_handling = 0b111  # full remote
    tags = {"AP"}

    settings: Settings = get_settings()

    class DualEvent:
        def __init__(self):
            self._set_event = asyncio.Event()
            self._clear_event = asyncio.Event()
            self._clear_event.set()

        def set(self):
            self._set_event.set()
            self._clear_event.clear()

        def clear(self):
            self._set_event.clear()
            self._clear_event.set()

        def is_set(self):
            return self._set_event.is_set()

        def wait(self):
            return self._set_event.wait()

        def wait_clear(self):
            return self._clear_event.wait()

    connected: DualEvent
    scouted: DualEvent

    proxy_port: int
    proxy_task: asyncio.Task | None

    slot_data: dict[str, Any]
    active_mods: list[str]

    enemy_rando_manager: EnemyRandoManager

    config_file: str | None
    spoiler_file: str | None
    encounters_file: str | None
    encounter_lists_file: str | None
    mod_version: str | None
    mod_minimum_client_version: str | None

    def __init__(self, server_address: str | None, password: str | None):
        super().__init__(server_address, password)
        self.locations_checked = set()
        self.locations_scouted = set()

        self.connected = self.DualEvent()
        self.scouted = self.DualEvent()

        self.proxy_port = 24728
        self.proxy_task = None

        self.slot_data = {}
        self.active_mods = []

        self.enemy_rando_manager = EnemyRandoManager()

        self.config_file = None
        self.spoiler_file = None
        self.encounters_file = None
        self.encounter_lists_file = None
        self.mod_version = None
        self.mod_minimum_client_version = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)
        if self.connected.is_set():
            self.reset_config()
        self.connected.clear()
        self.scouted.clear()
        self.locations_scouted = set()
        self.slot_data = {}
        self.active_mods = []

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)

        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            if not self.validate_world_version():
                async_start(self.disconnect())
                return

            self.active_mods = sorted(self.slot_data.get("active_mods", []))
            self.enemy_rando_manager.set_enemy_shuffle(self.slot_data["enemy_shuffle"])
            if not self.validate_mod_config_and_version():
                async_start(self.disconnect())
                return

            self.connected.set()
            self.patch_config()
            self.update_config()
            self.patch_encounters()
            self.print_info("Client connected and config updated. Please restart your game if it is already running.")

        elif cmd == "LocationInfo":
            scouted_locations = set(item.location for item in args["locations"])
            if self.locations_scouted == scouted_locations:
                self.scouted.set()

        # Help players who don't know to hint progressive items
        elif cmd == "PrintJSON":
            for message in args["data"]:
                text: str = message.get("text", "").rsplit('"', 1)[0]
                prefix = text.split('"', 1)[0]
                if prefix != "Nothing found for recognized item name ":
                    return

                item_name = text.split('"', 1)[1]
                item_key = item_display_name_to_key[item_name]
                progressive_item_names = [
                        item_data.display_name
                        for item_data in item_table.values()
                        if item_data.stages is not None and item_key in item_data.stages
                ]

                if progressive_item_names:
                    self.print_info("Try hinting one of the following items instead:")
                    for progressive_item_name in progressive_item_names:
                        self.print_info(f"- {progressive_item_name}")

    def validate_world_version(self) -> bool:
        world_version = self.slot_data["world_version"]
        world_minimum_client_version = self.slot_data["minimum_client_version"]

        if tuplize_version(world_version) < tuplize_version(client_minimum_world_version):
            self.print_error(
                f"Client version {client_version} requires "
                f"at least world version {client_minimum_world_version}, "
                f"but world was generated with version {world_version}. "
                "Please revert to an older version of the client."
            )
            return False

        if tuplize_version(client_version) < tuplize_version(world_minimum_client_version):
            self.print_error(
                f"World version {world_version} requires "
                f"at least client version {world_minimum_client_version}, "
                f"but client is version {client_version}. "
                "Please update to a newer version of the client."
            )
            return False

        return True

    def validate_mod_config_and_version(self) -> bool:
        manual_folders = ["WOTCArchipelago", "3281191663"]
        manual_exts = [
            f"/XCom2-WarOfTheChosen/XComGame/Mods/{manual_folder}/Config/XComWOTCArchipelago.ini"
            for manual_folder in manual_folders
        ]
        workshop_ext = "/content/268500/3281191663/Config/XComWOTCArchipelago.ini"  # after /steamapps/workshop

        # Check for the mod config file in possible manual installation locations first,
        # then fall back to the default Steam workshop installation path if it doesn't exist
        game_path: str = self.settings["x2wotc_options"]["game_path"]
        self.settings.save()
        for manual_ext in manual_exts:
            self.config_file = game_path + manual_ext
            if os.path.isfile(self.config_file):
                break
        else:
            workshop_path: str = game_path.split("/common/")[0] + "/workshop"
            self.config_file = workshop_path + workshop_ext

        # If this also fails, ask for a potential foreign Steam workshop path
        if not os.path.isfile(self.config_file):
            workshop_path: str = self.settings["x2wotc_options"]["workshop_path"]
            self.settings.save()
            self.config_file = workshop_path + workshop_ext

        # If this STILL fails, give up and print an error
        if not os.path.isfile(self.config_file):
            self.print_error(
                "Config file not found in game folder or Steam workshop folder. "
                "Please check and/or correct the game_path setting in your host.yaml "
                "or by using the /game_path client command "
                "and make sure the Archipelago game mod is installed."
            )
            return False

        self.spoiler_file = self.config_file.replace("XComWOTCArchipelago.ini", "XComWOTCArchipelago_Spoiler.ini")
        self.encounters_file = self.config_file.replace("XComWOTCArchipelago.ini", "XComEncounters.ini")
        self.encounter_lists_file = self.config_file.replace("XComWOTCArchipelago.ini", "XComEncounterLists.ini")

        if (not os.path.isfile(self.spoiler_file) or
            not os.path.isfile(self.encounters_file) or
            not os.path.isfile(self.encounter_lists_file)):
            self.print_error(
                "Some but not all config files found. This is most likely due to a version mismatch. "
                "Please install the required mod version as indicated by the /version client command."
            )
            return False

        # Retrieve mod version info from config file
        with open(self.config_file, "r") as file:
            config = file.read()

        match_mod_version = re.search(f"\nModVersion={r"(?P<mod_version>\S*)"}", config)
        match_minimum_client_version = re.search(f"\nMinimumClientVersion={r"(?P<minimum_client_version>\S*)"}", config)

        if not match_mod_version or not match_minimum_client_version:
            self.print_error(
                "Config file missing version information, most likely due to a corrupted mod installation. "
                "Please reinstall the XCOM 2 WotC Archipelago Multiworld mod."
            )
            return False

        self.mod_version = match_mod_version["mod_version"]
        self.mod_minimum_client_version = match_minimum_client_version["minimum_client_version"]

        # Validate mod version
        if tuplize_version(self.mod_version) < tuplize_version(client_minimum_mod_version):
            self.print_error(
                f"Client version {client_version} requires "
                f"at least mod version {client_minimum_mod_version}, "
                f"but mod is version {self.mod_version}. "
                "Please update to a newer version of the mod."
            )
            return False

        if tuplize_version(client_version) < tuplize_version(self.mod_minimum_client_version):
            self.print_error(
                f"Mod version {self.mod_version} requires "
                f"at least client version {self.mod_minimum_client_version}, "
                f"but client is version {client_version}. "
                "Please revert to an older version of the mod."
            )
            return False

        return True

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = CLIENT_NAME
        return ui

    def print_error(self, text: str):
        if self.ui:
            self.ui.print_json([{"text": text, "type": "color", "color": "red"}])
        else:
            logger.error(text)

    def print_info(self, text: str):
        if self.ui:
            self.ui.print_json([{"text": text, "type": "color", "color": "blue"}])
        else:
            logger.info(text)

    def start_proxy(self):
        if self.proxy_task:
            self.proxy_task.cancel()
        self.proxy_task = asyncio.create_task(run_proxy(self), name="proxy")
        if self.connected.is_set():
            self.update_config({"ProxyPort": str(self.proxy_port)})

    def patch_config(self):
        CLASS_PREFIX = "[WOTCArchipelago."
        CLASS_SUFFIX = "]"
        AUTO_CODE_BEGIN = "; MOD ENTRIES BEGIN\n"
        AUTO_CODE_END = "; MOD ENTRIES END\n"

        with open(self.config_file, "r") as file:
            config = file.read()

        insert_dict = {
            line[len(CLASS_PREFIX):-len(CLASS_SUFFIX)]: ""
            for line in config.splitlines()
            if line.startswith(CLASS_PREFIX) and line.endswith(CLASS_SUFFIX)
        }

        for mod_data in mods_data:
            if mod_data.name in self.active_mods:
                for key, value in mod_data.config.items():
                    if key not in insert_dict:
                        logger.warning(
                            f"X2WOTCClient: Class {key} for mod {mod_data.name} "
                            "not mentioned in config file, skipping"
                        )
                        continue
                    insert_dict[key] += f"{value}\n"

        for key, value in insert_dict.items():
            class_index = config.find(CLASS_PREFIX + key + CLASS_SUFFIX)

            auto_code_begin_index = config.find(AUTO_CODE_BEGIN, class_index) + len(AUTO_CODE_BEGIN)
            auto_code_end_index = config.find(AUTO_CODE_END, class_index)

            if auto_code_end_index != -1:
                config = config[:auto_code_begin_index] + value + config[auto_code_end_index:]

        with open(self.config_file, "w") as file:
            file.write(config)

    def update_config(self, config_values: dict[str, str] = {}):
        if not config_values:
            campaign_completion_requirements = self.slot_data.get("campaign_completion_requirements", [])
            hint_research_projects = self.slot_data.get("hint_research_projects", HintResearchProjects.default)
            skip_mission_types = self.slot_data.get("skip_mission_types", [])
            disable_covert_action_risks = self.slot_data.get("disable_covert_action_risks", [])
            config_values = {
                "ClientVersion": client_version,
                "MinimumModVersion": client_minimum_mod_version,
                "WorldVersion": self.slot_data["world_version"],
                "ProxyPort": str(self.proxy_port),
                "bRequirePsiGate": str("PsiGateObjective" in campaign_completion_requirements),
                "bRequireStasisSuit": str("StasisSuitObjective" in campaign_completion_requirements),
                "bRequireAvatarCorpse": str("AvatarCorpseObjective" in campaign_completion_requirements),
                "bRemoveCorpseCosts": str(self.slot_data.get("remove_corpse_costs", False)),
                "DEF_AP_GEN_ID": f"{"".join(self.slot_data["seed_name"].split())}_{self.slot_data["player"]}",
                "DEF_HINT_TECH_LOC_PART": str(hint_research_projects == HintResearchProjects.option_partial),
                "DEF_HINT_TECH_LOC_FULL": str(hint_research_projects == HintResearchProjects.option_full),
                "DEF_SKIP_SUPPLY_RAIDS": str("SupplyRaid" in skip_mission_types),
                "DEF_SKIP_COUNCIL_MISSIONS": str("CouncilMission" in skip_mission_types),
                "DEF_SKIP_FACTION_MISSIONS": str("ResistanceOp" in skip_mission_types),
                "DEF_DISABLE_AMBUSH_RISK": str("Ambush" in disable_covert_action_risks),
                "DEF_DISABLE_CAPTURE_RISK": str("Capture" in disable_covert_action_risks),
                "DEF_SKIP_RAID_REWARD_MULT_BASE": str(float(self.slot_data.get("supply_raid_reward_base", 0)) / 100.0),
                "DEF_SKIP_RAID_REWARD_MULT_ERR": str(float(self.slot_data.get("supply_raid_reward_error", 0)) / 100.0),
                "DEF_EXTRA_XP_MULT": str(float(self.slot_data.get("extra_xp_gain", 0)) / 100.0),
                "DEF_EXTRA_CORPSES": str(self.slot_data.get("extra_corpse_gain", 0)),
                "DEF_INSTANT_ROOKIE_TRAINING": str(self.slot_data.get("instant_rookie_training", False)),
                "DEF_INSTANT_SPARK_BUILDING": str(self.slot_data.get("instant_spark_construction", False)),
                "DEF_REFUND_SPARK_COST": str(self.slot_data.get("refund_spark_costs", False)),
                "DEF_REPLACE_FACTION_HERO": str(self.slot_data.get("replace_faction_heroes", False)),
                "DEF_NO_STARTING_TRAPS": str(self.slot_data.get("disable_day_one_traps", False)),
                "DEF_NO_STARTING_TRAPS_TACTICAL": str(self.slot_data.get("disable_turn_one_traps", False)),
            }

        with open(self.config_file, "r") as file:
            config = file.read()

        for key, value in config_values.items():
            config = re.sub(f"\n{re.escape(key)}={r"(\S*)"}", f"\n{key}={value}", config)

        with open(self.config_file, "w") as file:
            file.write(config)

    def reset_config(self):
        self.update_config({
            "ClientVersion": "",
            "MinimumModVersion": "",
            "WorldVersion": "",
            "DEF_AP_GEN_ID": "",
        })

    def patch_encounters(self):
        for file_path in [self.encounters_file, self.encounter_lists_file]:
            with open(file_path, "r") as file:
                old_lines = file.readlines()

            new_text = ""
            for old_line in old_lines:
                if not old_line.startswith("+"):
                    new_text += old_line

                if old_line.startswith("-"):
                    new_line = old_line.replace("-", "+", 1)
                    for placement_index, placed_index in enumerate(self.enemy_rando_manager.enemy_shuffle):
                        placement_enemy = self.enemy_rando_manager.enemy_names[placement_index]
                        new_line = re.sub(f'"{re.escape(placement_enemy)}"', f"[enemy_{placed_index}]", new_line, flags=re.IGNORECASE)
                    for placed_index, placed_enemy in enumerate(self.enemy_rando_manager.enemy_names):
                        new_line = new_line.replace(f"[enemy_{placed_index}]", f'"{placed_enemy}"')
                    new_text += new_line

            with open(file_path, "w") as file:
                file.write(new_text)

    def fill_spoiler(self, entries: list[dict[str, str | int]]):
        spoiler = "[WOTCArchipelago.WOTCArchipelago_Spoiler]\n"

        # Multiworld item placements
        for entry in entries:
            spoiler += (
                "+Spoiler=("
                f'Location="{entry["location"]}", '
                f'Item="{"".join(entry["item"].splitlines())}", '
                f'Player="{"".join(entry["player"].splitlines())}", '
                f'Game="{"".join(entry["game"].splitlines())}", '
                f"bProgression={bool(entry["flags"] & 0b001)}, "
                f"bUseful={bool(entry["flags"] & 0b010)}, "
                f"bTrap={bool(entry["flags"] & 0b100)})\n"
            )

        # Enemy rando
        if self.slot_data["enemy_rando"]:
            for placed_enemy in self.enemy_rando_manager.enemy_names:
                placement_enemy = self.enemy_rando_manager.get_placement_enemy(placed_enemy)
                spoiler += (
                    "+EnemyRando=("
                    f'DefaultTemplateName="{placement_enemy}", '
                    f'OverrideTemplateName="{placed_enemy}")\n'
                )

                # Stat changes
                stat_changes = self.enemy_rando_manager.get_stat_changes(placed_enemy)
                for stat_change in stat_changes:
                    spoiler += (
                        f"+CharStatChanges=("
                        f'TemplateName="{placed_enemy}", '
                        f'StatType="{stat_change.type}", '
                        f"Delta={stat_change.delta}, "
                        f"Minimum={stat_change.min}, "
                        f"Maximum={stat_change.max})\n"
                    )

        with open(self.spoiler_file, "w") as file:
            file.write(spoiler)


def launch(*args):
    async def main(args):
        ctx = X2WOTCContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server_loop")
        ctx.start_proxy()

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.proxy_task
        if ctx.connected.is_set():
            ctx.reset_config()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url.")
    parsed_args = handle_url_arg(parser.parse_args(args))

    colorama.just_fix_windows_console()
    asyncio.run(main(parsed_args))
    colorama.deinit()
