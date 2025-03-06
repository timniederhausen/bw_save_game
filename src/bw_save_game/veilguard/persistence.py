import typing

from bw_save_game.persistence import (
    PersistenceKey,
    PersistencePropertyDefinition,
    registered_persistence_key,
)
from bw_save_game.veilguard.types import CharacterArchetype

DIFFICULTY_COMBAT_PRESETS = {
    # UI/SCREENS/Settings/OptionsData/GamePresetOption
    1: "Adventurer",
    2: "Storyteller",
    3: "Keeper",
    4: "Underdog",
    5: "Nightmare",
    6: "Custom",
}
DIFFICULTY_COMBAT_PRESET_VALUES = list(DIFFICULTY_COMBAT_PRESETS.keys())
DIFFICULTY_COMBAT_PRESET_LABELS = list(DIFFICULTY_COMBAT_PRESETS.values())

DIFFICULTY_EXPLORATION_PRESETS = {
    # UI/SCREENS/Settings/OptionsData/ExplorePresetOption
    0: "No Assists",
    1: "Pulse Only",
    2: "Standard",
    3: "Directed",
    4: "Custom",
}
DIFFICULTY_EXPLORATION_PRESET_VALUES = list(DIFFICULTY_EXPLORATION_PRESETS.keys())
DIFFICULTY_EXPLORATION_PRESET_LABELS = list(DIFFICULTY_EXPLORATION_PRESETS.values())

CLASS_KEYBINDINGS = {
    # UI/SCREENS/Settings/OptionsData/ControlsOptions/ClassKeybindingsOption
    0: "Warrior",
    1: "Rogue",
    2: "Mage",
}
CLASS_KEYBINDING_VALUES = list(CLASS_KEYBINDINGS.keys())
CLASS_KEYBINDING_LABELS = list(CLASS_KEYBINDINGS.values())

# CharacterGenerator_RDA_1647819227
CHARACTER_GENERATOR_DEF = registered_persistence_key(1647819227)
CHARACTER_GENERATOR_GENDER = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 894942981, "Int32", 1)
CHARACTER_GENERATOR_VOICE_TONE = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 1419752156, "Int32", 0)
CHARACTER_GENERATOR_LINEAGE = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 1491933783, "Int32", 3)
CHARACTER_GENERATOR_PRONOUNS = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 2061714718, "Int32", 1)
CHARACTER_GENERATOR_IS_TRANS = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 2684529018, "Boolean", False)
CHARACTER_GENERATOR_VOICE = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 3513989292, "Int32", 0)
CHARACTER_GENERATOR_FACTION = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 3942110114, "Int32", 2)

CHARACTER_GENERATOR_LINEAGES = {
    # UI/_Common/DesignerEnums/CharacterCreator/CharGenLineageEnum
    0: "Human",
    1: "Dwarf",
    2: "Elf",
    3: "Qunari",
}
CHARACTER_GENERATOR_LINEAGE_VALUES = list(CHARACTER_GENERATOR_LINEAGES.keys())
CHARACTER_GENERATOR_LINEAGE_LABELS = list(CHARACTER_GENERATOR_LINEAGES.values())

CHARACTER_GENERATOR_FACTIONS = {
    # Globals/RPG/FactionTypes
    0: "Grey Wardens",
    1: "Veil Jumpers",
    2: "Shadow Dragons",
    3: "Lords Of Fortune",
    4: "The Mourn Watch",
    5: "Antivan Crows",
}
CHARACTER_GENERATOR_FACTION_VALUES = list(CHARACTER_GENERATOR_FACTIONS.keys())
CHARACTER_GENERATOR_FACTION_LABELS = list(CHARACTER_GENERATOR_FACTIONS.values())

CHARACTER_GENERATOR_PRONOUN_OPTIONS = {
    # DesignContent/PlotLogic/Global/Rook/Gender/
    0: "He",
    1: "She",
    2: "They",
}
CHARACTER_GENERATOR_PRONOUN_OPTION_VALUES = list(CHARACTER_GENERATOR_PRONOUN_OPTIONS.keys())
CHARACTER_GENERATOR_PRONOUN_OPTION_LABELS = list(CHARACTER_GENERATOR_PRONOUN_OPTIONS.values())

CHARACTER_GENERATOR_VOICES = {
    # manual
    0: "Feminine 2",
    1: "Masculine 2",
    2: "Feminine",
    3: "Masculine",
}
CHARACTER_GENERATOR_VOICE_VALUES = list(CHARACTER_GENERATOR_VOICES.keys())
CHARACTER_GENERATOR_VOICE_LABELS = list(CHARACTER_GENERATOR_VOICES.values())

CHARACTER_GENERATOR_VOICE_TONES = {
    # manual
    0: "medium",
    1: "low",
}
CHARACTER_GENERATOR_VOICE_TONE_VALUES = list(CHARACTER_GENERATOR_VOICE_TONES.keys())
CHARACTER_GENERATOR_VOICE_TONE_LABELS = list(CHARACTER_GENERATOR_VOICE_TONES.values())

# Globals/Persistence/InquisitorGeneratorDataAsset
INQUISITION_CHOICES = registered_persistence_key(1250272560)  # InquisitionChoices_RDA_1250272560
INQUISITION_CHOICES_Inquisitor_Lineage = PersistencePropertyDefinition(INQUISITION_CHOICES, 589036284, "Int32", 1)
# DesignContent/PlotLogic/Global/PastDAChoices/UseReferences/Reference_Past_DA_fc
INQUISITION_CHOICES_LegacyReferences = PersistencePropertyDefinition(INQUISITION_CHOICES, 746726984, "Boolean", False)
INQUISITION_CHOICES_Keep_Inquisition = PersistencePropertyDefinition(INQUISITION_CHOICES, 1504326507, "Int32", 0)
INQUISITION_CHOICES_Inquisitor_Gender = PersistencePropertyDefinition(INQUISITION_CHOICES, 1557862999, "Int32", 1)
INQUISITION_CHOICES_Keep_Romance = PersistencePropertyDefinition(INQUISITION_CHOICES, 2643758781, "Int32", 8)
INQUISITION_CHOICES_Inquisitor_Class = PersistencePropertyDefinition(INQUISITION_CHOICES, 2647290538, "Int32", 2)
INQUISITION_CHOICES_Keep_Trespasser = PersistencePropertyDefinition(INQUISITION_CHOICES, 3170937725, "Int32", 1)
INQUISITION_CHOICES_Keep_WellOfSorrows = PersistencePropertyDefinition(INQUISITION_CHOICES, 3196298401, "Int32", 1)
INQUISITION_CHOICES_Inquisitor_Voice = PersistencePropertyDefinition(INQUISITION_CHOICES, 3572077324, "Int32", 1)

INQUISITION_CHOICES_Inquisitor_Lineage_OPTIONS = {
    # UI/SCREENS/Keep/DesignerEnum/Keep_InquisitorLineage
    0: "Dwarf",
    1: "Elf",
    2: "Human",
    3: "Qunari",
}
INQUISITION_CHOICES_Inquisitor_Lineage_VALUES = list(INQUISITION_CHOICES_Inquisitor_Lineage_OPTIONS.keys())
INQUISITION_CHOICES_Inquisitor_Lineage_LABELS = list(INQUISITION_CHOICES_Inquisitor_Lineage_OPTIONS.values())

INQUISITION_CHOICES_Keep_Inquisition_OPTIONS = {
    # manual
    0: "Disband",
    1: "Part of Chantry",
}
INQUISITION_CHOICES_Keep_Inquisition_VALUES = list(INQUISITION_CHOICES_Keep_Inquisition_OPTIONS.keys())
INQUISITION_CHOICES_Keep_Inquisition_LABELS = list(INQUISITION_CHOICES_Keep_Inquisition_OPTIONS.values())

INQUISITION_CHOICES_Inquisitor_Gender_OPTIONS = {
    # manual
    0: "Male",
    1: "Female",
}
INQUISITION_CHOICES_Inquisitor_Gender_VALUES = list(INQUISITION_CHOICES_Inquisitor_Gender_OPTIONS.keys())
INQUISITION_CHOICES_Inquisitor_Gender_LABELS = list(INQUISITION_CHOICES_Inquisitor_Gender_OPTIONS.values())

INQUISITION_CHOICES_Keep_Romance_OPTIONS = {
    # DesignContent/PlotLogic/Global/PastDAChoices/InquisitorRomance/...
    0: "None",
    1: "Blackwall",
    2: "Cassandra",
    3: "Cullen",
    4: "Dorian",
    5: "IronBull",
    6: "Josephine",
    7: "Sera",
    8: "Solas",
}
INQUISITION_CHOICES_Keep_Romance_VALUES = list(INQUISITION_CHOICES_Keep_Romance_OPTIONS.keys())
INQUISITION_CHOICES_Keep_Romance_LABELS = list(INQUISITION_CHOICES_Keep_Romance_OPTIONS.values())

INQUISITION_CHOICES_Keep_Trespasser_OPTIONS = {
    # manual
    0: "Vowed to save Solas",
    1: "Vowed to stop Solas",
}
INQUISITION_CHOICES_Keep_Trespasser_VALUES = list(INQUISITION_CHOICES_Keep_Trespasser_OPTIONS.keys())
INQUISITION_CHOICES_Keep_Trespasser_LABELS = list(INQUISITION_CHOICES_Keep_Trespasser_OPTIONS.values())

