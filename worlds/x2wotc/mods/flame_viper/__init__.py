from BaseClasses import ItemClassification

from worlds.x2wotc.ItemData import X2WOTCItemData, TECH_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    TECH_LOCATION_PREFIX,
    ENEMY_KILL_LOCATION_PREFIX,
    get_new_location_id
)


# Steam workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=1160638944
name = "Flame Viper - WotC"

items: dict[str, X2WOTCItemData] = {
    "Autopsy_AshFlameViperCompleted": X2WOTCItemData(
        display_name = TECH_ITEM_PREFIX + "Flame Viper Autopsy",
        id = get_new_item_id(),
        classification = ItemClassification.progression,
        layer = "Strategy",
        type = "TechCompleted",
        tags = {"armor", "weapon"},
        power = 25.0,
        normal_location = "Autopsy_AshFlameViper"
    ),
}

# Electing not to add ammo checks because they require specific experimental ammo to build which involves RNG
locations: dict[str, X2WOTCLocationData] = {
    "Autopsy_AshFlameViper": X2WOTCLocationData(
        display_name = TECH_LOCATION_PREFIX + "Flame Viper Autopsy",
        id = get_new_location_id(),
        layer = "Strategy",
        type = "Tech",
        tags = {"autopsy", "tree:AlienBiotech"},
        difficulty = 28.0,  # FL 6
        normal_item = "Autops_AshFlameViperCompleted"
    ),
    "KillAshFlameViper": X2WOTCLocationData(
        display_name = ENEMY_KILL_LOCATION_PREFIX + "Flame Viper",
        id = get_new_location_id(),
        layer = "Tactical",
        type = "EnemyKill",
        difficulty = 25.0  # FL 6
    ),
}

config: dict[str, str] = {
    "X2Item_ResearchCompleted": "+CheckCompleteTechs=(TechName=Autopsy_AshFlameViper)",
    "X2EventListener_WOTCArchipelago": "+CheckKillDefaultCharacterGroups=AshFlameViper",
}
