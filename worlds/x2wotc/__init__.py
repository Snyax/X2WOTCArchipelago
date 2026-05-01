import dataclasses
from logging import info, warning
from typing import Any, ClassVar, TextIO

from BaseClasses import CollectionState, Item, MultiWorld, Tutorial
from Options import OptionError, PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components
from worlds.LauncherComponents import launch as launch_component

from .EnemyRando import EnemyRandoManager
from .Items import ItemManager, X2WOTCItem, item_display_name_to_id, item_groups
from .LocationData import GOAL_VALUE_TO_LOCATION
from .Locations import LocationManager, loc_display_name_to_id, loc_groups
from .Options import AlienHuntersDLC, ChosenHuntSanity, ChosenWeaponFragments, EnemyPlandoPreset, X2WOTCOptions
from .Options import x2wotc_option_groups
from .Regions import RegionManager
from .Rules import RuleManager
from .Settings import X2WOTCSettings
from .Version import CLIENT_NAME, GAME_NAME, world_minimum_client_version

from .mods import mods_data


def launch_client(*args):
    from .Client import launch

    launch_component(launch, name=CLIENT_NAME, args=args)

components.append(Component(
    CLIENT_NAME,
    component_type=Type.CLIENT,
    func=launch_client,
    game_name=GAME_NAME,
    supports_uri=True
))


class X2WOTCWeb(WebWorld):
    theme = "partyTime"
    option_groups = x2wotc_option_groups
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the XCOM 2: War of the Chosen Archipelago mod.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Snyax"]
    )]


