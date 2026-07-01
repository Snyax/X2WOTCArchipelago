from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

MAX_RANK = 7

locations: dict[str, X2WOTCLocationData] = {
    f"KeeperRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Keeper" + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"keeper", f"item:KeeperRank:{rank - 1}"},
        difficulty = 5.0,  # Obtained in the first retal
        dlc = None,
        normal_item = "KeeperRank"
    )
    for rank in range(2, MAX_RANK + 1)
}
