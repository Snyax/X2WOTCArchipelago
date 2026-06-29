from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id

items: dict[str, X2WOTCItemData] = {
    "WardenRank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "Warden",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {"warden"},
        power = 15.0,
    )
}
