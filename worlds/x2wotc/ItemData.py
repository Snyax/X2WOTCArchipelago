from collections import Counter
from typing import NamedTuple

from BaseClasses import ItemClassification as IC


TECH_ITEM_PREFIX = "[Tech] "
SHADOW_TECH_ITEM_PREFIX = "[Tech] "
PROMOTION_ITEM_PREFIX = "[Promotion] "
CHOSEN_HUNT_ITEM_PREFIX = "[Chosen Hunt] "
RESOURCE_ITEM_PREFIX = "[Resource] "
WEAPON_MOD_ITEM_PREFIX = "[Upgrade] "
PCS_ITEM_PREFIX = "[PCS] "
STAFF_ITEM_PREFIX = "[Staff] "
TRAP_ITEM_PREFIX = "[Trap] "


class X2WOTCItemData(NamedTuple):
    display_name: str
    id: int | None = None
    classification: IC = IC.filler
    layer: str = "Strategy"  # "Strategy" or "Tactical"
    type: str = "Event"
    tags: set[str] = set()
    power: float = 0.0  # Relative to other values
                        # (For reference: Magnetic Weapons = 100.0)
    dlc: str | None = None  # None: Base Game,
                            # "AH": Alien Hunters,
                            # "SLG": Shens Last Gift,
                            # "WOTC": War of the Chosen
    normal_location: str | None = None
    stages: list[str | None] | None = None  # For progressive items
    shuffle_stages: set[int] | None = None  # Shuffle stages at these indices

    mutable_fields = {"classification", "tags", "power", "stages"}

    def replace(self, **kwargs) -> "X2WOTCItemData":
        immutable_fields = set(self._fields) & set(kwargs.keys()) - self.mutable_fields
        if immutable_fields:
            raise ValueError(f"Cannot replace immutable fields {immutable_fields}.")

        # Validate stages
        if "stages" in kwargs:
            if not self.stages or Counter(kwargs["stages"]) != Counter(self.stages):
                raise ValueError(f"Invalid replacement item stages: {self.stages} -> {kwargs["stages"]}.")

        return self._replace(**kwargs)


next_item_id = 240223152003  # X2WOTC

def get_new_item_id() -> int:
    global next_item_id
    new_item_id = next_item_id
    next_item_id += 1
    return new_item_id


########################################################################################################################
##                        TECH COMPLETION ITEMS (RESEARCH PROJECTS / SHADOW PROJECTS)                                 ##
########################################################################################################################

#=======================================================================================================================
#                                                 BASE GAME
#-----------------------------------------------------------------------------------------------------------------------

vanilla_weapon_tech_items: dict[str, X2WOTCItemData] = {
    "ModularWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Modular Weapons",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 40.0,
        normal_location = "ModularWeapons"
    ),
    "MagnetizedWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Magnetic Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 100.0,
        normal_location = "MagnetizedWeapons"
    ),
    "GaussWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Gauss Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 100.0,
        normal_location = "GaussWeapons"
    ),
    "PlasmaRifleCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Plasma Rifle",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 160.0,
        normal_location = "PlasmaRifle"
    ),
    "HeavyPlasmaCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Beam Cannon",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 160.0,
        normal_location = "HeavyPlasma"
    ),
    "PlasmaSniperCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Plasma Lance",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 160.0,
        normal_location = "PlasmaSniper"
    ),
    "AlloyCannonCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Storm Gun",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 160.0,
        normal_location = "AlloyCannon"
    ),
}

vanilla_armor_tech_items: dict[str, X2WOTCItemData] = {
    "HybridMaterialsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Hybrid Materials",
        id = get_new_item_id(),
        classification = IC.progression_deprioritized_skip_balancing,
        type = "TechCompleted",
        tags = {"armor"},
        power = 0.0,
        normal_location = "HybridMaterials"
    ),
    "PlatedArmorCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Plated Armor",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor"},
        power = 100.0,
        normal_location = "PlatedArmor"
    ),
    "PoweredArmorCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Powered Armor",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor"},
        power = 180.0,
        normal_location = "PoweredArmor"
    ),
}

