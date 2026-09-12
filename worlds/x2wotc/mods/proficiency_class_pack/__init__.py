from textwrap import dedent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld
from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

name = "Proficiency Class Pack"

rule_priority = 0.0

MAX_RANK = 7
RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
# Keys are internal names, values are localized names
SOLDIER_CLASSES = {
    "WOTC_APA_Assault": "Assault Infantry",
    "WOTC_APA_Medic": "Field Medic",
    "WOTC_APA_Marine": "Marine",
    "WOTC_APA_Marksman": "Marksman",
    "WOTC_APA_Sapper": "Sapper",
    "WOTC_APA_Specialist": "Tech Specialist",
}

def generate_early(world: "X2WOTCWorld"):
    # Base game GTS classes are disabled
    for soldier_class in [
        "Ranger",
        "Grenadier",
        "Specialist",
        "Sharpshooter",
    ]:
        for rank in range(2, 8):
            world.loc_manager.disable_location(f"{soldier_class.title()}Rank{rank}")
            world.item_manager.remove_item(f"{soldier_class.title()}Rank")

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
    "WOTCArchipelago_Ranksanity": dedent(
        """
        +DisabledDataEntries=DefaultRanger
        +DisabledDataEntries=DefaultGrenadier
        +DisabledDataEntries=DefaultSpecialist
        +DisabledDataEntries=DefaultSharpshooter
        """
    ) + "\n".join(
        f'+RanksanityData=(ID="{internal_name.title()}", ClassName="{internal_name.title()}", {RANKS_STR})' for internal_name in SOLDIER_CLASSES.keys()
    )
}
