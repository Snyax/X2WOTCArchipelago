from dataclasses import dataclass, make_dataclass
from schema import And, Schema

from Options import (
    Choice,
    OptionDict,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)

from .mods import mod_names, mod_options


class AlienHuntersDLC(Choice):
    """Set which locations and items from the Alien Hunters DLC are enabled.

    none:                 All Alien Hunters DLC locations and items are disabled.
    no_integrated_dlc:    Experimental Weapons location is disabled; for playing without the Integrated DLC option.
    no_alien_rulers:      Alien Ruler locations are disabled; for avoiding tedious encounters.
    all:                  All Alien Hunters DLC locations and items are enabled."""
    display_name = "Alien Hunters DLC"
    option_none = 0
    option_no_integrated_dlc = 1
    option_no_alien_rulers = 2
    option_all = 3
    default = option_none


class ShensLastGiftDLC(Toggle):
    """Enable locations and items from the Shen's Last Gift DLC."""
    display_name = "Shen's Last Gift DLC"
    default = False


class Goal(Choice):
    """Set the goal of the seed.

    alien_fortress:         Beat the Alien Fortress Assault mission. (final mission)
    network_tower:          Beat the ADVENT Network Tower Assault mission. (second to last mission)
    chosen_stronghold_1:    Beat any Chosen Stronghold Assault mission.
    chosen_stronghold_2:    Beat any two Chosen Stronghold Assault missions.
    chosen_stronghold_3:    Beat all three Chosen Stronghold Assault missions.

    alien_fortress and network_tower (without extra considerations) are only recommended for async settings.
    For sync settings, maybe try chosen_stronghold_1 first and experiment from there."""
    display_name = "Goal"
    option_alien_fortress = 0
    option_network_tower = 1
    option_chosen_stronghold_1 = 2
    option_chosen_stronghold_2 = 3
    option_chosen_stronghold_3 = 4
    default = option_alien_fortress

    value_to_event = {
        option_alien_fortress: "Victory",
        option_network_tower: "Broadcast",
        option_chosen_stronghold_1: "Stronghold1",
        option_chosen_stronghold_2: "Stronghold2",
        option_chosen_stronghold_3: "Stronghold3",
    }

    def as_event(self) -> str:
        return self.value_to_event[self.value]


class CampaignCompletionRequirements(OptionSet):
    """Require these objectives to be completed for the final mission to be unlocked.
    Set all if you wish to experience a more vanilla XCOM 2 story progression.

    'PsiGateObjective':         Require completion of the psi gate research.
    'StasisSuitObjective':      Require completion of the stasis suit research.
    'AvatarCorpseObjective':    Require acquisition of an avatar corpse."""
    display_name = "Campaign Completion Requirements"
    completion_requirements = frozenset([
        "PsiGateObjective",
        "StasisSuitObjective",
        "AvatarCorpseObjective",
    ])
    valid_keys = completion_requirements
    default = frozenset()


class ExcludePostGoalLocations(Toggle):
    """Exclude locations that are considered more difficult than the selected goal event.
    These locations will not contain important items or items from other worlds.
    Recommended when using an early goal option, e.g. in sync settings.
    NOTE: This option requires enabling additional vacant locations, e.g. through Enemysanity or Itemsanity."""
    display_name = "Exclude Post-Goal Locations"
    default = True


class EnemySanity(Toggle):
    """Enable locations for the first kill of each enemy type."""
    display_name = "Enemysanity"
    default = True


class ItemSanity(Toggle):
    """Enable locations for the first use of each item type."""
    display_name = "Itemsanity"
    default = False


class RankSanity(Choice):
    """Shuffle soldier rank-up locations and promotion items.

    none:               Do not shuffle soldier promotions.
    base_classes_only:  Only shuffle promotions for the four base soldier classes.
    no_spark:           Only shuffle promotions for the four base soldier classes and the three faction hero classes.
    no_faction_heroes:  Only shuffle promotions for the four base soldier classes and SPARKs.
    all:                Shuffle promotions for all eight soldier classes."""
    display_name = "Ranksanity"
    option_none = 0
    option_base_classes_only = 1
    option_no_spark = 2
    option_no_faction_heroes = 3
    option_all = 4
    default = option_none

    spark_tags = {"spark"}
    faction_hero_tags = {"reaper", "skirmisher", "templar"}

    def is_excluded(self, tags: set[str]) -> bool:
        return (self.value == self.option_none
                or (self.value == self.option_no_spark
                    and any(tag in tags for tag in self.spark_tags))
                or (self.value == self.option_no_faction_heroes
                    and any(tag in tags for tag in self.faction_hero_tags))
                or (self.value == self.option_base_classes_only
                    and any(tag in tags for tag in self.spark_tags | self.faction_hero_tags)))

    def all_humans_included(self) -> bool:
        return self.value == self.option_no_spark or self.value == self.option_all


