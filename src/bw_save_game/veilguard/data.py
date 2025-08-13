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
from uuid import UUID

from importlib_resources import files

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
ALL_PERSISTENCE_DEFINITIONS = _load_data_file("persistence")
ALL_FOLLOWERS = _load_data_file("followers")
ALL_MAPS = _load_data_file("maps")
ALL_XP_THRESHOLDS = _load_data_file("xp_thresholds")
ALL_PARAMDB_KEYS = _load_data_file("paramdb_keys")
ALL_SHADER_PARAMS = _load_data_file("shader_params")

# post-processing for data files:
for item in ALL_ITEMS:
    item["key"] = f"{item['name'] or 'NO NAME'} ({item['id']})"
    item["guid"] = UUID(item["guid"])

SKILL_GRAPHS = {g["id"]: g for g in ALL_SKILL_GRAPHS}

COLLECTIBLES = sorted(ALL_COLLECTIBLES, key=lambda s: s["name"])
COLLECTIBLE_LABELS = [s["name"] for s in COLLECTIBLES]

PERSISTENCE_DEFINITIONS = {d["id"]: d for d in ALL_PERSISTENCE_DEFINITIONS}
PERSISTENCE_DEFINITION_LABELS = [d["name"] for d in ALL_PERSISTENCE_DEFINITIONS]

QUESTS = {q["id"]: q for q in ALL_QUESTS}
QUEST_LABELS = [f"{q['debug_name']} ({q['name']})" if q["debug_name"] else q["name"] for q in ALL_QUESTS]

PERSISTENCE_DEFINITION_TO_QUEST = {q["definition_id"]: q for q in ALL_QUESTS if q["definition_id"]}


def _make_transition_start_points():
    transition_start_points = set()
    for m in ALL_MAPS:
        if m["transition_start_point_name"]:
            transition_start_points.add(m["transition_start_point_name"])
        for n in m["region_transition_point_names"]:
            transition_start_points.add(n)
    return transition_start_points


TRANSITION_START_POINTS = sorted(_make_transition_start_points())

FOLLOWER_IDS = [0] + [f["id"] for f in ALL_FOLLOWERS]
FOLLOWER_LABELS = ["<empty>"] + [f["name"] for f in ALL_FOLLOWERS]

XP_THRESHOLDS = {m["name"]: m for m in ALL_XP_THRESHOLDS}

PARAMDB_KEYS = {k["raw"]["hash"]: k for k in ALL_PARAMDB_KEYS}

SHADER_PARAMS = {p["parameter_name_hash"]: p for p in ALL_SHADER_PARAMS}
