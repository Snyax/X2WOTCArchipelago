from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id

items: dict[str, X2WOTCItemData] = {
    "AlphaRiflemanRank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "Vanguard",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {"vanguard"},
        power = 15.0,
    )
}
