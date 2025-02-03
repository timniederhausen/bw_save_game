import json
from uuid import UUID

from importlib_resources import files

from .highlevel import *  # noqa: F401,F403
from .persistence import *  # noqa: F401,F403
from .scripts import *  # noqa: F401,F403
from .types import *  # noqa: F401,F403

_FILES = files("bw_save_game.data").joinpath("veilguard")


def _load_data_file(name: str):
    with _FILES.joinpath(f"{name}.json").open() as fp:
        return json.load(fp)


# from data files:
ALL_ITEMS = _load_data_file("items")
ALL_CURRENCIES = _load_data_file("currencies")
ALL_SKILL_GRAPHS = _load_data_file("skill_graphs")
ALL_COLLECTIBLES = _load_data_file("collectibles")
ALL_QUESTS = _load_data_file("quests")
ALL_PERSISTENCE = _load_data_file("persistence")

# post-processing for data files:
for item in ALL_ITEMS:
    item["key"] = f"{item['name'] or 'NO NAME'} ({item['id']})"
    item["guid"] = UUID(item["guid"])

SKILL_GRAPHS = {g["id"]: g for g in ALL_SKILL_GRAPHS}

COLLECTIBLES = sorted(ALL_COLLECTIBLES, key=lambda s: s["name"])
COLLECTIBLE_LABELS = [s["name"] for s in COLLECTIBLES]
