from typing import NamedTuple


TECH_LOCATION_PREFIX = "Research "
SHADOW_TECH_LOCATION_PREFIX = "Research "
ENEMY_KILL_LOCATION_PREFIX = "Kill "
ENEMY_DESTROY_LOCATION_PREFIX = "Destroy "
ITEM_USE_LOCATION_PREFIX = "Use "
SOLDIER_RANK_LOCATION_PREFIX = "Promote "
SOLDIER_RANK_LOCATION_INFIX = " to "
COVERT_ACTION_LOCATION_PREFIX = "Complete "
DEFAULT_RANK_NAME_SET = [
    "Rookie",
    "Squaddie",
    "Corporal",
    "Sergeant",
    "Lieutenant",
    "Captain",
    "Major",
    "Colonel",
    "Brigadier",
]


class X2WOTCLocationData(NamedTuple):
    display_name: str
    id: int | None = None
    layer: str = "Strategy"  # "Strategy" or "Tactical"
    type: str = "Event"
    tags: set[str] = set()
    difficulty: float = 0.0  # Relative to total power in percent (0 to 100)
    dlc: str | None = None  # None: Base Game,
                            # "AH": Alien Hunters,
                            # "SLG": Shens Last Gift,
                            # "WOTC": War of the Chosen
    normal_item: str | None = None

    mutable_fields = {"tags", "difficulty"}

    def replace(self, **kwargs) -> "X2WOTCLocationData":
        immutable_fields = set(self._fields) & set(kwargs.keys()) - self.mutable_fields
        if immutable_fields:
            raise ValueError(f"Cannot replace immutable fields {immutable_fields}.")
        return self._replace(**kwargs)


next_location_id = 240223152003  # X2WOTC

def get_new_location_id() -> int:
    global next_location_id
    new_location_id = next_location_id
    next_location_id += 1
    return new_location_id


########################################################################################################################
##                            TECH LOCATIONS (RESEARCH PROJECTS / SHADOW PROJECTS)                                    ##
########################################################################################################################

#=======================================================================================================================
#                                                 BASE GAME
#-----------------------------------------------------------------------------------------------------------------------

vanilla_weapon_techs: dict[str, X2WOTCLocationData] = {
    "ModularWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Modular Weapons",
        id = get_new_location_id(),
        type = "Tech",
        difficulty = 0.0,
        normal_item = "ModularWeaponsCompleted"
    ),
    "MagnetizedWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Magnetic Weapons",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:ModularWeapons"},
        difficulty = 20.0,
        normal_item = "MagnetizedWeaponsCompleted"
    ),
    "GaussWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Gauss Weapons",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:MagnetizedWeapons"},
        difficulty = 30.0,
        normal_item = "GaussWeaponsCompleted"
    ),
    "PlasmaRifle": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Plasma Rifle",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:Tech_Elerium"},
        difficulty = 50.0,
        normal_item = "PlasmaRifleCompleted"
    ),
    "HeavyPlasma": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Beam Cannon",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:PlasmaRifle"},
        difficulty = 60.0,
        normal_item = "HeavyPlasmaCompleted"
    ),
    "PlasmaSniper": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Plasma Lance",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:PlasmaRifle", "tree:AutopsyArchon"},
        difficulty = 60.0,
        normal_item = "PlasmaSniperCompleted"
    ),
    "AlloyCannon": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Storm Gun",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:PlasmaRifle"},
        difficulty = 60.0,
        normal_item = "AlloyCannonCompleted"
    ),
}

vanilla_armor_techs: dict[str, X2WOTCLocationData] = {
    "HybridMaterials": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Hybrid Materials",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"diff:AdvTrooperM1", "diff:AdvTrooperM2", "diff:AdvTrooperM3"},
        difficulty = 0.0,
        normal_item = "HybridMaterialsCompleted"
    ),
    "PlatedArmor": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Plated Armor",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:HybridMaterials"},
        difficulty = 30.0,
        normal_item = "PlatedArmorCompleted"
    ),
    "PoweredArmor": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Powered Armor",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:Tech_Elerium"},
        difficulty = 50.0,
        normal_item = "PoweredArmorCompleted"
    ),
}

