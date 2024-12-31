from bw_save_game.persistence import (
    EcoPersistenceKey,
    PersistenceFamilyId,
    RegisteredPersistenceKey,
    parse_persistence_key_string,
    registered_persistence_key,
)


def test_key_serialization_with_uid():
    key_str = "7:Registered:3237998318|uid=122476741|1522966120|0"
    key = parse_persistence_key_string(key_str)

    assert isinstance(key, RegisteredPersistenceKey)
    assert key.version == 7
    assert key.family == PersistenceFamilyId.Registered
    assert key.persona_id == 3237998318
    assert key.definition_id == 1522966120
    assert key.uid == 122476741

    assert str(key) == key_str


def test_key_serialization_without_uid():
    key_str = "7:Registered:3237998318|1910846056|0"
    key = parse_persistence_key_string(key_str)

    assert isinstance(key, RegisteredPersistenceKey)
    assert key.version == 7
    assert key.family == PersistenceFamilyId.Registered
    assert key.persona_id == 3237998318
    assert key.definition_id == 1910846056
    assert key.uid is None

    assert str(key) == key_str


def test_key_serialization_eco():
    key_str = "7:Eco:0|743239629|652756416|4166880828"
    key = parse_persistence_key_string(key_str)

    assert isinstance(key, EcoPersistenceKey)
    assert key.version == 7
    assert key.family == PersistenceFamilyId.Eco
    assert key.first == 0
    assert key.second == 743239629
    assert key.definition_id == 652756416
    assert key.last == 4166880828


def test_static_keys():
    assert str(registered_persistence_key(1647819227)) == "7:Registered:3237998318|1647819227|0"
