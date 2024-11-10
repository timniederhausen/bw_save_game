from binascii import hexlify, unhexlify
from dataclasses import dataclass
from uuid import UUID

# We need some type-safe way of representing the different DbObject element types
# TODO: There are other / better ways of doing this.


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

    if isinstance(obj, dict):
        return obj
    raise TypeError(f"Cannot serialize {type(obj)}")