vanilla_autopsy_techs: dict[str, X2WOTCLocationData] = {
    "AutopsySectoid": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Sectoid Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Sectoid"},
        normal_item = "AutopsySectoidCompleted"
    ),
    "AutopsyViper": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Viper Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Viper"},
        normal_item = "AutopsyViperCompleted"
    ),
    "AutopsyMuton": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Muton Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Muton"},
        normal_item = "AutopsyMutonCompleted"
    ),
    "AutopsyBerserker": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Berserker Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Berserker"},
        normal_item = "AutopsyBerserkerCompleted"
    ),
    "AutopsyArchon": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Archon Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Archon"},
        normal_item = "AutopsyArchonCompleted"
    ),
    "AutopsyGatekeeper": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Gatekeeper Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Gatekeeper"},
        normal_item = "AutopsyGatekeeperCompleted"
    ),
    "AutopsyAndromedon": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Andromedon Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:AndromedonRobot"},
        normal_item = "AutopsyAndromedonCompleted"
    ),
    "AutopsyFaceless": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Faceless Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Faceless"},
        normal_item = "AutopsyFacelessCompleted"
    ),
    "AutopsyChryssalid": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Chryssalid Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Chryssalid"},
        normal_item = "AutopsyChryssalidCompleted"
    ),
    "AutopsyAdventTrooper": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Trooper Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer", "diff:AdvTrooperM1", "diff:AdvTrooperM2", "diff:AdvTrooperM3"},
        normal_item = "AutopsyAdventTrooperCompleted"
    ),
    "AutopsyAdventStunLancer": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Stun Lancer Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer", "diff:AdvStunLancerM1", "diff:AdvStunLancerM2", "diff:AdvStunLancerM3"},
        normal_item = "AutopsyAdventStunLancerCompleted"
    ),
    "AutopsyAdventShieldbearer": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Shieldbearer Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer", "diff:AdvShieldBearerM2", "diff:AdvShieldBearerM3"},
        normal_item = "AutopsyAdventShieldbearerCompleted"
    ),
    "AutopsyAdventMEC": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT MEC Breakdown",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer", "diff:AdvMEC_M1", "diff:AdvMEC_M2"},
        normal_item = "AutopsyAdventMECCompleted"
    ),
    "AutopsyAdventTurret": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Turret Breakdown",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer"},
        difficulty = 85.0,  # Not shuffled (and turret wrecks are deceptively hard to get)
        normal_item = "AutopsyAdventTurretCompleted"
    ),
    "AutopsySectopod": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Sectopod Breakdown",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:Sectopod"},
        normal_item = "AutopsySectopodCompleted"
    ),
}

vanilla_goldenpath_techs: dict[str, X2WOTCLocationData] = {
    "AlienBiotech": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Alien Biotech",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath"},
        difficulty = 0.0,
        normal_item = "AlienBiotechCompleted"
    ),
    "ResistanceCommunications": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Resistance Communications",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath"},
        difficulty = 10.0,
        normal_item = "ResistanceCommunicationsCompleted"
    ),
    "AutopsyAdventOfficer": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Officer Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "autopsy", "tree:AlienBiotech"},
        difficulty = 2.0,  # Not shuffled, Gatecrasher
        normal_item = "AutopsyAdventOfficerCompleted"
    ),
    "AlienEncryption": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Alien Encryption",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath"},
        difficulty = 35.0,  # Blacksite mission and Codex kill are ~30
        normal_item = "AlienEncryptionCompleted"
    ),
    "CodexBrainPt1": X2WOTCLocationData(
        display_name = SHADOW_TECH_LOCATION_PREFIX + "Codex Brain",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "autopsy", "shadow", "skulljack_officer"},
        difficulty = 45.0,  # Shadow chamber is ~40
        normal_item = "CodexBrainPt1Completed"
    ),
    "CodexBrainPt2": X2WOTCLocationData(
        display_name = SHADOW_TECH_LOCATION_PREFIX + "Encrypted Codex Data",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "shadow", "tree:CodexBrainPt1"},
        difficulty = 55.0,
        normal_item = "CodexBrainPt2Completed"
    ),
    "BlacksiteData": X2WOTCLocationData(
        display_name = SHADOW_TECH_LOCATION_PREFIX + "Blacksite Vial",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "shadow"},
        difficulty = 45.0,  # Shadow chamber is ~40
        normal_item = "BlacksiteDataCompleted"
    ),
    "ForgeStasisSuit": X2WOTCLocationData(
        display_name = SHADOW_TECH_LOCATION_PREFIX + "Recovered ADVENT Stasis Suit",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "shadow"},
        difficulty = 55.0,  # Forge mission is ~50
        normal_item = "ForgeStasisSuitCompleted"
    ),
    "PsiGate": X2WOTCLocationData(
        display_name = SHADOW_TECH_LOCATION_PREFIX + "Psionic Gate",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "shadow"},
        difficulty = 65.0,  # Psi Gate mission is ~60
        normal_item = "PsiGateCompleted"
    ),
    "AutopsyAdventPsiWitch": X2WOTCLocationData(
        display_name = SHADOW_TECH_LOCATION_PREFIX + "Avatar Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"goldenpath", "autopsy", "shadow", "tree:ForgeStasisSuit", "tree:PsiGate", "skulljack_codex"},
        difficulty = 75.0,  # Avatar kill is ~70
        normal_item = "AutopsyAdventPsiWitchCompleted"
    ),
}

