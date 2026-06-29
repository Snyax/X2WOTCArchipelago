from textwrap import dedent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld

from .Items import items
from .Locations import locations, MAX_RANK

name = "Iridar's Bounty Hunter Class"

rule_priority = 0.0

RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": f"+RanksanityData=(ID=\"BountyHunter\", ClassName=\"BountyHunter\", \\\\\n{RANKS_STR})\n"
}
