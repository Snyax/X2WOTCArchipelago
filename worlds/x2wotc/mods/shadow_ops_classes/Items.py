from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id

from .Locations import soldier_classes

promotion_items: dict[str, X2WOTCItemData] = {
    f"{internal_name.title()}Rank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + localized_name,
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {f"{localized_name.lower().replace(" ", "_")}"},
        power = 15.0,
    )
    for internal_name, localized_name in soldier_classes.items()
}

items: dict[str, X2WOTCItemData] = {
    **promotion_items
}
