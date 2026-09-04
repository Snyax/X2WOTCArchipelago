from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld

from .Items import items, resource_items
from .Locations import locations
from .Options import options
from .Rules import set_rules


name = "Example Mod"

# For defining the order rules are applied in (in case of set_rule)
# The order is lowest to highest priority
rule_priority = 0.0

# Handle mod options here
def generate_early(world: "X2WOTCWorld"):
    if world.options.example_mod_option:
        world.loc_manager.disable_location("ExampleModLocation")
        world.item_manager.disable_item("ExampleModItem")

    # Add keys to filler item pool
    world.item_manager.resource_items.update(resource_items)

    # Edit item and location data if needed
    world.item_manager.replace("AutopsySectoidCompleted", power=50.0)
    world.loc_manager.replace("AutopsySectoid", difficulty=50.0)

# Insert config data here to define in-game behavior
# See Config/XComWOTCArchipelago.ini in the game mod directory
# for more information on the structure of the config file
config: dict[str, str] = {
    "X2Item_ResearchCompleted": "+CheckCompleteTechs=(TechName=ExampleTech)",
    "X2EventListener_WOTCArchipelago": "+CheckKillDefaultCharacterGroups=ExampleCharacterGroup",
    "X2Effect_ItemUseCheck": "+CheckUseItems=ExampleItem",
}