vanilla_autopsy_tech_items: dict[str, X2WOTCItemData] = {
    "AutopsySectoidCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Sectoid Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"utility"},
        power = 20.0,
        normal_location = "AutopsySectoid"
    ),
    "AutopsyViperCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Viper Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"utility"},
        power = 20.0,
        normal_location = "AutopsyViper"
    ),
    "AutopsyMutonCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Muton Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 80.0,
        normal_location = "AutopsyMuton"
    ),
    "AutopsyBerserkerCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Berserker Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"utility"},
        power = 20.0,
        normal_location = "AutopsyBerserker"
    ),
    "AutopsyArchonCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Archon Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 120.0,
        normal_location = "AutopsyArchon"
    ),
    "AutopsyGatekeeperCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Gatekeeper Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 60.0,
        normal_location = "AutopsyGatekeeper"
    ),
    "AutopsyAndromedonCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Andromedon Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 40.0,
        normal_location = "AutopsyAndromedon"
    ),
    "AutopsyFacelessCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Faceless Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"utility"},
        power = 100.0,
        normal_location = "AutopsyFaceless"
    ),
    "AutopsyChryssalidCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Chryssalid Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 20.0,
        normal_location = "AutopsyChryssalid"
    ),
    "AutopsyAdventTrooperCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Trooper Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"utility"},
        power = 20.0,
        normal_location = "AutopsyAdventTrooper"
    ),
    "AutopsyAdventStunLancerCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Stun Lancer Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 80.0,
        normal_location = "AutopsyAdventStunLancer"
    ),
    "AutopsyAdventShieldbearerCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Shieldbearer Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 20.0,
        normal_location = "AutopsyAdventShieldbearer"
    ),
    "AutopsyAdventMECCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT MEC Breakdown",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "utility"},
        power = 120.0,
        normal_location = "AutopsyAdventMEC"
    ),
    "AutopsyAdventTurretCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Turret Breakdown",
        id = get_new_item_id(),
        classification = IC.progression_deprioritized_skip_balancing,
        type = "TechCompleted",
        tags = {"facility"},
        power = 0.0,
        normal_location = "AutopsyAdventTurret"
    ),
    "AutopsySectopodCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Sectopod Breakdown",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "utility"},
        power = 60.0,
        normal_location = "AutopsySectopod"
    ),
}

vanilla_goldenpath_tech_items: dict[str, X2WOTCItemData] = {
    "AlienBiotechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Alien Biotech",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"facility"},
        power = 20.0,
        normal_location = "AlienBiotech"
    ),
    "ResistanceCommunicationsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Resistance Communications",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"facility"},
        power = 0.0,
        normal_location = "ResistanceCommunications"
    ),
    "AutopsyAdventOfficerCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Officer Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"facility"},
        power = 160.0,
        normal_location = "AutopsyAdventOfficer"
    ),
    "AlienEncryptionCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Alien Encryption",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"facility"},
        power = 20.0,
        normal_location = "AlienEncryption"
    ),
    "CodexBrainPt1Completed": X2WOTCItemData(
        display_name = SHADOW_TECH_ITEM_PREFIX + "Codex Brain",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"mission"},
        power = 0.0,
        normal_location = "CodexBrainPt1"
    ),
    "CodexBrainPt2Completed": X2WOTCItemData(
        display_name = SHADOW_TECH_ITEM_PREFIX + "Encrypted Codex Data",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        power = 0.0,
        normal_location = "CodexBrainPt2"
    ),
    "BlacksiteDataCompleted": X2WOTCItemData(
        display_name = SHADOW_TECH_ITEM_PREFIX + "Blacksite Vial",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"mission"},
        power = 0.0,
        normal_location = "BlacksiteData"
    ),
    "ForgeStasisSuitCompleted": X2WOTCItemData(
        display_name = SHADOW_TECH_ITEM_PREFIX + "Recovered ADVENT Stasis Suit",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        power = 0.0,
        normal_location = "ForgeStasisSuit"
    ),
    "PsiGateCompleted": X2WOTCItemData(
        display_name = SHADOW_TECH_ITEM_PREFIX + "Psionic Gate",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        power = 0.0,
        normal_location = "PsiGate"
    ),
    "AutopsyAdventPsiWitchCompleted": X2WOTCItemData(
        display_name = SHADOW_TECH_ITEM_PREFIX + "Avatar Autopsy",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"mission"},
        power = 0.0,
        normal_location = "AutopsyAdventPsiWitch"
    ),
}