INQUISITION_CHOICES_Inquisitor_Voice_OPTIONS = {
    # manual
    0: "Voice 2",
    1: "Voice 1",
}
INQUISITION_CHOICES_Inquisitor_Voice_VALUES = list(INQUISITION_CHOICES_Inquisitor_Voice_OPTIONS.keys())
INQUISITION_CHOICES_Inquisitor_Voice_LABELS = list(INQUISITION_CHOICES_Inquisitor_Voice_OPTIONS.values())

PROGRESSION = registered_persistence_key(1576630552)  # Progression_RDA_1576630552
PROGRESSION_DEPRECATED_Dagger_CanUseChests = PersistencePropertyDefinition(PROGRESSION, 21147654, "Boolean", False)
PROGRESSION_DEPRECATED_Dagger_CanUseFHAltars = PersistencePropertyDefinition(PROGRESSION, 530863613, "Boolean", False)
PROGRESSION_BackgroundTraitGranted = PersistencePropertyDefinition(PROGRESSION, 589535686, "Boolean", False)
PROGRESSION_Skills_StartedBellara = PersistencePropertyDefinition(PROGRESSION, 643085077, "Boolean", False)
PROGRESSION_PotionLoadCount = PersistencePropertyDefinition(PROGRESSION, 863441793, "Int32", 3)
PROGRESSION_DivinerAcquired = PersistencePropertyDefinition(PROGRESSION, 1222498433, "Boolean", False)
PROGRESSION_InventoryTutorialReached = PersistencePropertyDefinition(PROGRESSION, 1291717646, "Boolean", False)
PROGRESSION_Specialization1 = PersistencePropertyDefinition(PROGRESSION, 1660426999, "Boolean", False)
PROGRESSION_CurrentLevel = PersistencePropertyDefinition(PROGRESSION, 2062776528, "Int32", 1)
PROGRESSION_FollowerLevelUpTutorialReached = PersistencePropertyDefinition(PROGRESSION, 2097167731, "Boolean", False)
PROGRESSION_FadeSmithUnlocked = PersistencePropertyDefinition(PROGRESSION, 2198525296, "Boolean", False)
PROGRESSION_CanCheckEntitlements = PersistencePropertyDefinition(PROGRESSION, 2355626220, "Boolean", False)
PROGRESSION_DEPRECATED_Dagger_CanUseEVAltars = PersistencePropertyDefinition(PROGRESSION, 2751582104, "Boolean", False)
PROGRESSION_DEPRECATED_DaggerRankAvailable = PersistencePropertyDefinition(PROGRESSION, 2829214563, "Int32", 0)
PROGRESSION_Specialization3 = PersistencePropertyDefinition(PROGRESSION, 2916814191, "Boolean", False)
PROGRESSION_HealthUpgradesAcquired = PersistencePropertyDefinition(PROGRESSION, 3176868873, "Int32", 0)
PROGRESSION_Specialization2 = PersistencePropertyDefinition(PROGRESSION, 3225557027, "Boolean", False)
PROGRESSION_UltCanBeUnlocked = PersistencePropertyDefinition(PROGRESSION, 3628985747, "Boolean", False)
PROGRESSION_DaggerState = PersistencePropertyDefinition(PROGRESSION, 3657647123, "Int32", 0)
PROGRESSION_SkillsLevelUpReached = PersistencePropertyDefinition(PROGRESSION, 4033230091, "Boolean", False)
PROGRESSION_DaggerRank = PersistencePropertyDefinition(PROGRESSION, 4125407861, "Int32", 0)
PROGRESSION_DEPRECATED_Dagger_CanUseGates = PersistencePropertyDefinition(PROGRESSION, 4228552677, "Boolean", False)
PROGRESSION_CanDropMaterials = PersistencePropertyDefinition(PROGRESSION, 4282910745, "Boolean", False)

PROGRESSION_XP = registered_persistence_key(2027853126)  # Progression_XP_RDA_2027853126
PROGRESSION_XP_XP = PersistencePropertyDefinition(PROGRESSION_XP, 264381177, "Int32", 0)

DEFAULTXPBUCKET = registered_persistence_key(1137295114)  # DefaultXPBucketRDA_1137295114
DEFAULTXPBUCKET_XP = PersistencePropertyDefinition(DEFAULTXPBUCKET, 264381177, "Int32", 0)

CARETAKERPROGRESSION = registered_persistence_key(1570166263)  # CaretakerProgression_RDA_1570166263
CARETAKERPROGRESSION_XP = PersistencePropertyDefinition(CARETAKERPROGRESSION, 3442105829, "Int32", 0)

PROGRESSION_NEVE = registered_persistence_key(1978619566)  # Neve_RDA_1978619566
PROGRESSION_NEVE__IsHardened = PersistencePropertyDefinition(PROGRESSION_NEVE, 1034336597, "Boolean", False)
PROGRESSION_NEVE_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_NEVE, 1363998350, "Int32", 0)
PROGRESSION_NEVE__UnavailableReasonString = PersistencePropertyDefinition(PROGRESSION_NEVE, 1534810185, "Int32", 0)
PROGRESSION_NEVE_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(PROGRESSION_NEVE, 1801418090, "Boolean", False)
PROGRESSION_NEVE__Unlocked = PersistencePropertyDefinition(PROGRESSION_NEVE, 2184345643, "Boolean", False)
PROGRESSION_NEVE__IsHeroic = PersistencePropertyDefinition(PROGRESSION_NEVE, 2245837626, "Boolean", False)
PROGRESSION_NEVE_Bit = PersistencePropertyDefinition(PROGRESSION_NEVE, 2295053469, "Int32", 0)
PROGRESSION_NEVE__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_NEVE, 2599909908, "Boolean", False)
PROGRESSION_NEVE_XP = PersistencePropertyDefinition(PROGRESSION_NEVE, 3442105829, "Int32", 0)
PROGRESSION_NEVE__State = PersistencePropertyDefinition(PROGRESSION_NEVE, 3518571373, "Int32", 2)
PROGRESSION_NEVE_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_NEVE, 3799491550, "Int32", 0)
PROGRESSION_NEVE_Context = PersistencePropertyDefinition(PROGRESSION_NEVE, 3901334258, "Int32", 0)
PROGRESSION_NEVE__Available = PersistencePropertyDefinition(PROGRESSION_NEVE, 4103292835, "Boolean", True)

PROGRESSION_NEVE_PROPERTIES = {
    "State": PROGRESSION_NEVE__State,
    "Relationship XP": PROGRESSION_NEVE_Relationship_XP,
}

PROGRESSION_LUCANIS = registered_persistence_key(1623302849)  # Lucanis_RDA_1623302849
PROGRESSION_LUCANIS__IsHardened = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 1034336597, "Boolean", False)
PROGRESSION_LUCANIS_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 1363998350, "Int32", 0)
PROGRESSION_LUCANIS__UnavailableReasonString = PersistencePropertyDefinition(
    PROGRESSION_LUCANIS, 1534810185, "Int32", 0
)
PROGRESSION_LUCANIS_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(
    PROGRESSION_LUCANIS, 1801418090, "Boolean", False
)
PROGRESSION_LUCANIS__Unlocked = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 2184345643, "Boolean", False)
PROGRESSION_LUCANIS_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 2234541938, "Int32", 0)
PROGRESSION_LUCANIS__IsHeroic = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 2245837626, "Boolean", False)
PROGRESSION_LUCANIS_Bit = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 2295053469, "Int32", 0)
PROGRESSION_LUCANIS__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 2599909908, "Boolean", False)
PROGRESSION_LUCANIS_XP = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 3442105829, "Int32", 0)
PROGRESSION_LUCANIS__State = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 3518571373, "Int32", 2)
PROGRESSION_LUCANIS_Context = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 3901334258, "Int32", 0)
PROGRESSION_LUCANIS__Available = PersistencePropertyDefinition(PROGRESSION_LUCANIS, 4103292835, "Boolean", True)

PROGRESSION_LUCANIS_PROPERTIES = {
    "State": PROGRESSION_LUCANIS__State,
    "Relationship XP": PROGRESSION_LUCANIS_Relationship_XP,
}

PROGRESSION_TAASH = registered_persistence_key(1259630094)  # Taash_RDA_1259630094
PROGRESSION_TAASH__IsHardened = PersistencePropertyDefinition(PROGRESSION_TAASH, 1034336597, "Boolean", False)
PROGRESSION_TAASH_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_TAASH, 1363998350, "Int32", 0)
PROGRESSION_TAASH__UnavailableReasonString = PersistencePropertyDefinition(PROGRESSION_TAASH, 1534810185, "Int32", 0)
PROGRESSION_TAASH_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(
    PROGRESSION_TAASH, 1801418090, "Boolean", False
)
PROGRESSION_TAASH__Unlocked = PersistencePropertyDefinition(PROGRESSION_TAASH, 2184345643, "Boolean", False)
PROGRESSION_TAASH__IsHeroic = PersistencePropertyDefinition(PROGRESSION_TAASH, 2245837626, "Boolean", False)
PROGRESSION_TAASH_Bit = PersistencePropertyDefinition(PROGRESSION_TAASH, 2295053469, "Int32", 0)
PROGRESSION_TAASH__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_TAASH, 2599909908, "Boolean", False)
PROGRESSION_TAASH_XP = PersistencePropertyDefinition(PROGRESSION_TAASH, 3442105829, "Int32", 0)
PROGRESSION_TAASH__State = PersistencePropertyDefinition(PROGRESSION_TAASH, 3518571373, "Int32", 2)
PROGRESSION_TAASH_Context = PersistencePropertyDefinition(PROGRESSION_TAASH, 3901334258, "Int32", 0)
PROGRESSION_TAASH_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_TAASH, 3913848809, "Int32", 0)
PROGRESSION_TAASH__Available = PersistencePropertyDefinition(PROGRESSION_TAASH, 4103292835, "Boolean", True)