class GlobalPromotions(Toggle):
    """Enable global promotions for all soldier classes, including those not covered by Ranksanity.
    This adds no locations to the multiworld but rewards default promotion items for rank-up events of all classes,
    meaning when one soldier reaches a certain rank, all soldiers of the same class will now have that rank going forward.
    Recommended if you want insurance against DeathLink without enabling full Ranksanity (as it "saves your progress")."""
    display_name = "Global Promotions"
    default = False


class ChosenHuntSanity(Choice):
    """Shuffle Chosen Hunt covert actions and their rewards, i.e. Resistance Faction influence and Chosen Stronghold missions."""
    display_name = "Chosen Huntsanity"
    option_off = 0
    option_separate = 1
    option_progressive = 2
    default = option_off


class ProgressiveItems(OptionSet):
    """Force these items to be collected in order.
    Valid values: 'GunTech', 'GunTech+' (includes [Tech] Modular Weapons),
                  'ArmorTech', 'ArmorTech+' (includes [Tech] Hybrid Materials),
                  'SwordTech', 'GREMLINTech', 'PsionicsTech'"""
    display_name = "Progressive Items"
    valid_keys = frozenset([
        "GunTech",
        "GunTech+",
        "ArmorTech",
        "ArmorTech+",
        "SwordTech",
        "GREMLINTech",
        "PsionicsTech",
    ])
    default = frozenset([
        "GunTech",
        "ArmorTech",
        "SwordTech",
        "GREMLINTech",
        "PsionicsTech",
    ])


class ChosenWeaponFragments(Choice):
    """Split Chosen weapons into two or three fragments each. Collect all fragments to unlock the corresponding tech.
    This should decrease the likelihood of receiving Chosen weapons too early and trivializing the game.
    NOTE: This option requires enabling additional vacant locations, e.g. through Enemysanity or Itemsanity."""
    display_name = "Chosen Weapon Fragments"
    option_off = 0
    option_two = 1
    option_three = 2
    default = option_off


class EarlyProvingGround(Toggle):
    """Force the Proving Ground to be unlockable very early (sphere 1)."""
    display_name = "Early Proving Ground"
    default = True


class ResourceShare(Range):
    """Set the share of filler items to be resources."""
    display_name = "Resource Share"
    range_start = 0
    range_end = 100
    default = 65


class WeaponModShare(Range):
    """Set the share of filler items to be weapon upgrades."""
    display_name = "Weapon Mod Share"
    range_start = 0
    range_end = 100
    default = 15


class PCSShare(Range):
    """Set the share of filler items to be PCSs."""
    display_name = "PCS Share"
    range_start = 0
    range_end = 100
    default = 10


class StaffShare(Range):
    """Set the share of filler items to be staff."""
    display_name = "Staff Share"
    range_start = 0
    range_end = 100
    default = 10


class TrapShare(Range):
    """Set the share of filler items to be traps."""
    display_name = "Trap Share"
    range_start = 0
    range_end = 100
    default = 0


class NothingShare(Range):
    """Set the share of filler items to be nothing."""
    display_name = "Nothing Share"
    range_start = 0
    range_end = 100
    default = 0


class EnemyRando(Toggle):
    """Enable enemy shuffle, randomizing both scripted and procedural encounters."""
    display_name = "Enemy Rando"
    default = False


class EnemyPlandoPreset(Choice):
    """Override enemy plando with a preset configuration.

    custom:         All enemies are shuffled by default. Edit enemy plando manually for finer control.
    advent_only:    Only ADVENT enemies are shuffled.
    aliens_only:    Only alien (non-ADVENT) enemies are shuffled.
    separate:       ADVENT and non-ADVENT enemies are shuffled separately."""
    display_name = "Enemy Plando Preset"
    option_custom = 0
    option_advent_only = 1
    option_aliens_only = 2
    option_separate = 3
    default = option_custom


class EnemyPlando(OptionDict):
    """If enemy rando is enabled, constrain enemy placements.
    Define explicit shuffle groups with the 'forced' key.
    Exempt enemies from shuffling with the 'fixed' key.

    Example: {
        'forced': [
            [['Sectoid', 'Muton'], ['Viper', 'Archon']],
            [['Adv'], ['Adv']]
        ],
        'fixed': ['Gatekeeper', 'Sectopod']
    }
    Sectoids and Mutons will be replaced by Vipers and Archons randomly.
    All ADVENT enemies will be replaced by random ADVENT enemies.
    Gatekeepers and Sectopods will not be shuffled.
    All other enemies will be shuffled among each other."""
    display_name = "Enemy Plando"
    schema = Schema({
        "forced": [And([[str]], lambda l: len(l) == 2)],
        "fixed": [str],
    })
    default = {"forced": [], "fixed": []}


