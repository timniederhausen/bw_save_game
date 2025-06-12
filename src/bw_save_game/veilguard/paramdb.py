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