PROGRESSION_TAASH_PROPERTIES = {
    "State": PROGRESSION_TAASH__State,
    "Relationship XP": PROGRESSION_TAASH_Relationship_XP,
}

PROGRESSION_EMMRICH = registered_persistence_key(1548220455)  # Emmrich_RDA_1548220455
PROGRESSION_EMMRICH__IsHardened = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 1034336597, "Boolean", False)
PROGRESSION_EMMRICH_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 1363998350, "Int32", 0)
PROGRESSION_EMMRICH__UnavailableReasonString = PersistencePropertyDefinition(
    PROGRESSION_EMMRICH, 1534810185, "Int32", 0
)
PROGRESSION_EMMRICH_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 1770605512, "Int32", 0)
PROGRESSION_EMMRICH_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(
    PROGRESSION_EMMRICH, 1801418090, "Boolean", False
)
PROGRESSION_EMMRICH__Unlocked = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 2184345643, "Boolean", False)
PROGRESSION_EMMRICH__IsHeroic = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 2245837626, "Boolean", False)
PROGRESSION_EMMRICH_Bit = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 2295053469, "Int32", 0)
PROGRESSION_EMMRICH__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 2599909908, "Boolean", False)
PROGRESSION_EMMRICH_XP = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 3442105829, "Int32", 0)
PROGRESSION_EMMRICH__State = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 3518571373, "Int32", 2)
PROGRESSION_EMMRICH_Context = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 3901334258, "Int32", 0)
PROGRESSION_EMMRICH__Available = PersistencePropertyDefinition(PROGRESSION_EMMRICH, 4103292835, "Boolean", True)

EMMRICH_GENERAL = registered_persistence_key(1496155608)  # Emmrich_00_General_1496155608
EMMRICH_GENERAL_Manfred_Is_Revived = PersistencePropertyDefinition(EMMRICH_GENERAL, 2031954296, "Boolean", False)
EMMRICH_GENERAL_Emmrich_Is_Lich = PersistencePropertyDefinition(EMMRICH_GENERAL, 2156617276, "Boolean", False)
EMMRICH_GENERAL_Rook_Dislikes_Necromancy = PersistencePropertyDefinition(EMMRICH_GENERAL, 2902701791, "Int32", 0)
EMMRICH_GENERAL_Emmrich_Strife_Dating = PersistencePropertyDefinition(EMMRICH_GENERAL, 3132677744, "Boolean", False)

EMMRICH_SACRIFICE = registered_persistence_key(1146399126)  # Emmrich_22_Sacrifice_1146399126
EMMRICH_SACRIFICE_Hezenkoss_Noticed_Romance = PersistencePropertyDefinition(
    EMMRICH_SACRIFICE, 2658489548, "Boolean", False
)
EMMRICH_SACRIFICE_Emmrich_Chooses_Manfred = PersistencePropertyDefinition(
    EMMRICH_SACRIFICE, 3304176969, "Boolean", False
)
EMMRICH_SACRIFICE_Emmrich_Chooses_Lich = PersistencePropertyDefinition(EMMRICH_SACRIFICE, 3980442991, "Boolean", False)

PROGRESSION_EMMRICH_PROPERTIES = {
    "State": PROGRESSION_EMMRICH__State,
    "Relationship XP": PROGRESSION_EMMRICH_Relationship_XP,
    # "Is Manfred revived?": EMMRICH_GENERAL_Manfred_Is_Revived,
    # "Is Emmrich a Lich?": EMMRICH_GENERAL_Emmrich_Is_Lich,
    "Emmrich chose Manfred?": EMMRICH_SACRIFICE_Emmrich_Chooses_Manfred,
    "Emmrich chose Lichdom?": EMMRICH_SACRIFICE_Emmrich_Chooses_Lich,
}

PROGRESSION_DAVRIN = registered_persistence_key(1160045836)  # Davrin_RDA_1160045836
PROGRESSION_DAVRIN_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 401913055, "Int32", 0)
PROGRESSION_DAVRIN__IsHardened = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 1034336597, "Boolean", False)
PROGRESSION_DAVRIN_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 1363998350, "Int32", 0)
PROGRESSION_DAVRIN__UnavailableReasonString = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 1534810185, "Int32", 0)
PROGRESSION_DAVRIN_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(
    PROGRESSION_DAVRIN, 1801418090, "Boolean", False
)
PROGRESSION_DAVRIN__Unlocked = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 2184345643, "Boolean", False)
PROGRESSION_DAVRIN__IsHeroic = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 2245837626, "Boolean", False)
PROGRESSION_DAVRIN_Bit = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 2295053469, "Int32", 0)
PROGRESSION_DAVRIN__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 2599909908, "Boolean", False)
PROGRESSION_DAVRIN_XP = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 3442105829, "Int32", 0)
PROGRESSION_DAVRIN__State = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 3518571373, "Int32", 2)
PROGRESSION_DAVRIN_Context = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 3901334258, "Int32", 0)
PROGRESSION_DAVRIN__Available = PersistencePropertyDefinition(PROGRESSION_DAVRIN, 4103292835, "Boolean", True)

PROGRESSION_DAVRIN_PROPERTIES = {
    "State": PROGRESSION_DAVRIN__State,
    "Relationship XP": PROGRESSION_DAVRIN_Relationship_XP,
}

PROGRESSION_BELLARA = registered_persistence_key(1135958718)  # Bellara_RDA_1135958718
PROGRESSION_BELLARA__IsHardened = PersistencePropertyDefinition(PROGRESSION_BELLARA, 1034336597, "Boolean", False)
PROGRESSION_BELLARA_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_BELLARA, 1363998350, "Int32", 0)
PROGRESSION_BELLARA__UnavailableReasonString = PersistencePropertyDefinition(
    PROGRESSION_BELLARA, 1534810185, "Int32", 0
)
PROGRESSION_BELLARA_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(
    PROGRESSION_BELLARA, 1801418090, "Boolean", False
)
PROGRESSION_BELLARA_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_BELLARA, 2074033460, "Int32", 0)
PROGRESSION_BELLARA__Unlocked = PersistencePropertyDefinition(PROGRESSION_BELLARA, 2184345643, "Boolean", False)
PROGRESSION_BELLARA__IsHeroic = PersistencePropertyDefinition(PROGRESSION_BELLARA, 2245837626, "Boolean", False)
PROGRESSION_BELLARA_Bit = PersistencePropertyDefinition(PROGRESSION_BELLARA, 2295053469, "Int32", 0)
PROGRESSION_BELLARA__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_BELLARA, 2599909908, "Boolean", False)
PROGRESSION_BELLARA_XP = PersistencePropertyDefinition(PROGRESSION_BELLARA, 3442105829, "Int32", 0)
PROGRESSION_BELLARA__State = PersistencePropertyDefinition(PROGRESSION_BELLARA, 3518571373, "Int32", 2)
PROGRESSION_BELLARA_Context = PersistencePropertyDefinition(PROGRESSION_BELLARA, 3901334258, "Int32", 0)
PROGRESSION_BELLARA__Available = PersistencePropertyDefinition(PROGRESSION_BELLARA, 4103292835, "Boolean", True)

PROGRESSION_BELLARA_PROPERTIES = {
    "State": PROGRESSION_BELLARA__State,
    "Relationship XP": PROGRESSION_BELLARA_Relationship_XP,
}

PROGRESSION_HARDING = registered_persistence_key(1580103331)  # Harding_RDA_1580103331
PROGRESSION_HARDING__IsHardened = PersistencePropertyDefinition(PROGRESSION_HARDING, 1034336597, "Boolean", False)
PROGRESSION_HARDING_ExploreAbilityUnlock = PersistencePropertyDefinition(PROGRESSION_HARDING, 1226829174, "Int32", 0)
PROGRESSION_HARDING_Relationship_XP = PersistencePropertyDefinition(PROGRESSION_HARDING, 1363998350, "Int32", 0)
PROGRESSION_HARDING__UnavailableReasonString = PersistencePropertyDefinition(
    PROGRESSION_HARDING, 1534810185, "Int32", 0
)
PROGRESSION_HARDING_HasTriggeredHeroicFTUE = PersistencePropertyDefinition(
    PROGRESSION_HARDING, 1801418090, "Boolean", False
)
PROGRESSION_HARDING__Unlocked = PersistencePropertyDefinition(PROGRESSION_HARDING, 2184345643, "Boolean", False)
PROGRESSION_HARDING__IsHeroic = PersistencePropertyDefinition(PROGRESSION_HARDING, 2245837626, "Boolean", False)
PROGRESSION_HARDING_Bit = PersistencePropertyDefinition(PROGRESSION_HARDING, 2295053469, "Int32", 0)
PROGRESSION_HARDING__WasInLastQuest = PersistencePropertyDefinition(PROGRESSION_HARDING, 2599909908, "Boolean", False)
PROGRESSION_HARDING_XP = PersistencePropertyDefinition(PROGRESSION_HARDING, 3442105829, "Int32", 0)
PROGRESSION_HARDING__State = PersistencePropertyDefinition(PROGRESSION_HARDING, 3518571373, "Int32", 2)
PROGRESSION_HARDING_Context = PersistencePropertyDefinition(PROGRESSION_HARDING, 3901334258, "Int32", 0)
PROGRESSION_HARDING__Available = PersistencePropertyDefinition(PROGRESSION_HARDING, 4103292835, "Boolean", True)