class RemoveCorpseCosts(Toggle):
    """Remove corpse costs from all items. Recommended if enemy rando is enabled."""
    display_name = "Remove Corpse Costs"
    default = False


class HintResearchProjects(Choice):
    """Enable research project hints in the Avenger laboratory and shadow chamber.
    Can be changed in-game via Mod Config Menu.

    off:       Reveal no item info and don't create server hints.
    partial:   Reveal item categories but don't create server hints.
    full:      Reveal all item info and create server hints."""
    display_name = "Hint Research Projects"
    option_off = 0
    option_partial = 1
    option_full = 2
    default = option_partial


class SkipMissionTypes(OptionSet):
    """Automatically skip these mission types when they are spawned from a regular calendar event.
    Can be changed in-game via Mod Config Menu.
    Valid values: 'SupplyRaid', 'CouncilMission', 'ResistanceOp'"""
    display_name = "Skip Tedious Missions"
    mission_types = frozenset([
        "SupplyRaid",
        "CouncilMission",
        "ResistanceOp",
    ])
    valid_keys = mission_types
    default = mission_types


class DisableCovertActionRisks(OptionSet):
    """Disable these covert action risks.
    Can be changed in-game via Mod Config Menu.
    Valid values: 'Ambush', 'Capture'"""
    display_name = "Disarm Covert Action Risks"
    covert_action_risks = frozenset([
        "Ambush",
        "Capture",
    ])
    valid_keys = covert_action_risks
    default = covert_action_risks


class SupplyRaidRewardBase(Range):
    """Set the amount of resources that are rewarded for skipped supply raids.
    The base represents a percentage of set maximum values for supplies (200), alien alloys (80), elerium crystals (40) and elerium cores (3).
    The error determines the range of possible values, e.g. 35-65% for default settings.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Supply Raid Reward Base"
    range_start = 0
    range_end = 100
    default = 50


class SupplyRaidRewardError(Range):
    """Set the amount of resources that are rewarded for skipped supply raids.
    The base represents a percentage of set maximum values for supplies (200), alien alloys (80), elerium crystals (40) and elerium cores (3).
    The error determines the range of possible values, e.g. 35-65% for default settings.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Supply Raid Reward Error"
    range_start = 0
    range_end = 100
    default = 15


class ExtraXPGain(Range):
    """Set the amount of extra XP that soldiers gain passively.
    Each time an enemy dies, each soldier has the given fraction of a kill attributed to them, speeding up promotions.
    Because this system is agnostic to who got the final hit, soldiers with low kill counts will benefit more from the increase.
    In general, the effect will be much stronger than it seems; the default setting for example will work out to a 35% increase in XP from kills,
    but something like a 140% increase in XP from assists, meaning the actual bonus lies somewhere in between.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Extra XP Gain"
    range_start = 0
    range_end = 200
    default = 35


class ExtraCorpseGain(Range):
    """Set the amount of extra corpses that each enemy drops.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Extra Corpse Gain"
    range_start = 0
    range_end = 5
    default = 1


class DeathLink(Toggle):
    """When one of XCOM's soldiers dies, everyone else who enabled DeathLink dies, and vice versa.
    Can be changed in-game via Mod Config Menu."""
    display_name = "DeathLink"
    default = False


class DeathLinkChance(Range):
    """Set the probability of a received DeathLink packet killing one of XCOM's soldiers.
    Yes, it's random. That's XCOM, baby!
    Can be changed in-game via Mod Config Menu."""
    display_name = "DeathLink Chance"
    range_start = 0
    range_end = 100
    default = 10


class InstantRookieTraining(Toggle):
    """Make training rookies in the GTS instant.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Instant Rookie Training"
    default = False


class InstantSPARKConstruction(Toggle):
    """Make constructing SPARKs in the Proving Ground instant. No effect if Shen's Last Gift DLC is disabled.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Instant SPARK Construction"
    default = False


class RefundSPARKCosts(Toggle):
    """Get construction costs refunded when a SPARK is destroyed. No effect if Shen's Last Gift DLC is disabled.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Refund SPARK Costs"
    default = False


class ReplaceFactionHeroes(Toggle):
    """Gain automatic replacements for dead or missing faction heroes.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Replace Faction Heroes"
    default = False


