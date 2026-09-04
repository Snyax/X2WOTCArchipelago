from collections import defaultdict
from copy import deepcopy
from logging import warning
from random import Random
from typing import Any

from BaseClasses import Item
from BaseClasses import ItemClassification as IC

from .ItemData import (
    X2WOTCItemData,
    resource_item_table,
    weapon_mod_item_table,
    pcs_item_table,
    staff_item_table,
    trap_item_table,
    nothing_items,
    item_table,
)

from .mods import mod_items


class X2WOTCItem(Item):
    game: str = "XCOM 2 War of the Chosen"

    def __init__(self, player: int, item_data: X2WOTCItemData):
        super(X2WOTCItem, self).__init__(
            item_data.display_name,
            item_data.classification,
            item_data.id,
            player
        )


# Add mod items
for item_name, item_data in mod_items.items():
    if item_name not in item_table:
        item_table[item_name] = item_data
    else:
        warning(f"X2WOTC: Duplicate item {item_name} in mods, skipping")

# Lookup tables
item_display_name_to_id = {
    item_data.display_name: item_data.id
    for item_data in item_table.values()
    if item_data.id
}
item_display_name_to_key = {
    item_data.display_name: key
    for key, item_data in item_table.items()
}
item_id_to_key = {
    item_data.id: key
    for key, item_data in item_table.items()
    if item_data.id
}

# Item groups
item_groups: dict[str, set[str]] = defaultdict(set)
for item_data in item_table.values():
    if item_data.id:
        # Type
        item_groups[item_data.type].add(item_data.display_name)
        # DLC
        if item_data.dlc:
            item_groups[item_data.dlc].add(item_data.display_name)
        # Tags
        for tag in item_data.tags:
            if ":" not in tag:
                # Convert snake_case tag to PascalCase
                tag = "".join(word.capitalize() for word in tag.split("_"))
                item_groups[tag].add(item_data.display_name)