vanilla_other_tech_items: dict[str, X2WOTCItemData] = {
    "ResistanceRadioCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Resistance Radio",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"facility"},
        power = 0.0,
        normal_location = "ResistanceRadio"
    ),
    "EleriumCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Elerium",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"facility"},
        power = 20.0,
        normal_location = "Tech_Elerium"
    ),
    "PsionicsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Psionics",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"facility", "weapon"},
        power = 160.0,
        normal_location = "Psionics"
    ),
}

#=======================================================================================================================
#                                               ALIEN HUNTERS
#-----------------------------------------------------------------------------------------------------------------------

alien_hunters_tech_items: dict[str, X2WOTCItemData] = {
    "ExperimentalWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Experimental Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "utility"},
        power = 140.0,
        dlc = "AH",
        normal_location = "ExperimentalWeapons"
    ),
    "AutopsyViperKingCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Viper King Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor"},
        power = 120.0,
        dlc = "AH",
        normal_location = "AutopsyViperKing"
    ),
    "AutopsyBerserkerQueenCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Berserker Queen Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor"},
        power = 140.0,
        dlc = "AH",
        normal_location = "AutopsyBerserkerQueen"
    ),
    "AutopsyArchonKingCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Archon King Autopsy",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor"},
        power = 160.0,
        dlc = "AH",
        normal_location = "AutopsyArchonKing"
    ),
}

#=======================================================================================================================
#                                             WAR OF THE CHOSEN
#-----------------------------------------------------------------------------------------------------------------------

wotc_autopsy_tech_items: dict[str, X2WOTCItemData] = {
    "AutopsyAdventPurifierCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Purifier Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 20.0,
        dlc = "WOTC",
        normal_location = "AutopsyAdventPurifier"
    ),
    "AutopsyAdventPriestCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Priest Autopsy",
        id = get_new_item_id(),
        classification = IC.progression_deprioritized_skip_balancing,
        type = "TechCompleted",
        tags = {"utility"},
        power = 0.0,
        dlc = "WOTC",
        normal_location = "AutopsyAdventPriest"
    ),
    "AutopsyTheLostCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "The Lost Autopsy",
        id = get_new_item_id(),
        classification = IC.progression_deprioritized_skip_balancing,
        type = "TechCompleted",
        tags = {"utility"},
        power = 0.0,
        dlc = "WOTC",
        normal_location = "AutopsyTheLost"
    ),
    "AutopsySpectreCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Spectre Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"utility"},
        power = 20.0,
        dlc = "WOTC",
        normal_location = "AutopsySpectre"
    ),
}

wotc_chosen_weapon_tech_items: dict[str, X2WOTCItemData] = {
    "ChosenAssassinWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Assassin Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 200.0,
        dlc = "WOTC",
        normal_location = "ChosenAssassinWeapons"
    ),
    "ChosenHunterWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Hunter Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 200.0,
        dlc = "WOTC",
        normal_location = "ChosenHunterWeapons"
    ),
    "ChosenWarlockWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Warlock Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 200.0,
        dlc = "WOTC",
        normal_location = "ChosenWarlockWeapons"
    ),
}

#=======================================================================================================================
#                                            PROGRESSIVE TECH ITEMS
#-----------------------------------------------------------------------------------------------------------------------