class DisableDayOneTraps(Toggle):
    """Disable traps received on (or before) the first day of a campaign.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Disable Day One Traps"
    default = True


class DisableTurnOneTraps(Toggle):
    """Disable traps received on (or before) the first turn of a mission.
    Can be changed in-game via Mod Config Menu."""
    display_name = "Disable Turn One Traps"
    default = True


class ActiveMods(OptionSet):
    """Activate these mods from the x2wotc/mods directory.
    This is only relevant when modding *the APWorld* (NOT the game), leave empty if you're unsure what that means.
    Read about APWorld mods at https://github.com/Snyax/X2WOTCArchipelago/blob/main/worlds/x2wotc/docs/apworld_mods.md
    List all available mods with the /mods client command."""
    display_name = "Active Mods"
    valid_keys = frozenset(mod_names)
    default = frozenset()


@dataclass
class X2WOTCOptions(PerGameCommonOptions):

    # Generic options
    start_inventory_from_pool: StartInventoryPool

    # DLC options
    alien_hunters_dlc: AlienHuntersDLC
    shens_last_gift_dlc: ShensLastGiftDLC

    # Goal options
    goal: Goal
    campaign_completion_requirements: CampaignCompletionRequirements
    exclude_post_goal_locations: ExcludePostGoalLocations

    # Location options
    enemy_sanity: EnemySanity
    item_sanity: ItemSanity
    rank_sanity: RankSanity
    global_promotions: GlobalPromotions
    chosen_hunt_sanity: ChosenHuntSanity

    # Item options
    progressive_items: ProgressiveItems
    chosen_weapon_fragments: ChosenWeaponFragments
    early_proving_ground: EarlyProvingGround

    # Filler options
    resource_share: ResourceShare
    weapon_mod_share: WeaponModShare
    pcs_share: PCSShare
    staff_share: StaffShare
    trap_share: TrapShare
    nothing_share: NothingShare

    # Randomization options
    enemy_rando: EnemyRando
    enemy_plando_preset: EnemyPlandoPreset
    enemy_plando: EnemyPlando
    remove_corpse_costs: RemoveCorpseCosts

    # Config options
    hint_research_projects: HintResearchProjects
    skip_mission_types: SkipMissionTypes
    disable_covert_action_risks: DisableCovertActionRisks
    supply_raid_reward_base: SupplyRaidRewardBase
    supply_raid_reward_error: SupplyRaidRewardError
    extra_xp_gain: ExtraXPGain
    extra_corpse_gain: ExtraCorpseGain
    deathlink: DeathLink
    deathlink_chance: DeathLinkChance
    instant_rookie_training: InstantRookieTraining
    instant_spark_construction: InstantSPARKConstruction
    refund_spark_costs: RefundSPARKCosts
    replace_faction_heroes: ReplaceFactionHeroes
    disable_day_one_traps: DisableDayOneTraps
    disable_turn_one_traps: DisableTurnOneTraps

    # Mod options
    active_mods: ActiveMods


# Add mod options
X2WOTCOptions = make_dataclass("X2WOTCOptions", mod_options, bases=(X2WOTCOptions,))

# Define option groups
x2wotc_option_groups: list[OptionGroup] = [
    OptionGroup(
        "DLC Options",
        [
            AlienHuntersDLC,
            ShensLastGiftDLC,
        ]
    ),
    OptionGroup(
        "Goal Options",
        [
            Goal,
            CampaignCompletionRequirements,
            ExcludePostGoalLocations,
        ]
    ),
    OptionGroup(
        "Location Options",
        [
            EnemySanity,
            ItemSanity,
            RankSanity,
            GlobalPromotions,
            ChosenHuntSanity,
        ]
    ),
    OptionGroup(
        "Item Options",
        [
            ProgressiveItems,
            ChosenWeaponFragments,
            EarlyProvingGround,
        ]
    ),
    OptionGroup(
        "Filler Options",
        [
            ResourceShare,
            WeaponModShare,
            PCSShare,
            StaffShare,
            TrapShare,
            NothingShare,
        ]
    ),
    OptionGroup(
        "Randomization Options",
        [
            EnemyRando,
            EnemyPlandoPreset,
            EnemyPlando,
            RemoveCorpseCosts,
        ]
    ),
    OptionGroup(
        "Config Options",
        [
            HintResearchProjects,
            SkipMissionTypes,
            DisableCovertActionRisks,
            SupplyRaidRewardBase,
            SupplyRaidRewardError,
            ExtraXPGain,
            ExtraCorpseGain,
            DeathLink,
            DeathLinkChance,
            InstantRookieTraining,
            InstantSPARKConstruction,
            RefundSPARKCosts,
            ReplaceFactionHeroes,
            DisableDayOneTraps,
            DisableTurnOneTraps,
        ]
    ),
    OptionGroup(
        "Mod Options",
        [
            ActiveMods,
        ] + [
            mod_option[1]
            for mod_option in mod_options
        ]
    ),
]
