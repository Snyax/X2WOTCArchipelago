from collections import defaultdict
from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from . import X2WOTCWorld
    from .Items import ItemManager
    from .Locations import LocationManager
    from .Options import X2WOTCOptions


# Cache per-player current power values to update on world.collect/remove
class X2WOTCState(LogicMixin):
    x2wotc_power_cache: dict[int, float]
    x2wotc_power_valid: dict[int, bool]

    def init_mixin(self, _: MultiWorld):
        self.x2wotc_power_cache = defaultdict(lambda: 0.0)
        self.x2wotc_power_valid = defaultdict(lambda: False)

    def copy_mixin(self, other: CollectionState) -> CollectionState:
        other.x2wotc_power_cache = self.x2wotc_power_cache.copy()
        other.x2wotc_power_valid = self.x2wotc_power_valid.copy()
        return other


class RuleManager:
    def __init__(self, world: "X2WOTCWorld"):
        self.item_manager: "ItemManager" = world.item_manager
        self.loc_manager: "LocationManager" = world.loc_manager
        self.options: "X2WOTCOptions" = world.options
        self.multiworld: MultiWorld = world.multiworld
        self.player: int = world.player

        # Precompute per-location required power values
        total_power = self.item_manager.get_total_power()
        self.req_power_lookup: dict[str, float] = {
            loc_name: self.loc_manager.get_location_difficulty(loc_name) * total_power / 100.0
            for loc_name in self.loc_manager.location_table.keys()
        }

        # Compile promotion items for human soldier classes
        self.human_rank_items: set[str] = {
            item_name
            for item_name, item_data in self.item_manager.item_table.items()
            if item_data.type == "Promotion" and "spark" not in item_data.tags
        }

    #==================================================================================================================#
    #                                               GENERAL HELPERS                                                    #
    #------------------------------------------------------------------------------------------------------------------#

    def get_item_count(self, state: CollectionState, item: str) -> int:
        return state.count(self.item_manager.item_table[item].display_name, self.player)

    def has_item_or_impossible(self, state: CollectionState, item: str, count: int = 1) -> bool:
        return (self.get_item_count(state, item) >= count
                or self.item_manager.real_count[item] < count)

    def get_item_count_rule(self, item: str, count: int = 1) -> Callable[[CollectionState], bool]:
        return lambda state: self.has_item_or_impossible(state, item, count)

    def can_reach_or_disabled(self, state: CollectionState, loc_name: str) -> bool:
        if not self.loc_manager.enabled[loc_name]:
            return True

        loc_display_name = self.loc_manager.location_table[loc_name].display_name
        return state.can_reach_location(loc_display_name, self.player)

    def get_reachability_rule(self, loc_names: list[str]) -> Callable[[CollectionState], bool]:
        return lambda state: all(self.can_reach_or_disabled(state, loc_name) for loc_name in loc_names)

    #==================================================================================================================#
    #                                             POWER RULE HELPERS                                                   #
    #------------------------------------------------------------------------------------------------------------------#

    def get_current_power(self, state: CollectionState) -> float:
        if not state.x2wotc_power_valid[self.player]:
            state.x2wotc_power_cache[self.player] = sum([
                self.item_manager.get_item_power(self.item_manager.item_display_name_to_key[display_name], count)
                for display_name, count in state.prog_items[self.player].items()
            ])
            state.x2wotc_power_valid[self.player] = True
        return state.x2wotc_power_cache[self.player]

    def can_reasonably_reach(self, state: CollectionState, location: str) -> bool:
        req_power = self.req_power_lookup[location]
        return self.get_current_power(state) >= req_power

    def get_power_rule(self, location: str) -> Callable[[CollectionState], bool]:
        return lambda state: self.can_reasonably_reach(state, location)

    #==================================================================================================================#
    #                                             RANKSANITY HELPERS                                                   #
    #------------------------------------------------------------------------------------------------------------------#

    def has_human_soldier_rank(self, state: CollectionState, rank: int) -> bool:
        if not self.options.rank_sanity.all_humans_included():
            return True

        for human_rank_item in self.human_rank_items:
            if self.get_item_count(state, human_rank_item) >= rank - 1:
                return True

        return False

    #==================================================================================================================#
    #                                             STORY RULE HELPERS                                                   #
    #------------------------------------------------------------------------------------------------------------------#

    # Contact
    def can_make_contact(self, state: CollectionState) -> bool:
        return self.has_item_or_impossible(state, "ResistanceCommunicationsCompleted")

    def has_radio_relays(self, state: CollectionState) -> bool:
        return self.has_item_or_impossible(state, "ResistanceRadioCompleted")

    def can_make_more_contact(self, state: CollectionState) -> bool:
        return (self.can_make_contact(state)
                and self.has_radio_relays(state))

    # Facility Assault
    def can_do_facility_mission(self, state: CollectionState) -> bool:
        return self.can_make_more_contact(state)

    # Chosen Hunt
    def has_resistance_ring(self, state: CollectionState) -> bool:
        return True

    def can_meet_first_chosen(self, state: CollectionState) -> bool:
        return True

    def can_meet_all_chosen(self, state: CollectionState) -> bool:
        return self.can_make_more_contact(state)

    def can_hunt_all_chosen(self, state: CollectionState) -> bool:
        return (self.can_meet_all_chosen(state)
                and self.has_resistance_ring(state))

    def can_defeat_assassin(self, state: CollectionState) -> bool:
        return (self.options.chosen_hunt_sanity
                and self.has_item_or_impossible(state, "AssassinStronghold")
                and self.can_meet_all_chosen(state)
                or (not self.options.chosen_hunt_sanity
                    and self.can_hunt_all_chosen(state)))

    def can_defeat_hunter(self, state: CollectionState) -> bool:
        return (self.options.chosen_hunt_sanity
                and self.has_item_or_impossible(state, "HunterStronghold")
                and self.can_meet_all_chosen(state)
                or (not self.options.chosen_hunt_sanity
                    and self.can_hunt_all_chosen(state)))

    def can_defeat_warlock(self, state: CollectionState) -> bool:
        return (self.options.chosen_hunt_sanity
                and self.has_item_or_impossible(state, "WarlockStronghold")
                and self.can_meet_all_chosen(state)
                or (not self.options.chosen_hunt_sanity
                    and self.can_hunt_all_chosen(state)))

    def can_defeat_one_chosen(self, state: CollectionState) -> bool:
        return (self.can_defeat_assassin(state)
                or self.can_defeat_hunter(state)
                or self.can_defeat_warlock(state))

    def can_defeat_two_chosen(self, state: CollectionState) -> bool:
        return ((self.can_defeat_assassin(state) and self.can_defeat_hunter(state))
                or (self.can_defeat_assassin(state) and self.can_defeat_warlock(state))
                or (self.can_defeat_hunter(state) and self.can_defeat_warlock(state)))

    def can_defeat_all_chosen(self, state: CollectionState) -> bool:
        return (self.can_defeat_assassin(state)
                and self.can_defeat_hunter(state)
                and self.can_defeat_warlock(state))

    def can_kill_assassin(self, state: CollectionState) -> bool:
        return (self.can_meet_all_chosen(state)
                or self.can_defeat_assassin(state))

    def can_kill_hunter(self, state: CollectionState) -> bool:
        return (self.can_meet_all_chosen(state)
                or self.can_defeat_hunter(state))

    def can_kill_warlock(self, state: CollectionState) -> bool:
        return (self.can_meet_all_chosen(state)
                or self.can_defeat_warlock(state))

    # Shadow Chamber
    def has_shadow_chamber(self, state: CollectionState) -> bool:
        return self.has_item_or_impossible(state, "AlienEncryptionCompleted")

    # Blacksite -> Blacksite Data -> Forge -> Forge Stasis Suit
    def can_do_blacksite_mission(self, state: CollectionState) -> bool:
        return self.can_make_contact(state)

    def has_blacksite_data_objective(self, state: CollectionState) -> bool:
        return (self.can_do_blacksite_mission(state)
                and self.has_shadow_chamber(state))

    def can_do_forge_mission(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "BlacksiteDataCompleted")
                and self.has_blacksite_data_objective(state)
                and self.can_make_more_contact(state))

    def has_forge_stasis_suit_objective(self, state: CollectionState) -> bool:
        return self.can_do_forge_mission(state)

    def finished_forge_stasis_suit_objective(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "ForgeStasisSuitCompleted")
                and self.has_forge_stasis_suit_objective(state))

    # Skulljack
    def has_proving_ground(self, state: CollectionState) -> bool:
        return self.has_item_or_impossible(state, "AutopsyAdventOfficerCompleted")

    def has_skulljack(self, state: CollectionState) -> bool:
        return self.has_proving_ground(state)

    # Skulljack Officer -> Codex Brain -> Psi Gate
    def has_autopsy_officer_objective(self, state: CollectionState) -> bool:
        return True  # Immediately active as of mod version 0.10.3

    def has_skulljack_officer_objective(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "AutopsyAdventOfficerCompleted")
                and self.has_autopsy_officer_objective(state))

    def can_skulljack_officer(self, state: CollectionState) -> bool:
        return (self.has_skulljack_officer_objective(state)
                and self.has_skulljack(state))

    def has_codex_brain_pt1_objective(self, state: CollectionState) -> bool:
        return (self.can_skulljack_officer(state)
                and self.has_shadow_chamber(state))

    def can_do_psi_gate_mission(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "CodexBrainPt1Completed")
                and self.has_codex_brain_pt1_objective(state)
                and self.can_make_more_contact(state))

    def has_psi_gate_objective(self, state: CollectionState) -> bool:
        return self.can_do_psi_gate_mission(state)

    def finished_psi_gate_objective(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "PsiGateCompleted")
                and self.has_psi_gate_objective(state))

    # Skulljack Codex -> Avatar Corpse
    def has_codex_brain_pt2_objective(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "CodexBrainPt1Completed")
                and self.has_codex_brain_pt1_objective(state))

    def has_skulljack_codex_objective(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "CodexBrainPt2Completed")
                and self.has_codex_brain_pt2_objective(state))

    def can_skulljack_codex(self, state: CollectionState) -> bool:
        return (self.has_skulljack_codex_objective(state)
                and self.has_skulljack(state))

    # Final Mission
    def has_autopsy_avatar_objective(self, state: CollectionState) -> bool:
        return (self.finished_forge_stasis_suit_objective(state)
                or self.finished_psi_gate_objective(state)
                or self.can_skulljack_codex(state))

    def can_finish_autopsy_avatar_objective(self, state: CollectionState) -> bool:
        req_psi_gate_obj = "PsiGateObjective" in self.options.campaign_completion_requirements
        req_stasis_suit_obj = "StasisSuitObjective" in self.options.campaign_completion_requirements
        req_avatar_corpse_obj = "AvatarCorpseObjective" in self.options.campaign_completion_requirements

        psi_gate_condition = self.finished_psi_gate_objective(state) or not req_psi_gate_obj
        stasis_suit_condition = self.finished_forge_stasis_suit_objective(state) or not req_stasis_suit_obj
        avatar_corpse_condition = self.can_skulljack_codex(state) or not req_avatar_corpse_obj

        return (psi_gate_condition and stasis_suit_condition and avatar_corpse_condition)

    def can_do_truth_mission(self, state: CollectionState) -> bool:
        return (self.has_item_or_impossible(state, "AutopsyAdventPsiWitchCompleted")
                and self.has_autopsy_avatar_objective(state)
                and self.can_finish_autopsy_avatar_objective(state)
                and self.has_shadow_chamber(state))

    def can_do_final_mission(self, state: CollectionState) -> bool:
        return self.can_do_truth_mission(state)

    # Victory
    def has_won(self, state: CollectionState) -> bool:
        return self.has_item_or_impossible(state, self.options.goal.as_event())

    #==================================================================================================================#
    #                                                 SET RULES                                                        #
    #------------------------------------------------------------------------------------------------------------------#

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: self.has_won(state)

        for loc_name, loc_data in self.loc_manager.location_table.items():
            if not self.loc_manager.enabled[loc_name]:
                continue

            location = self.multiworld.get_location(loc_data.display_name, self.player)

            #---------------------------------------- Power rules -----------------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            power_rule = self.get_power_rule(loc_name)
            set_rule(location, power_rule)

            #---------------------------------------- Story rules -----------------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            if loc_name == "AlienEncryption":
                add_rule(location, lambda state: (self.can_do_blacksite_mission(state)
                                                  or self.can_skulljack_officer(state)))

            # CodexBrainPt1 and CodexBrainPt2 are handled by tags

            if loc_name == "BlacksiteData":
                add_rule(location, lambda state: self.can_do_blacksite_mission(state))

            if loc_name == "ForgeStasisSuit":
                add_rule(location, lambda state: self.can_do_forge_mission(state))

            if loc_name == "PsiGate":
                add_rule(location, lambda state: self.can_do_psi_gate_mission(state))

            # AutopsyAdventPsiWitch is handled by tags

            if loc_name == "Broadcast":
                add_rule(location, lambda state: self.can_do_truth_mission(state))

            if loc_name == "Victory":
                add_rule(location, lambda state: self.can_do_final_mission(state))

            #-------------------------------------- Alien Ruler rules -------------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            if "kill_ruler" in loc_data.tags:
                add_rule(location, lambda state: self.can_do_facility_mission(state))

            #----------------------------------------- Chosen rules ---------------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            if "meet_first_chosen" in loc_data.tags:
                add_rule(location, lambda state: self.can_meet_first_chosen(state))
            if "meet_all_chosen" in loc_data.tags:
                add_rule(location, lambda state: self.can_meet_all_chosen(state))

            if "kill_assassin" in loc_data.tags:
                add_rule(location, lambda state: self.can_kill_assassin(state))
            if "kill_hunter" in loc_data.tags:
                add_rule(location, lambda state: self.can_kill_hunter(state))
            if "kill_warlock" in loc_data.tags:
                add_rule(location, lambda state: self.can_kill_warlock(state))

            if "defeat_assassin" in loc_data.tags:
                add_rule(location, lambda state: self.can_defeat_assassin(state))
            if "defeat_hunter" in loc_data.tags:
                add_rule(location, lambda state: self.can_defeat_hunter(state))
            if "defeat_warlock" in loc_data.tags:
                add_rule(location, lambda state: self.can_defeat_warlock(state))

            if loc_name == "Stronghold1":
                add_rule(location, lambda state: self.can_defeat_one_chosen(state))

            if loc_name == "Stronghold2":
                add_rule(location, lambda state: self.can_defeat_two_chosen(state))

            if loc_name == "Stronghold3":
                add_rule(location, lambda state: self.can_defeat_all_chosen(state))

            #---------------------------------------- Skulljack rules -------------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            if "skulljack_officer" in loc_data.tags:
                add_rule(location, lambda state: self.can_skulljack_officer(state))

            if "skulljack_codex" in loc_data.tags:
                add_rule(location, lambda state: self.can_skulljack_codex(state))

            #------------------------------------ Item requirement rules ----------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            if "proving_ground" in loc_data.tags:
                add_rule(location, lambda state: self.has_proving_ground(state))

            for tag in loc_data.tags:
                if tag.startswith("item:"):
                    data = tag[5:].split(":") + [1]
                    requirement_rule = self.get_item_count_rule(data[0], int(data[1]))
                    add_rule(location, requirement_rule)

            #--------------------------------------- Ranksanity rules -------------------------------------------------#
            #----------------------------------------------------------------------------------------------------------#
            if loc_name.startswith("ChosenHuntPt1"):
                add_rule(location, lambda state: self.has_human_soldier_rank(state, 3))

            if loc_name.startswith("ChosenHuntPt2"):
                add_rule(location, lambda state: self.has_human_soldier_rank(state, 4))

            if loc_name.startswith("ChosenHuntPt3"):
                add_rule(location, lambda state: self.has_human_soldier_rank(state, 6))

            #----------------------------------------------------------------------------------------------------------#
            #------------------------- See ./Regions.py for entrance access rules -------------------------------------#
