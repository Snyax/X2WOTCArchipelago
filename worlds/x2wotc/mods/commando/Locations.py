from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

MAX_RANK = 7

locations: dict[str, X2WOTCLocationData] = {
    f"AlphaCommandoRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Commando" + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"commando", f"item:AlphaCommandoRank:{rank - 1}"},
        dlc = None,
        normal_item = "AlphaCommandoRank"
    )
    for rank in range(2, MAX_RANK + 1)
}
