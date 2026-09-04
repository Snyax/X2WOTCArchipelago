from logging import warning
from textwrap import dedent
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld

from .Items import items, lwotc_pcs_items, lwotc_weapon_mod_items
from .Locations import locations, fl_to_diff, fl_to_diff_autopsy, fl_to_diff_pg, PG_GRENADE, PG_GRENADE_M2
from .Rules import set_rules


name = "Long War of the Chosen"
location_map = {
    "GaussWeapons": "_GaussWeapons_LW",
    "SkirmisherRank2": "_Skirmisher_LWRank2",
    "SkirmisherRank3": "_Skirmisher_LWRank3",
    "SkirmisherRank4": "_Skirmisher_LWRank4",
    "SkirmisherRank5": "_Skirmisher_LWRank5",
    "SkirmisherRank6": "_Skirmisher_LWRank6",
    "SkirmisherRank7": "_Skirmisher_LWRank7",
    "SkirmisherRank8": "_Skirmisher_LWRank8",
    "ReaperRank2": "_Reaper_LWRank2",
    "ReaperRank3": "_Reaper_LWRank3",
    "ReaperRank4": "_Reaper_LWRank4",
    "ReaperRank5": "_Reaper_LWRank5",
    "ReaperRank6": "_Reaper_LWRank6",
    "ReaperRank7": "_Reaper_LWRank7",
    "ReaperRank8": "_Reaper_LWRank8",
    "TemplarRank2": "_Templar_LWRank2",
    "TemplarRank3": "_Templar_LWRank3",
    "TemplarRank4": "_Templar_LWRank4",
    "TemplarRank5": "_Templar_LWRank5",
    "TemplarRank6": "_Templar_LWRank6",
    "TemplarRank7": "_Templar_LWRank7",
    "TemplarRank8": "_Templar_LWRank8",
    "SparkRank2": "_Spark_LWRank2",
    "SparkRank3": "_Spark_LWRank3",
    "SparkRank4": "_Spark_LWRank4",
    "SparkRank5": "_Spark_LWRank5",
    "SparkRank6": "_Spark_LWRank6",
    "SparkRank7": "_Spark_LWRank7",
    "SparkRank8": "_Spark_LWRank8",
}
item_map = {
    "_GaussWeaponsCompleted_LW": "GaussWeaponsCompleted",
    "_AimUpgrade_Sup_LW:1": "AimUpgrade_Sup:1",
    "_CritUpgrade_Sup_LW:1": "CritUpgrade_Sup:1",
    "_ReloadUpgrade_Sup_LW:1": "ReloadUpgrade_Sup:1",
    "_MissDamageUpgrade_Sup_LW:1": "MissDamageUpgrade_Sup:1",
    "_FreeFireUpgrade_Sup_LW:1": "FreeFireUpgrade_Sup:1",
    "_ClipSizeUpgrade_Sup_LW:1": "ClipSizeUpgrade_Sup:1",
    "_FreeKillUpgrade_Bsc_LW:1": "FreeKillUpgrade_Bsc:1",
    "_FreeKillUpgrade_Adv_LW:1": "FreeKillUpgrade_Adv:1",
    "_FreeKillUpgrade_Sup_LW:1": "FreeKillUpgrade_Sup:1",
    "_Skirmisher_LWRank": "SkirmisherRank",
    "_Reaper_LWRank": "ReaperRank",
    "_Templar_LWRank": "TemplarRank",
    "_Spark_LWRank": "SparkRank",
}

# For defining the order rules are applied in (in case of set_rule)
# The order is lowest to highest priority
rule_priority = 0.0

