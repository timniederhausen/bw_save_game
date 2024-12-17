import json

from importlib_resources import files

from bw_save_game.persistence import (
    PersistenceDefinition,
    PersistenceFamilyId,
    PersistencePropertyDefinition,
)

# Actual game data:

KNOWN_CHARACTER_ARCHETYPES = [
    # Globals/CharacterArchetypes/...
    dict(value=2325381541, label="Watcher"),
    dict(value=267923513, label="Warrior"),
    dict(value=1486725849, label="Warden_Technique"),
    dict(value=2257715964, label="Warden_Strategy"),
    dict(value=28757921, label="Warden_Power"),
    dict(value=4003900063, label="Warden_Endurance"),
    dict(value=294481, label="Warden_Cine"),
    dict(value=3998641339, label="Warden_Challenger"),
    dict(value=3723887171, label="Warden_Art"),
    dict(value=2903517207, label="Warden_4"),
    dict(value=1837455073, label="Shadow_Evoker"),
    dict(value=1902731980, label="Rogue"),
    dict(value=3822852109, label="Ranger_03"),
    dict(value=1480587723, label="Ranger_02"),
    dict(value=3517341798, label="Ranger_01"),
    dict(value=2930410500, label="Player_RGZtest"),
    dict(value=3509394015, label="NullPlayer"),
    dict(value=240491018, label="Mage"),
    dict(value=624386075, label="Fortune"),
    dict(value=3417468734, label="Follower_Varric"),
    dict(value=4131396826, label="Follower_Taash"),
    dict(value=1887180846, label="Follower_Spite"),
    dict(value=394763556, label="Follower_Solas"),
    dict(value=1928218134, label="Follower_Neve"),
    dict(value=2143795149, label="Follower_Lucanis"),
    dict(value=1326121707, label="Follower_Harding"),
    dict(value=3734548853, label="Follower_Emmrich"),
    dict(value=2602884150, label="Follower_Davrin"),
    dict(value=116806840, label="Follower_Bellara"),
    dict(value=2714609019, label="Desperado"),
    dict(value=291152393, label="Dalish"),
    dict(value=2366407241, label="Crow"),
]

# Globals/Persistence/InquisitorGeneratorDataAsset
PAST_DA_INQUISITOR_DEF = PersistenceDefinition(1250272560, PersistenceFamilyId.Registered)
# DesignContent/PlotLogic/Global/PastDAChoices/UseReferences/Reference_Past_DA_fc
PAST_DA_SHOULD_REFERENCE_PROPERTY = PersistencePropertyDefinition(PAST_DA_INQUISITOR_DEF, 746726984, "Boolean")
PAST_DA_INQUISITOR_ROMANCE_PROPERTY = PersistencePropertyDefinition(PAST_DA_INQUISITOR_DEF, 3170937725, "Int32")
PAST_DA_INQUISITOR_ROMANCE_OPTIONS = [
    # DesignContent/PlotLogic/Global/PastDAChoices/InquisitorRomance/...
    dict(value=1, label="Blackwall"),
    dict(value=2, label="Cassandra"),
    dict(value=3, label="Cullen"),
    dict(value=4, label="Dorian"),
    dict(value=5, label="IronBull"),
    dict(value=6, label="Josephine"),
    dict(value=7, label="Sera"),
    dict(value=8, label="Solas"),
]
PAST_DA_INQUISITOR_ROMANCE_DEFAULT = 7  # Solas

# from data files:
ALL_ITEMS = json.loads(files("bw_save_game.data").joinpath("veilguard", "item_list.json").read_text("utf-8"))
ALL_CURRENCIES = json.loads(files("bw_save_game.data").joinpath("veilguard", "currencies.json").read_text("utf-8"))