PROGRESSION_HARDING_PROPERTIES = {
    "State": PROGRESSION_HARDING__State,
    "Relationship XP": PROGRESSION_HARDING_Relationship_XP,
}

# Factions
FACTION_MOURNWATCH = registered_persistence_key(1648677464)  # Faction_Mournwatch_RDA_1648677464
FACTION_MOURNWATCH_Faction_XP = PersistencePropertyDefinition(FACTION_MOURNWATCH, 836139687, "Int32", 0)
FACTION_MOURNWATCH_FinaleStrength = PersistencePropertyDefinition(FACTION_MOURNWATCH, 873206043, "Int32", 1)
FACTION_MOURNWATCH__IsHardened = PersistencePropertyDefinition(FACTION_MOURNWATCH, 1034336597, "Boolean", False)
FACTION_MOURNWATCH_Faction_Level_4_Threshold = PersistencePropertyDefinition(
    FACTION_MOURNWATCH, 1508987368, "Int32", 3200
)
FACTION_MOURNWATCH__UnavailableReasonString = PersistencePropertyDefinition(FACTION_MOURNWATCH, 1534810185, "Int32", 0)
FACTION_MOURNWATCH__Unlocked = PersistencePropertyDefinition(FACTION_MOURNWATCH, 2184345643, "Boolean", False)
FACTION_MOURNWATCH__IsHeroic = PersistencePropertyDefinition(FACTION_MOURNWATCH, 2245837626, "Boolean", False)
FACTION_MOURNWATCH_Faction_Level_3_Threshold = PersistencePropertyDefinition(
    FACTION_MOURNWATCH, 2274850050, "Int32", 1600
)
FACTION_MOURNWATCH_Faction_Level_2_Threshold = PersistencePropertyDefinition(
    FACTION_MOURNWATCH, 2370141904, "Int32", 500
)
FACTION_MOURNWATCH_Faction_Level_1_Threshold = PersistencePropertyDefinition(FACTION_MOURNWATCH, 2501250810, "Int32", 0)
FACTION_MOURNWATCH__WasInLastQuest = PersistencePropertyDefinition(FACTION_MOURNWATCH, 2599909908, "Boolean", False)
FACTION_MOURNWATCH_Faction_Power = PersistencePropertyDefinition(FACTION_MOURNWATCH, 3250645730, "Int32", 0)
FACTION_MOURNWATCH__State = PersistencePropertyDefinition(FACTION_MOURNWATCH, 3518571373, "Int32", 2)
FACTION_MOURNWATCH__Available = PersistencePropertyDefinition(FACTION_MOURNWATCH, 4103292835, "Boolean", True)

FACTION_MOURNWATCH_PROPERTIES = {
    # "State": FACTION_MOURNWATCH__State,
    "Faction XP": FACTION_MOURNWATCH_Faction_XP,
    "Faction Power": FACTION_MOURNWATCH_Faction_Power,
    "Finale Strength": FACTION_MOURNWATCH_FinaleStrength,
}

FACTION_ANTIVANCROWS = registered_persistence_key(1947141027)  # Faction_AntivanCrows_RDA_1947141027
FACTION_ANTIVANCROWS_Faction_XP = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 836139687, "Int32", 0)
FACTION_ANTIVANCROWS__IsHardened = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 1034336597, "Boolean", False)
FACTION_ANTIVANCROWS_Faction_Level_4_Threshold = PersistencePropertyDefinition(
    FACTION_ANTIVANCROWS, 1508987368, "Int32", 3200
)
FACTION_ANTIVANCROWS__UnavailableReasonString = PersistencePropertyDefinition(
    FACTION_ANTIVANCROWS, 1534810185, "Int32", 0
)
FACTION_ANTIVANCROWS_FinaleStrength = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 1840556428, "Int32", 1)
FACTION_ANTIVANCROWS__Unlocked = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 2184345643, "Boolean", False)
FACTION_ANTIVANCROWS__IsHeroic = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 2245837626, "Boolean", False)
FACTION_ANTIVANCROWS_Faction_Level_3_Threshold = PersistencePropertyDefinition(
    FACTION_ANTIVANCROWS, 2274850050, "Int32", 1600
)
FACTION_ANTIVANCROWS_Faction_Level_2_Threshold = PersistencePropertyDefinition(
    FACTION_ANTIVANCROWS, 2370141904, "Int32", 500
)
FACTION_ANTIVANCROWS_Faction_Power = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 2374116801, "Int32", 0)
FACTION_ANTIVANCROWS_Faction_Level_1_Threshold = PersistencePropertyDefinition(
    FACTION_ANTIVANCROWS, 2501250810, "Int32", 0
)
FACTION_ANTIVANCROWS__WasInLastQuest = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 2599909908, "Boolean", False)
FACTION_ANTIVANCROWS__State = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 3518571373, "Int32", 2)
FACTION_ANTIVANCROWS__Available = PersistencePropertyDefinition(FACTION_ANTIVANCROWS, 4103292835, "Boolean", True)

FACTION_ANTIVANCROWS_PROPERTIES = {
    # "State": FACTION_ANTIVANCROWS__State,
    "Faction XP": FACTION_ANTIVANCROWS_Faction_XP,
    "Faction Power": FACTION_ANTIVANCROWS_Faction_Power,
    "Finale Strength": FACTION_ANTIVANCROWS_FinaleStrength,
}

FACTION_LORDSOFFORTUNE = registered_persistence_key(1604031236)  # Faction_LordsOfFortune_RDA_1604031236
FACTION_LORDSOFFORTUNE_Faction_Power = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 5185996, "Int32", 0)
FACTION_LORDSOFFORTUNE_Faction_XP = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 836139687, "Int32", 0)
FACTION_LORDSOFFORTUNE__IsHardened = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 1034336597, "Boolean", False)
FACTION_LORDSOFFORTUNE_Faction_Level_4_Threshold = PersistencePropertyDefinition(
    FACTION_LORDSOFFORTUNE, 1508987368, "Int32", 3200
)
FACTION_LORDSOFFORTUNE__UnavailableReasonString = PersistencePropertyDefinition(
    FACTION_LORDSOFFORTUNE, 1534810185, "Int32", 0
)
FACTION_LORDSOFFORTUNE_FinaleStrength = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 2016182132, "Int32", 1)
FACTION_LORDSOFFORTUNE__Unlocked = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 2184345643, "Boolean", False)
FACTION_LORDSOFFORTUNE__IsHeroic = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 2245837626, "Boolean", False)
FACTION_LORDSOFFORTUNE_Faction_Level_3_Threshold = PersistencePropertyDefinition(
    FACTION_LORDSOFFORTUNE, 2274850050, "Int32", 1600
)
FACTION_LORDSOFFORTUNE_Faction_Level_2_Threshold = PersistencePropertyDefinition(
    FACTION_LORDSOFFORTUNE, 2370141904, "Int32", 500
)
FACTION_LORDSOFFORTUNE_Faction_Level_1_Threshold = PersistencePropertyDefinition(
    FACTION_LORDSOFFORTUNE, 2501250810, "Int32", 0
)
FACTION_LORDSOFFORTUNE__WasInLastQuest = PersistencePropertyDefinition(
    FACTION_LORDSOFFORTUNE, 2599909908, "Boolean", False
)
FACTION_LORDSOFFORTUNE__State = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 3518571373, "Int32", 2)
FACTION_LORDSOFFORTUNE__Available = PersistencePropertyDefinition(FACTION_LORDSOFFORTUNE, 4103292835, "Boolean", True)

FACTION_LORDSOFFORTUNE_PROPERTIES = {
    # "State": FACTION_LORDSOFFORTUNE__State,
    "Faction XP": FACTION_LORDSOFFORTUNE_Faction_XP,
    "Faction Power": FACTION_LORDSOFFORTUNE_Faction_Power,
    "Finale Strength": FACTION_LORDSOFFORTUNE_FinaleStrength,
}

