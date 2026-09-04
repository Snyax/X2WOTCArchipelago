from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import (
    get_new_item_id,
    X2WOTCItemData,
    TECH_ITEM_PREFIX,
    PCS_ITEM_PREFIX,
    WEAPON_MOD_ITEM_PREFIX,
    PROMOTION_ITEM_PREFIX,
)


# For the full definition of X2WOTCItemData, see worlds/x2wotc/ItemData.py
lwotc_items: dict[str, X2WOTCItemData] = {
    "LaserWeaponsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Laser Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 50.0,
        normal_location = "LaserWeapons"
    ),
    "AdvancedLasersCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Advanced Laser Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 50.0,
        normal_location = "AdvancedLasers"
    ),
    "_GaussWeaponsCompleted_LW": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Advanced Magnetic Weapons",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 100.0,
        normal_location = "_GaussWeapons_LW"
    ),
    "CoilgunsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Coilguns",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 150.0,
        normal_location = "Coilguns"
    ),
    "AdvancedCoilgunsCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Advanced Coilguns",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 150.0,
        normal_location = "AdvancedCoilguns"
    ),
    "ProgressiveRifleTechLwotcCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Rifle (LWOTC)",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "LaserWeaponsCompleted",
            "MagnetizedWeaponsCompleted",
            "CoilgunsCompleted",
            "PlasmaRifleCompleted",
        ]
    ),
    "ProgressiveRifleTechLwotcCompleted+": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Rifle+ (LWOTC)",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "ModularWeaponsCompleted",
            "LaserWeaponsCompleted",
            "MagnetizedWeaponsCompleted",
            "CoilgunsCompleted",
            "PlasmaRifleCompleted",
        ]
    ),
    "ProgressiveAdvancedWeaponTechLwotcCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Advanced Weapons (LWOTC)",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon", "progressive"},
        stages = [
            "AdvancedLasersCompleted",
            "_GaussWeaponsCompleted_LW",
            "AdvancedCoilgunsCompleted",
            "HeavyPlasmaCompleted",
            "PlasmaSniperCompleted",
            "AlloyCannonCompleted",
        ],
        shuffle_stages = {3, 4, 5}
    ),
    "ProgressiveHeavyArmorTechLwotcCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Heavy Armor (LWOTC)",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor", "progressive"},
        stages = [
            "EXOSuitCompleted",
            "WARSuitCompleted",
        ]
    ),
    "ProgressiveLightArmorTechLwotcCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive Light Armor (LWOTC)",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"armor", "progressive"},
        stages = [
            "SpiderSuitCompleted",
            "WraithSuitCompleted",
        ]
    ),
    "AutopsyDroneCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "ADVENT Robotics",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 50.0,
        normal_location = "AutopsyDrone"
    ),
    "ProgressiveGREMLINTechLwotcCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Progressive GREMLIN (LWOTC)",
        id = get_new_item_id(),
        classification = IC.progression | IC.useful,
        type = "TechCompleted",
        tags = {"utility", "weapon", "progressive"},
        stages = [
            "AutopsyDroneCompleted",
            "AutopsySectopodCompleted",
        ]
    ),
    "AutopsyMutonEliteCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Muton Elite Autopsy",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"weapon"},
        power = 60.0,
        normal_location = "AutopsyMutonElite"
    ),
    "EXOSuitCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Battle Armor",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 120.0,
        normal_location = "EXOSuit"
    ),
    "WARSuitCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Battlesuits",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 200.0,
        normal_location = "WARSuit"
    ),
    "SpiderSuitCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Mobile Armor",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 120.0,
        normal_location = "SpiderSuit"
    ),
    "WraithSuitCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Shadow Armor",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "TechCompleted",
        tags = {"armor"},
        power = 200.0,
        normal_location = "WraithSuit"
    ),
}

