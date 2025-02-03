from enum import IntEnum, IntFlag


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

ITEM_ATTACHMENT_SLOT_NAMES = [e.name for e in ItemAttachmentSlot]
ITEM_ATTACHMENT_SLOT_VALUES = [e.value for e in ItemAttachmentSlot]


class CharacterGender(IntEnum):
    Male = 0
    Female = 1
    NonBinary = 2


CHARACTER_GENDER_LABELS = [e.name for e in CharacterGender]
CHARACTER_GENDER_VALUES = [e.value for e in CharacterGender]


class LootRarity(IntEnum):
    Rarity_None = 0
    Rarity_Common = 1
    Rarity_Uncommon = 2
    Rarity_Rare = 3
    Rarity_Epic = 4
    Rarity_Legendary = 5
    Rarity_Ancient = 6
    Rarity_Max = 7


LOOT_RARITY_NAMES = [e.name for e in LootRarity]
LOOT_RARITY_VALUES = [e.value for e in LootRarity]


class CollectibleSetFlag(IntFlag):
    NoFlags = 0
    IsCollected = 1 << 1
    IsDiscovered = 1 << 2
    IsDisabled = 1 << 3
    IsViewed = 1 << 4
    IsSecret = 1 << 5


class BWFollowerStateFlag(IntFlag):
    NoFlags = 0
    Unlocked = 1
    Available = 2
    WasInLastQuest = 4
    IsHardened = 8
    IsHeroic = 16
    IsWaiting = 32
    IsDead = 64


class EcoQuestRegisteredStateFlags(IntFlag):
    Unset = 0
    Eligible = 1
    Completed = 2
    MissionUnlocked = 4
    Expired = 8
    Cheated = 128


class CharacterArchetype(IntEnum):
    Fortune = 624386075
    Follower_Solas = 394763556
    Follower_Davrin = 2602884150
    Follower_Varric = 3417468734
    Rogue = 1902731980
    Warrior = 267923513
    Follower_Lucanis = 2143795149
    Desperado = 2714609019
    Follower_Taash = 4131396826
    Warden_Cine = 294481
    Ranger_03 = 3822852109
    Ranger_02 = 1480587723
    Follower_Bellara = 116806840
    Dalish = 291152393
    Warden_Strategy = 2257715964
    Mage = 240491018
    Warden_4 = 2903517207
    Follower_Neve = 1928218134
    Warden_Challenger = 3998641339
    Crow = 2366407241
    Warden_Endurance = 4003900063
    Shadow_Evoker = 1837455073
    Ranger_01 = 3517341798
    Watcher = 2325381541
    Warden_Art = 3723887171
    Follower_Harding = 1326121707
    NullPlayer = 3509394015
    Player_RGZtest = 2930410500
    Warden_Power = 28757921
    Warden_Technique = 1486725849
    Follower_Spite = 1887180846
    Follower_Emmrich = 3734548853


VISIBLE_CHARACTER_ARCHETYPES = {
    624386075,
    394763556,
    2602884150,
    3417468734,
    1902731980,
    267923513,
    2143795149,
    2714609019,
    4131396826,
    294481,
    3822852109,
    1480587723,
    116806840,
    291152393,
    2257715964,
    240491018,
    2903517207,
    1928218134,
    3998641339,
    2366407241,
    4003900063,
    1837455073,
    3517341798,
    2325381541,
    3723887171,
    1326121707,
    3509394015,
    2930410500,
    28757921,
    1486725849,
    1887180846,
    3734548853,
}

KNOWN_CHARACTER_ARCHETYPE_VALUES = [e.value for e in CharacterArchetype]
KNOWN_CHARACTER_ARCHETYPE_LABELS = [e.name for e in CharacterArchetype]
