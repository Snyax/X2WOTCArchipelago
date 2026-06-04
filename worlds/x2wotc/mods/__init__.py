import importlib
from logging import warning
import pkgutil
from typing import NamedTuple, Callable, TYPE_CHECKING

from Options import Option

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld
from worlds.x2wotc.ItemData import X2WOTCItemData
from worlds.x2wotc.LocationData import X2WOTCLocationData


class X2WOTCModData(NamedTuple):
    name: str
    rule_priority: float = 0.0
    items: dict[str, X2WOTCItemData] = {}
    item_map: dict[str, str] = {}
    locations: dict[str, X2WOTCLocationData] = {}
    location_map: dict[str, str] = {}
    set_rules: Callable[["X2WOTCWorld"], None] | None = None
    options: list[tuple[str, type[Option]]] = []
    generate_early: Callable[["X2WOTCWorld"], None] | None = None
    config: dict[str, str] = {}


mods_data: list[X2WOTCModData] = []

mod_names: list[str] = []
mod_items: dict[str, X2WOTCItemData] = {}
mod_locations: dict[str, X2WOTCLocationData] = {}
mod_options: list[tuple[str, type[Option]]] = []

# Collect mod data from directories
for loader, module_name, ispkg in pkgutil.iter_modules(__path__):
    try:
        module = importlib.import_module(f".{module_name}", __name__)
    except ImportError as e:
        warning(f"X2WOTC: Failed to import module mods/{module_name}, {e}")
        continue

    mods_data.append(X2WOTCModData(
        name = module.name if hasattr(module, "name") else module_name,
        rule_priority = module.rule_priority if hasattr(module, "rule_priority") else 0,
        items = module.items if hasattr(module, "items") else {},
        item_map = module.item_map if hasattr(module, "item_map") else {},
        locations = module.locations if hasattr(module, "locations") else {},
        location_map = module.location_map if hasattr(module, "location_map") else {},
        set_rules = module.set_rules if hasattr(module, "set_rules") else None,
        options = module.options if hasattr(module, "options") else [],
        generate_early = module.generate_early if hasattr(module, "generate_early") else None,
        config = module.config if hasattr(module, "config") else {}
    ))

# Sort mods by rule priority
mods_data.sort(key=lambda x: x.rule_priority)

# Flatten mod data and check for duplicates
for mod_data in mods_data:
    if mod_data.name not in mod_names:
        mod_names.append(mod_data.name)
    else:
        warning(f"X2WOTC: Duplicate mod name {mod_data.name}")

    for item_name, item_data in mod_data.items.items():
        if item_name not in mod_items:
            mod_items[item_name] = item_data
        else:
            warning(f"X2WOTC: Duplicate item name {item_name} in mod {mod_data.name}")

    for loc_name, loc_data in mod_data.locations.items():
        if loc_name not in mod_locations:
            mod_locations[loc_name] = loc_data
        else:
            warning(f"X2WOTC: Duplicate location name {loc_name} in mod {mod_data.name}")

    for option in mod_data.options:
        if option[0] not in [mod_option[0] for mod_option in mod_options]:
            mod_options.append(option)
        else:
            warning(f"X2WOTC: Duplicate option name {option[0]} in mod {mod_data.name}")

# Sort mod names alphabetically
mod_names.sort()