lwotc_pcs_items: dict[str, X2WOTCItemData] = {
    "DepthPerceptionPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Depth Perception",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "depth_perception"},
    ),
    "HyperReactivePupilsPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Hyper-Reactive Pupils",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "hyper_reactive_pupils"},
    ),
    "CombatAwarenessPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Unwavering Stance",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "combat_awareness"},
    ),
    "CombatRushPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Combat Rush",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "combat_rush"},
    ),
    "DamageControlPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Damage Control",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "damage_control"},
    ),
    "AbsorptionFieldsPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Absorption Fields",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "absorption_fields"},
    ),
    "BodyShieldPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Body Shield",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "body_shield"},
    ),
    "EmergencyLifeSupportPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Emergency Life Support",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "emergency_life_support"},
    ),
    "IronSkinPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Iron Skin",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "iron_skin"},
    ),
    "SmartMacrophagesPCS:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Smart Macrophages",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "smart_macrophages"},
    ),
    "CommonPCSDefense:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Defense",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "basic", "defense"},
    ),
    "RarePCSDefense:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Defense",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "advanced", "defense"},
    ),
    "EpicPCSDefense:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Defense",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "superior", "elite", "defense"},
    ),
    "CommonPCSPsi:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Psi",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "basic", "psi"},
    ),
    "RarePCSPsi:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Psi",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "advanced", "psi"},
    ),
    "EpicPCSPsi:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Psi",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "superior", "elite", "psi"},
    ),
    "CommonPCSHacking:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Basic Hacking",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "basic", "hacking"},
    ),
    "RarePCSHacking:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Advanced Hacking",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "pcs", "advanced", "hacking"},
    ),
    "EpicPCSHacking:1": X2WOTCItemData(
        display_name = PCS_ITEM_PREFIX + "Superior Hacking",
        id = get_new_item_id(),
        type = "Resource",
        classification = IC.useful,
        tags = {"filler", "pcs", "superior", "elite", "hacking"},
    ),
}

lwotc_weapon_mod_items: dict[str, X2WOTCItemData] = {
    "_AimUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Scope",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "scope", "superior", "elite"}
    ),
    "_CritUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Laser Sight",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "laser_sight", "superior", "elite"}
    ),
    "_ReloadUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Auto-Loader",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "auto_loader", "superior", "elite"}
    ),
    "_MissDamageUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Stock",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "stock", "superior", "elite"}
    ),
    "_FreeFireUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Hair Trigger",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "hair_trigger", "superior", "elite"}
    ),
    "_ClipSizeUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Expanded Magazine",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "expanded_magazine", "superior", "elite"}
    ),
    "_FreeKillUpgrade_Bsc_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Basic Suppressor",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "repeater", "suppressor", "basic"}
    ),
    "_FreeKillUpgrade_Adv_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Advanced Suppressor",
        id = get_new_item_id(),
        type = "Resource",
        tags = {"filler", "weapon_mod", "repeater", "suppressor", "advanced"}
    ),
    "_FreeKillUpgrade_Sup_LW:1": X2WOTCItemData(
        display_name = WEAPON_MOD_ITEM_PREFIX + "Elite Suppressor",
        id = get_new_item_id(),
        classification = IC.useful,
        type = "Resource",
        tags = {"filler", "weapon_mod", "repeater", "suppressor", "superior", "elite"}
    ),
}

lwotc_native_promotion_items: dict[str, X2WOTCItemData] = {
    f"LWS_{class_name.title()}Rank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "LW " + class_name,
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {f"{class_name.lower()}"},
        power = 15.0,
    )
    for class_name in [
        "Assault",
        "Grenadier",
        "Gunner",
        "Ranger",
        "Sharpshooter",
        "Shinobi",
        "Specialist",
        "Technical",
    ]
}

lwotc_modified_promotion_items = {
    f"_{class_name.title()}_LWRank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "LW " + class_name,
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {f"{class_name.lower()}"},
        power = 15.0,
    )
    for class_name in [
        "Skirmisher",
        "Reaper",
        "Templar",
        "SPARK",
    ]
}

items: dict[str, X2WOTCItemData] = {
    **lwotc_items,
    **lwotc_pcs_items,
    **lwotc_weapon_mod_items,
    **lwotc_native_promotion_items,
    **lwotc_modified_promotion_items,
}