vanilla_other_techs: dict[str, X2WOTCLocationData] = {
    "ResistanceRadio": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Resistance Radio",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:ResistanceCommunications"},
        difficulty = 15.0,
        normal_item = "ResistanceRadioCompleted"
    ),
    "Tech_Elerium": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Elerium",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:GaussWeapons", "tree:PlatedArmor", "tree:AutopsyAdventMEC"},
        difficulty = 40.0,
        normal_item = "EleriumCompleted"
    ),
    "Psionics": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Psionics",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"tree:AutopsySectoid"},
        difficulty = 20.0,
        normal_item = "PsionicsCompleted"
    ),
}

#=======================================================================================================================
#                                               ALIEN HUNTERS
#-----------------------------------------------------------------------------------------------------------------------

alien_hunters_techs: dict[str, X2WOTCLocationData] = {
    "ExperimentalWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Experimental Weapons",
        id = get_new_location_id(),
        type = "Tech",
        difficulty = 5.0,
        dlc = "AH",
        normal_item = "ExperimentalWeaponsCompleted"
    ),
    "AutopsyViperKing": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Viper King Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "kill_ruler", "tree:AlienBiotech"},
        difficulty = 45.0,
        dlc = "AH",
        normal_item = "AutopsyViperKingCompleted"
    ),
    "AutopsyBerserkerQueen": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Berserker Queen Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "kill_ruler", "tree:AlienBiotech"},
        difficulty = 60.0,
        dlc = "AH",
        normal_item = "AutopsyBerserkerQueenCompleted"
    ),
    "AutopsyArchonKing": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Archon King Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "kill_ruler", "tree:AlienBiotech"},
        difficulty = 75.0,
        dlc = "AH",
        normal_item = "AutopsyArchonKingCompleted"
    ),
}

#=======================================================================================================================
#                                             WAR OF THE CHOSEN
#-----------------------------------------------------------------------------------------------------------------------

wotc_autopsy_techs: dict[str, X2WOTCLocationData] = {
    "AutopsyAdventPurifier": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Purifier Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer", "diff:AdvPurifierM1", "diff:AdvPurifierM2", "diff:AdvPurifierM3"},
        dlc = "WOTC",
        normal_item = "AutopsyAdventPurifierCompleted"
    ),
    "AutopsyAdventPriest": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Priest Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventOfficer", "diff:AdvPriestM1", "diff:AdvPriestM2", "diff:AdvPriestM3"},
        dlc = "WOTC",
        normal_item = "AutopsyAdventPriestCompleted"
    ),
    "AutopsyTheLost": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "The Lost Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech"},
        difficulty = 35.0,  # Not shuffled
        dlc = "WOTC",
        normal_item = "AutopsyTheLostCompleted"
    ),
    "AutopsySpectre": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Spectre Autopsy",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech", "diff:SpectreM1", "diff:SpectreM2"},
        dlc = "WOTC",
        normal_item = "AutopsySpectreCompleted"
    ),
}

