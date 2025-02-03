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
import ctypes
import gzip
import typing
import zlib

MAGIC = b"<!--DAS"
CURRENT_FORMAT_VERSION = 2
CRC32_STARTING_VALUE = 0xA018471F


class SaveHeader(ctypes.Structure):
    _pack_ = 8
    _fields_ = [
        # Names come from a possibly unused JSON version of this header that
        # Dragon Age The Veilguard.exe can write.
        ("formatversion", ctypes.c_uint32),
        ("data_checksum", ctypes.c_uint32),
        ("data_length", ctypes.c_uint64),
        ("data_compressed_length", ctypes.c_uint64),
        ("meta_length", ctypes.c_uint64),
        ("meta_compressed_length", ctypes.c_uint64),
        ("meta_checksum", ctypes.c_uint32),
    ]


class SaveLoadingError(ValueError):
    pass


def read_save_from_reader(reader: typing.BinaryIO, expected_save_type: bytes = b"C", strict=True):
    magic = reader.read(7)
    if magic != MAGIC:
        raise SaveLoadingError(f"Invalid magic bytes: {magic} != {MAGIC}")

    save_type = reader.read(1)
    if expected_save_type is not None and save_type != expected_save_type:
        raise SaveLoadingError(f"Invalid save type: ${save_type} != {expected_save_type}")

    header = SaveHeader.from_buffer_copy(reader.read(ctypes.sizeof(SaveHeader)))
    if header.formatversion != CURRENT_FORMAT_VERSION:
        raise SaveLoadingError(f"Invalid format version: {header.formatversion} != {CURRENT_FORMAT_VERSION}")

    meta = reader.read(header.meta_compressed_length)
    data = reader.read(header.data_compressed_length)

    # If we want to be sure, verify the integrity of our compressed data
    if strict:
        actual_meta_checksum = zlib.crc32(meta, CRC32_STARTING_VALUE)
        actual_data_checksum = zlib.crc32(data, CRC32_STARTING_VALUE)

        if header.meta_checksum != actual_meta_checksum:
            raise SaveLoadingError(f"Invalid meta checksum: {header.meta_checksum} != {actual_meta_checksum}")
        if header.data_checksum != actual_data_checksum:
            raise SaveLoadingError(f"Invalid data checksum: {header.data_checksum} != {actual_data_checksum}")

    # all good, so now we just have to decompress
    meta = gzip.decompress(meta)
    data = gzip.decompress(data)

    assert len(meta) == header.meta_length
    assert len(data) == header.data_length

    return meta, data


def write_save_to_writer(
    writer: typing.BinaryIO,
    meta: typing.ByteString,
    data: typing.ByteString,
    save_type: bytes = b"C",
):
    header = SaveHeader()
    header.formatversion = CURRENT_FORMAT_VERSION
    header.data_length = len(data)
    header.meta_length = len(meta)

    meta = gzip.compress(meta)
    data = gzip.compress(data)

    header.data_checksum = zlib.crc32(data, CRC32_STARTING_VALUE)
    header.data_compressed_length = len(data)
    header.meta_checksum = zlib.crc32(meta, CRC32_STARTING_VALUE)
    header.meta_compressed_length = len(meta)

    writer.write(MAGIC)
    writer.write(save_type)
    writer.write(bytes(header))
    writer.write(meta)
    writer.write(data)
