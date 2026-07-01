from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

MAX_RANK = 8

# Keys are internal names, values are localized names
soldier_classes = {
    "ShadowOps_CombatEngineer_LW2": "Combat Engineer",
    "ShadowOps_Dragoon_LW2": "Dragoon",
    "ShadowOps_Hunter_LW2": "Hunter",
    "ShadowOps_Infantry_LW2": "Infantry",
    "ShadowOps_Scrapper_LW2": "Scrapper",
    "ShadowOps_Juggernaut_LW2": "Juggernaut",
    "ShadowOps_Survivalist_LW2": "Survivalist",
    "ShadowOps_Recon_LW2": "Recon",
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
