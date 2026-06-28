from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAME_SET,
)

MAX_RANK = 7

locations: dict[str, X2WOTCLocationData] = {
    f"BountyHunterRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Bounty Hunter" + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAME_SET[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"bounty_hunter", f"item:BountyHunterRank:{rank - 1}"},
        dlc = None,
        normal_item = "BountyHunterRank"
    )
    for rank in range(2, MAX_RANK + 1)
}