wotc_chosen_weapon_techs: dict[str, X2WOTCLocationData] = {
    "ChosenAssassinWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Assassin Weapons",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"defeat_assassin"},
        difficulty = 75.0,
        dlc = "WOTC",
        normal_item = "ChosenAssassinWeaponsCompleted"
    ),
    "ChosenHunterWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Hunter Weapons",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"defeat_hunter"},
        difficulty = 75.0,
        dlc = "WOTC",
        normal_item = "ChosenHunterWeaponsCompleted"
    ),
    "ChosenWarlockWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Warlock Weapons",
        id = get_new_location_id(),
        type = "Tech",
        tags = {"defeat_warlock"},
        difficulty = 75.0,
        dlc = "WOTC",
        normal_item = "ChosenWarlockWeaponsCompleted"
    ),
}

########################################################################################################################
##                                            ENEMY KILL LOCATIONS                                                    ##
########################################################################################################################

#=======================================================================================================================
#                                                 BASE GAME
#-----------------------------------------------------------------------------------------------------------------------

vanilla_enemy_kills: dict[str, X2WOTCLocationData] = {
    "KillSectoid": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Sectoid",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Sectoid"}
    ),
    "KillViper": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Viper",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Viper"}
    ),
    "KillMuton": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Muton",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Muton"}
    ),
    "KillBerserker": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Berserker",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Berserker"}
    ),
    "KillArchon": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Archon",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Archon"}
    ),
    "KillGatekeeper": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Gatekeeper",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Gatekeeper"}
    ),
    "KillAndromedon": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Andromedon",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Andromedon"}
    ),
    "KillAndromedonRobot": X2WOTCLocationData(
        display_name = ENEMY_DESTROY_LOCATION_PREFIX + "Andromedon Shell",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AndromedonRobot"}
    ),
    "KillFaceless": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Faceless",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Faceless"},
    ),
    "KillChryssalid": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Chryssalid",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Chryssalid"}
    ),
    "KillAdventTrooper": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Trooper",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AdvTrooperM1", "diff:AdvTrooperM2", "diff:AdvTrooperM3"}
    ),
    "KillAdventCaptain": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Officer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        difficulty = 0.0  # Not shuffled, Gatecrasher
    ),
    "KillCyberus": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Codex",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"skulljack_officer"},
        difficulty = 30.0  # Not shuffled
    ),
    "KillAdventPsiWitch": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Avatar",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"skulljack_codex"},
        difficulty = 70.0  # Not shuffled
    ),
    "KillAdventStunLancer": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Stun Lancer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AdvStunLancerM1", "diff:AdvStunLancerM2", "diff:AdvStunLancerM3"}
    ),
    "KillAdventShieldBearer": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Shieldbearer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AdvShieldBearerM2", "diff:AdvShieldBearerM3"}
    ),
    "KillAdventMEC": X2WOTCLocationData(
        display_name = ENEMY_DESTROY_LOCATION_PREFIX + "ADVENT MEC",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AdvMEC_M1", "diff:AdvMEC_M2"}
    ),
    "KillAdventTurret": X2WOTCLocationData(
        display_name = ENEMY_DESTROY_LOCATION_PREFIX + "ADVENT Turret",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        difficulty = 30.0  # Not shuffled
    ),
    "KillSectopod": X2WOTCLocationData(
        display_name = ENEMY_DESTROY_LOCATION_PREFIX + "Sectopod",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:Sectopod"}
    ),
}

#=======================================================================================================================
#                                               ALIEN HUNTERS
#-----------------------------------------------------------------------------------------------------------------------

alien_hunters_enemy_kills: dict[str, X2WOTCLocationData] = {
    "KillViperKing": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Viper King",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"kill_ruler"},
        difficulty = 45.0,
        dlc = "AH"
    ),
    "KillBerserkerQueen": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Berserker Queen",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"kill_ruler"},
        difficulty = 60.0,
        dlc = "AH"
    ),
    "KillArchonKing": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Archon King",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"kill_ruler"},
        difficulty = 75.0,
        dlc = "AH"
    ),
}

#=======================================================================================================================
#                                             WAR OF THE CHOSEN
#-----------------------------------------------------------------------------------------------------------------------

