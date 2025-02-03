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
from binascii import hexlify, unhexlify
from dataclasses import dataclass
from uuid import UUID

# We could represent most of these as basic Python objects (int, bytes, ...)
# but would lose the original type in the process (e.g. was it Integer or Long?).
# Since we strive for bit-for-bit identical output with the game itself we can't afford to lose that type info.
# TODO: Are there better ways of doing this?


@dataclass
class DbObjectId:
    value: bytes  # 12 bytes


@dataclass
class DbSHA1:
    value: bytes  # 20 bytes


@dataclass
class DbAttachment:
    hash: bytes  # 20 bytes


@dataclass
class DbTimestamp:
    value: int  # 8 bytes


@dataclass
class DbRecordId:
    extentId: int
    pageId: int
    slotId: int


@dataclass
class Vector4D:
    x: float
    y: float
    z: float
    w: float


@dataclass
class Matrix4x4:
    row1: Vector4D
    row2: Vector4D
    row3: Vector4D
    row4: Vector4D


@dataclass
class DbTimespan:
    length: int


@dataclass
class Long:
    value: int  # 8 bytes


@dataclass
class VarInt:
    value: int  # 8 bytes


@dataclass
class Double:
    value: float  # 8 bytes


def from_raw_dict(obj):
    typ = obj.get("@type")
    if not typ:
        return obj

    if typ == DbObjectId.__name__:
        return DbObjectId(unhexlify(obj["value"]))
    if typ == DbSHA1.__name__:
        return DbSHA1(unhexlify(obj["value"]))
    if typ == DbAttachment.__name__:
        return DbAttachment(unhexlify(obj["value"]))
    if typ == DbTimestamp.__name__:
        return DbTimestamp(obj["value"])
    if typ == DbRecordId.__name__:
        return DbRecordId(obj["extentId"], obj["pageId"], obj["slotId"])
    if typ == Vector4D.__name__:
        return Vector4D(obj["x"], obj["y"], obj["z"], obj["w"])
    if typ == Matrix4x4.__name__:
        return Matrix4x4(obj["row1"], obj["row2"], obj["row3"], obj["row4"])
    if typ == DbTimespan.__name__:
        return DbTimespan(obj["length"])
    if typ == UUID.__name__:
        return UUID(hex=obj["value"])
    if typ == Long.__name__:
        return Long(obj["value"])
    if typ == VarInt.__name__:
        return VarInt(obj["value"])
    if typ == Double.__name__:
        return Double(obj["value"])


def to_raw_dict(obj):
    if isinstance(obj, DbObjectId):
        return {"@type": DbObjectId.__name__, "value": hexlify(obj.value)}
    if isinstance(obj, DbSHA1):
        return {"@type": DbSHA1.__name__, "value": hexlify(obj.value)}
    if isinstance(obj, DbAttachment):
        return {"@type": DbAttachment.__name__, "value": hexlify(obj.hash)}
    if isinstance(obj, DbTimestamp):
        return {"@type": DbTimestamp.__name__, "value": obj.value}
    if isinstance(obj, DbRecordId):
        return {
            "@type": DbRecordId.__name__,
            "extentId": obj.extentId,
            "pageId": obj.pageId,
            "slotId": obj.slotId,
        }
    if isinstance(obj, Vector4D):
        return {
            "@type": Vector4D.__name__,
            "x": obj.x,
            "y": obj.y,
            "z": obj.z,
            "w": obj.w,
        }
    if isinstance(obj, Matrix4x4):
        return {
            "@type": Matrix4x4.__name__,
            "rows": [obj.row1, obj.row2, obj.row3, obj.row4],
        }
    if isinstance(obj, DbTimespan):
        return {"@type": DbTimespan.__name__, "value": obj.length}
    if isinstance(obj, UUID):
        return {"@type": UUID.__name__, "value": obj.hex}
    if isinstance(obj, Long):
        return {"@type": Long.__name__, "value": obj.value}
    if isinstance(obj, VarInt):
        return {"@type": VarInt.__name__, "value": obj.value}
    if isinstance(obj, Double):
        return {"@type": Double.__name__, "value": obj.value}

    if isinstance(obj, dict):
        return obj
    raise TypeError(f"Cannot serialize {type(obj)}")


def to_native(obj):
    if isinstance(obj, DbObjectId):
        return obj.value
    if isinstance(obj, DbSHA1):
        return obj.value
    if isinstance(obj, DbAttachment):
        return obj.hash
    if isinstance(obj, DbTimestamp):
        return obj.value
    if isinstance(obj, DbTimespan):
        return obj.length
    if isinstance(obj, Long):
        return obj.value
    if isinstance(obj, VarInt):
        return obj.value
    if isinstance(obj, Double):
        return obj.value
    return obj
