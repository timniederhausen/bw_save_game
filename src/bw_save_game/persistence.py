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
import typing
from dataclasses import dataclass
from enum import Enum

from bw_save_game.db_object import Long, to_native


class PersistenceFamilyId(Enum):
    FC_Conv = 345856344
    Orbit = 666784212
    Eco = 1933140063
    Default = 2431249405  # -1863717891,
    Registered = 2787728606  # -1507238690,
    Invalid = 3013396903  # -1281570393


PROPERTY_TYPES = {
    # TODO: this is incomplete!
    "Boolean": bool,
    "Uint8": int,
    "Uint16": int,
    "Uint32": Long,
    "Uint64": Long,
    "Int8": int,
    "Int16": int,
    "Int32": int,
    "Int64": Long,
}

_DEFAULT_PERSONA_ID = 0xC0FFEEEE
_UID_PREFIX = "uid="


@dataclass(unsafe_hash=True)
class PersistenceKey:
    version: int  # usually 7
    family: PersistenceFamilyId
    definition_id: int = 0
    last: int = None  # TODO: unknown function so far

    def __post_init__(self):
        if self.last is None:
            definition_id = self.definition_id & 0xFFFFFFFF
            if (
                (definition_id & 0x80000000) != 0
                or definition_id - 1 <= 0xFFFFFFFD
                or (definition_id & 0x40000000) != 0
            ):
                self.last = 0
            else:
                self.last = -1

    def _collect_values(self, sep):
        return f"{self.definition_id}{sep}{self.last}"

    def __str__(self):
        return f"{self.version}:{self.family.name}:{self._collect_values('|' if self.version >= 6 else '.')}"


@dataclass(unsafe_hash=True)
class EcoPersistenceKey(PersistenceKey):
    first: int = 0  # TODO: unknown function so far
    second: int = 0  # TODO: unknown function so far

    def _collect_values(self, sep):
        return f"{self.first}{sep}{self.second}{sep}{super()._collect_values(sep)}"


@dataclass(unsafe_hash=True)
class PersistenceKeyWithUniqueId(PersistenceKey):
    uid: typing.Optional[int] = None  # TODO: where do these come from?

    def _collect_values(self, sep):
        if self.uid is not None:
            return f"{_UID_PREFIX}{self.uid}{sep}{super()._collect_values(sep)}"
        return super()._collect_values(sep)


@dataclass(unsafe_hash=True)
class RegisteredPersistenceKey(PersistenceKeyWithUniqueId):
    persona_id: int = _DEFAULT_PERSONA_ID

    def _collect_values(self, sep):
        return f"{self.persona_id}{sep}{super()._collect_values(sep)}"


def parse_persistence_key_string(key_str: str):
    colon_separated = key_str.split(":", 3)
    if len(colon_separated) < 3:
        version = 5
        family = PersistenceFamilyId[colon_separated[0]]
        family_data = colon_separated[1]
    else:
        version = int(colon_separated[0])
        family = PersistenceFamilyId[colon_separated[1]]
        family_data = colon_separated[2]

    # XXX: This is a bit convoluted to avoid having to create too many temporary objects
    values_sep = "|" if version >= 6 else "."
    values = family_data.split(values_sep, 13)
    values_len = len(values)
    values_index = 0

    # family-specific values:
    if family == PersistenceFamilyId.Eco:
        first = 0
        second = 0
        if values_index < values_len:
            first = int(values[values_index])
            values_index += 1
        if values_index < values_len:
            second = int(values[values_index])
            values_index += 1

    if family == PersistenceFamilyId.Registered:
        persona = 0
        uid = None

        if values_index < values_len:
            persona = int(values[values_index])
            values_index += 1

        if values_index < values_len and values[values_index].startswith(_UID_PREFIX):
            uid = int(values[values_index][len(_UID_PREFIX) :])
            values_index += 1

    # common values
    definition_id = 0
    third = 0
    if values_index < values_len:
        definition_id = int(values[values_index])
        values_index += 1

    if values_index < values_len:
        third = int(values[values_index])
        values_index += 1

    if family == PersistenceFamilyId.Eco:
        return EcoPersistenceKey(version, family, definition_id, third, first, second)
    if family == PersistenceFamilyId.Registered:
        return RegisteredPersistenceKey(version, family, definition_id, third, uid, persona)
    return PersistenceKey(version, family, definition_id, third)


def registered_persistence_key(definition_id: int) -> RegisteredPersistenceKey:
    return RegisteredPersistenceKey(version=7, family=PersistenceFamilyId.Registered, definition_id=definition_id)


@dataclass(frozen=True)
class PersistencePropertyDefinition:
    key: PersistenceKey
    id: int  # uint32
    type: str
    default: object


def get_persisted_value(def_instance: dict, property_id: int, property_type: str, default_value):
    prop_name = f",{property_id}:{property_type}"

    all_props = def_instance["PropertyValueData"]["DefinitionProperties"]
    found_prop = None
    for prop in all_props:
        if prop_name in prop:
            found_prop = prop
    if found_prop is None:
        return default_value
    return to_native(found_prop[prop_name])


def set_persisted_value(def_instance: dict, property_id: int, property_type: str, value):
    prop_name = f",{property_id}:{property_type}"

    all_props = def_instance["PropertyValueData"]["DefinitionProperties"]
    for prop in all_props:
        if prop_name in prop:
            prop[prop_name] = PROPERTY_TYPES[property_type](value)
            return
    all_props.append({prop_name: PROPERTY_TYPES[property_type](value)})


def get_or_create_persisted_value(def_instance: dict, property_id: int, property_type: str, default_value):
    prop_name = f",{property_id}:{property_type}"

    all_props = def_instance["PropertyValueData"]["DefinitionProperties"]
    found_prop = None
    for prop in all_props:
        if prop_name in prop:
            found_prop = prop
    if found_prop is None:
        found_prop = {prop_name: PROPERTY_TYPES[property_type](default_value)}
        all_props.append(found_prop)
    return found_prop, prop_name