FACTION_VEILJUMPERS = registered_persistence_key(1822830084)  # Faction_VeilJumpers_RDA_1822830084
FACTION_VEILJUMPERS_Faction_XP = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 836139687, "Int32", 0)
FACTION_VEILJUMPERS__IsHardened = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 1034336597, "Boolean", False)
FACTION_VEILJUMPERS_Faction_Level_4_Threshold = PersistencePropertyDefinition(
    FACTION_VEILJUMPERS, 1508987368, "Int32", 3200
)
FACTION_VEILJUMPERS__UnavailableReasonString = PersistencePropertyDefinition(
    FACTION_VEILJUMPERS, 1534810185, "Int32", 0
)
FACTION_VEILJUMPERS_Faction_Power = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 1997498116, "Int32", 0)
FACTION_VEILJUMPERS__Unlocked = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 2184345643, "Boolean", False)
FACTION_VEILJUMPERS__IsHeroic = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 2245837626, "Boolean", False)
FACTION_VEILJUMPERS_Faction_Level_3_Threshold = PersistencePropertyDefinition(
    FACTION_VEILJUMPERS, 2274850050, "Int32", 1600
)
FACTION_VEILJUMPERS_Faction_Level_2_Threshold = PersistencePropertyDefinition(
    FACTION_VEILJUMPERS, 2370141904, "Int32", 500
)
FACTION_VEILJUMPERS_Faction_Level_1_Threshold = PersistencePropertyDefinition(
    FACTION_VEILJUMPERS, 2501250810, "Int32", 0
)
FACTION_VEILJUMPERS_FinaleStrength = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 2598850265, "Int32", 1)
FACTION_VEILJUMPERS__WasInLastQuest = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 2599909908, "Boolean", False)
FACTION_VEILJUMPERS__State = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 3518571373, "Int32", 2)
FACTION_VEILJUMPERS__Available = PersistencePropertyDefinition(FACTION_VEILJUMPERS, 4103292835, "Boolean", True)

FACTION_VEILJUMPERS_PROPERTIES = {
    # "State": FACTION_VEILJUMPERS__State,
    "Faction XP": FACTION_VEILJUMPERS_Faction_XP,
    "Faction Power": FACTION_VEILJUMPERS_Faction_Power,
    "Finale Strength": FACTION_VEILJUMPERS_FinaleStrength,
}

FACTION_GREYWARDENS = registered_persistence_key(1793983220)  # Faction_GreyWardens_RDA_1793983220
FACTION_GREYWARDENS_FinaleStrength = PersistencePropertyDefinition(FACTION_GREYWARDENS, 143290146, "Int32", 1)
FACTION_GREYWARDENS_Faction_XP = PersistencePropertyDefinition(FACTION_GREYWARDENS, 836139687, "Int32", 0)
FACTION_GREYWARDENS__IsHardened = PersistencePropertyDefinition(FACTION_GREYWARDENS, 1034336597, "Boolean", False)
FACTION_GREYWARDENS_Faction_Power = PersistencePropertyDefinition(FACTION_GREYWARDENS, 1381090647, "Int32", 0)
FACTION_GREYWARDENS_Faction_Level_4_Threshold = PersistencePropertyDefinition(
    FACTION_GREYWARDENS, 1508987368, "Int32", 3200
)
FACTION_GREYWARDENS__UnavailableReasonString = PersistencePropertyDefinition(
    FACTION_GREYWARDENS, 1534810185, "Int32", 0
)
FACTION_GREYWARDENS__Unlocked = PersistencePropertyDefinition(FACTION_GREYWARDENS, 2184345643, "Boolean", False)
FACTION_GREYWARDENS__IsHeroic = PersistencePropertyDefinition(FACTION_GREYWARDENS, 2245837626, "Boolean", False)
FACTION_GREYWARDENS_Faction_Level_3_Threshold = PersistencePropertyDefinition(
    FACTION_GREYWARDENS, 2274850050, "Int32", 1600
)
FACTION_GREYWARDENS_Faction_Level_2_Threshold = PersistencePropertyDefinition(
    FACTION_GREYWARDENS, 2370141904, "Int32", 500
)
FACTION_GREYWARDENS_Faction_Level_1_Threshold = PersistencePropertyDefinition(
    FACTION_GREYWARDENS, 2501250810, "Int32", 0
)
FACTION_GREYWARDENS__WasInLastQuest = PersistencePropertyDefinition(FACTION_GREYWARDENS, 2599909908, "Boolean", False)
FACTION_GREYWARDENS__State = PersistencePropertyDefinition(FACTION_GREYWARDENS, 3518571373, "Int32", 2)
FACTION_GREYWARDENS__Available = PersistencePropertyDefinition(FACTION_GREYWARDENS, 4103292835, "Boolean", True)

FACTION_GREYWARDENS_PROPERTIES = {
    # "State": FACTION_GREYWARDENS__State,
    "Faction XP": FACTION_GREYWARDENS_Faction_XP,
    "Faction Power": FACTION_GREYWARDENS_Faction_Power,
    "Finale Strength": FACTION_GREYWARDENS_FinaleStrength,
}

FACTION_SHADOWDRAGONS = registered_persistence_key(1235554634)  # Faction_ShadowDragons_RDA_1235554634
FACTION_SHADOWDRAGONS_Faction_XP = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 836139687, "Int32", 0)
FACTION_SHADOWDRAGONS__IsHardened = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 1034336597, "Boolean", False)
FACTION_SHADOWDRAGONS_FinaleStrength = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 1206563472, "Int32", 1)
FACTION_SHADOWDRAGONS_Faction_Level_4_Threshold = PersistencePropertyDefinition(
    FACTION_SHADOWDRAGONS, 1508987368, "Int32", 3200
)
FACTION_SHADOWDRAGONS__UnavailableReasonString = PersistencePropertyDefinition(
    FACTION_SHADOWDRAGONS, 1534810185, "Int32", 0
)
FACTION_SHADOWDRAGONS__Unlocked = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 2184345643, "Boolean", False)
FACTION_SHADOWDRAGONS__IsHeroic = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 2245837626, "Boolean", False)
FACTION_SHADOWDRAGONS_Faction_Level_3_Threshold = PersistencePropertyDefinition(
    FACTION_SHADOWDRAGONS, 2274850050, "Int32", 1600
)
FACTION_SHADOWDRAGONS_Faction_Level_2_Threshold = PersistencePropertyDefinition(
    FACTION_SHADOWDRAGONS, 2370141904, "Int32", 500
)
FACTION_SHADOWDRAGONS_Faction_Level_1_Threshold = PersistencePropertyDefinition(
    FACTION_SHADOWDRAGONS, 2501250810, "Int32", 0
)
FACTION_SHADOWDRAGONS__WasInLastQuest = PersistencePropertyDefinition(
    FACTION_SHADOWDRAGONS, 2599909908, "Boolean", False
)
FACTION_SHADOWDRAGONS_Faction_Power = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 2983243664, "Int32", 0)
FACTION_SHADOWDRAGONS__State = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 3518571373, "Int32", 2)
FACTION_SHADOWDRAGONS__Available = PersistencePropertyDefinition(FACTION_SHADOWDRAGONS, 4103292835, "Boolean", True)

FACTION_SHADOWDRAGONS_PROPERTIES = {
    # "State": FACTION_SHADOWDRAGONS__State,
    "Faction XP": FACTION_SHADOWDRAGONS_Faction_XP,
    "Faction Power": FACTION_SHADOWDRAGONS_Faction_Power,
    "Finale Strength": FACTION_SHADOWDRAGONS_FinaleStrength,
}

HARDING_AND_TASH = registered_persistence_key(1395335409)  # Hrd_Tsh_General_1395335409
HARDING_AND_TASH_hrd_tsh_romance_active = PersistencePropertyDefinition(HARDING_AND_TASH, 30545043, "Boolean", False)
HARDING_AND_TASH_gift_chose_jewelry = PersistencePropertyDefinition(HARDING_AND_TASH, 1782945647, "Boolean", False)
HARDING_AND_TASH_gift_chose_archery = PersistencePropertyDefinition(HARDING_AND_TASH, 2246275998, "Boolean", False)
HARDING_AND_TASH_gift_chose_flowers = PersistencePropertyDefinition(HARDING_AND_TASH, 3930540536, "Boolean", False)

HARDING_AND_TASH_PROPERTIES = {
    "Romanced?": HARDING_AND_TASH_hrd_tsh_romance_active,
    "Gift: Jewelry": HARDING_AND_TASH_gift_chose_jewelry,
    "Gift: Archery": HARDING_AND_TASH_gift_chose_archery,
    "Gift: Flowers": HARDING_AND_TASH_gift_chose_flowers,
}

LUCANIS_AND_NEVE = registered_persistence_key(1592749924)  # Luc_Nev_General_1592749924
LUCANIS_AND_NEVE_Neve_Lucanis_Romance = PersistencePropertyDefinition(LUCANIS_AND_NEVE, 227845584, "Boolean", False)
LUCANIS_AND_NEVE_No_Pie = PersistencePropertyDefinition(LUCANIS_AND_NEVE, 1738918478, "Boolean", False)
LUCANIS_AND_NEVE_Made_Pie = PersistencePropertyDefinition(LUCANIS_AND_NEVE, 2632247097, "Boolean", False)

LUCANIS_AND_NEVE_PROPERTIES = {
    "Romanced?": LUCANIS_AND_NEVE_Neve_Lucanis_Romance,
    "No Pie": LUCANIS_AND_NEVE_No_Pie,
    "Made Pie": LUCANIS_AND_NEVE_Made_Pie,
}

EMMRICH_STRIFE_DATE = registered_persistence_key(1791028401)  # Emmrich_99_StrifeDateScene_1791028401
EMMRICH_STRIFE_DATE_Emmrich_Strife_Caves = PersistencePropertyDefinition(
    EMMRICH_STRIFE_DATE, 2383745674, "Boolean", False
)
EMMRICH_STRIFE_DATE_Emmrich_Strife_Grove = PersistencePropertyDefinition(
    EMMRICH_STRIFE_DATE, 3776408187, "Boolean", False
)

