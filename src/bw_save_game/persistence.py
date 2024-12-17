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
    "Uint8": Long,
    "Uint16": Long,
    "Uint32": Long,
    "Uint64": Long,
    "Int8": Long,
    "Int16": Long,
    "Int32": Long,
    "Int64": Long,
}


@dataclass
class PersistenceDefinition:
    definitionId: int  # uint32
    familyId: PersistenceFamilyId


@dataclass
class PersistencePropertyDefinition:
    definition: PersistenceDefinition
    propertyId: int  # uint32
    propertyType: str


# from the .exe:
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


def get_or_create_persisted_value(definition: dict, property_id: int, property_type: str):
    key = f",{property_id}:{property_type}"

    all_props = definition["PropertyValueData"]["DefinitionProperties"]
    found_prop = None
    for prop in all_props:
        if key in prop:
            found_prop = prop
    if found_prop is None:
        found_prop = {key: PROPERTY_TYPES[property_type]()}
        all_props.append(found_prop)
    return found_prop, key