progressive_tech_items: dict[str, X2WOTCItemData] = {
    "ProgressiveRifleShotgunTechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Rifle/Shotgun",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "MagnetizedWeaponsCompleted",
            "PlasmaRifleCompleted",
            "AlloyCannonCompleted",
        ],
        shuffle_stages = {1, 2}
    ),
    "ProgressiveRifleShotgunTechCompleted+": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Rifle/Shotgun+",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "ModularWeaponsCompleted",
            "MagnetizedWeaponsCompleted",
            "PlasmaRifleCompleted",
            "AlloyCannonCompleted",
        ],
        shuffle_stages = {2, 3}
    ),
    "ProgressiveCannonSniperTechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Cannon/Sniper",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "GaussWeaponsCompleted",
            "HeavyPlasmaCompleted",
            "PlasmaSniperCompleted",
        ],
        shuffle_stages = {1, 2}
    ),
    "ProgressiveArmorTechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Armor",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor", "progressive"},
        stages = [
            "PlatedArmorCompleted",
            "PoweredArmorCompleted",
        ]
    ),
    "ProgressiveArmorTechCompleted+": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Armor+",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor", "progressive"},
        stages = [
            "HybridMaterialsCompleted",
            "PlatedArmorCompleted",
            "PoweredArmorCompleted",
        ]
    ),
    "ProgressiveSwordTechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Sword",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "AutopsyAdventStunLancerCompleted",
            "AutopsyArchonCompleted",
        ]
    ),
    "ProgressiveGREMLINTechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive GREMLIN",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"utility", "weapon", "progressive"},
        stages = [
            "AutopsyAdventMECCompleted",
            "AutopsySectopodCompleted",
        ]
    ),
    "ProgressivePsionicsTechCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Psionics",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"facility", "weapon", "progressive"},
        stages = [
            "PsionicsCompleted",
            "AutopsyGatekeeperCompleted",
        ]
    ),
}

#=======================================================================================================================
#                                             TECH FRAGMENT ITEMS
#-----------------------------------------------------------------------------------------------------------------------

tech_fragment_items: dict[str, X2WOTCItemData] = {
    "ChosenAssassinWeaponsFragment2": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Assassin Weapons Fragment (1/2)",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"weapon", "fragment"},
        dlc = "WOTC",
        stages = [
            None,
            "ChosenAssassinWeaponsCompleted",
        ]
    ),
    "ChosenHunterWeaponsFragment2": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Hunter Weapons Fragment (1/2)",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"weapon", "fragment"},
        dlc = "WOTC",
        stages = [
            None,
            "ChosenHunterWeaponsCompleted",
        ]
    ),
    "ChosenWarlockWeaponsFragment2": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Warlock Weapons Fragment (1/2)",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"weapon", "fragment"},
        dlc = "WOTC",
        stages = [
            None,
            "ChosenWarlockWeaponsCompleted",
        ]
    ),
    "ChosenAssassinWeaponsFragment3": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Assassin Weapons Fragment (1/3)",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"weapon", "fragment"},
        dlc = "WOTC",
        stages = [
            None,
            None,
            "ChosenAssassinWeaponsCompleted",
        ]
    ),
    "ChosenHunterWeaponsFragment3": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Hunter Weapons Fragment (1/3)",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"weapon", "fragment"},
        dlc = "WOTC",
        stages = [
            None,
            None,
            "ChosenHunterWeaponsCompleted",
        ]
    ),
    "ChosenWarlockWeaponsFragment3": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Warlock Weapons Fragment (1/3)",
        id = get_new_item_id(),
        classification = IC.progression_skip_balancing,
        type = "TechCompleted",
        tags = {"weapon", "fragment"},
        dlc = "WOTC",
        stages = [
            None,
            None,
            "ChosenWarlockWeaponsCompleted",
        ]
    ),
}

########################################################################################################################
##                                               PROMOTION ITEMS                                                      ##
########################################################################################################################

promotion_items: dict[str, X2WOTCItemData] = {
    f"{soldier_class.title()}Rank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + soldier_class,
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {soldier_class.lower()},
        power = 15.0,
        dlc = dlc
    )
    for (soldier_class, dlc) in [
        ("Ranger", None),
        ("Grenadier", None),
        ("Specialist", None),
        ("Sharpshooter", None),
        ("SPARK", "SLG"),
        ("Reaper", "WOTC"),
        ("Skirmisher", "WOTC"),
        ("Templar", "WOTC"),
    ]
}

