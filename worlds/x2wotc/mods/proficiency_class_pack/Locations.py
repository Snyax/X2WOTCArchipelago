from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

MAX_RANK = 7

# Keys are internal names, values are localized names
soldier_classes = {
    "WOTC_APA_Assault": "Assault Infantry",
    "WOTC_APA_Medic": "Field Medic",
    "WOTC_APA_Marine": "Marine",
    "WOTC_APA_Marksman": "Marksman",
    "WOTC_APA_Sapper": "Sapper",
    "WOTC_APA_Specialist": "Tech Specialist",
}


soldier_ranks: dict[str, X2WOTCLocationData] = {
    f"{internal_name.title()}Rank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + localized_name + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {f"{localized_name.lower().replace(" ", "_")}", f"item:{internal_name.title()}Rank:{rank - 1}"},
        dlc = None,
        normal_item = f"{internal_name.title()}Rank"
    )
    for internal_name, localized_name in soldier_classes.items()
    for rank in range(2, MAX_RANK + 1)
}

locations: dict[str, X2WOTCLocationData] = {
    **soldier_ranks,
}