EMMRICH_AND_STRIFE_PROPERTIES = {
    "Romanced?": EMMRICH_GENERAL_Emmrich_Strife_Dating,
    "Date at Caves?": EMMRICH_STRIFE_DATE_Emmrich_Strife_Caves,
    "Date at Grove?": EMMRICH_STRIFE_DATE_Emmrich_Strife_Grove,
}

LUCANIS_M21 = registered_persistence_key(1232360751)  # Luc_2_1_140_m21_request_QST_RDA_1232360751
LUCANIS_M23 = registered_persistence_key(1744784847)  # Luc_2_3_100_m23_request_QST_RDA_1744784847
EMMRICH_M23_LICHBECOMING = registered_persistence_key(
    1170183125
)  # Emm_2_3_100_m23_LichBecoming_request_QST_RDA_1170183125
EMMRICH_M23_MANFREDREVIVE = registered_persistence_key(
    2083352105
)  # Emm_2_3_100_m23_ManfredRevive_request_QST_RDA_2083352105

# Romance properties
ROMANCE_NEVE = registered_persistence_key(2022350065)  # Neve_00_Romance_2022350065
ROMANCE_NEVE_Rook_Can_Flirt_Neve = PersistencePropertyDefinition(ROMANCE_NEVE, 1309495461, "Boolean", True)
ROMANCE_NEVE_Neve_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_NEVE, 1711736383, "Boolean", False)
ROMANCE_NEVE_Neve_Romance_TestingWaters_Complete = PersistencePropertyDefinition(
    ROMANCE_NEVE, 2152232388, "Boolean", False
)
ROMANCE_NEVE_Neve_Flirt_Count = PersistencePropertyDefinition(ROMANCE_NEVE, 2675503667, "Int32", 0)
ROMANCE_NEVE_Neve_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_NEVE, 2851760417, "Boolean", False)
ROMANCE_NEVE_Neve_Afterglow_Complete = PersistencePropertyDefinition(ROMANCE_NEVE, 3429055734, "Boolean", False)
ROMANCE_NEVE_Rook_Backs_Neve = PersistencePropertyDefinition(ROMANCE_NEVE, 3737124597, "Int32", 0)

ROMANCE_NEVE_PROPERTIES = {
    "Can Flirt?": ROMANCE_NEVE_Rook_Can_Flirt_Neve,
    "Cut Off?": ROMANCE_NEVE_Neve_Romance_Cut_Off,
    "Testing waters complete?": ROMANCE_NEVE_Neve_Romance_TestingWaters_Complete,
    "Flirt Count": ROMANCE_NEVE_Neve_Flirt_Count,
    "Exclusive": ROMANCE_NEVE_Neve_Romance_Exclusive,
    "Afterglow": ROMANCE_NEVE_Neve_Afterglow_Complete,
    "Rook backs Neve": ROMANCE_NEVE_Rook_Backs_Neve,
}

ROMANCE_DAVRIN = registered_persistence_key(1805940062)  # Davrin_00_Romance_1805940062
ROMANCE_DAVRIN_Afterglow_Life_of_Adventure_choice_taken = PersistencePropertyDefinition(
    ROMANCE_DAVRIN, 571409871, "Boolean", False
)
ROMANCE_DAVRIN_Afterglow_Domestic_Bliss_choice_taken = PersistencePropertyDefinition(
    ROMANCE_DAVRIN, 2651224975, "Boolean", False
)
ROMANCE_DAVRIN_Davrin_Flirt_Count = PersistencePropertyDefinition(ROMANCE_DAVRIN, 2732057980, "Int32", 0)
ROMANCE_DAVRIN_Rook_Can_Flirt_Davrin = PersistencePropertyDefinition(ROMANCE_DAVRIN, 3175505004, "Boolean", True)
ROMANCE_DAVRIN_Davrin_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_DAVRIN, 3287038745, "Boolean", False)
ROMANCE_DAVRIN_Afterglow_Whatever_Comes_choice_taken = PersistencePropertyDefinition(
    ROMANCE_DAVRIN, 3372923222, "Boolean", False
)
ROMANCE_DAVRIN_Davrin_Postreturn_Scene_Complete = PersistencePropertyDefinition(
    ROMANCE_DAVRIN, 3643375017, "Boolean", False
)
ROMANCE_DAVRIN_Davrin_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_DAVRIN, 4037795175, "Boolean", False)
ROMANCE_DAVRIN_Davrin_TestingWaters_Romantic = PersistencePropertyDefinition(
    ROMANCE_DAVRIN, 4044905858, "Boolean", False
)

ROMANCE_DAVRIN_PROPERTIES = {
    "Afterglow: Life of Adventure choice taken?": ROMANCE_DAVRIN_Afterglow_Life_of_Adventure_choice_taken,
    "Domestic Bliss choice taken?": ROMANCE_DAVRIN_Afterglow_Domestic_Bliss_choice_taken,
    "Flirt Count": ROMANCE_DAVRIN_Davrin_Flirt_Count,
    "Can Flirt?": ROMANCE_DAVRIN_Rook_Can_Flirt_Davrin,
    "Exclusive": ROMANCE_DAVRIN_Davrin_Romance_Exclusive,
    "Afterglow: Whatever Comes choice taken": ROMANCE_DAVRIN_Afterglow_Whatever_Comes_choice_taken,
    "Postreturn Scene Complete": ROMANCE_DAVRIN_Davrin_Postreturn_Scene_Complete,
    "Cut Off?": ROMANCE_DAVRIN_Davrin_Romance_Cut_Off,
    "Testing waters romantic?": ROMANCE_DAVRIN_Davrin_TestingWaters_Romantic,
}

ROMANCE_BELLARA = registered_persistence_key(1628101232)  # Bellara_00_Romance_1628101232
ROMANCE_BELLARA_Bellara_TW_SaidYes = PersistencePropertyDefinition(ROMANCE_BELLARA, 2044255856, "Boolean", False)
ROMANCE_BELLARA_Bellara_AfterGlow_Complete = PersistencePropertyDefinition(
    ROMANCE_BELLARA, 2934582687, "Boolean", False
)
ROMANCE_BELLARA_Rook_Can_Flirt_Bellara = PersistencePropertyDefinition(ROMANCE_BELLARA, 2987001456, "Boolean", True)
ROMANCE_BELLARA_Bellara_Flirt_Count = PersistencePropertyDefinition(ROMANCE_BELLARA, 3199595209, "Int32", 0)
ROMANCE_BELLARA_Bellara_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_BELLARA, 3951225758, "Boolean", False)
ROMANCE_BELLARA_Bellara_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_BELLARA, 4128137329, "Boolean", False)

ROMANCE_BELLARA_PROPERTIES = {
    "TW Said Yes?": ROMANCE_BELLARA_Bellara_TW_SaidYes,
    "Afterglow": ROMANCE_BELLARA_Bellara_AfterGlow_Complete,
    "Can Flirt?": ROMANCE_BELLARA_Rook_Can_Flirt_Bellara,
    "Flirt Count": ROMANCE_BELLARA_Bellara_Flirt_Count,
    "Exclusive": ROMANCE_BELLARA_Bellara_Romance_Exclusive,
    "Cut Off?": ROMANCE_BELLARA_Bellara_Romance_Cut_Off,
}

ROMANCE_TAASH = registered_persistence_key(1100432818)  # Taash_00_Romance_1100432818
ROMANCE_TAASH_Taash_Dragon_Noises = PersistencePropertyDefinition(ROMANCE_TAASH, 422033019, "Boolean", False)
ROMANCE_TAASH_Taash_talk_Feels = PersistencePropertyDefinition(ROMANCE_TAASH, 815699466, "Boolean", False)
ROMANCE_TAASH_Taash_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_TAASH, 1540447246, "Boolean", False)
ROMANCE_TAASH_postreturn_irrev = PersistencePropertyDefinition(ROMANCE_TAASH, 1849171720, "Boolean", False)
ROMANCE_TAASH_Taash_Flirt_Count = PersistencePropertyDefinition(ROMANCE_TAASH, 2016422682, "Int32", 0)
ROMANCE_TAASH_Taash_Does_Feelings = PersistencePropertyDefinition(ROMANCE_TAASH, 2097810245, "Boolean", False)
ROMANCE_TAASH_Taash_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_TAASH, 2458726006, "Boolean", False)
ROMANCE_TAASH_Has_Flirted = PersistencePropertyDefinition(ROMANCE_TAASH, 2487640600, "Boolean", False)
ROMANCE_TAASH_Rook_Can_Flirt_Taash = PersistencePropertyDefinition(ROMANCE_TAASH, 3547828755, "Boolean", True)
ROMANCE_TAASH_postreturn_affable = PersistencePropertyDefinition(ROMANCE_TAASH, 3926517825, "Boolean", False)

ROMANCE_TAASH_PROPERTIES = {
    "Dragon Noises?": ROMANCE_TAASH_Taash_Dragon_Noises,
    "Talk Feels?": ROMANCE_TAASH_Taash_talk_Feels,
    "Exclusive": ROMANCE_TAASH_Taash_Romance_Exclusive,
    "Postreturn: irreverent?": ROMANCE_TAASH_postreturn_irrev,
    "Flirt Count": ROMANCE_TAASH_Taash_Flirt_Count,
    "Does Feelings?": ROMANCE_TAASH_Taash_Does_Feelings,
    "Cut Off?": ROMANCE_TAASH_Taash_Romance_Cut_Off,
    "Has Flirted?": ROMANCE_TAASH_Has_Flirted,
    "Can Flirt?": ROMANCE_TAASH_Rook_Can_Flirt_Taash,
    "Postreturn: Affable?": ROMANCE_TAASH_postreturn_affable,
}

