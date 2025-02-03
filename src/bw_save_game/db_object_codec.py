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
from decimal import Decimal
from io import BytesIO
from uuid import UUID

from .db_object import (
    DbAttachment,
    DbObjectId,
    DbRecordId,
    DbSHA1,
    DbTimespan,
    DbTimestamp,
    Double,
    Long,
    Matrix4x4,
    VarInt,
    Vector4D,
)


class UnknownSerializerError(TypeError):
    def __init__(self, key, value):
        super(UnknownSerializerError, self).__init__(
            f"Unable to serialize: key '{key}' value: {value} type: {type(value)}"
        )


# Thankfully they left that enum-to-string in the shipping build!
TYPE_Eoo = 0x0
TYPE_Array = 0x1
TYPE_Object = 0x2
TYPE_HomoArray = 0x3
TYPE_Null = 0x4
TYPE_ObjectId = 0x5
TYPE_Bool = 0x6
TYPE_String = 0x7
TYPE_Integer = 0x8
TYPE_Long = 0x9
TYPE_VarInt = 0xA
TYPE_Float = 0xB
TYPE_Double = 0xC
TYPE_Timestamp = 0xD
TYPE_RecordId = 0xE
TYPE_GUID = 0xF
TYPE_SHA1 = 0x10
TYPE_Matrix44 = 0x11
TYPE_Vector4 = 0x12
TYPE_Blob = 0x13
TYPE_Attachment = 0x14
TYPE_Timespan = 0x15
TYPE_InternalMax = 0x1F
TYPE_Anonymous = 0x80

# Cache all the struct formats we might use.
int32_struct = struct.Struct("<i")
uint32_struct = struct.Struct("<I")
byte_struct = struct.Struct("<B")
int64_struct = struct.Struct("<q")
uint64_struct = struct.Struct("<Q")
int_char_struct = struct.Struct("<ib")
float_struct = struct.Struct("<f")
double_struct = struct.Struct("<d")
record_id_struct = struct.Struct("<HHH")
vec4_struct = struct.Struct("<ffff")


def decode_varint_leb128(data, base):
    """Reads the next few bytes in a file as LEB128/7bit encoding and returns an integer"""
    result, shift = 0, 0
    while True:
        byte = byte_struct.unpack(data[base : base + 1])[0]
        base += 1
        result |= (byte & 0x7F) << shift
        if byte >> 7 == 0:
            return base, result
        shift += 7


def encode_varint_leb128(value):
    result = bytearray()
    while True:
        slice = value & 0x7F
        value >>= 7

        if value:
            slice |= 0x80

        result.append(slice)
        if not value:
            break
    return result


# https://stackoverflow.com/a/49659900
def zigzag(x: int) -> int:
    return x << 1 if x >= 0 else (-x - 1) << 1 | 1


def zagzig(x: int) -> int:
    assert x >= 0
    sign = x & 1
    return -(x >> 1) - 1 if sign else x >> 1


def encode_string(value):
    value = value.encode("utf-8")
    length = len(value)
    return encode_varint_leb128(length + 1) + struct.pack("<%dsb" % (length,), value, 0)


def encode_cstring(value):
    if not isinstance(value, bytes):
        value = str(value).encode("utf-8")
    if b"\x00" in value:
        raise ValueError("Element names may not include NUL bytes.")
        # A NUL byte is used to delimit our string, accepting one would cause
        # our string to terminate early.
    return value + b"\x00"


def encode_binary(value):
    length = len(value)
    return encode_varint_leb128(length) + value


def encode_prefix(element_type, name: str):
    if not name:
        return byte_struct.pack(element_type | TYPE_Anonymous)
    return byte_struct.pack(element_type) + encode_cstring(name)


