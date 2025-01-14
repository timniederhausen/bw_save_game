import json
from uuid import UUID

from importlib_resources import files

from .highlevel import *  # noqa: F401,F403
from .persistence import *  # noqa: F401,F403
from .types import *  # noqa: F401,F403

# from data files:
_FILES = files("bw_save_game.data")
ALL_ITEMS = json.loads(_FILES.joinpath("veilguard", "item_list.json").read_text("utf-8"))
ALL_CURRENCIES = json.loads(_FILES.joinpath("veilguard", "currencies.json").read_text("utf-8"))
ALL_SKILL_GRAPHS = json.loads(_FILES.joinpath("veilguard", "skill_graphs.json").read_text("utf-8"))
ALL_COLLECTIBLES = json.loads(_FILES.joinpath("veilguard", "collectibles.json").read_text("utf-8"))

# post-processing for data files:
for item in ALL_ITEMS:
    item["key"] = f"{item['name' or 'NO NAME']} ({item['id']})"
    item["guid"] = UUID(item["guid"])

SKILL_GRAPHS = {g["id"]: g for g in ALL_SKILL_GRAPHS}

COLLECTIBLES = sorted(ALL_COLLECTIBLES, key=lambda s: s["name"])
COLLECTIBLE_LABELS = [s["name"] for s in COLLECTIBLES]