ROMANCE_EMMRICH = registered_persistence_key(1377196124)  # Emmrich_00_Romance_1377196124
ROMANCE_EMMRICH_Emmrich_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_EMMRICH, 104776446, "Boolean", False)
ROMANCE_EMMRICH_Rook_necromancy_secretly_intrigued = PersistencePropertyDefinition(
    ROMANCE_EMMRICH, 193508850, "Boolean", False
)
ROMANCE_EMMRICH_Emmrich_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_EMMRICH, 602628047, "Boolean", False)
ROMANCE_EMMRICH_Rook_Can_Flirt_Emmrich = PersistencePropertyDefinition(ROMANCE_EMMRICH, 1113132626, "Boolean", True)
ROMANCE_EMMRICH_Emmrich_Flirt_Count = PersistencePropertyDefinition(ROMANCE_EMMRICH, 1596288471, "Int32", 0)
ROMANCE_EMMRICH_Rook_Told_Emmrich_I_Love_You = PersistencePropertyDefinition(
    ROMANCE_EMMRICH, 2122535518, "Boolean", False
)
ROMANCE_EMMRICH_Emmrich_Postreturn_Scene_Complete = PersistencePropertyDefinition(
    ROMANCE_EMMRICH, 2344312078, "Boolean", False
)

ROMANCE_EMMRICH_PROPERTIES = {
    "Exclusive": ROMANCE_EMMRICH_Emmrich_Romance_Exclusive,
    "Rook: Ncromancy secretly intrigued?": ROMANCE_EMMRICH_Rook_necromancy_secretly_intrigued,
    "Cut Off?": ROMANCE_EMMRICH_Emmrich_Romance_Cut_Off,
    "Can Flirt?": ROMANCE_EMMRICH_Rook_Can_Flirt_Emmrich,
    "Flirt Count": ROMANCE_EMMRICH_Emmrich_Flirt_Count,
    "Rook Told Emmrich I Love_You?": ROMANCE_EMMRICH_Rook_Told_Emmrich_I_Love_You,
    "Postreturn: Complete?": ROMANCE_EMMRICH_Emmrich_Postreturn_Scene_Complete,
}

ROMANCE_HARDING = registered_persistence_key(1823151982)  # Harding_00_Romance_1823151982
ROMANCE_HARDING_Rook_postmoment_friendly = PersistencePropertyDefinition(ROMANCE_HARDING, 50584005, "Boolean", False)
ROMANCE_HARDING_Harding_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_HARDING, 354677581, "Boolean", False)
ROMANCE_HARDING_Rook_postmoment_tough = PersistencePropertyDefinition(ROMANCE_HARDING, 501814079, "Boolean", False)
ROMANCE_HARDING_Haash_Rook_revealed_crush = PersistencePropertyDefinition(ROMANCE_HARDING, 505689755, "Boolean", False)
ROMANCE_HARDING_Harding_examined_by_Emmrich = PersistencePropertyDefinition(
    ROMANCE_HARDING, 1208785000, "Boolean", False
)
ROMANCE_HARDING_Rook_ok_with_toxic_Harding = PersistencePropertyDefinition(
    ROMANCE_HARDING, 2566208300, "Boolean", False
)
ROMANCE_HARDING_Rook_Can_Flirt_Harding = PersistencePropertyDefinition(ROMANCE_HARDING, 2932984777, "Boolean", True)
ROMANCE_HARDING_Harding_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_HARDING, 3145448906, "Boolean", False)
ROMANCE_HARDING_Harding_Flirt_Count = PersistencePropertyDefinition(ROMANCE_HARDING, 3715419413, "Int32", 0)
ROMANCE_HARDING_Rook_postmoment_irreverent = PersistencePropertyDefinition(
    ROMANCE_HARDING, 3785189163, "Boolean", False
)
ROMANCE_HARDING_Harding_revealed_dreams = PersistencePropertyDefinition(ROMANCE_HARDING, 3915839206, "Boolean", False)
ROMANCE_HARDING_PostReturn_Done = PersistencePropertyDefinition(ROMANCE_HARDING, 4128551096, "Boolean", False)

ROMANCE_HARDING_PROPERTIES = {
    "Rook postmoment friendly?": ROMANCE_HARDING_Rook_postmoment_friendly,
    "Rook postmoment tough?": ROMANCE_HARDING_Rook_postmoment_tough,
    "Cut Off?": ROMANCE_HARDING_Harding_Romance_Cut_Off,
    "Haash: Rook revealed crush?": ROMANCE_HARDING_Haash_Rook_revealed_crush,
    "Harding examined by Emmrich?": ROMANCE_HARDING_Harding_examined_by_Emmrich,
    "Rook ok with toxic Harding?": ROMANCE_HARDING_Rook_ok_with_toxic_Harding,
    "Can Flirt?": ROMANCE_HARDING_Rook_Can_Flirt_Harding,
    "Exclusive": ROMANCE_HARDING_Harding_Romance_Exclusive,
    "Flirt Count": ROMANCE_HARDING_Harding_Flirt_Count,
    "Rook postmoment irreverent?": ROMANCE_HARDING_Rook_postmoment_irreverent,
    "Harding revealed dreams?": ROMANCE_HARDING_Harding_revealed_dreams,
    "Postreturn: Done?": ROMANCE_HARDING_PostReturn_Done,
}

ROMANCE_LUCANIS = registered_persistence_key(2014269085)  # Lucanis_00_Romance_2014269085
ROMANCE_LUCANIS_Lucanis_TestingWater_Romantic = PersistencePropertyDefinition(
    ROMANCE_LUCANIS, 476713944, "Boolean", False
)
ROMANCE_LUCANIS_Lucanis_Romance_Exclusive = PersistencePropertyDefinition(ROMANCE_LUCANIS, 763737897, "Boolean", False)
ROMANCE_LUCANIS_Took_CoffeeFlirt = PersistencePropertyDefinition(ROMANCE_LUCANIS, 1452072980, "Boolean", False)
ROMANCE_LUCANIS_Rook_Can_Flirt_Lucanis = PersistencePropertyDefinition(ROMANCE_LUCANIS, 1960706744, "Boolean", True)
ROMANCE_LUCANIS_Lucanis_Flirt_Count = PersistencePropertyDefinition(ROMANCE_LUCANIS, 2233014916, "Int32", 0)
ROMANCE_LUCANIS_Lucanis_Romance_Cut_Off = PersistencePropertyDefinition(ROMANCE_LUCANIS, 3625457665, "Boolean", False)
ROMANCE_LUCANIS_Lucanis_Afterglow_Complete = PersistencePropertyDefinition(
    ROMANCE_LUCANIS, 4203863220, "Boolean", False
)

ROMANCE_LUCANIS_PROPERTIES = {
    "Testing water Romantic?": ROMANCE_LUCANIS_Lucanis_TestingWater_Romantic,
    "Exclusive": ROMANCE_LUCANIS_Lucanis_Romance_Exclusive,
    "Took Coffee Flirt?": ROMANCE_LUCANIS_Took_CoffeeFlirt,
    "Can Flirt?": ROMANCE_LUCANIS_Rook_Can_Flirt_Lucanis,
    "Flirt Count": ROMANCE_LUCANIS_Lucanis_Flirt_Count,
    "Cut Off?": ROMANCE_LUCANIS_Lucanis_Romance_Cut_Off,
    "Afterglow: Complete?": ROMANCE_LUCANIS_Lucanis_Afterglow_Complete,
}

QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION = registered_persistence_key(
    1898131446
)  # QST_SHD_2_1_SoulOfACity_Lighthouse_Acquisition_RDA_1898131446
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__QuestState = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 1, "Uint8", 0
)
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__ActiveQuestPhaseId = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 2, "Uint32", 0
)
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__NumTimesCompleted = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 3, "Uint32", 0
)
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__ResetTime = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 302578490, "Uint64", 0
)
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION_HasSeenNote = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 782031478, "Boolean", False
)
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__RewardsAvailable = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 3215455463, "Boolean", False
)
QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__EligibleNotified = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION, 3821129581, "Boolean", False
)

QST_SHD_2_1_SOULOFACITY_ACQUISITION = registered_persistence_key(
    1586564090
)  # QST_SHD_2_1_SoulOfACity_Acquisition_RDA_1586564090
QST_SHD_2_1_SOULOFACITY_ACQUISITION__QuestState = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_ACQUISITION, 1, "Uint8", 0
)
QST_SHD_2_1_SOULOFACITY_ACQUISITION__ActiveQuestPhaseId = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_ACQUISITION, 2, "Uint32", 0
)
QST_SHD_2_1_SOULOFACITY_ACQUISITION__NumTimesCompleted = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_ACQUISITION, 3, "Uint32", 0
)
QST_SHD_2_1_SOULOFACITY_ACQUISITION__ResetTime = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_ACQUISITION, 302578490, "Uint64", 0
)
QST_SHD_2_1_SOULOFACITY_ACQUISITION__RewardsAvailable = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_ACQUISITION, 3215455463, "Boolean", False
)
QST_SHD_2_1_SOULOFACITY_ACQUISITION__EligibleNotified = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_ACQUISITION, 3821129581, "Boolean", False
)

