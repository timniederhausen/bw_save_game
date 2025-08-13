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
import struct

from bw_save_game.veilguard.data import PARAMDB_KEYS

PARAMDB_STRUCT = struct.Struct("<IHHQ")
VEC4_PARAMDB_STRUCT = struct.Struct("<ffff")


class ParamDbKey(object):
    def __init__(self, handle: int, type_index: int, size: int, hash_value: int):
        self.handle = handle
        self.type_index = type_index
        self.size = size
        self.hash = hash_value

    def __str__(self):
        try:
            known_key = PARAMDB_KEYS[self.hash]
            return f"ParamDb: {known_key["name"]} ({known_key["type_name"]})"
        except KeyError:
            return f"ParamDb: handle={self.handle} type={self.type_index} size={self.size} hash={self.hash}"


def parse_ParamDbKeyData(wrapper) -> ParamDbKey:
    vec4_repr = VEC4_PARAMDB_STRUCT.pack(*wrapper["data"])
    return ParamDbKey(*PARAMDB_STRUCT.unpack(vec4_repr))