########################################################################################################################
##                                         COVERT ACTION REWARD ITEMS                                                 ##
########################################################################################################################

#=======================================================================================================================
#                                              CHOSEN HUNT ITEMS
#-----------------------------------------------------------------------------------------------------------------------

chosen_hunt_items: dict[str, X2WOTCItemData] = {
    "FactionInfluence": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Faction Influence",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        power = 40.0,
        dlc = "WOTC"
    ),
    "AssassinStronghold": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Assassin Stronghold",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        power = 80.0,
        dlc = "WOTC"
    ),
    "HunterStronghold": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Hunter Stronghold",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        power = 80.0,
        dlc = "WOTC"
    ),
    "WarlockStronghold": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Warlock Stronghold",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        power = 80.0,
        dlc = "WOTC"
    ),
    "ProgressiveAssassinChosenHunt": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Progressive Assassin",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        dlc = "WOTC",
        stages = [
            "FactionInfluence",
            "FactionInfluence",
            "AssassinStronghold",
        ]
    ),
    "ProgressiveHunterChosenHunt": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Progressive Hunter",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        dlc = "WOTC",
        stages = [
            "FactionInfluence",
            "FactionInfluence",
            "HunterStronghold",
        ]
    ),
    "ProgressiveWarlockChosenHunt": X2WOTCItemData(
        display_name = CHOSEN_HUNT_ITEM_PREFIX + "Progressive Warlock",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "CovertActionReward",
        tags = {"chosen_hunt"},
        dlc = "WOTC",
        stages = [
            "FactionInfluence",
            "FactionInfluence",
            "WarlockStronghold",
        ]
    ),
}

########################################################################################################################
##                                                FILLER ITEMS                                                        ##
########################################################################################################################

#=======================================================================================================================
#                                                RESOURCE ITEMS
#-----------------------------------------------------------------------------------------------------------------------

supplies_items: dict[str, X2WOTCItemData] = {
    "Supplies:20": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "20 Supplies",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "supplies"}
    ),
    "Supplies:35": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "35 Supplies",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "supplies"}
    ),
    "Supplies:50": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "50 Supplies",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "supplies"}
    ),
}

intel_items: dict[str, X2WOTCItemData] = {
    "Intel:10": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "10 Intel",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "intel"}
    ),
    "Intel:15": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "15 Intel",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "intel"}
    ),
    "Intel:20": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "20 Intel",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "intel"}
    ),
}

alien_alloy_items: dict[str, X2WOTCItemData] = {
    "AlienAlloy:5": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "5 Alien Alloys",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "alien_alloy"}
    ),
    "AlienAlloy:10": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "10 Alien Alloys",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "alien_alloy"}
    ),
    "AlienAlloy:15": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "15 Alien Alloys",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "alien_alloy"}
    ),
}

elerium_dust_items: dict[str, X2WOTCItemData] = {
    "EleriumDust:5": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "5 Elerium Crystals",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "elerium_dust"}
    ),
    "EleriumDust:10": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "10 Elerium Crystals",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "elerium_dust"}
    ),
    "EleriumDust:15": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "15 Elerium Crystals",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "elerium_dust"}
    ),
}

elerium_core_items: dict[str, X2WOTCItemData] = {
    "EleriumCore:1": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "1 Elerium Core",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "elerium_core"}
    ),
}

ability_point_items: dict[str, X2WOTCItemData] = {
    "AbilityPoint:3": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "3 Ability Points",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "ability_point"},
        dlc = "WOTC"
    ),
    "AbilityPoint:5": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "5 Ability Points",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "ability_point"},
        dlc = "WOTC"
    ),
    "AbilityPoint:7": X2WOTCItemData(
        display_name = RESOURCE_ITEM_PREFIX + "7 Ability Points",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "ability_point"},
        dlc = "WOTC"
    ),
}

#=======================================================================================================================
#                                               WEAPON MOD ITEMS
#-----------------------------------------------------------------------------------------------------------------------