wotc_enemy_kills: dict[str, X2WOTCLocationData] = {
    "KillAdventPurifier": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Purifier",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AdvPurifierM1", "diff:AdvPurifierM2", "diff:AdvPurifierM3"},
        dlc = "WOTC"
    ),
    "KillAdventPriest": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Priest",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:AdvPriestM1", "diff:AdvPriestM2", "diff:AdvPriestM3"},
        dlc = "WOTC"
    ),
    "KillTheLost": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "The Lost",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        difficulty = 35.0,  # Not shuffled
        dlc = "WOTC"
    ),
    "KillSpectre": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Spectre",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"diff:SpectreM1", "diff:SpectreM2"},
        dlc = "WOTC"
    ),
    "KillChosenAssassin": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Chosen Assassin",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"kill_assassin"},
        difficulty = 70.0,
        dlc = "WOTC"
    ),
    "KillChosenSniper": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Chosen Hunter",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"kill_hunter"},
        difficulty = 70.0,
        dlc = "WOTC"
    ),
    "KillChosenWarlock": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Chosen Warlock",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = {"kill_warlock"},
        difficulty = 70.0,
        dlc = "WOTC"
    ),
}

########################################################################################################################
##                                             ITEM USE LOCATIONS                                                     ##
########################################################################################################################

# Item use difficulties are primarily intended to prevent a location from being in logic way too early,
# when it would be unreasonable to have already acquired the necessary resources; ignoring however
# the timing at which a player might *want* to build the item.
# As an additional consideration, the proving ground will not be expected to have been built before
# difficulty 25, and the time needed to complete any proving ground projects will also be factored in.
# Also note that the wiki lies about Advanced Explosives, it does not actually require Experimental Grenade.
#
# Proving ground project abbreviations used below (all others are omitted):
# PL  - Plasma Grenade
# AE  - Advanced Explosives
# BP  - Bluescreen Protocol
# EG  - Experimental Grenade
# EXO - E.X.O. Suit
# EHW - Experimental Heavy Weapon
# WAR - W.A.R. Suit
# EPW - Experimental Powered Weapon

#=======================================================================================================================
#                                                 BASE GAME
#-----------------------------------------------------------------------------------------------------------------------

vanilla_item_uses: dict[str, X2WOTCLocationData] = {
    "UseMedikit": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Medikit",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility"},
        difficulty = 5.0  # 35 supplies (but difficult to use so avoid sphere 1)
    ),
    "UseNanoMedikit": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Nanomedikit",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "proving_ground", "item:AutopsyViperCompleted", "diff:Viper"},
        difficulty = 35.0  # 100 supplies, 1 core, 3 corpses (1 PG project)
    ),
    "UseSKULLJACK": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Skulljack",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "proving_ground", "skulljack_officer"},
        difficulty = 30.0  # 50 supplies (1 PG project)
    ),
    "UseFragGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Frag Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade"},
        difficulty = 0.0  # Free
    ),
    "UseAlienGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Plasma Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:AutopsyMutonCompleted"},
        difficulty = 35.0  # 75 supplies, 1 cores, 5 alloys, 5 elerium (1 PG project; PL)
    ),
    "UseProximityMine": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Proximity Mine",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "item:AutopsyAndromedonCompleted"},
        difficulty = 10.0  # 100 supplies
    ),
    "UseFlashbangGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Flashbang Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade"},
        difficulty = 0.0  # 35 supplies
    ),
    "UseEMPGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "EMP Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:AutopsyAdventMECCompleted"},
        difficulty = 35.0  # 50 supplies, 1 core (1 PG project; BP)
    ),
    "UseEMPGrenadeMk2": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "EMP Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:AutopsyAdventMECCompleted", "item:AutopsyMutonCompleted"},
        difficulty = 45.0  # 160 supplies, 2 cores, 10 alloys, 10 elerium (3 PG projects; PL + AE + BP)
    ),
    "UseSmokeGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Smoke Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade"},
        difficulty = 0.0  # 25 supplies
    ),
    "UseSmokeGrenadeMk2": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Smoke Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:AutopsyMutonCompleted"},
        difficulty = 45.0  # 150 supplies, 2 cores, 10 alloys, 10 elerium (2 PG projects; PL + AE)
    ),
    "UseBattleScanner": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Battle Scanner",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "item:AutopsyAdventTrooperCompleted"},
        difficulty = 0.0  # 30 supplies
    ),
    "UseMimicBeacon": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Mimic Beacon",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "item:AutopsyFacelessCompleted", "diff:Faceless"},
        difficulty = 10.0  # 75 supplies, 2 corpses
    ),
    "UseCombatStims": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Overdrive Serum",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "item:AutopsyBerserkerCompleted", "diff:Berserker"},
        difficulty = 0.0  # 35 supplies, 1 corpse
    ),
    "UseBluescreenRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Bluescreen Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"ammo", "proving_ground", "item:AutopsyAdventMECCompleted"},
        difficulty = 35.0  # 75 supplies, 1 core (1 PG project; BP)
    ),
    "UseExperimentalAmmo": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Experimental Ammo",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"ammo", "proving_ground"},
        difficulty = 30.0  # 1 core (1 PG project)
    ),
    "UseExperimentalGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Experimental Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground"},
        difficulty = 30.0  # 1 core (1 PG project; EG)
    ),
    "UseExperimentalGrenadeMk2": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Experimental Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:AutopsyMutonCompleted"},
        difficulty = 45.0  # 125 supplies, 3 cores, 10 alloys, 10 elerium (3 PG projects; PL + AE + EG)
    ),
    "UseRocketLauncher": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Rocket Launcher",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "proving_ground", "item:PlatedArmorCompleted", "diff:AdvTrooperM1", "diff:AdvTrooperM2", "diff:AdvTrooperM3"},
        difficulty = 35.0  # 1 core, 5 alloys, 5 elerium, 2 corpses (1 PG project; EXO)
    ),
    "UseExperimentalHeavyWeapon": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Experimental Heavy Weapon",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "proving_ground", "item:PlatedArmorCompleted", "diff:AdvTrooperM1", "diff:AdvTrooperM2", "diff:AdvTrooperM3"},
        difficulty = 40.0  # 2 cores, 5 alloys, 5 elerium, 2 corpses (2 PG projects; EXO + EHW)
    ),
    "UseExperimentalPoweredWeapon": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Experimental Powered Weapon",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "proving_ground", "item:PoweredArmorCompleted"},
        difficulty = 50.0  # 100 supplies, 2 cores, 10 alloys, 5 elerium (2 PG projects; WAR + EPW)
    ),
}

