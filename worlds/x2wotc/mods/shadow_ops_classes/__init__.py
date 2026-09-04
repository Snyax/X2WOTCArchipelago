from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

name = "Shadow Ops Perk Pack"

rule_priority = 0.0

MAX_RANK = 8
RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
# Keys are internal names, values are localized names
SOLDIER_CLASSES = {
    "ShadowOps_CombatEngineer_LW2": "Combat Engineer",
    "ShadowOps_Dragoon_LW2": "Dragoon",
    "ShadowOps_Hunter_LW2": "Hunter",
    "ShadowOps_Infantry_LW2": "Infantry",
    "ShadowOps_Scrapper_LW2": "Scrapper",
    "ShadowOps_Juggernaut_LW2": "Juggernaut",
    "ShadowOps_Survivalist_LW2": "Survivalist",
    "ShadowOps_Recon_LW2": "Recon",
}

items: dict[str, X2WOTCItemData] = {
    f"{internal_name.title()}Rank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + localized_name,
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {f"{localized_name.lower().replace(" ", "_")}"},
        power = 15.0,
    )
    for internal_name, localized_name in SOLDIER_CLASSES.items()
}

locations: dict[str, X2WOTCLocationData] = {
    f"{internal_name.title()}Rank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + localized_name + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {f"{localized_name.lower().replace(" ", "_")}", f"item:{internal_name.title()}Rank:{rank - 1}"},
        dlc = None,
        normal_item = f"{internal_name.title()}Rank"
    )
    for internal_name, localized_name in SOLDIER_CLASSES.items()
    for rank in range(2, MAX_RANK + 1)
}

config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": "\n".join(
        f'+RanksanityData=(ID="{internal_name.title()}", ClassName="{internal_name.title()}", {RANKS_STR})' for internal_name in SOLDIER_CLASSES.keys()
    )
}
