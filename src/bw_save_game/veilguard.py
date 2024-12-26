import json
from enum import IntEnum
from uuid import UUID

from importlib_resources import files

from bw_save_game.db_object import Long, to_native
from bw_save_game.persistence import (
    PersistenceDefinition,
    PersistenceFamilyId,
    PersistencePropertyDefinition,
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

# Globals/Persistence/InquisitorGeneratorDataAsset
PAST_DA_INQUISITOR_DEF = PersistenceDefinition(1250272560, PersistenceFamilyId.Registered)
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

# from data files:
ALL_ITEMS = json.loads(files("bw_save_game.data").joinpath("veilguard", "item_list.json").read_text("utf-8"))
ALL_CURRENCIES = json.loads(files("bw_save_game.data").joinpath("veilguard", "currencies.json").read_text("utf-8"))


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
        return f"{typ.name} {parent}: {attach_slot}"
    return "Not Attached"