basic_weapon_mod_items: dict[str, X2WOTCItemData] = {
    "AimUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Scope",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "scope", "basic"}
    ),
    "CritUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Laser Sight",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "laser_sight", "basic"}
    ),
    "ReloadUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Auto-Loader",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "auto_loader", "basic"}
    ),
    "FreeKillUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Repeater",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "repeater", "basic"}
    ),
    "MissDamageUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Stock",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "stock", "basic"}
    ),
    "FreeFireUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Hair Trigger",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "hair_trigger", "basic"}
    ),
    "ClipSizeUpgrade_Bsc:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Expanded Magazine",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "expanded_magazine", "basic"}
    ),
}

advanced_weapon_mod_items: dict[str, X2WOTCItemData] = {
    "AimUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Scope",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "scope", "advanced"}
    ),
    "CritUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Laser Sight",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "laser_sight", "advanced"}
    ),
    "ReloadUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Auto-Loader",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "auto_loader", "advanced"}
    ),
    "FreeKillUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Repeater",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "repeater", "advanced"}
    ),
    "MissDamageUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Stock",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "stock", "advanced"}
    ),
    "FreeFireUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Hair Trigger",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "hair_trigger", "advanced"}
    ),
    "ClipSizeUpgrade_Adv:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Expanded Magazine",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "expanded_magazine", "advanced"}
    ),
}

superior_weapon_mod_items: dict[str, X2WOTCItemData] = {
    "AimUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Scope",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "scope", "superior"}
    ),
    "CritUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Laser Sight",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "laser_sight", "superior"}
    ),
    "ReloadUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Auto-Loader",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "auto_loader", "superior"}
    ),
    "FreeKillUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Repeater",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "repeater", "superior"}
    ),
    "MissDamageUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Stock",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "stock", "superior"}
    ),
    "FreeFireUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Hair Trigger",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "hair_trigger", "superior"}
    ),
    "ClipSizeUpgrade_Sup:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Superior Expanded Magazine",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "expanded_magazine", "superior"}
    ),
}

#=======================================================================================================================
#                                                  PCS ITEMS
#-----------------------------------------------------------------------------------------------------------------------

basic_pcs_items: dict[str, X2WOTCItemData] = {
    "CommonPCSSpeed:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Speed",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "speed", "basic"}
    ),
    "CommonPCSConditioning:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Conditioning",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "conditioning", "basic"}
    ),
    "CommonPCSFocus:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Focus",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "focus", "basic"}
    ),
    "CommonPCSPerception:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Perception",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "perception", "basic"}
    ),
    "CommonPCSAgility:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Agility",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "agility", "basic"}
    ),
}

advanced_pcs_items: dict[str, X2WOTCItemData] = {
    "RarePCSSpeed:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Speed",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "speed", "advanced"}
    ),
    "RarePCSConditioning:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Conditioning",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "conditioning", "advanced"}
    ),
    "RarePCSFocus:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Focus",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "focus", "advanced"}
    ),
    "RarePCSPerception:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Perception",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "perception", "advanced"}
    ),
    "RarePCSAgility:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Agility",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "agility", "advanced"}
    ),
}

superior_pcs_items: dict[str, X2WOTCItemData] = {
    "EpicPCSSpeed:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Speed",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "pcs", "speed", "superior"}
    ),
    "EpicPCSConditioning:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Conditioning",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "pcs", "conditioning", "superior"}
    ),
    "EpicPCSFocus:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Focus",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "pcs", "focus", "superior"}
    ),
    "EpicPCSPerception:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Perception",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "pcs", "perception", "superior"}
    ),
    "EpicPCSAgility:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Agility",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "pcs", "agility", "superior"}
    ),
}

#=======================================================================================================================
#                                                 STAFF ITEMS
#-----------------------------------------------------------------------------------------------------------------------

scientist_items: dict[str, X2WOTCItemData] = {
    "Scientist:1": X2WOTCItemData(
        display_name = STAFF_ITEM_PREFIX + "1 Scientist",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Staff",
        tags = {"filler", "scientist"}
    ),
}

