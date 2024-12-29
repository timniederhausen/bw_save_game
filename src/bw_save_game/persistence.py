from dataclasses import dataclass
from enum import Enum

from bw_save_game.db_object import Long


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
    "Uint32": int,
    "Uint64": Long,
    "Int8": int,
    "Int16": int,
    "Int32": int,
    "Int64": Long,
}


@dataclass
class PersistenceDefinition:
    definition_id: int  # uint32
    family_id: PersistenceFamilyId


@dataclass
class PersistencePropertyDefinition:
    definition: PersistenceDefinition
    id: int  # uint32
    type: str
    default: object


def parse_key_string(key: str):
    dots = key.split(":", 3)
    if len(dots) < 3:
        version = 5
    else:
        version = int(dots[0])
        dots = dots[1:]

    family, family_data = dots
    family_data = family_data.split("|" if version >= 6 else ".", 13)
    return version, family, family_data


def format_key_string(family: str, family_data: list, version: int = 7):
    return f"{version}:{family}:{('|' if version >= 6 else '.').join(family_data)}"


def get_persisted_value(definition: dict, property_id: int, property_type: str, default_value: object):
    prop_name = f",{property_id}:{property_type}"

    all_props = definition["PropertyValueData"]["DefinitionProperties"]
    found_prop = None
    for prop in all_props:
        if prop_name in prop:
            found_prop = prop
    if found_prop is None:
        return PROPERTY_TYPES[property_type](default_value)
    return found_prop[prop_name]


def get_or_create_persisted_value(definition: dict, property_id: int, property_type: str, default_value: object):
    prop_name = f",{property_id}:{property_type}"

    all_props = definition["PropertyValueData"]["DefinitionProperties"]
    found_prop = None
    for prop in all_props:
        if prop_name in prop:
            found_prop = prop
    if found_prop is None:
        found_prop = {prop_name: PROPERTY_TYPES[property_type](default_value)}
        all_props.append(found_prop)
    return found_prop, prop_name
