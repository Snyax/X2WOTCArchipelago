from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    TECH_LOCATION_PREFIX,
    ENEMY_KILL_LOCATION_PREFIX,
    ENEMY_DESTROY_LOCATION_PREFIX,
    ITEM_USE_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
)


def clamp(x, min_, max_):
    return max(min(x, max_), min_)

def fl_to_diff(fl: int):
    return clamp(4.0 * (fl-1), 0.0, 100.0)

def fl_to_diff_autopsy(fl: int):
    return clamp(4.0 * (fl+1), 0.0, 100.0)

def fl_to_diff_pg(fl: int):
    return clamp(4.0 * (fl+2), 0.0, 100.0)

PG_GRENADE = {
    "grenade",
    "proving_ground",
    "item:HybridMaterialsCompleted",
}

PG_GRENADE_M2 = {
    "grenade",
    "proving_ground",
    "item:HybridMaterialsCompleted",
    "item:AutopsyMutonCompleted",
    "item:AutopsyAndromedonCompleted"
}

PG_AMMO = {
    "ammo",
    "proving_ground",
    "item:HybridMaterialsCompleted",
}

RANK_NAMES = [
    "Rookie",
    "Squaddie",
    "Lance Corporal",
    "Corporal",
    "Sergeant",
    "Staff Sergeant",
    "Tech Sergeant",
    "Gunnery Sergeant",
    "Master Sergeant",
]

PSI_RANK_NAMES = [
    "Rookie",
    "Initiate",
    "Acolyte",
    "Adept",
    "Disciple",
    "Mystic",
    "Warlock",
    "Magus",
    "Master",
]

SPARK_RANK_NAMES = [
    "Rookie",
    "Squire",
    "Aspirant",
    "Knight",
    "Cavalier",
    "Vanguard",
    "Paladin",
    "Champion",
    "Templar",
]

lwotc_techs: dict[str, X2WOTCLocationData] = {
    "AutopsyDrone": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "ADVENT Robotics",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyAdventTrooper", "tree:HybridMaterials"},
        difficulty = fl_to_diff_autopsy(8),
        normal_item = "AutopsyDroneCompleted"
    ),
    "AutopsyMutonElite": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Muton Elite Autopsy",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"autopsy", "tree:AutopsyMuton"},
        difficulty = fl_to_diff_autopsy(13),
        normal_item = "AutopsyMutonEliteCompleted"
    ),
    "LaserWeapons": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Laser Weapons",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:ModularWeapons", "tree:HybridMaterials"},
        difficulty = fl_to_diff(3),
        normal_item = "LaserWeaponsCompleted"
    ),
    "AdvancedLasers": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Advanced Laser Weapons",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:LaserWeapons"},
        difficulty = fl_to_diff(5),
        normal_item = "AdvancedLasersCompleted"
    ),
    "_GaussWeapons_LW": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Advanced Magnetic Weapons",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:MagnetizedWeapons"},
        difficulty = fl_to_diff(9),
        normal_item = "_GaussWeaponsCompleted_LW"
    ),
    "Coilguns": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Coilguns",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:_GaussWeapons_LW", "tree:Tech_Elerium"},
        difficulty = fl_to_diff(13),
        normal_item = "CoilgunsCompleted"
    ),
    "AdvancedCoilguns": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Advanced Coilguns",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:Coilguns"},
        difficulty = fl_to_diff(15),
        normal_item = "AdvancedCoilgunsCompleted"
    ),
    "EXOSuit": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Battle Armor",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:PlatedArmor"},
        difficulty = fl_to_diff(10),
        normal_item = "EXOSuitCompleted"
    ),
    "WARSuit": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Battlesuits",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:PoweredArmor", "tree:EXOSuit"},
        difficulty = fl_to_diff(18),
        normal_item = "WARSuitCompleted"
    ),
    "SpiderSuit": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Mobile Armor",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:PlatedArmor"},
        difficulty = fl_to_diff(10),
        normal_item = "SpiderSuitCompleted"
    ),
    "WraithSuit": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Shadow Armor",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"tree:PoweredArmor", "tree:SpiderSuit"},
        difficulty = fl_to_diff(18),
        normal_item = "WraithSuitCompleted"
    ),
}