QST_SHD_2_1_SOULOFACITY_DOCKTOWN = registered_persistence_key(
    1928917107
)  # QST_SHD_2_1_SoulOfACity_DockTown_RDA_1928917107
QST_SHD_2_1_SOULOFACITY_DOCKTOWN__QuestState = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN, 1, "Uint8", 0
)
QST_SHD_2_1_SOULOFACITY_DOCKTOWN__ActiveQuestPhaseId = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN, 2, "Uint32", 0
)
QST_SHD_2_1_SOULOFACITY_DOCKTOWN__NumTimesCompleted = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN, 3, "Uint32", 0
)
QST_SHD_2_1_SOULOFACITY_DOCKTOWN__ResetTime = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN, 302578490, "Uint64", 0
)
QST_SHD_2_1_SOULOFACITY_DOCKTOWN__RewardsAvailable = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN, 3215455463, "Boolean", False
)
QST_SHD_2_1_SOULOFACITY_DOCKTOWN__EligibleNotified = PersistencePropertyDefinition(
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN, 3821129581, "Boolean", False
)

ISLEOFTHEGODS_00_CHOICES = registered_persistence_key(1619648310)  # IsleOfTheGods_00_Choices_1619648310
ISLEOFTHEGODS_00_CHOICES_Freed_Lucanis = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 389089548, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_ReturnedBlightedFollower = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 393652444, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Neve = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 396051283, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Freed_Taash = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 764712764, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Taash = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 1158431396, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Freed_Davrin = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 1474940403, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Chose_Bellara = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 1789587008, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Freed_Neve = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 1869660478, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Davrin = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 1885778107, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Harding = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2035009497, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Freed_Emmrich = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2156074536, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Lucanis = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2400693220, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Chose_Neve = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2438401137, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Bellara = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2605951304, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Chose_Harding = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2745032273, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Chose_Davrin = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 2804938228, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Freed_Harding = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 3237531616, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_I_Love_the_Gods = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 3658555516, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_RandomFollower_Emmrich = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 3682322430, "Boolean", False
)
ISLEOFTHEGODS_00_CHOICES_Freed_Bellara = PersistencePropertyDefinition(
    ISLEOFTHEGODS_00_CHOICES, 4109623615, "Boolean", False
)

ISLEOFTHEGODS_00_CHOICES_PROPERTIES = {
    "Freed Lucanis": ISLEOFTHEGODS_00_CHOICES_Freed_Lucanis,
    "ReturnedBlightedFollower": ISLEOFTHEGODS_00_CHOICES_ReturnedBlightedFollower,
    "RandomFollower Neve": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Neve,
    "Freed Taash": ISLEOFTHEGODS_00_CHOICES_Freed_Taash,
    "RandomFollower Taash": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Taash,
    "Freed Davrin": ISLEOFTHEGODS_00_CHOICES_Freed_Davrin,
    "Chose Bellara": ISLEOFTHEGODS_00_CHOICES_Chose_Bellara,
    "Freed Neve": ISLEOFTHEGODS_00_CHOICES_Freed_Neve,
    "RandomFollower Davrin": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Davrin,
    "RandomFollower Harding": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Harding,
    "Freed Emmrich": ISLEOFTHEGODS_00_CHOICES_Freed_Emmrich,
    "RandomFollower Lucanis": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Lucanis,
    "Chose Neve": ISLEOFTHEGODS_00_CHOICES_Chose_Neve,
    "RandomFollower Bellara": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Bellara,
    "Chose Harding": ISLEOFTHEGODS_00_CHOICES_Chose_Harding,
    "Chose Davrin": ISLEOFTHEGODS_00_CHOICES_Chose_Davrin,
    "Freed Harding": ISLEOFTHEGODS_00_CHOICES_Freed_Harding,
    "I Love the Gods": ISLEOFTHEGODS_00_CHOICES_I_Love_the_Gods,
    "RandomFollower Emmrich": ISLEOFTHEGODS_00_CHOICES_RandomFollower_Emmrich,
    "Freed Bellara": ISLEOFTHEGODS_00_CHOICES_Freed_Bellara,
}

# Skills
NEVE_SKILLS = registered_persistence_key(1218516147)  # NeveSkillRDA_1218516147
NEVE_SKILLS_MaxSkills = PersistencePropertyDefinition(NEVE_SKILLS, 610427180, "Uint32", 160)
NEVE_SKILLS_SkillPoints = PersistencePropertyDefinition(NEVE_SKILLS, 2271481620, "Uint32", 0)

TAASH_SKILLS = registered_persistence_key(1151124387)  # TaashSkillRDA_1151124387
TAASH_SKILLS_MaxSkills = PersistencePropertyDefinition(TAASH_SKILLS, 610427180, "Uint32", 160)
TAASH_SKILLS_SkillPoints = PersistencePropertyDefinition(TAASH_SKILLS, 2271481620, "Uint32", 0)

HARDING_SKILLS = registered_persistence_key(1637377456)  # HardingSkillRDA_1637377456
HARDING_SKILLS_MaxSkills = PersistencePropertyDefinition(HARDING_SKILLS, 610427180, "Uint32", 160)
HARDING_SKILLS_SkillPoints = PersistencePropertyDefinition(HARDING_SKILLS, 2271481620, "Uint32", 0)

LUCANIS_SKILLS = registered_persistence_key(1969410800)  # LucanisSkillRDA_1969410800
LUCANIS_SKILLS_MaxSkills = PersistencePropertyDefinition(LUCANIS_SKILLS, 610427180, "Uint32", 160)
LUCANIS_SKILLS_SkillPoints = PersistencePropertyDefinition(LUCANIS_SKILLS, 2271481620, "Uint32", 0)

PLAYER_SKILLS = registered_persistence_key(1414565872)  # PlayerSkillRDA_1414565872
PLAYER_SKILLS_MaxSkills = PersistencePropertyDefinition(PLAYER_SKILLS, 610427180, "Uint32", 160)
PLAYER_SKILLS_SkillPoints = PersistencePropertyDefinition(PLAYER_SKILLS, 2271481620, "Uint32", 0)

DAVRIN_SKILLS = registered_persistence_key(2127371774)  # DavrinSkillRDA_2127371774
DAVRIN_SKILLS_MaxSkills = PersistencePropertyDefinition(DAVRIN_SKILLS, 610427180, "Uint32", 160)
DAVRIN_SKILLS_SkillPoints = PersistencePropertyDefinition(DAVRIN_SKILLS, 2271481620, "Uint32", 0)

EMMRICH_SKILLS = registered_persistence_key(1097328601)  # EmmrichSkillRDA_1097328601
EMMRICH_SKILLS_MaxSkills = PersistencePropertyDefinition(EMMRICH_SKILLS, 610427180, "Uint32", 160)
EMMRICH_SKILLS_SkillPoints = PersistencePropertyDefinition(EMMRICH_SKILLS, 2271481620, "Uint32", 0)

VARRIC_SKILLS = registered_persistence_key(1761904797)  # VarricSkillRDA_1761904797
VARRIC_SKILLS_MaxSkills = PersistencePropertyDefinition(VARRIC_SKILLS, 610427180, "Uint32", 160)
VARRIC_SKILLS_SkillPoints = PersistencePropertyDefinition(VARRIC_SKILLS, 2271481620, "Uint32", 0)

# FOLLOWERSKILLCHOICE_RDA_1527920706 = registered_persistence_key(1527920706) # FollowerSkillChoice_RDA_1527920706
BELLARA_SKILLS = registered_persistence_key(1567044626)  # BellaraSkillRDA_1567044626
BELLARA_SKILLS_MaxSkills = PersistencePropertyDefinition(BELLARA_SKILLS, 610427180, "Uint32", 160)
BELLARA_SKILLS_SkillPoints = PersistencePropertyDefinition(BELLARA_SKILLS, 2271481620, "Uint32", 0)

ARCHETYPE_TO_SKILL_DATA: typing.Dict[CharacterArchetype, typing.Tuple[int, PersistenceKey]] = {
    CharacterArchetype.Warrior: (3890969023, PLAYER_SKILLS),
    CharacterArchetype.Rogue: (811552702, PLAYER_SKILLS),
    CharacterArchetype.Mage: (493362280, PLAYER_SKILLS),
    CharacterArchetype.Follower_Neve: (1888629511, NEVE_SKILLS),
    CharacterArchetype.Follower_Davrin: (2132560412, DAVRIN_SKILLS),
    CharacterArchetype.Follower_Taash: (84671452, TAASH_SKILLS),
    CharacterArchetype.Follower_Bellara: (3116575990, BELLARA_SKILLS),
    CharacterArchetype.Follower_Emmrich: (802714501, EMMRICH_SKILLS),
    CharacterArchetype.Follower_Harding: (3622914845, HARDING_SKILLS),
    CharacterArchetype.Follower_Lucanis: (2545231076, LUCANIS_SKILLS),
}

SKILLS_REQUIRED_MAGE = [2231077721, 2488445902, 2488445993, 2800769157, 2800769186, 514330679, 514330450]
SKILLS_REQUIRED_ROGUE = [514330392, 2231077684, 2488445733, 2488445902, 2800769186, 2800769417, 514330547]
SKILLS_REQUIRED_WARRIOR = [514330551, 514330615, 2231077531, 2231077723, 2488445600, 2800769548, 2488445573]
