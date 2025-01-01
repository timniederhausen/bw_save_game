# bw-save-game - BioWare save game tools
# Copyright (C) 2024 Tim Niederhausen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Website: https://github.com/timniederhausen/bw_save_game
# -*- coding: utf-8 -*-
import json
import typing
from enum import IntEnum
from uuid import UUID

from importlib_resources import files

from bw_save_game import (
    __version__,
    dumps,
    loads,
    read_save_from_reader,
    write_save_to_writer,
)
from bw_save_game.db_object import Long, from_raw_dict, to_native, to_raw_dict
from bw_save_game.persistence import (
    PersistenceKey,
    PersistencePropertyDefinition,
    get_persisted_value,
    parse_persistence_key_string,
    registered_persistence_key,
)


class ItemAttachmentType(IntEnum):
    None_ = 0
    Character = 1
    Item = 2
    ItemGuid = 3


# https://stackoverflow.com/a/53791136
ItemAttachmentType.None_._name_ = "None"
ItemAttachmentType._member_map_["None"] = ItemAttachmentType.None_


class ItemAttachmentSlot(IntEnum):
    Preview = 0
    Item_Helm = 1
    Item_Body = 2
    Item_Ring1 = 3
    Item_Ring2 = 4
    Item_Amulet = 5
    Item_Accessory1 = 6
    Item_Accessory2 = 7
    Item_Accessory3 = 8
    Item_WeaponMH = 9
    Item_WeaponOH = 10
    Item_Weapon2H = 11
    Rune_Root = 12
    Rune_Base1 = 13
    Rune_Base2 = 14
    Rune_Equip1 = 15
    Rune_Equip2 = 16
    Rune_Equip3 = 17
    Rune_Equip4 = 18
    Rune_Equip5 = 19
    Rune_Equip6 = 20
    Rune_Equip7 = 21
    Rune_Equip8 = 22
    Rune_Equip9 = 23
    Rune_Equip10 = 24
    Rune_Equip12 = 25
    Rune_Equip_13 = 26
    Rune_Equip14 = 27
    Ability_Player1 = 28
    Ability_Player2 = 29
    Ability_Player3 = 30
    Ability_Follower1 = 31
    Ability_Follower2 = 32
    Ability_Ultimate = 33
    Ability_Dodge = 34
    Ability_Jump = 35
    Ability_Proc1 = 36
    Ability_Proc2 = 37
    CasualWear = 38
    Stats_Chargen = 39
    Stats_Class = 40
    Stats_Skills = 41
    Item_LyriumDagger = 42
    Misc_Flashlight = 43
    Misc_Temp1 = 44
    Misc_Temp2 = 45
    Misc_Temp3 = 46
    Misc_Temp4 = 47
    Weapon_1_Primary = 48
    Weapon_1_Secondary = 49
    Weapon_2_Primary = 50
    Weapon_2_Secondary = 51
    Weapon_Defend = 52
    Weapon_Swap = 53
    Weapon_Deathblow = 54
    ADS = 55
    ADS_Primary = 56
    ADS_Secondary = 57
    TargetLock = 58
    TargetLock_Forward = 59
    TargetLock_Back = 60
    Command_Ping = 61
    Command_Radial = 62
    Command_Follower1 = 63
    Command_Follower2 = 64
    MountedWeapon = 65
    DefaultAppearance = 66
    Quiver = 67
    Hair = 68
    PartSlot_Set = 69
    SpecialAppearance = 70
    Rune_Root2 = 71
    Undergarment = 72
    Count = 73
    Dynamic = -2
    None_ = -1


# https://stackoverflow.com/a/53791136
ItemAttachmentSlot.None_._name_ = "None"
ItemAttachmentSlot._member_map_["None"] = ItemAttachmentSlot.None_


class LootRarity(IntEnum):
    Rarity_None = 0
    Rarity_Common = 1
    Rarity_Uncommon = 2
    Rarity_Rare = 3
    Rarity_Epic = 4
    Rarity_Legendary = 5
    Rarity_Ancient = 6
    Rarity_Max = 7


KNOWN_CHARACTER_ARCHETYPES = {
    # Globals/CharacterArchetypes/...
    2325381541: "Watcher",
    267923513: "Warrior",
    1486725849: "Warden_Technique",
    2257715964: "Warden_Strategy",
    28757921: "Warden_Power",
    4003900063: "Warden_Endurance",
    294481: "Warden_Cine",
    3998641339: "Warden_Challenger",
    3723887171: "Warden_Art",
    2903517207: "Warden_4",
    1837455073: "Shadow_Evoker",
    1902731980: "Rogue",
    3822852109: "Ranger_03",
    1480587723: "Ranger_02",
    3517341798: "Ranger_01",
    2930410500: "Player_RGZtest",
    3509394015: "NullPlayer",
    240491018: "Mage",
    624386075: "Fortune",
    3417468734: "Follower_Varric",
    4131396826: "Follower_Taash",
    1887180846: "Follower_Spite",
    394763556: "Follower_Solas",
    1928218134: "Follower_Neve",
    2143795149: "Follower_Lucanis",
    1326121707: "Follower_Harding",
    3734548853: "Follower_Emmrich",
    2602884150: "Follower_Davrin",
    116806840: "Follower_Bellara",
    2714609019: "Desperado",
    291152393: "Dalish",
    2366407241: "Crow",
}
KNOWN_CHARACTER_ARCHETYPE_VALUES = list(KNOWN_CHARACTER_ARCHETYPES.keys())
KNOWN_CHARACTER_ARCHETYPE_LABELS = list(KNOWN_CHARACTER_ARCHETYPES.values())

