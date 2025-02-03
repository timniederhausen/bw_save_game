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
from io import BytesIO
from pathlib import Path

from bw_save_game import dumps, loads, read_save_from_reader, write_save_to_writer
from bw_save_game.db_object import from_raw_dict, to_raw_dict

_DATA_DIR = Path(__file__).parent / "data"
_ACTUAL_SAVE_GAMES = [
    _DATA_DIR / "correct_romance_1.csav",
    _DATA_DIR / "correct_romance_2.csav",
    _DATA_DIR / "wrong_romance_1.csav",
    _DATA_DIR / "wrong_romance_2.csav",
]


def test_actual_save_games_binary():
    for actual_save_path in _ACTUAL_SAVE_GAMES:
        with open(actual_save_path, "rb") as f:
            meta, data = read_save_from_reader(f)

        intermediary = BytesIO()
        write_save_to_writer(intermediary, meta, data)
        intermediary.seek(0)
        meta2, data2 = read_save_from_reader(intermediary)

        assert meta == meta2
        assert data == data2


def test_actual_save_games_python():
    for actual_save_path in _ACTUAL_SAVE_GAMES:
        with open(actual_save_path, "rb") as f:
            meta, data = read_save_from_reader(f)

        meta_py = loads(meta)
        data_py = loads(data)

        meta2 = dumps(meta_py)
        data2 = dumps(data_py)

        assert meta == meta2
        assert data == data2

        assert meta_py == loads(meta2)
        assert data_py == loads(data2)


def test_actual_save_games_json():
    for actual_save_path in _ACTUAL_SAVE_GAMES:
        with open(actual_save_path, "rb") as f:
            meta, data = read_save_from_reader(f)

        meta_py = loads(meta)
        data_py = loads(data)

        meta_py_json = json.dumps(meta_py, default=to_raw_dict)
        data_py_json = json.dumps(data_py, default=to_raw_dict)

        meta_py = json.loads(meta_py_json, object_hook=from_raw_dict)
        data_py = json.loads(data_py_json, object_hook=from_raw_dict)

        meta2 = dumps(meta_py)
        data2 = dumps(data_py)

        assert meta == meta2
        assert data == data2

        assert meta_py == loads(meta2)
        assert data_py == loads(data2)