lwotc_item_uses: dict[str, X2WOTCLocationData] = {
    "UseShapedCharge": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Shaped Charge",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade"},
        difficulty = 0.0,
    ),
    "UseGasGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Gas Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyViperCompleted"} | PG_GRENADE,
        difficulty = fl_to_diff_pg(3),
    ),
    "UseGasGrenadeMk2": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Gas Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyViperCompleted"} | PG_GRENADE_M2,
        difficulty = fl_to_diff_pg(3),
    ),
    "UseFirebomb": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Incendiary Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyAdventPurifierCompleted"} | PG_GRENADE,
        difficulty = fl_to_diff_pg(4),
    ),
    "UseFirebombMk2": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Incendiary Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        difficulty = fl_to_diff_pg(4),
        tags = {"item:AutopsyAdventPurifierCompleted"} | PG_GRENADE_M2,
    ),
    "UseAcidGrenade": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Acid Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsySpectreCompleted"} | PG_GRENADE,
        difficulty = fl_to_diff_pg(8),
    ),
    "UseAcidGrenadeMk2": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Acid Bomb",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsySpectreCompleted"} | PG_GRENADE_M2,
        difficulty = fl_to_diff_pg(8),
    ),
    "UsePrototypePlasmaBlaster": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Prototype Plasma Blaster",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "item:EXOSuitCompleted"},
        difficulty = fl_to_diff_pg(10),
    ),
    "UsePlasmaBlaster": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Plasma Blaster",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "proving_ground", "item:PlasmaRifleCompleted", "item:EXOSuitCompleted"},
        difficulty = fl_to_diff_pg(17),
    ),
    "UseShredderGun": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Shredder Gun",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "item:EXOSuitCompleted"},
        difficulty = fl_to_diff_pg(10),
    ),
    "UseShredstormCannon": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Shredstorm Cannon",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"weapon", "proving_ground", "item:AdvancedCoilgunsCompleted", "item:WARSuitCompleted"},
        difficulty = fl_to_diff_pg(18),
    ),
    "UseAPRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "AP Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"ammo", "item:AlienBiotechCompleted"},
        difficulty = 0.0,
    ),
    "UseTracerRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Tracer Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"ammo", "item:HybridMaterialsCompleted"},
        difficulty = 0.0,
    ),
    "UseTalonRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Talon Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyAdventOfficerCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(2),
    ),
    "UseVenomRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Venom Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyViperCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(3),
    ),
    "UseIncendiaryRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Dragon Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyMutonEliteCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(13),
    ),
    "UseStilettoRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Stiletto Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyAdventShieldbearerCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(7),
    ),
    "UseFlechetteRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Flechette Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyChryssalidCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(9),
    ),
    "UseRedscreenRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Redscreen Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyDroneCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(1),
    ),
    "UseNeedleRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Needle Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyFacelessCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(3),
    ),
    "UseFalconRounds": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Shredder Rounds",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"item:AutopsyAdventTurretCompleted"} | PG_AMMO,
        difficulty = fl_to_diff_pg(2),
    ),
}

lwotc_enemy_kills: dict[str, X2WOTCLocationData] = {
    "KillAdvEngineer": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Engineer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = 0.0
    ),
    "KillAdvGunner": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Gunner",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = 0.0
    ),
    "KillAdvSentry": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Sentry",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = 0.0
    ),
    "KillAdvRocketeer": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Rocketeer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(4)
    ),
    "KillAdvScout": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Scout",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(5)
    ),
    "KillAdvSergeant": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Sergeant",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(6)
    ),
    "KillAdvGrenadier": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Grenadier",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(7)
    ),
    "KillAdvGeneral_LW": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT General",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(10)
    ),
    "KillAdvShockTroop": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Shock Trooper",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(14)
    ),
    "KillAdvVanguard": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "ADVENT Vanguard",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(14)
    ),
    "KillLWDrone": X2WOTCLocationData(
        display_name = ENEMY_DESTROY_LOCATION_PREFIX + "Drone",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = 0.0
    ),
    "KillAdvMECArcher": X2WOTCLocationData(
        display_name = ENEMY_DESTROY_LOCATION_PREFIX + "MEC Archer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(8)
    ),
    "KillSidewinder": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Sidewinder",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(4)
    ),
    "KillNaja": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Naja",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(5)
    ),
    "KillMutonM2_LW": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Muton Centurion",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(9)
    ),
    "KillMutonM3_LW": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Muton Elite",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(13)
    ),
    "KillChryssalidSoldier": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Chryssalid Soldier",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(14)
    ),
    "KillHiveQueen": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Hive Queen",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        tags = set(),
        difficulty = fl_to_diff(17)
    ),
}

lwotc_native_soldier_ranks: dict[str, X2WOTCLocationData] = {
    f"LWS_{class_name.title()}Rank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "LW " + class_name + SOLDIER_RANK_LOCATION_INFIX + rank_name_set[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {f"{class_name.lower()}", f"item:LWS_{class_name.title()}Rank:{rank - 1}"},
        dlc = None,
        normal_item = f"LWS_{class_name.title()}Rank"
    )
    for class_name, rank_name_set in [
        ("Assault", RANK_NAMES),
        ("Grenadier", RANK_NAMES),
        ("Gunner", RANK_NAMES),
        ("Ranger", RANK_NAMES),
        ("Sharpshooter", RANK_NAMES),
        ("Shinobi", RANK_NAMES),
        ("Specialist", RANK_NAMES),
        ("Technical", RANK_NAMES),
    ]
    for rank in range(2, 9)
}

lwotc_modified_soldier_ranks: dict[str, X2WOTCLocationData] = {
    f"_{class_name.title()}_LWRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + f"LW {class_name}" + SOLDIER_RANK_LOCATION_INFIX + rank_name_set[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {f"{class_name.lower()}", f"item:_{class_name.title()}_LWRank:{rank - 1}"} | tags,
        difficulty = 40.0 if class_name == "SPARK" else 0.0,
        dlc = "SLG" if class_name == "SPARK" else "WOTC",
        normal_item = f"_{class_name.title()}_LWRank"
    )
    for class_name, rank_name_set, tags in [
        ("Skirmisher", RANK_NAMES, set[str]()),
        ("Reaper", RANK_NAMES, set[str]()),
        ("Templar", PSI_RANK_NAMES, set[str]()),
        ("SPARK", SPARK_RANK_NAMES, {"proving_ground"}),
    ]
    for rank in range(2, 9)
}

locations: dict[str, X2WOTCLocationData] = {
    **lwotc_techs,
    **lwotc_item_uses,
    **lwotc_enemy_kills,
    **lwotc_native_soldier_ranks,
    **lwotc_modified_soldier_ranks,
}