def encode_value(name, value, buf, on_unknown=None):
    if isinstance(value, bool):
        buf.write(encode_prefix(TYPE_Bool, name))
        buf.write(byte_struct.pack(value))
    elif isinstance(value, int):
        # Auto-upgrade ints to Long if we need to.
        if value < -(2**31) or value >= 2**32:
            buf.write(encode_prefix(TYPE_Long, name))
            buf.write(uint64_struct.pack(value & (2**64 - 1)))
        else:
            buf.write(encode_prefix(TYPE_Integer, name))
            buf.write(uint32_struct.pack(value & (2**32 - 1)))
    elif isinstance(value, float):
        buf.write(encode_prefix(TYPE_Float, name))
        buf.write(float_struct.pack(value))
    elif isinstance(value, str):
        buf.write(encode_prefix(TYPE_String, name))
        buf.write(encode_string(value))
    elif isinstance(value, bytes):
        buf.write(encode_prefix(TYPE_Blob, name))
        buf.write(encode_binary(value))
    elif isinstance(value, UUID):
        buf.write(encode_prefix(TYPE_GUID, name))
        buf.write(value.bytes_le)
    elif isinstance(value, DbObjectId):
        buf.write(encode_prefix(TYPE_ObjectId, name))
        assert len(value.value) == 12
        buf.write(value.value)
    elif isinstance(value, DbSHA1):
        buf.write(encode_prefix(TYPE_SHA1, name))
        assert len(value.value) == 20
        buf.write(value.value)
    elif isinstance(value, DbAttachment):
        buf.write(encode_prefix(TYPE_Attachment, name))
        assert len(value.hash) == 20
        buf.write(value.hash)
    elif isinstance(value, DbTimestamp):
        buf.write(encode_prefix(TYPE_Timestamp, name))
        buf.write(uint64_struct.pack(value.value))
    elif isinstance(value, DbRecordId):
        buf.write(encode_prefix(TYPE_RecordId, name))
        buf.write(record_id_struct.pack(value.extentId, value.pageId, value.slotId))
    elif isinstance(value, Vector4D):
        buf.write(encode_prefix(TYPE_Vector4, name))
        buf.write(vec4_struct.pack(value.x, value.y, value.z, value.w))
    elif isinstance(value, Matrix4x4):
        buf.write(encode_prefix(TYPE_Matrix44, name))
        buf.write(vec4_struct.pack(value.row1.x, value.row1.y, value.row1.z, value.row1.w))
        buf.write(vec4_struct.pack(value.row2.x, value.row2.y, value.row2.z, value.row2.w))
        buf.write(vec4_struct.pack(value.row3.x, value.row3.y, value.row3.z, value.row3.w))
        buf.write(vec4_struct.pack(value.row4.x, value.row4.y, value.row4.z, value.row4.w))
    elif isinstance(value, DbTimespan):
        buf.write(encode_prefix(TYPE_Timespan, name))
        buf.write(encode_varint_leb128(zigzag(value.length)))
    elif value is None:
        buf.write(encode_prefix(TYPE_Null, name))
    elif isinstance(value, dict):
        buf.write(encode_prefix(TYPE_Object, name))
        buf.write(encode_document(value, on_unknown=on_unknown))
    elif isinstance(value, list) or isinstance(value, tuple):
        buf.write(encode_prefix(TYPE_Array, name))
        buf.write(encode_array(value, on_unknown=on_unknown))
    elif isinstance(value, Decimal):
        buf.write(encode_prefix(TYPE_Double, name))
        buf.write(double_struct.pack(float(value)))
    elif isinstance(value, Long):
        buf.write(encode_prefix(TYPE_Long, name))
        buf.write(uint64_struct.pack(value.value))
    elif isinstance(value, VarInt):
        buf.write(encode_prefix(TYPE_VarInt, name))
        buf.write(encode_varint_leb128(zigzag(value.value)))
    elif isinstance(value, Double):
        buf.write(encode_prefix(TYPE_Double, name))
        buf.write(double_struct.pack(value.value))
    else:
        if on_unknown is not None:
            encode_value(name, on_unknown(value), buf, on_unknown)
        else:
            raise UnknownSerializerError(name, value)


def encode_document(obj, on_unknown=None, with_envelope=True):
    buf = BytesIO()
    for name in iter(obj):
        value = obj[name]
        encode_value(name, value, buf, on_unknown)
    encoded = buf.getvalue()
    encoded_size = len(encoded)
    if with_envelope:
        return encode_varint_leb128(encoded_size + 1) + encoded + byte_struct.pack(TYPE_Eoo)
    return encoded


def encode_array(array, on_unknown=None):
    buf = BytesIO()
    for i in range(0, len(array)):
        value = array[i]
        encode_value(None, value, buf, on_unknown)
    encoded = buf.getvalue()
    encoded_size = len(encoded)
    return encode_varint_leb128(encoded_size + 1) + struct.pack("<%dsb" % (encoded_size,), encoded, 0)


