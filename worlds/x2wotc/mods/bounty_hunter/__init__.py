from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

name = "Iridar's Bounty Hunter Class"

rule_priority = 0.0

MAX_RANK = 7
RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))

items: dict[str, X2WOTCItemData] = {
    "BountyHunterRank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "Bounty Hunter",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {"bounty_hunter"},
        power = 15.0,
    )
}

locations: dict[str, X2WOTCLocationData] = {
    f"BountyHunterRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Bounty Hunter" + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"bounty_hunter", f"item:BountyHunterRank:{rank - 1}"},
        difficulty = 10.0,  # You get one out of a CA
        dlc = None,
        normal_item = "BountyHunterRank"
    )
    for rank in range(2, MAX_RANK + 1)
}

config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": f'+RanksanityData=(ID="BountyHunter", ClassName="BountyHunter", {RANKS_STR})'
}
