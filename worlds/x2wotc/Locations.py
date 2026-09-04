from collections import defaultdict
from copy import deepcopy
from logging import warning
from typing import Any

from BaseClasses import Location

from .EnemyRando import EnemyRandoManager
from .LocationData import X2WOTCLocationData, location_table

from .mods import mod_locations


class X2WOTCLocation(Location):
    game: str = "XCOM 2 War of the Chosen"


# Add mod locations
for loc_name, loc_data in mod_locations.items():
    if loc_name not in location_table:
        location_table[loc_name] = loc_data
    else:
        warning(f"X2WOTC: Duplicate location {loc_name} in mods, skipping")

# Lookup tables
loc_display_name_to_id = {
    loc_data.display_name: loc_data.id
    for loc_data in location_table.values()
    if loc_data.id
}
loc_display_name_to_key = {
    loc_data.display_name: key
    for key, loc_data in location_table.items()
}
loc_id_to_key = {
    loc_data.id: key
    for key, loc_data in location_table.items()
    if loc_data.id
}

# Location groups
loc_groups: dict[str, set[str]] = defaultdict(set)
for loc_data in location_table.values():
    # Type
    loc_groups[loc_data.type].add(loc_data.display_name)
    # DLC
    if loc_data.dlc:
        loc_groups[loc_data.dlc].add(loc_data.display_name)
    # Tags
    for tag in loc_data.tags:
        if ":" not in tag:
            # Convert snake_case tag to PascalCase
            tag = "".join(word.capitalize() for word in tag.split("_"))
            loc_groups[tag].add(loc_data.display_name)


class LocationManager:
    loc_display_name_to_id = loc_display_name_to_id
    loc_display_name_to_key = loc_display_name_to_key
    loc_id_to_key = loc_id_to_key
    loc_groups = loc_groups

    def __init__(self, enemy_rando_manager: EnemyRandoManager):
        self.enemy_rando_manager: EnemyRandoManager = enemy_rando_manager
        self.autopsy_difficulty: float = 3.0

        self.location_table: dict[str, X2WOTCLocationData] = deepcopy(location_table)
        self.replaced: dict[str, dict[str, Any]] = defaultdict(dict)
        self.locked: bool = False

        self.enabled: dict[str, bool] = {loc_name: True for loc_name in self.location_table.keys()}
        self.num_locations: int = len(self.location_table)

    def replace(self, loc_name: str, **kwargs):
        if self.locked:
            raise RuntimeError("Cannot replace location data after location manager has been locked.")

        loc_data = self.location_table[loc_name]
        self.location_table[loc_name] = loc_data.replace(**kwargs)
        self.replaced[loc_name].update(kwargs)

    def get_location_difficulty(self, loc_name: str) -> float:
        loc_data = self.location_table[loc_name]
        base_difficulty = loc_data.difficulty

        # Handle difficulty tags for enemy rando
        diff_tag_enemies = [tag[5:] for tag in loc_data.tags if tag.startswith("diff:")]
        diff_tag_difficulty = self.enemy_rando_manager.get_difficulty(diff_tag_enemies)
        if "autopsy" in loc_data.tags:
            diff_tag_difficulty += self.autopsy_difficulty  # Autopsies take time

        return max(base_difficulty, diff_tag_difficulty)

    def disable_location(self, loc_name: str) -> bool:
        if self.locked:
            raise RuntimeError("Cannot disable locations after location manager has been locked.")

        if not self.enabled[loc_name]:
            return False

        self.enabled[loc_name] = False
        self.num_locations -= 1
        return True