#=======================================================================================================================
#                                               ALIEN HUNTERS
#-----------------------------------------------------------------------------------------------------------------------

alien_hunters_item_uses: dict[str, X2WOTCLocationData] = {
    "UseFrostbomb": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Frost Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:ExperimentalWeaponsCompleted"},
        difficulty = 30.0,  # 35 supplies (1 PG project)
        dlc = "AH"
    ),
}

#=======================================================================================================================
#                                             WAR OF THE CHOSEN
#-----------------------------------------------------------------------------------------------------------------------

wotc_item_uses: dict[str, X2WOTCLocationData] = {
    "UseUltrasonicLure": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Ultrasonic Lure",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "item:AutopsyTheLostCompleted"},
        difficulty = 0.0,  # 30 supplies
        dlc = "WOTC"
    ),
    "UseRefractionField": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Refraction Field",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"utility", "item:AutopsySpectreCompleted", "diff:SpectreM1", "diff:SpectreM2"},
        difficulty = 10.0,  # 50 supplies, 1 corpse
        dlc = "WOTC"
    ),
}

########################################################################################################################
##                                           SOLDIER RANK LOCATIONS                                                   ##
########################################################################################################################

human_soldier_ranks: dict[str, X2WOTCLocationData] = {
    f"{soldier_class.title()}Rank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + soldier_class + SOLDIER_RANK_LOCATION_INFIX + rank_name,
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {soldier_class.lower(), f"item:{soldier_class.title()}Rank:{rank - 1}"},
        dlc = dlc,
        normal_item = f"{soldier_class.title()}Rank"
    )
    for (soldier_class, dlc) in [
        ("Ranger", None),
        ("Grenadier", None),
        ("Specialist", None),
        ("Sharpshooter", None),
        ("Reaper", "WOTC"),
        ("Skirmisher", "WOTC"),
        ("Templar", "WOTC"),
    ]
    for (rank, rank_name) in zip(range(2, 8), DEFAULT_RANK_NAME_SET)
}