# Handle mod options here
def generate_early(world: "X2WOTCWorld"):

    # Mission skips not supported
    if world.options.skip_mission_types:
        world.options.skip_mission_types.value = set()
        warning(f"X2WOTC: Ignoring mission skips for player {world.player_name} because the mod 'Long War of the Chosen' is enabled")

    # Enemy rando not supported
    for loc_name, loc_data in world.loc_manager.location_table.items():
        world.loc_manager.replace(loc_name, tags={tag for tag in loc_data.tags if not tag.startswith("diff:")})
    if world.options.enemy_rando:
        world.options.enemy_rando.value = False
        world.enemy_rando_manager.enemy_shuffle.sort()
        warning(f"X2WOTC: Ignoring enemy rando for player {world.player_name} because the mod 'Long War of the Chosen' is enabled")

    # Weapons have 5 tiers
    if "GunTech+" in world.options.progressive_items:
        world.item_manager.disable_progressive_item("ProgressiveRifleShotgunTechCompleted+")
        world.item_manager.disable_progressive_item("ProgressiveCannonSniperTechCompleted")
        world.item_manager.enable_progressive_item("ProgressiveRifleTechLwotcCompleted+")
        world.item_manager.enable_progressive_item("ProgressiveAdvancedWeaponTechLwotcCompleted", random=world.random)
    elif "GunTech" in world.options.progressive_items:
        world.item_manager.disable_progressive_item("ProgressiveRifleShotgunTechCompleted")
        world.item_manager.disable_progressive_item("ProgressiveCannonSniperTechCompleted")
        world.item_manager.enable_progressive_item("ProgressiveRifleTechLwotcCompleted")
        world.item_manager.enable_progressive_item("ProgressiveAdvancedWeaponTechLwotcCompleted", random=world.random)

    # GREMLINs are upgraded from ADVENT Robotics
    if "GREMLINTech" in world.options.progressive_items:
        world.item_manager.disable_progressive_item("ProgressiveGREMLINTechCompleted")
        world.item_manager.enable_progressive_item("ProgressiveGREMLINTechLwotcCompleted")

    # Light and Heavy Armor are researches, not PG projects
    if "ArmorTech" in world.options.progressive_items:
        world.item_manager.enable_progressive_item("ProgressiveLightArmorTechLwotcCompleted")
        world.item_manager.enable_progressive_item("ProgressiveHeavyArmorTechLwotcCompleted")

    # Handle option to force early proving ground
    if world.options.early_proving_ground:
        del world.multiworld.early_items[world.player][
            world.item_manager.item_table["AutopsyAdventOfficerCompleted"].display_name
        ]
        world.multiworld.early_items[world.player][
            world.item_manager.item_table["AutopsyAdventTrooperCompleted"].display_name
        ] = 1

    # Gauss Weapons is called Advanced Magnetic Weapons
    world.loc_manager.disable_location("GaussWeapons")
    world.item_manager.disable_item("GaussWeaponsCompleted")

    # Repeaters are called Suppressors, Superior attachments are called Elite
    world.item_manager.weapon_mod_items.difference_update([
        "AimUpgrade_Sup:1",
        "CritUpgrade_Sup:1",
        "ReloadUpgrade_Sup:1",
        "MissDamageUpgrade_Sup:1",
        "FreeFireUpgrade_Sup:1",
        "ClipSizeUpgrade_Sup:1",
        "FreeKillUpgrade_Bsc:1",
        "FreeKillUpgrade_Adv:1",
        "FreeKillUpgrade_Sup:1",
    ])
    world.item_manager.weapon_mod_items.update(set(lwotc_weapon_mod_items.keys()))

    # Rocket Launcher is a squaddie Technical skill
    world.loc_manager.disable_location("UseRocketLauncher")

    # Lost corpses are unobtainable
    world.loc_manager.disable_location("AutopsyTheLost")
    world.item_manager.disable_item("AutopsyTheLostCompleted")
    world.loc_manager.disable_location("UseUltrasonicLure")

    # Ammo, heavy weapons and grenades are deterministic
    world.loc_manager.disable_location("UseExperimentalAmmo")
    world.loc_manager.disable_location("UseExperimentalGrenade")
    world.loc_manager.disable_location("UseExperimentalGrenadeMk2")
    world.loc_manager.disable_location("UseExperimentalHeavyWeapon")
    world.loc_manager.disable_location("UseExperimentalPoweredWeapon")

    # Base game classes are disabled
    for soldier_class in [
        "Ranger",
        "Grenadier",
        "Specialist",
        "Sharpshooter",
        "Reaper",
        "Skirmisher",
        "Templar",
        "SPARK",
    ]:
        for rank in range(2, 8):
            world.loc_manager.disable_location(f"{soldier_class.title()}Rank{rank}")
            world.item_manager.remove_item(f"{soldier_class.title()}Rank")

    # Force Level increases by off-world reinforcements which requires special handling
    world.item_manager.trap_items.discard("ForceLevel:1")

    # Patch LWOTC PCSes into item pool
    world.item_manager.pcs_items.update(set(lwotc_pcs_items.keys()))

    for item, cat in [
        ("ModularWeaponsCompleted", IC.progression | IC.useful),
        ("HybridMaterialsCompleted", IC.progression | IC.useful),
    ]:
        world.item_manager.replace(item, classification=cat)

    for loc, tag in [
        ("MagnetizedWeapons", {"tree:HybridMaterials", "tree:AutopsyAdventOfficer"}),
        ("PlasmaRifle", {"tree:AdvancedLasers", "tree:AdvancedCoilguns"}),
        ("PlasmaSniper", {"tree:PlasmaRifle"}),
        ("HeavyPlasma", {"tree:PlasmaRifle"}),
        ("AlloyCannon", {"tree:PlasmaRifle"}),
        ("PlatedArmor", {"tree:HybridMaterials"}),
        ("PoweredArmor", {"tree:PlatedArmor", "tree:Tech_Elerium"}),
        ("AutopsyAdventTrooper", {"autopsy", "tree:AlienBiotech", "goldenpath"}),  # Somewhat guaranteed
        ("AutopsyAdventOfficer", {"autopsy", "tree:AutopsyAdventTrooper", "goldenpath"}),  # Somewhat guaranteed
        ("AutopsyAdventStunLancer", {"autopsy", "tree:AutopsyAdventTrooper"}),
        ("AutopsyAdventShieldbearer", {"autopsy", "tree:AutopsyAdventTrooper"}),
        ("AutopsyAdventMEC", {"autopsy", "tree:AutopsyDrone"}),
        ("AutopsyAdventTurret", {"autopsy", "tree:AutopsyDrone"}),
        ("AutopsySectopod", {"autopsy", "tree:AutopsyDrone"}),
        ("AutopsyBerserker", {"autopsy", "tree:AutopsyMuton"}),
        ("AutopsyGatekeeper", {"autopsy", "tree:Psionics"}),
        ("AutopsyViperKing", {"autopsy", "kill_ruler", "tree:AutopsyViper"}),
        ("AutopsyBerserkerQueen", {"autopsy", "kill_ruler", "tree:AutopsyBerserker"}),
        ("AutopsyArchonKing", {"autopsy", "kill_ruler", "tree:AutopsyArchon"}),
        ("Tech_Elerium", {"tree:HybridMaterials", "tree:_GaussWeapons_LW", "tree:PlatedArmor"}),
        ("UseBattleScanner", {"utility", "proving_ground", "item:HybridMaterialsCompleted"}),
        ("UseAlienGrenade", PG_GRENADE | {"item:AutopsyMutonCompleted"}),
        ("UseEMPGrenade", PG_GRENADE | {"item:AutopsyAdventMECCompleted"}),
        ("UseEMPGrenadeMk2", {"item:AutopsyAdventMECCompleted"} | PG_GRENADE_M2),
        ("UseSmokeGrenadeMk2", PG_GRENADE_M2),
        ("UseProximityMine", {"item:AutopsySectopodCompleted"} | PG_GRENADE_M2),
        ("UseMimicBeacon", {"utility", "item:PsiGateCompleted",} | PG_GRENADE_M2 - {"grenade"}),
        ("ChosenHuntPt1:1", {"chosen_hunt", "meet_first_chosen", "influence:0"}),
        ("ChosenHuntPt1:2", {"chosen_hunt", "meet_first_chosen", "influence:0"}),
        ("ChosenHuntPt1:3", {"chosen_hunt", "meet_first_chosen", "influence:0"}),
        ("ChosenHuntPt2:1", {"chosen_hunt", "meet_first_chosen", "influence:1"}),
        ("ChosenHuntPt2:2", {"chosen_hunt", "meet_first_chosen", "influence:3"}),
        ("ChosenHuntPt2:3", {"chosen_hunt", "meet_first_chosen", "influence:5"}),
        ("ChosenHuntPt3:1", {"chosen_hunt", "meet_first_chosen", "influence:2"}),
        ("ChosenHuntPt3:2", {"chosen_hunt", "meet_first_chosen", "influence:4"}),
        ("ChosenHuntPt3:3", {"chosen_hunt", "meet_first_chosen", "influence:6"}),
    ]:
        world.loc_manager.replace(loc, tags=tag)

    for loc, diff in [
        ("Psionics", fl_to_diff(4)),
        ("MagnetizedWeapons", fl_to_diff(7)),
        ("PlatedArmor", fl_to_diff(9)),
        ("Tech_Elerium", fl_to_diff(11)),
        ("PlasmaRifle", fl_to_diff(17)),
        ("PoweredArmor", fl_to_diff(17)),
        ("PlasmaSniper", fl_to_diff(19)),
        ("HeavyPlasma", fl_to_diff(19)),
        ("AlloyCannon", fl_to_diff(19)),
        ("AutopsyAdventTrooper", fl_to_diff(1)),  # Somewhat guaranteed
        ("AutopsyAdventOfficer", fl_to_diff(2)),  # Somewhat guaranteed
        ("AutopsyAdventStunLancer", fl_to_diff_autopsy(3)),
        ("AutopsyAdventPriest", fl_to_diff_autopsy(3)),
        ("AutopsyAdventPurifier", fl_to_diff_autopsy(4)),
        ("AutopsyAdventShieldbearer", fl_to_diff_autopsy(7)),
        ("AutopsyAdventTurret", fl_to_diff_autopsy(2)),
        ("AutopsyAdventMEC", fl_to_diff_autopsy(4)),
        ("AutopsySectopod", fl_to_diff_autopsy(16)),
        ("AutopsySectoid", fl_to_diff(1)),
        ("AutopsyViper", fl_to_diff_autopsy(3)),
        ("AutopsyFaceless", fl_to_diff_autopsy(3)),
        ("AutopsyMuton", fl_to_diff_autopsy(5)),
        ("AutopsyBerserker", fl_to_diff_autopsy(8)),
        ("AutopsySpectre", fl_to_diff_autopsy(8)),
        ("AutopsyChryssalid", fl_to_diff_autopsy(9)),
        ("AutopsyArchon", fl_to_diff_autopsy(11)),
        ("AutopsyAndromedon", fl_to_diff_autopsy(14)),
        ("AutopsyGatekeeper", fl_to_diff_autopsy(18)),
        ("AutopsyViperKing", 90.0),
        ("AutopsyBerserkerQueen", 90.0),
        ("AutopsyArchonKing", 90.0),
        ("AlienEncryption", fl_to_diff(15)),
        ("CodexBrainPt1", fl_to_diff(12)),
        ("KillCyberus", fl_to_diff(12)),
        ("CodexBrainPt2", fl_to_diff(16)),
        ("KillAdventPsiWitch", fl_to_diff(16)),
        ("BlacksiteData", fl_to_diff(15)),
        ("ForgeStasisSuit", fl_to_diff(17)),
        ("PsiGate", fl_to_diff(18)),
        ("AutopsyAdventPsiWitch", fl_to_diff(19)),
        ("ChosenHuntPt1:1", fl_to_diff(5)),
        ("ChosenHuntPt1:2", fl_to_diff(6)),
        ("ChosenHuntPt1:3", fl_to_diff(7)),
        ("ChosenHuntPt2:1", fl_to_diff(10)),
        ("ChosenHuntPt2:2", fl_to_diff(11)),
        ("ChosenHuntPt2:3", fl_to_diff(12)),
        ("ChosenHuntPt3:1", fl_to_diff(15)),
        ("ChosenHuntPt3:2", fl_to_diff(16)),
        ("ChosenHuntPt3:3", fl_to_diff(17)),
        ("ChosenAssassinWeapons", fl_to_diff(17)),
        ("ChosenHunterWeapons", fl_to_diff(17)),
        ("ChosenWarlockWeapons", fl_to_diff(17)),
        # ("KillAdventTrooper", fl_to_diff(0)),
        # ("KillAdventCaptain", fl_to_diff(0)),
        ("KillAdventStunLancer", fl_to_diff(3)),
        ("KillAdventPriest", fl_to_diff(3)),
        ("KillAdventPurifier", fl_to_diff(4)),
        ("KillAdventShieldBearer", fl_to_diff(7)),
        ("KillAdventTurret", fl_to_diff(2)),
        ("KillAdventMEC", fl_to_diff(4)),
        ("KillSectopod", fl_to_diff(16)),
        ("KillSectoid", fl_to_diff(0)),
        ("KillViper", fl_to_diff(3)),
        ("KillFaceless", fl_to_diff(3)),
        ("KillMuton", fl_to_diff(5)),
        ("KillBerserker", fl_to_diff(8)),
        ("KillSpectre", fl_to_diff(8)),
        ("KillChryssalid", fl_to_diff(9)),
        ("KillArchon", fl_to_diff(11)),
        ("KillAndromedon", fl_to_diff(14)),
        ("KillAndromedonRobot", fl_to_diff(14)),
        ("KillGatekeeper", fl_to_diff(18)),
        ("KillViperKing", 90.0),
        ("KillBerserkerQueen", 90.0),
        ("KillArchonKing", 90.0),
        ("KillTheLost", fl_to_diff(10)),
        ("UseBattleScanner", fl_to_diff_pg(1)),
        ("UseNanoMedikit", fl_to_diff_pg(3)),
        ("UseEMPGrenade", fl_to_diff_pg(4)),
        ("UseEMPGrenadeMk2", fl_to_diff_pg(4)),
        ("UseSmokeGrenadeMk2", fl_to_diff_pg(4)),
        ("UseAlienGrenade", fl_to_diff_pg(5)),
        ("UseBluescreenRounds", fl_to_diff_autopsy(8)),
        ("UseRefractionField", fl_to_diff_autopsy(8)),
        ("UseCombatStims", fl_to_diff_autopsy(8)),
        ("UseSKULLJACK", fl_to_diff_pg(12)),
        ("UseProximityMine", fl_to_diff_pg(16)),
        ("UseMimicBeacon", fl_to_diff_pg(18)),
        ("Stronghold1", fl_to_diff(16)),
        ("Stronghold2", fl_to_diff(17)),
        ("Stronghold3", fl_to_diff(18)),
        ("Broadcast", fl_to_diff(19)),
        ("Victory", fl_to_diff(20)),
    ]:
        world.loc_manager.replace(loc, difficulty=diff)

    for item, power in [
        ("PlasmaRifleCompleted", 200.0),
        ("HeavyPlasmaCompleted", 200.0),
        ("PlasmaSniperCompleted", 200.0),
        ("AlloyCannonCompleted", 200.0),
        ("AutopsyAdventTrooperCompleted", 80.0),
        ("AutopsyAdventOfficerCompleted", 40.0),
        ("AutopsyFacelessCompleted", 10.0),
        ("AutopsyChryssalidCompleted", 30.0),
        ("AutopsyAdventTurretCompleted", 30.0),
        ("ExperimentalWeaponsCompleted", 15.0),
    ]:
        world.item_manager.replace(item, power=power)

