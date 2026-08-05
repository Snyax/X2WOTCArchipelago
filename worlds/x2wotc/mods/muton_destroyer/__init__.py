from BaseClasses import ItemClassification

from worlds.x2wotc.ItemData import X2WOTCItemData, TECH_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    TECH_LOCATION_PREFIX,
    ENEMY_KILL_LOCATION_PREFIX,
    ITEM_USE_LOCATION_PREFIX,
    get_new_location_id
)


# Steam workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=2482812108
name = "Muton Destroyer - WotC"

items: dict[str, X2WOTCItemData] = {
    "Autopsy_AshMutonDestroyerCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Muton Destroyer Autopsy",
        id = get_new_item_id(),
        classification = ItemClassification.progression,
        layer = "Strategy",
        type = "TechCompleted",
        tags = {"armor", "weapon"},
        power = 35.0,
        normal_location = "Autopsy_AshMutonDestroyer"
    ),
}

locations: dict[str, X2WOTCLocationData] = {
    "Autopsy_AshMutonDestroyer": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Muton Destroyer Autopsy",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech"},
        difficulty = 32.0,  # FL 7
        normal_item = "Autopsy_AshMutonDestroyerCompleted"
    ),
    "KillAshMutonDestroyer": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Muton Destroyer",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        difficulty = 29.0  # FL 7
    ),
    "UseWeapon_AshConcussionGrenadeXCom": X2WOTCLocationData(
        display_name = ITEM_USE_LOCATION_PREFIX + "Concussion Grenade",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "ItemUse",
        tags = {"grenade", "proving_ground", "item:Autopsy_AshMutonDestroyerCompleted"},
        difficulty = 20.0,
    ),
}

config: dict[str, str] = {
    "X2Item_ResearchCompleted": "+CheckCompleteTechs=(TechName=Autopsy_AshMutonDestroyer)",
    "X2EventListener_WOTCArchipelago": (
        "+CheckKillCustomCharacterGroups=(GroupName=AshMutonDestroyer, "
        "Members[0]=AshMutonDestroyerM1, "
        "Members[1]=AshMutonDestroyerM2, "
        "Members[2]=AshMutonDestroyerM3, "
        "Members[3]=AshMutonDestroyerM4)"
    ),
    "X2Effect_ItemUseCheck": "+CheckUseItems=Weapon_AshConcussionGrenadeXCom",
}
