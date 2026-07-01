from .Items import items
from .Locations import locations, soldier_classes, MAX_RANK

name = "Shadow Ops Perk Pack"

rule_priority = 0.0

RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": "".join(
        f'+RanksanityData=(ID="{internal_name.title()}", ClassName="{internal_name.title()}", {RANKS_STR})' for internal_name in soldier_classes.keys()
    )
}