config: dict[str, str] = {
    "X2Item_ResearchCompleted": dedent(
        r"""
        +CheckCompleteTechs=(TechName=AutopsyDrone)
        +CheckCompleteTechs=(TechName=AutopsyMutonElite)
        +CheckCompleteTechs=(TechName=LaserWeapons)
        +CheckCompleteTechs=(TechName=AdvancedLasers)
        +CheckCompleteTechs=(TechName=Coilguns)
        +CheckCompleteTechs=(TechName=AdvancedCoilguns)
        +CheckCompleteTechs=(TechName=EXOSuit)
        +CheckCompleteTechs=(TechName=WARSuit)
        +CheckCompleteTechs=(TechName=SpiderSuit)
        +CheckCompleteTechs=(TechName=WraithSuit)
        """
    ),
    "X2EventListener_WOTCArchipelago": dedent(
        r"""
        +CheckKillCustomCharacterGroups=(GroupName=AdvEngineer, \\
            Members[0]=AdvGrenadierM1, \\
            Members[1]=AdvHeavyEngineer \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvGunner, \\
            Members[0]=AdvGunnerM1, \\
            Members[1]=AdvGunnerM2, \\
            Members[2]=AdvGunnerM3 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvSentry, \\
            Members[0]=AdvSentryM1, \\
            Members[1]=AdvSentryM2, \\
            Members[2]=AdvSentryM3 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvRocketeer, \\
            Members[0]=AdvRocketeerM1, \\
            Members[1]=AdvRocketeerM2, \\
            Members[2]=AdvRocketeerM3 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvScout, \\
            Members[0]=AdvScout, \\
            Members[1]=AdvCommando \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvSergeant, \\
            Members[0]=AdvSergeantM1, \\
            Members[1]=AdvSergeantM2 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvGrenadier, \\
            Members[0]=AdvGrenadierM2, \\
            Members[1]=AdvGrenadierM3 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvGeneral_LW, \\
            Members[0]=AdvGeneralM1_LW, \\
            Members[1]=AdvGeneralM2_LW \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvShockTroop, Members[0]=AdvShockTroop)
        +CheckKillCustomCharacterGroups=(GroupName=AdvVanguard, Members[0]=AdvVanguard)

        +CheckKillCustomCharacterGroups=(GroupName=LWDrone, \\
            Members[0]=LWDroneM1, \\
            Members[1]=LWDroneM2 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=AdvMECArcher, \\
            Members[0]=AdvMECArcherM1, \\
            Members[1]=AdvMECArcherM2 \\
        )

        +CheckKillCustomCharacterGroups=(GroupName=Sidewinder, \\
            Members[0]=SidewinderM1, \\
            Members[1]=SidewinderM2, \\
            Members[2]=SidewinderM3 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=Naja, \\
            Members[0]=NajaM1, \\
            Members[1]=NajaM2, \\
            Members[2]=NajaM3 \\
        )
        +CheckKillCustomCharacterGroups=(GroupName=Muton, Members[0]=Muton)
        +CheckKillCustomCharacterGroups=(GroupName=MutonM2_LW, Members[0]=MutonM2_LW)
        +CheckKillCustomCharacterGroups=(GroupName=MutonM3_LW, Members[0]=MutonM3_LW)
        +CheckKillCustomCharacterGroups=(GroupName=Chryssalid, Members[0]=Chryssalid)
        +CheckKillCustomCharacterGroups=(GroupName=ChryssalidSoldier, Members[0]=ChryssalidSoldier)
        +CheckKillCustomCharacterGroups=(GroupName=HiveQueen, Members[0]=HiveQueen)
        """
    ),
    "X2Effect_ItemUseCheck": dedent(
        r"""
        +CheckUseItems=ShapedCharge
        +CheckUseItemCategories=(CategoryName=GasGrenade, Members[0]=GasGrenadeMk2)
        +CheckUseItemCategories=(CategoryName=Firebomb, Members[0]=FirebombMk2)
        +CheckUseItemCategories=(CategoryName=AcidGrenade, Members[0]=AcidGrenadeMk2)
        +CheckUseItems=GasGrenadeMk2
        +CheckUseItems=FirebombMk2
        +CheckUseItems=AcidGrenadeMk2
        +CheckUseItemCategories=(CategoryName=ShredderGun, Members[0]=ShredstormCannon)
        +CheckUseItemCategories=(CategoryName=PrototypePlasmaBlaster, Members[0]=PlasmaBlaster)
        +CheckUseItems=PrototypePlasmaBlaster
        +CheckUseItems=PlasmaBlaster
        +CheckUseItems=ShredderGun
        +CheckUseItems=ShredstormCannon
        +CheckUseItems=APRounds
        +CheckUseItems=TracerRounds
        +CheckUseItems=TalonRounds
        +CheckUseItems=VenomRounds
        +CheckUseItems=IncendiaryRounds
        +CheckUseItems=StilettoRounds
        +CheckUseItems=FlechetteRounds
        +CheckUseItems=RedscreenRounds
        +CheckUseItems=NeedleRounds
        +CheckUseItems=FalconRounds

        +CheckUseItemExcludeAbilities=Suppression_LW
        +CheckUseItemIncludeAbilities=SuppressionShot_LW
        +CheckUseItemExcludeAbilities=AreaSuppression
        +CheckUseItemIncludeAbilities=AreaSuppressionShot_LW
        +CheckUseItemExcludeAbilities=LeadTheTarget_LW
        +CheckUseItemIncludeAbilities=LeadTheTargetShot_LW
        +CheckUseItemExcludeAbilities=Stock_LW_Bsc_Ability
        +CheckUseItemExcludeAbilities=Stock_LW_Adv_Ability
        +CheckUseItemExcludeAbilities=Stock_LW_Sup_Ability
        +CheckUseItemExcludeAbilities=Gunslinger
        +CheckUseItemIncludeAbilities=GunslingerShot
        """
    ),
    "WOTCArchipelago_Ranksanity": dedent(
        r"""
        +DisabledDataEntries=DefaultRanger
        +DisabledDataEntries=DefaultGrenadier
        +DisabledDataEntries=DefaultSpecialist
        +DisabledDataEntries=DefaultSharpshooter
        +DisabledDataEntries=DefaultSkirmisher
        +DisabledDataEntries=DefaultReaper
        +DisabledDataEntries=DefaultTemplar
        +DisabledDataEntries=DefaultSpark
        +RanksanityData=(ID=LWOTCAssault, SoldierClass=LWS_Assault, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCGrenadier, SoldierClass=LWS_Grenadier, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCGunner, SoldierClass=LWS_Gunner, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCRanger, SoldierClass=LWS_Ranger, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCSharpshooter, SoldierClass=LWS_Sharpshooter, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCShinobi, SoldierClass=LWS_Shinobi, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCSpecialist, SoldierClass=LWS_Specialist, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCTechnical, SoldierClass=LWS_Technical, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCReaper, SoldierClass=Reaper, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCSkirmisher, SoldierClass=Skirmisher, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCTemplar, SoldierClass=Templar, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LWOTCSpark, SoldierClass=Spark, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        """
    ),
}
