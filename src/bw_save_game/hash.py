def frostbite_fnv1(data: bytes):
    assert isinstance(data, bytes)
    h = 5381
    for byte in data:
        h = (((33 * h) & 0xFFFFFFFF) ^ byte) & 0xFFFFFFFF
    return h


def frostbite_fnv1_lowercase(data: bytes):
    """Return the FNV1 32bit hash for data.

    >>> frostbite_fnv1_lowercase(b"Characters/Generic/Universal/Makeup/Blush_Makeup/HF_MAK_Blush_12A_Mask")
    3828825916
    """
    assert isinstance(data, bytes)
    h = 5381
    for byte in data:
        v = (byte + 32 * ((byte - 65) & 0xFF <= 0x19)) & 0xFF
        h = (((33 * h) & 0xFFFFFFFF) ^ v) & 0xFFFFFFFF
    return h