class X2WOTCWorld(World):
    """
    XCOM 2 is the sequel to the acclaimed turn-based tactics game about defending earth from an alien invasion.
    Outwit your enemy on the battlefield and beyond, hunt the powerful Chosen, and build up an unstoppable
    resistance to save humanity from the occupation of the Elders!
    """

    game = GAME_NAME
    web = X2WOTCWeb()

    settings: ClassVar[X2WOTCSettings]
    options_dataclass = X2WOTCOptions
    options: X2WOTCOptions

    option_names = [
        attr.name for attr in dataclasses.fields(options_dataclass)
        if attr not in dataclasses.fields(PerGameCommonOptions)
    ]

    item_name_to_id = item_display_name_to_id
    location_name_to_id = loc_display_name_to_id

    item_name_groups = item_groups
    location_name_groups = loc_groups

    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.enemy_rando_manager: EnemyRandoManager = EnemyRandoManager()
        self.item_manager: ItemManager = ItemManager()
        self.loc_manager: LocationManager = LocationManager(self)  # Location manager requires enemy rando manager
        self.rule_manager: RuleManager = None  # Rule manager is initialized in generate_early
        self.reg_manager: RegionManager = None  # Region manager requires rule manager

    def generate_early(self):
        # Extract slot data for UT re-gen
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data = re_gen_passthrough[self.game]
            for option_name in self.option_names:
                if option_name in slot_data:
                    getattr(self.options, option_name).value = slot_data[option_name]

            # Enemy rando
            self.enemy_rando_manager.set_enemy_shuffle(slot_data["enemy_shuffle"])

        # Disable inactive mods
        for mod_data in mods_data:
            if mod_data.name not in self.options.active_mods:
                for item_name, item_data in mod_data.items.items():
                    self.item_manager.disable_item(item_name)
                for loc_name, loc_data in mod_data.locations.items():
                    self.loc_manager.disable_location(loc_name)

        # Disable contact techs
        # This always happens for now, while I haven't committed to MCO-ing XComHQ
        # (which currently seems like the only way to fix them)
        self.loc_manager.disable_location("ResistanceCommunications")
        self.item_manager.disable_item("ResistanceCommunicationsCompleted")
        self.loc_manager.disable_location("ResistanceRadio")
        self.item_manager.disable_item("ResistanceRadioCompleted")

        # Set Alien Hunters locations
        if self.options.alien_hunters_dlc == AlienHuntersDLC.option_no_integrated_dlc:
            self.loc_manager.disable_location("ExperimentalWeapons")
            self.item_manager.disable_item("ExperimentalWeaponsCompleted")

        elif self.options.alien_hunters_dlc == AlienHuntersDLC.option_no_alien_rulers:
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if "kill_ruler" in loc_data.tags:
                    self.loc_manager.disable_location(loc_name)
                    if loc_data.normal_item:
                        self.item_manager.disable_item(loc_data.normal_item)

        elif self.options.alien_hunters_dlc == AlienHuntersDLC.option_none:
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if loc_data.dlc == "AH":
                    self.loc_manager.disable_location(loc_name)
            for item_name, item_data in self.item_manager.item_table.items():
                if item_data.dlc == "AH":
                    self.item_manager.disable_item(item_name)

        # Enable progressive tech items
        if "RifleTech+" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressiveRifleTechCompleted+"):
                warning(f"X2WOTC: Failed to enable progressive rifle tech+ for player {self.player_name}")
        elif "RifleTech" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressiveRifleTechCompleted"):
                warning(f"X2WOTC: Failed to enable progressive rifle tech for player {self.player_name}")
        if "ArmorTech+" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressiveArmorTechCompleted+"):
                warning(f"X2WOTC: Failed to enable progressive armor tech+ for player {self.player_name}")
        elif "ArmorTech" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressiveArmorTechCompleted"):
                warning(f"X2WOTC: Failed to enable progressive armor tech for player {self.player_name}")
        if "MeleeWeaponTech" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressiveMeleeTechCompleted"):
                warning(f"X2WOTC: Failed to enable progressive melee tech for player {self.player_name}")
        if "GREMLINTech" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressiveGREMLINTechCompleted"):
                warning(f"X2WOTC: Failed to enable progressive GREMLIN tech for player {self.player_name}")
        if "PsionicsTech" in self.options.progressive_items:
            if not self.item_manager.enable_progressive_item("ProgressivePsionicsTechCompleted"):
                warning(f"X2WOTC: Failed to enable progressive psionics tech for player {self.player_name}")

        # Enable tech fragment items
        if self.options.chosen_weapon_fragments == ChosenWeaponFragments.option_two:
            if not self.item_manager.enable_progressive_item("ChosenAssassinWeaponsFragment2"):
                warning(f"X2WOTC: Failed to enable Assassin weapon fragments (2) for player {self.player_name}")
            if not self.item_manager.enable_progressive_item("ChosenHunterWeaponsFragment2"):
                warning(f"X2WOTC: Failed to enable Hunter weapon fragments (2) for player {self.player_name}")
            if not self.item_manager.enable_progressive_item("ChosenWarlockWeaponsFragment2"):
                warning(f"X2WOTC: Failed to enable Warlock weapon fragments (2) for player {self.player_name}")
        elif self.options.chosen_weapon_fragments == ChosenWeaponFragments.option_three:
            if not self.item_manager.enable_progressive_item("ChosenAssassinWeaponsFragment3"):
                warning(f"X2WOTC: Failed to enable Assassin weapon fragments (3) for player {self.player_name}")
            if not self.item_manager.enable_progressive_item("ChosenHunterWeaponsFragment3"):
                warning(f"X2WOTC: Failed to enable Hunter weapon fragments (3) for player {self.player_name}")
            if not self.item_manager.enable_progressive_item("ChosenWarlockWeaponsFragment3"):
                warning(f"X2WOTC: Failed to enable Warlock weapon fragments (3) for player {self.player_name}")

        # Force early proving ground
        if self.options.early_proving_ground:
            self.multiworld.early_items[self.player][
                self.item_manager.item_table["AutopsyAdventOfficerCompleted"].display_name
            ] = 1

        # Disable Enemysanity
        if not self.options.enemy_sanity:
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if loc_data.type == "EnemyKill":
                    self.loc_manager.disable_location(loc_name)

        # Disable Itemsanity
        if not self.options.item_sanity:
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if loc_data.type == "ItemUse":
                    self.loc_manager.disable_location(loc_name)

        # Disable/enable Chosen Huntsanity
        if self.options.chosen_hunt_sanity.value == ChosenHuntSanity.option_off:
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if "chosen_hunt" in loc_data.tags:
                    self.loc_manager.disable_location(loc_name)
        else:
            progressive = self.options.chosen_hunt_sanity.value == ChosenHuntSanity.option_progressive
            self.item_manager.enable_chosen_hunt_items(progressive)

        # Shuffle enemies
        if self.options.enemy_rando:
            if self.options.enemy_plando_preset.value == EnemyPlandoPreset.option_advent_only:
                self.options.enemy_plando.value = {"forced": [], "fixed": [
                    enemy_name for enemy_name in self.enemy_rando_manager.enemy_names
                    if not enemy_name.startswith("Adv")
                ]}
            elif self.options.enemy_plando_preset.value == EnemyPlandoPreset.option_aliens_only:
                self.options.enemy_plando.value = {"forced": [], "fixed": ["Adv"]}
            elif self.options.enemy_plando_preset.value == EnemyPlandoPreset.option_separate:
                self.options.enemy_plando.value = {"forced": [[["Adv"], ["Adv"]]], "fixed": []}
            self.enemy_rando_manager.shuffle_enemies(self.options.enemy_plando, self.random)

        # Handle mod options
        for mod_data in mods_data:
            if mod_data.generate_early and mod_data.name in self.options.active_mods:
                mod_data.generate_early(self)

        # Remove corpse cost logic (after mod options, in case mods add corpse costs)
        if self.options.remove_corpse_costs:
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if loc_data.type == "ItemUse":
                    self.loc_manager.replace(loc_name, tags={
                        tag for tag in loc_data.tags
                        if not tag.startswith("diff:")
                    })

        # Lock location manager
        self.loc_manager.locked = True

        # Exclude post-goal locations (after location data becomes immutable)
        if self.options.exclude_post_goal_locations:
            goal_difficulty = self.loc_manager.get_location_difficulty(GOAL_VALUE_TO_LOCATION[self.options.goal.value])
            for loc_name, loc_data in self.loc_manager.location_table.items():
                if not loc_data.id or not self.loc_manager.enabled[loc_name]:
                    continue
                if self.loc_manager.get_location_difficulty(loc_name) > goal_difficulty:
                    self.options.exclude_locations.value.add(loc_data.display_name)

        # Validate location and item counts
        num_filler_items = self.loc_manager.num_locations - self.item_manager.num_items
        if num_filler_items < 0:
            raise OptionError(
                f"X2WOTC: Too many items for player {self.player_name}. "
                f"Disable Chosen Weapon Fragments or enable at least {-num_filler_items} more location(s)."
            )
        max_useful_filler = num_filler_items - len(self.options.exclude_locations.value)
        if self.options.exclude_post_goal_locations and max_useful_filler < 0:
            raise OptionError(
                f"X2WOTC: Too many excluded locations for player {self.player_name}. "
                "Consider enabling more locations or disabling Exclude Post-Goal Locations."
            )

        # Add filler items
        info(f"X2WOTC: Adding {num_filler_items} filler items for player {self.player_name}")
        self.item_manager.add_filler_items(
            num_filler_items,
            max_useful_filler,
            self.options.resource_share.value,
            self.options.weapon_mod_share.value,
            self.options.pcs_share.value,
            self.options.staff_share.value,
            self.options.trap_share.value,
            self.options.nothing_share.value,
            self.random
        )

        # Lock item manager
        self.item_manager.locked = True

        # Rule manager needs to exist for collect/remove, but requires options being resolved
        self.rule_manager = RuleManager(self)
        self.reg_manager = RegionManager(self)  # Region manager requires rule manager

    def create_regions(self):
        self.reg_manager.create_regions()

        # Place event items
        for loc_data in self.loc_manager.location_table.values():
            if loc_data.type == "Event":
                item_data = self.item_manager.item_table[loc_data.normal_item]
                location = self.multiworld.get_location(loc_data.display_name, self.player)
                location.place_locked_item(self.create_item(item_data.display_name))

    def create_item(self, name: str) -> X2WOTCItem:
        item_name = self.item_manager.item_display_name_to_key[name]
        item_data = self.item_manager.item_table[item_name]
        return X2WOTCItem(self.player, item_data)

    def create_items(self):
        for item_name, item_data in self.item_manager.item_table.items():
            if item_data.type != "Event":
                for i in range(self.item_manager.item_count[item_name]):
                    item = self.create_item(item_data.display_name)
                    self.multiworld.itempool.append(item)

    def set_rules(self):
        self.rule_manager.set_rules()

        for mod_data in mods_data:
            if mod_data.set_rules and mod_data.name in self.options.active_mods:
                mod_data.set_rules(self)

    def get_filler_item_name(self) -> str:
        return self.item_manager.get_filler_item_name(
            self.options.resource_share.value,
            self.options.weapon_mod_share.value,
            self.options.pcs_share.value,
            self.options.staff_share.value,
            self.options.trap_share.value,
            self.options.nothing_share.value,
            self.random
        )

    # Invalidate power cache on collect/remove
    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change and item.name in self.rule_manager.power_items:
            state.x2wotc_power_stale[self.player] = True
        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change and item.name in self.rule_manager.power_items:
            state.x2wotc_power_stale[self.player] = True
        return change

    def fill_slot_data(self):
        slot_data = {
            "world_version": self.world_version.as_simple_string(),
            "minimum_client_version": world_minimum_client_version,
            "seed_name": self.multiworld.seed_name,
            "player": self.player,
            "goal_location": GOAL_VALUE_TO_LOCATION[self.options.goal.value],
            "enemy_shuffle": self.enemy_rando_manager.enemy_shuffle,
        }

        slot_data |= self.options.as_dict(*self.option_names, toggles_as_bools=True)
        return slot_data

    # Trigger UT re-gen
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        hint_data[self.player] = {}

        # Enemy rando hint data
        if self.options.enemy_rando:
            for loc_data in self.loc_manager.location_table.values():
                diff_tag_enemies = [tag[5:] for tag in loc_data.tags if tag.startswith("diff:")]
                if loc_data.id is None or not diff_tag_enemies:
                    continue

                placement_enemies = sorted([
                    self.enemy_rando_manager.get_placement_enemy(diff_tag_enemy)
                    for diff_tag_enemy in diff_tag_enemies
                ])
                hint_data[self.player][loc_data.id] = ", ".join(placement_enemies)

    def write_spoiler(self, spoiler_handle: TextIO):
        if self.options.enemy_rando:
            spoiler_handle.write(f"\n\n=== Enemy Rando for player {self.player_name} ===\n")
            for placement_index, placed_index in enumerate(self.enemy_rando_manager.enemy_shuffle):
                spoiler_handle.write(
                    f"{self.enemy_rando_manager.enemy_names[placement_index]} <- "
                    f"{self.enemy_rando_manager.enemy_names[placed_index]}\n"
                )
