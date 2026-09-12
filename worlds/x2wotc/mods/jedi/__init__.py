from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
)

name = "Jedi Class Revised"

rule_priority = 0.0

MAX_RANK = 8
RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
RANK_NAMES = [
    "Rookie",
    "Initiate",
    "Padawan",
    "Knight",
    "Guardian",
    "Sentinel",
    "Consular",
    "Master",
    "Grand Master",
]

items: dict[str, X2WOTCItemData] = {
    "JediRank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "Jedi",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {"jedi"},
        power = 15.0,
    )
}

locations: dict[str, X2WOTCLocationData] = {
    f"JediRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Jedi" + SOLDIER_RANK_LOCATION_INFIX + RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"jedi", f"item:JediRank:{rank - 1}"},
        difficulty = 25.0,  # Only obtained by random promotion
        dlc = None,
        normal_item = "JediRank"
    )
    for rank in range(2, MAX_RANK + 1)
}

config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": f'+RanksanityData=(ID="Jedi", ClassName="Jedi", {RANKS_STR})'
}