ITEM_ATTACHMENT_SLOT_NAMES = [e.name for e in ItemAttachmentSlot]
ITEM_ATTACHMENT_SLOT_VALUES = [e.value for e in ItemAttachmentSlot]

LOOT_RARITY_NAMES = [e.name for e in LootRarity]
LOOT_RARITY_VALUES = [e.value for e in LootRarity]

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
CHARACTER_GENERATOR_VOICE_TONE = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 1419752156, "Int32", 1)
CHARACTER_GENERATOR_LINEAGE = PersistencePropertyDefinition(CHARACTER_GENERATOR_DEF, 1491933783, "Int32", 1)
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
    0: "GreyWardens",
    1: "VeilJumpers",
    2: "ShadowDragons",
    3: "LordsOfFortune",
    4: "TheMournWatch",
    5: "AntivanCrows",
}
CHARACTER_GENERATOR_FACTION_VALUES = list(CHARACTER_GENERATOR_FACTIONS.keys())
CHARACTER_GENERATOR_FACTION_LABELS = list(CHARACTER_GENERATOR_FACTIONS.values())

# Globals/Persistence/InquisitorGeneratorDataAsset
PAST_DA_INQUISITOR_DEF = registered_persistence_key(1250272560)
# DesignContent/PlotLogic/Global/PastDAChoices/UseReferences/Reference_Past_DA_fc
PAST_DA_SHOULD_REFERENCE_PROPERTY = PersistencePropertyDefinition(PAST_DA_INQUISITOR_DEF, 746726984, "Boolean", False)
PAST_DA_INQUISITOR_ROMANCE_PROPERTY = PersistencePropertyDefinition(PAST_DA_INQUISITOR_DEF, 2643758781, "Int32", 8)
PAST_DA_INQUISITOR_ROMANCES = {
    # DesignContent/PlotLogic/Global/PastDAChoices/InquisitorRomance/...
    1: "Blackwall",
    2: "Cassandra",
    3: "Cullen",
    4: "Dorian",
    5: "IronBull",
    6: "Josephine",
    7: "Sera",
    8: "Solas",
}
PAST_DA_INQUISITOR_ROMANCE_VALUES = list(PAST_DA_INQUISITOR_ROMANCES.keys())
PAST_DA_INQUISITOR_ROMANCE_LABELS = list(PAST_DA_INQUISITOR_ROMANCES.values())
PAST_DA_INQUISITOR_ROMANCE_DEFAULT_INDEX = 7  # Solas

# Romance properties
ROMANCE_NEVE = registered_persistence_key(2022350065)  # ROMANCE_NEVE
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

ROMANCE_DAVRIN = registered_persistence_key(1805940062)  # ROMANCE_DAVRIN
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

ROMANCE_BELLARA = registered_persistence_key(1628101232)  # ROMANCE_BELLARA
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

ROMANCE_TAASH = registered_persistence_key(1100432818)  # ROMANCE_TAASH
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

ROMANCE_EMMRICH = registered_persistence_key(1377196124)  # ROMANCE_EMMRICH
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

# from data files:
ALL_ITEMS = json.loads(files("bw_save_game.data").joinpath("veilguard", "item_list.json").read_text("utf-8"))
ALL_CURRENCIES = json.loads(files("bw_save_game.data").joinpath("veilguard", "currencies.json").read_text("utf-8"))

# post-processing for data files:
for item in ALL_ITEMS:
    item["key"] = f"{item['name' or 'NO NAME']} ({item['id']})"
    item["guid"] = UUID(item["guid"])