def decode_value(base: int, data: bytes):
    header = byte_struct.unpack(data[base : base + 1])[0]
    element_type = header & TYPE_InternalMax

    decode_name = (header & TYPE_Anonymous) == 0
    if decode_name:
        base_after_name = data.index(0, base + 1) + 1
        name = data[base + 1 : base_after_name - 1].decode("utf-8")
        base = base_after_name
    else:
        name = None
        base = base + 1

    if element_type == TYPE_Array:
        base, value = decode_document(data, base, as_array=True)
    elif element_type == TYPE_Object:
        base, value = decode_document(data, base)
    elif element_type == TYPE_Null:
        value = None

    elif element_type == TYPE_ObjectId:
        value = DbObjectId(data[base : base + 12])
        base = base + 12

    elif element_type == TYPE_Bool:
        value = bool(byte_struct.unpack(data[base : base + 1])[0])
        base += 1

    elif element_type == TYPE_String:
        base, length = decode_varint_leb128(data, base)
        value = data[base : base + length - 1]
        value = value.decode("utf-8")
        base += length

    elif element_type == TYPE_Integer:
        value = uint32_struct.unpack(data[base : base + 4])[0]
        base += 4

    elif element_type == TYPE_Long:
        value = uint64_struct.unpack(data[base : base + 8])[0]
        base += 8
        value = Long(value)

    elif element_type == TYPE_VarInt:
        base, value = decode_varint_leb128(data, base)
        value = VarInt(zagzig(value))

    elif element_type == TYPE_Float:
        value = float_struct.unpack(data[base : base + 4])[0]
        base += 4

    elif element_type == TYPE_Double:
        value = double_struct.unpack(data[base : base + 8])[0]
        base += 8
        value = Double(value)

    elif element_type == TYPE_Timestamp:
        value = uint64_struct.unpack(data[base : base + 8])[0]
        base += 8
        value = DbTimestamp(value)

    elif element_type == TYPE_RecordId:
        value = record_id_struct.unpack(data[base : base + 4])[0]
        base += 6
        value = DbRecordId(*value)

    elif element_type == TYPE_GUID:
        value = UUID(bytes_le=data[base : base + 16])
        base += 16

    elif element_type == TYPE_SHA1:
        value = DbSHA1(data[base : base + 20])
        base += 20

    elif element_type == TYPE_Vector4:
        value = vec4_struct.unpack(data[base : base + 16])
        base += 16
        value = Vector4D(*value)

    elif element_type == TYPE_Matrix44:
        row1 = vec4_struct.unpack(data[base : base + 16])
        base += 16
        row2 = vec4_struct.unpack(data[base : base + 16])
        base += 16
        row3 = vec4_struct.unpack(data[base : base + 16])
        base += 16
        row4 = vec4_struct.unpack(data[base : base + 16])
        base += 16

        value = Matrix4x4(Vector4D(*row1), Vector4D(*row2), Vector4D(*row3), Vector4D(*row4))

    elif element_type == TYPE_Blob:
        base, length = decode_varint_leb128(data, base)
        value = data[base : base + length]
        base += length

    elif element_type == TYPE_Attachment:
        value = DbAttachment(data[base : base + 20])
        base += 20

    elif element_type == TYPE_Timespan:
        base, value = decode_varint_leb128(data, base)
        value = DbTimespan(zagzig(value))

    else:
        raise ValueError(f"Unhandled DbObject type {element_type} at {base}")

    return base, name, value


def decode_document(data, base, as_array=False, with_envelope=True):
    if with_envelope:
        base, length = decode_varint_leb128(data, base)
        end_point = base + length
        if data[end_point - 1] not in ("\0", 0):
            raise ValueError("missing null-terminator in document")
    else:
        end_point = len(data)

    retval = [] if as_array else {}
    while base < end_point - 1:
        base, name, value = decode_value(base, data)
        if as_array:
            retval.append(value)
        else:
            retval[name] = value

    return end_point, retval


def dumps(obj, on_unknown=None):
    return encode_document({None: obj}, with_envelope=False, on_unknown=on_unknown)


def loads(data):
    return decode_document(data, 0, with_envelope=False)[1][None]
