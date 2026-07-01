from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

MAX_RANK = 7

locations: dict[str, X2WOTCLocationData] = {
    f"AkimboRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Akimbo" + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"akimbo", f"item:AkimboRank:{rank - 1}"},
        dlc = None,
        normal_item = "AkimboRank"
    )
    for rank in range(2, MAX_RANK + 1)
}
