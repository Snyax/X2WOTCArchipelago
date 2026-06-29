from textwrap import dedent

from .Items import items
from .Locations import locations, MAX_RANK

name = "Rescue Denmother"

rule_priority = 0.0

RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": f"+RanksanityData=(ID=\"Keeper\", ClassName=\"Keeper\", \\\\\n{RANKS_STR})\n"
}