spark_soldier_ranks: dict[str, X2WOTCLocationData] = {
    f"SparkRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "SPARK" + SOLDIER_RANK_LOCATION_INFIX + rank_name,
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"spark", "proving_ground", f"item:SparkRank:{rank - 1}"},
        dlc = "SLG",
        difficulty = 40.0,  # 100 supplies, 2 cores, 20 alloys, 15 elerium (1 PG project)
        normal_item = "SparkRank"
    )
    for (rank, rank_name) in [
        (2, "Aspirant"),
        (3, "Knight"),
        (4, "Cavalier"),
        (5, "Vanguard"),
        (6, "Paladin"),
        (7, "Champion"),
    ]
}

########################################################################################################################
##                                          COVERT ACTION LOCATIONS                                                   ##
########################################################################################################################

#=======================================================================================================================
#                                                 CHOSEN HUNT
#-----------------------------------------------------------------------------------------------------------------------

chosen_hunt_covert_actions: dict[str, X2WOTCLocationData] = {
    "ChosenHuntPt1:1": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Behind Enemy Lines (1/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_first_chosen"},
        difficulty = 20.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt1:2": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Behind Enemy Lines (2/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_all_chosen"},
        difficulty = 35.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt1:3": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Behind Enemy Lines (3/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_all_chosen"},
        difficulty = 50.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt2:1": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Find the Stronghold (1/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_first_chosen", "item:FactionInfluence:1"},
        difficulty = 30.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt2:2": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Find the Stronghold (2/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_all_chosen", "item:FactionInfluence:3"},
        difficulty = 45.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt2:3": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Find the Stronghold (3/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_all_chosen", "item:FactionInfluence:5"},
        difficulty = 60.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt3:1": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Into the Fire (1/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_first_chosen", "item:FactionInfluence:2"},
        difficulty = 40.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt3:2": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Into the Fire (2/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_all_chosen", "item:FactionInfluence:4"},
        difficulty = 55.0,
        dlc = "WOTC"
    ),
    "ChosenHuntPt3:3": X2WOTCLocationData(
        display_name = COVERT_ACTION_LOCATION_PREFIX + "Into the Fire (3/3)",
        id = get_new_location_id(),
        type = "CovertAction",
        tags = {"chosen_hunt", "meet_all_chosen", "item:FactionInfluence:6"},
        difficulty = 70.0,
        dlc = "WOTC"
    ),
}

########################################################################################################################
##                                              EVENT LOCATIONS                                                       ##
########################################################################################################################

event_locations: dict[str, X2WOTCLocationData] = {
    "Victory": X2WOTCLocationData(
        display_name = "Victory",
        difficulty = 90.0,
        normal_item = "Victory"
    ),
    "Broadcast": X2WOTCLocationData(
        display_name = "Broadcast",
        difficulty = 80.0,
        normal_item = "Broadcast"
    ),
    "Stronghold1": X2WOTCLocationData(
        display_name = "Stronghold 1",
        difficulty = 40.0,
        normal_item = "Stronghold1"
    ),
    "Stronghold2": X2WOTCLocationData(
        display_name = "Stronghold 2",
        difficulty = 55.0,
        normal_item = "Stronghold2"
    ),
    "Stronghold3": X2WOTCLocationData(
        display_name = "Stronghold 3",
        difficulty = 70.0,
        normal_item = "Stronghold3"
    ),
}

########################################################################################################################
##                                              TOTAL LOCATIONS                                                       ##
########################################################################################################################

tech_location_table: dict[str, X2WOTCLocationData] = {
    **vanilla_weapon_techs,
    **vanilla_armor_techs,
    **vanilla_autopsy_techs,
    **vanilla_goldenpath_techs,
    **vanilla_other_techs,
    **alien_hunters_techs,
    **wotc_autopsy_techs,
    **wotc_chosen_weapon_techs,
}

kill_location_table: dict[str, X2WOTCLocationData] = {
    **vanilla_enemy_kills,
    **alien_hunters_enemy_kills,
    **wotc_enemy_kills,
}

item_use_location_table: dict[str, X2WOTCLocationData] = {
    **vanilla_item_uses,
    **alien_hunters_item_uses,
    **wotc_item_uses,
}

soldier_rank_location_table: dict[str, X2WOTCLocationData] = {
    **human_soldier_ranks,
    **spark_soldier_ranks,
}

location_table: dict[str, X2WOTCLocationData] = {
    **tech_location_table,
    **kill_location_table,
    **item_use_location_table,
    **soldier_rank_location_table,
    **chosen_hunt_covert_actions,
    **event_locations,
}
