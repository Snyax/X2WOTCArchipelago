from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
)

RANK_NAME_SET = [
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
MAX_RANK = 8

locations: dict[str, X2WOTCLocationData] = {
    f"JediRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Jedi" + SOLDIER_RANK_LOCATION_INFIX + RANK_NAME_SET[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"jedi", f"item:JediRank:{rank - 1}"},
        difficulty = 25.0,  # Only obtained by random promotion
        dlc = None,
        normal_item = "JediRank"
    )
    for rank in range(2, MAX_RANK + 1)
}