engineer_items: dict[str, X2WOTCItemData] = {
    "Engineer:1": X2WOTCItemData(
        display_name = STAFF_ITEM_PREFIX + "1 Engineer",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Staff",
        tags = {"filler", "engineer"}
    ),
}

########################################################################################################################
##                                                TRAP ITEMS                                                          ##
########################################################################################################################

doom_items: dict[str, X2WOTCItemData] = {
    "Doom:1": X2WOTCItemData(
        display_name = TRAP_ITEM_PREFIX + "Avatar Project +1",
        id = get_new_item_id(),
        classification = IC.trap,
        type = "Trap",
        tags = {"doom"}
    ),
}

force_level_items: dict[str, X2WOTCItemData] = {
    "ForceLevel:1": X2WOTCItemData(
        display_name = TRAP_ITEM_PREFIX + "Force Level +1",
        id = get_new_item_id(),
        classification = IC.trap,
        type = "Trap",
        tags = {"force_level"}
    ),
}

########################################################################################################################
##                                               NOTHING ITEMS                                                        ##
########################################################################################################################

nothing_items: dict[str, X2WOTCItemData] = {
    "Nothing": X2WOTCItemData(
        display_name = "ADVENT Burger",
        id = get_new_item_id(),
        type = "Nothing"
    ),
}

########################################################################################################################
##                                                EVENT ITEMS                                                         ##
########################################################################################################################

event_items: dict[str, X2WOTCItemData] = {
    "Victory": X2WOTCItemData(
        display_name = "Victory",
        classification = IC.progression,
        normal_location = "Victory"
    ),
    "Broadcast": X2WOTCItemData(
        display_name = "Broadcast",
        classification = IC.progression,
        normal_location = "Broadcast"
    ),
    "Stronghold1": X2WOTCItemData(
        display_name = "Stronghold 1",
        classification = IC.progression,
        normal_location = "Stronghold1"
    ),
    "Stronghold2": X2WOTCItemData(
        display_name = "Stronghold 2",
        classification = IC.progression,
        normal_location = "Stronghold2"
    ),
    "Stronghold3": X2WOTCItemData(
        display_name = "Stronghold 3",
        classification = IC.progression,
        normal_location = "Stronghold3"
    ),
}

########################################################################################################################
##                                                TOTAL ITEMS                                                         ##
########################################################################################################################

tech_item_table: dict[str, X2WOTCItemData] = {
    **vanilla_weapon_tech_items,
    **vanilla_armor_tech_items,
    **vanilla_autopsy_tech_items,
    **vanilla_goldenpath_tech_items,
    **vanilla_other_tech_items,
    **alien_hunters_tech_items,
    **wotc_autopsy_tech_items,
    **wotc_chosen_weapon_tech_items,
    **progressive_tech_items,
    **tech_fragment_items,
}

resource_item_table: dict[str, X2WOTCItemData] = {
    **supplies_items,
    **intel_items,
    **alien_alloy_items,
    **elerium_dust_items,
    **elerium_core_items,
    **ability_point_items,
}

weapon_mod_item_table: dict[str, X2WOTCItemData] = {
    **basic_weapon_mod_items,
    **advanced_weapon_mod_items,
    **superior_weapon_mod_items,
}

pcs_item_table: dict[str, X2WOTCItemData] = {
    **basic_pcs_items,
    **advanced_pcs_items,
    **superior_pcs_items,
}

staff_item_table: dict[str, X2WOTCItemData] = {
    **scientist_items,
    **engineer_items,
}

filler_item_table: dict[str, X2WOTCItemData] = {
    **resource_item_table,
    **weapon_mod_item_table,
    **pcs_item_table,
    **staff_item_table,
}

trap_item_table: dict[str, X2WOTCItemData] = {
    **doom_items,
    **force_level_items,
}

item_table: dict[str, X2WOTCItemData] = {
    **tech_item_table,
    **promotion_items,
    **chosen_hunt_items,
    **filler_item_table,
    **trap_item_table,
    **nothing_items,
    **event_items,
}
