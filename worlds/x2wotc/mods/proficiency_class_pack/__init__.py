from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld

from .Items import items
from .Locations import locations, soldier_classes, MAX_RANK

name = "Proficiency Class Pack"

rule_priority = 0.0

def generate_early(world: "X2WOTCWorld"):
    # Base game GTS classes are disabled
    for soldier_class in [
        "Ranger",
        "Grenadier",
        "Specialist",
        "Sharpshooter",
    ]:
        for rank in range(2, 8):
            world.loc_manager.disable_location(f"{soldier_class.title()}Rank{rank}")
            world.item_manager.remove_item(f"{soldier_class.title()}Rank")

RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": dedent(
        """
        +DisabledDataEntries=DefaultRanger
        +DisabledDataEntries=DefaultGrenadier
        +DisabledDataEntries=DefaultSpecialist
        +DisabledDataEntries=DefaultSharpshooter
        """
    ) + "".join(
        f"+RanksanityData=(ID=\"{internal_name.title()}\", ClassName=\"{internal_name.title()}\", \\\\\n{RANKS_STR})\n" for internal_name in soldier_classes.keys()
    )
}