class VeilguardSaveGame(object):
    def __init__(self, meta: dict, data: dict):
        self.meta = meta
        self.data = data

        self._persistence_key_to_instance = {}  # type: typing.Dict[PersistenceKey, dict]

        self.refresh_derived_data()

    @staticmethod
    def from_file(fp):
        m, d = read_save_from_reader(fp)
        m = loads(m)
        d = loads(d)
        return VeilguardSaveGame(m, d)

    def to_file(self, fp):
        m = dumps(self.meta)
        d = dumps(self.data)
        write_save_to_writer(fp, m, d)

    @staticmethod
    def from_json(fp):
        root = json.load(fp, object_hook=from_raw_dict)

        m = root["meta"]
        d = root["data"]

        return VeilguardSaveGame(m, d)

    def to_json(self, fp):
        root = dict(meta=self.meta, data=self.data, exporter=dict(version=__version__, format=1))
        json.dump(root, fp, ensure_ascii=False, indent=2, default=to_raw_dict)

    def get_client_rpg_extents(self, loadpass=0) -> dict:
        for c in self.data["client"]["contributors"]:
            if c["name"] == "RPGPlayerExtent" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No client RPGPlayerExtent with loadpass {loadpass}")

    def get_server_rpg_extents(self, loadpass=0) -> dict:
        for c in self.data["server"]["contributors"]:
            if c["name"] == "RPGPlayerExtent" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No server RPGPlayerExtent with loadpass {loadpass}")

    def get_client_difficulty(self, loadpass=0) -> dict:
        for c in self.data["client"]["contributors"]:
            if c["name"] == "DifficultyOptions" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No client DifficultyOptions with loadpass {loadpass}")

    def get_currencies(self):
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("currencies", []), first_extent.setdefault("discoveredCurrencies", [])

    def get_items(self) -> list:
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("items", [])

    def get_registered_persistence(self, loadpass=0) -> dict:
        for c in self.data["server"]["contributors"]:
            if c["name"] == "RegisteredPersistence" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No RegisteredPersistence with loadpass {loadpass}")

    def get_persistence_instances(self) -> typing.List[dict]:
        return self.get_registered_persistence()["RegisteredData"]["Persistence"]

    def get_persistence_instance(self, key: PersistenceKey) -> typing.Optional[dict]:
        return self._persistence_key_to_instance.get(key)

    def get_persistence_instance_by_id(self, definition_id: int) -> typing.Optional[dict]:
        for def_instance in self.get_persistence_instances():
            if to_native(def_instance["DefinitionId"]) == definition_id:
                return def_instance
        return None

    def get_persistence_property(self, prop: PersistencePropertyDefinition):
        instance = self.get_persistence_instance(prop.key)
        if instance is None:
            return None
        return get_persisted_value(instance, prop.id, prop.type, prop.default)

    def refresh_derived_data(self):
        self._persistence_key_to_instance.clear()
        for def_instance in self.get_persistence_instances():
            key = parse_persistence_key_string(def_instance["Key"])
            self._persistence_key_to_instance[key] = def_instance

    def replace_character_archetype(self, old_archetype: int, new_archetype: int):
        self.meta["archetype"] = new_archetype

        client_rpg_player = self.get_client_rpg_extents(loadpass=0)
        for transmogSlot in client_rpg_player["transmogSlots"]:
            if to_native(transmogSlot["id"]) == old_archetype:
                transmogSlot["id"] = new_archetype

        server_rpg_player = self.get_server_rpg_extents(loadpass=0)
        server_rpg_player["archetype"] = new_archetype
        for item in server_rpg_player["items"]:
            if "parent" not in item:
                continue
            parent = item["parent"]
            if "parentArchetype" not in parent:
                continue
            if to_native(parent["parentArchetype"]["id"]) == old_archetype:
                parent["parentArchetype"]["id"] = Long(new_archetype)


def deconstruct_item_attachment(item: dict) -> tuple[ItemAttachmentType, None | int | UUID, None | str]:
    parent = item.get("parent")
    attach_slot = item.get("attachSlot")
    if not parent:
        return ItemAttachmentType.None_, None, attach_slot
    attachment_type = parent.get("attachmentType")
    if attachment_type == "Character":
        parent_archetype = parent.get("parentArchetype")
        if not parent_archetype or "id" not in parent_archetype:
            raise ValueError("No parentArchetype for Character attachment")
        return ItemAttachmentType.Character, to_native(parent_archetype["id"]), attach_slot
    if attachment_type == "ItemGuid":
        parent_guid = parent.get("parentGuid")
        if not parent_guid:
            raise ValueError("No parentGuid for ItemGuid attachment")
        return ItemAttachmentType.ItemGuid, parent_guid, attach_slot
    # TODO: What's the Item type?
    raise ValueError(f"Unsupported ItemAttachmentType type {attachment_type}")


def construct_item_attachment(item: dict, typ: ItemAttachmentType, parent: int | UUID = None, attach_slot: str = None):
    if typ == ItemAttachmentType.None_:
        item.pop("parent", None)
        item.pop("attachSlot", None)
        return
    if typ == ItemAttachmentType.Character:
        item["parent"] = dict(attachmentType="Character", parentArchetype=dict(id=Long(parent)))
    elif typ == ItemAttachmentType.ItemGuid:
        item["parent"] = dict(attachmentType="ItemGuid", parentGuid=parent)
    else:
        raise ValueError(f"Unsupported ItemAttachmentType type {typ}")

    if attach_slot is not None:
        item["attachSlot"] = attach_slot
    else:
        item.pop("attachSlot", None)


def item_attachment_to_string(item: dict):
    typ, parent, attach_slot = deconstruct_item_attachment(item)
    if parent:
        if typ == ItemAttachmentType.Character:
            parent = KNOWN_CHARACTER_ARCHETYPES[parent]
        return f"{typ.name} {parent}: {attach_slot}"
    return "Not Attached"