class ItemManager:
    item_display_name_to_id = item_display_name_to_id
    item_display_name_to_key = item_display_name_to_key
    item_id_to_key = item_id_to_key
    item_groups = item_groups

    def __init__(self):
        self.item_table: dict[str, X2WOTCItemData] = deepcopy(item_table)
        self.replaced: dict[str, dict[str, Any]] = defaultdict(dict)
        self.locked: bool = False

        self.resource_items: set[str] = set(resource_item_table.keys())
        self.weapon_mod_items: set[str] = set(weapon_mod_item_table.keys())
        self.pcs_items: set[str] = set(pcs_item_table.keys())
        self.staff_items: set[str] = set(staff_item_table.keys())
        self.trap_items: set[str] = set(trap_item_table.keys())
        self.nothing_items: set[str] = set(nothing_items.keys())

        self.item_count: dict[str, int] = {}
        self.real_count: dict[str, int] = {}
        self.num_items: int = 0

        # NOTE: not all non-filler items define normal_location,
        # those that don't must be added in generate_early
        for item_name, item_data in self.item_table.items():
            if item_data.normal_location is None:
                self.item_count[item_name] = 0
                self.real_count[item_name] = 0
            else:
                self.item_count[item_name] = 1
                self.real_count[item_name] = 1
                self.num_items += 1

    def replace(self, item_name: str, **kwargs):
        if self.locked:
            raise RuntimeError("Cannot replace item data after item manager has been locked.")

        item_data = self.item_table[item_name]
        self.item_table[item_name] = item_data.replace(**kwargs)
        self.replaced[item_name].update(kwargs)

    def shuffle_stages(self, item_name: str, random: Random):
        item_data = self.item_table[item_name]
        if not item_data.stages or not item_data.shuffle_stages:
            raise ValueError(f"Cannot shuffle stages for item {item_name}.")

        shuffled_indices = list(item_data.shuffle_stages)
        random.shuffle(shuffled_indices)
        shuffled_stages = [
            stage if index not in item_data.shuffle_stages
            else item_data.stages[shuffled_indices.pop()]
            for index, stage in enumerate(item_data.stages)
        ]
        self.replace(item_name, stages=shuffled_stages)

    def get_item_power(self, item_name: str, count: int) -> float:
        item_data = self.item_table[item_name]
        if item_data.stages is None:
            return item_data.power * min(count, self.item_count[item_name])
        else:
            return sum([
                self.item_table[item_data.stages[i]].power
                for i in range(min(count, len(item_data.stages)))
                if item_data.stages[i] is not None
            ])

    def get_total_power(self) -> float:
        return sum([
            self.get_item_power(item_name, count)
            for item_name, count in self.item_count.items()
        ])

    def set_item_count(self, item_name: str, new_count: int):
        if self.locked:
            raise RuntimeError("Cannot set item counts after item manager has been locked.")

        old_count = self.item_count[item_name]
        self.item_count[item_name] = new_count
        self.num_items += new_count - old_count

        # For real_count, progressive items aren't counted but their stages are
        item_data = self.item_table[item_name]
        if item_data.stages is None:
            self.real_count[item_name] += new_count - old_count
        else:
            for stage in item_data.stages[min(old_count, new_count):max(old_count, new_count)]:
                if stage is not None:
                    self.real_count[stage] += 1 if new_count > old_count else -1

    def add_item(self, item_name: str, count: int = 1):
        self.set_item_count(item_name, self.item_count[item_name] + count)

    def remove_item(self, item_name: str, count: int = 1) -> bool:
        if self.item_count[item_name] < count:
            return False

        self.set_item_count(item_name, self.item_count[item_name] - count)
        return True

    def disable_item(self, item_name: str):
        self.set_item_count(item_name, 0)

    def enable_progressive_item(self, item_name: str, random: Random | None = None):
        item_data = self.item_table[item_name]
        stages = item_data.stages
        if stages is None:
            raise ValueError(f"Cannot enable non-progressive item {item_name}.")

        if self.item_count[item_name] != 0:
            raise ValueError(f"Cannot enable progressive item {item_name}, ",
                             f"incorrect count ({self.item_count[item_name]} != 0).")
        for stage_name in stages:
            if stage_name is not None and self.item_count[stage_name] != 1:
                raise ValueError(f"Cannot enable progressive item {item_name}, ",
                                 f"incorrect count for stage {stage_name} ({self.item_count[stage_name]} != 1).")

        self.set_item_count(item_name, len(stages))
        for stage_name in stages:
            if stage_name is not None:
                self.set_item_count(stage_name, 0)

        if item_data.shuffle_stages and random is not None:
            self.shuffle_stages(item_name, random)

    def disable_progressive_item(self, item_name: str) -> bool:
        item_data = self.item_table[item_name]
        stages = item_data.stages
        if stages is None:
            raise ValueError(f"Cannot disable non-progressive item {item_name}.")

        if self.item_count[item_name] != len(stages):
            raise ValueError(f"Cannot disable progressive item {item_name}, ",
                             f"incorrect count ({self.item_count[item_name]} != {len(stages)}).")
        for stage_name in stages:
            if stage_name is not None and self.item_count[stage_name] != 0:
                raise ValueError(f"Cannot disable progressive item {item_name}, ",
                                 f"incorrect count for stage {stage_name} ({self.item_count[stage_name]} != 0).")

        self.set_item_count(item_name, 0)
        for stage_name in stages:
            if stage_name is not None:
                self.set_item_count(stage_name, 1)

    def enable_chosen_hunt_items(self, progressive: bool):
        if progressive:
            self.set_item_count("ProgressiveAssassinChosenHunt", 3)
            self.set_item_count("ProgressiveHunterChosenHunt", 3)
            self.set_item_count("ProgressiveWarlockChosenHunt", 3)
        else:
            self.set_item_count("FactionInfluence", 6)
            self.set_item_count("AssassinStronghold", 1)
            self.set_item_count("HunterStronghold", 1)
            self.set_item_count("WarlockStronghold", 1)

    def get_nothing_item(self, random: Random) -> str:
        if self.nothing_items:
            return random.choice(sorted(self.nothing_items))
        return "Nothing"

    def get_filler_item_name(
            self,
            resource_share: int,
            weapon_mod_share: int,
            pcs_share: int,
            staff_share: int,
            trap_share: int,
            nothing_share: int,
            random: Random
        ) -> str:
        filler_item_sets = (
            [self.resource_items] * resource_share
            + [self.weapon_mod_items] * weapon_mod_share
            + [self.pcs_items] * pcs_share
            + [self.staff_items] * staff_share
            + [self.trap_items] * trap_share
            + [self.nothing_items] * nothing_share
        )

        if filler_item_sets:
            filler_items = sorted(random.choice(filler_item_sets))
            if filler_items:
                filler_item = random.choice(filler_items)
                return self.item_table[filler_item].display_name

        nothing_item = self.get_nothing_item(random)
        return self.item_table[nothing_item].display_name

    def add_filler_items(
            self,
            num_filler_items: int,
            resource_share: int,
            weapon_mod_share: int,
            pcs_share: int,
            staff_share: int,
            trap_share: int,
            nothing_share: int,
            random: Random
        ):
        items_per_share = num_filler_items / max(1, sum([
            resource_share,
            weapon_mod_share,
            pcs_share,
            staff_share,
            trap_share,
            nothing_share,
        ]))
        num_names_pairs = [
            # Sort by priority for filling missing items (due to rounding errors, or in case all shares are 0)
            (round(items_per_share * nothing_share), sorted(self.nothing_items)),
            (round(items_per_share * resource_share), sorted(self.resource_items)),
            (round(items_per_share * weapon_mod_share), sorted(self.weapon_mod_items)),
            (round(items_per_share * pcs_share), sorted(self.pcs_items)),
            (round(items_per_share * staff_share), sorted(self.staff_items)),
            (round(items_per_share * trap_share), sorted(self.trap_items)),
        ]

        # Adjust largest share to fill missing items, respecting priority
        max_num = max([n for n, _ in num_names_pairs])
        missing = num_filler_items - sum([n for n, _ in num_names_pairs])
        for index, (num, names) in enumerate(num_names_pairs):
            if num == max_num:
                num_names_pairs[index] = (num + missing, names)
                break

        # Add specified number of each type of filler/trap
        for (num, names) in num_names_pairs:
            for _ in range(num):
                if names:
                    self.add_item(random.choice(names))
                else:
                    self.add_item(self.get_nothing_item(random))
