import json
import time
import typing
from collections import defaultdict
from uuid import UUID

from bw_save_game import (
    __version__,
    dumps,
    loads,
    read_save_from_reader,
    write_save_to_writer,
)
from bw_save_game.db_object import Long, from_raw_dict, to_native, to_raw_dict
from bw_save_game.persistence import (
    PersistenceKey,
    PersistencePropertyDefinition,
    get_persisted_value,
    parse_persistence_key_string,
    set_persisted_value,
)
from bw_save_game.veilguard.data import XP_THRESHOLDS
from bw_save_game.veilguard.persistence import (
    DEFAULTXPBUCKET_XP,
    PLAYER_SKILLS,
    PROGRESSION_XP_XP,
    SKILLS_REQUIRED_MAGE,
    SKILLS_REQUIRED_ROGUE,
    SKILLS_REQUIRED_WARRIOR,
    CharacterArchetype,
    PROGRESSION_CurrentLevel,
)
from bw_save_game.veilguard.types import (
    EcoQuestRegisteredStateFlags,
    ItemAttachmentType,
)


class VeilguardSaveGame(object):
    def __init__(self, meta: dict, data: dict):
        self.meta = meta
        self.data = data

        self._definition_id_to_instances, self._persistence_key_to_instance = self.build_persistence_instance_map()

    @staticmethod
    def from_file(fp):
        m, d = read_save_from_reader(fp)
        m = loads(m)
        d = loads(d)
        return VeilguardSaveGame(m, d)

    def to_file(self, fp):
        m = dumps(self.meta)
        d = dumps(self.data)
        write_save_to_writer(fp, m, d)

    @staticmethod
    def from_json(fp):
        root = json.load(fp, object_hook=from_raw_dict)

        m = root["meta"]
        d = root["data"]

        return VeilguardSaveGame(m, d)

    def to_json(self, fp):
        root = dict(meta=self.meta, data=self.data, exporter=dict(version=__version__, format=1))
        json.dump(root, fp, ensure_ascii=False, indent=2, default=to_raw_dict)

    def get_client_rpg_extents(self, loadpass=0) -> dict:
        for c in self.data["client"]["contributors"]:
            if c["name"] == "RPGPlayerExtent" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No client RPGPlayerExtent with loadpass {loadpass}")

    def get_server_rpg_extents(self, loadpass=0) -> dict:
        for c in self.data["server"]["contributors"]:
            if c["name"] == "RPGPlayerExtent" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No server RPGPlayerExtent with loadpass {loadpass}")

    def get_client_difficulty(self, loadpass=0) -> dict:
        for c in self.data["client"]["contributors"]:
            if c["name"] == "DifficultyOptions" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No client DifficultyOptions with loadpass {loadpass}")

    def get_currencies(self):
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("currencies", []), first_extent.setdefault("discoveredCurrencies", [])

    def get_party(self):
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("party", [])

    def get_items(self) -> list:
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("items", [])

    def get_registered_persistence(self, loadpass: int = 0) -> dict:
        for c in self.data["server"]["contributors"]:
            if c["name"] == "RegisteredPersistence" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No RegisteredPersistence with loadpass {loadpass}")

    def get_persistence_instances(self) -> typing.List[dict]:
        return self.get_registered_persistence()["RegisteredData"]["Persistence"]

    def set_persistence_instances(self, new_persistence: typing.List[dict]):
        self.get_registered_persistence()["RegisteredData"]["Persistence"] = new_persistence
        self._definition_id_to_instances, self._persistence_key_to_instance = self.build_persistence_instance_map()

    def get_persistence_instance(self, key: PersistenceKey) -> typing.Optional[dict]:
        return self._persistence_key_to_instance.get(key)

    def get_persistence_instances_by_id(self, definition_id: int) -> typing.List[dict]:
        return self._definition_id_to_instances[definition_id]

    def make_persistence_instance(self, key: PersistenceKey) -> dict:
        new_instance = dict(
            DefinitionId=Long(key.definition_id),
            PersistenceVersion=12,
            Key=str(key),
            CreationTime=Long(time.time_ns() // 1000000000),
            PropertyValueData=dict(DefinitionProperties=[]),
        )
        self.get_persistence_instances().append(new_instance)
        self._persistence_key_to_instance[key] = new_instance
        self._definition_id_to_instances[key.definition_id].append(new_instance)
        return new_instance

    def get_persistence_property(self, prop: PersistencePropertyDefinition):
        instance = self.get_persistence_instance(prop.key)
        if instance is None:
            return prop.default
        return get_persisted_value(instance, prop.id, prop.type, prop.default)

    def set_persistence_property(self, prop: PersistencePropertyDefinition, value):
        instance = self.get_persistence_instance(prop.key)
        if instance is None:
            instance = self.make_persistence_instance(prop.key)
        set_persisted_value(instance, prop.id, prop.type, value)

    def build_persistence_instance_map(self):
        all_instances = self.get_persistence_instances()

        definition_id_to_instances = defaultdict(list)
        for instance in all_instances:
            definition_id = to_native(instance["DefinitionId"])
            definition_id_to_instances[definition_id].append(instance)

        key_to_instance = {parse_persistence_key_string(instance["Key"]): instance for instance in all_instances}
        return definition_id_to_instances, key_to_instance

    def replace_character_archetype(self, old_archetype: int, new_archetype: int):
        if old_archetype == new_archetype:
            return

        self.meta["archetype"] = new_archetype  # for save preview

        client_rpg_player = self.get_client_rpg_extents(loadpass=0)
        for transmogSlot in client_rpg_player["transmogSlots"]:
            if to_native(transmogSlot["id"]) == old_archetype:
                transmogSlot["id"] = new_archetype

        server_rpg_player = self.get_server_rpg_extents(loadpass=0)
        server_rpg_player["archetype"] = new_archetype
        for item in server_rpg_player["items"]:
            if "parent" not in item:
                continue
            parent = item["parent"]
            if "parentArchetype" not in parent:
                continue
            if to_native(parent["parentArchetype"]["id"]) == old_archetype:
                parent["parentArchetype"]["id"] = Long(new_archetype)

        if new_archetype == CharacterArchetype.Mage:
            skills_to_add = SKILLS_REQUIRED_MAGE
        elif new_archetype == CharacterArchetype.Rogue:
            skills_to_add = SKILLS_REQUIRED_ROGUE
        elif new_archetype == CharacterArchetype.Warrior:
            skills_to_add = SKILLS_REQUIRED_WARRIOR
        else:
            skills_to_add = []

        for property_id in skills_to_add:
            prop = PersistencePropertyDefinition(PLAYER_SKILLS, property_id, "Boolean", False)
            self.set_persistence_property(prop, True)

    def change_level(self, new_level: int):
        self.set_persistence_property(PROGRESSION_CurrentLevel, new_level)
        self.meta["projdata"]["level"] = new_level  # for save preview

        min_xp_for_level = 0
        for bucket in XP_THRESHOLDS["DefaultProgressionMap"]["level_thresholds"]:
            if bucket["level"] == new_level:
                min_xp_for_level = bucket["value"]

        cur_xp = self.get_persistence_property(PROGRESSION_XP_XP)
        if cur_xp < min_xp_for_level:
            self.set_persistence_property(PROGRESSION_XP_XP, min_xp_for_level)

        cur_xp = self.get_persistence_property(DEFAULTXPBUCKET_XP)
        if cur_xp < min_xp_for_level:
            self.set_persistence_property(DEFAULTXPBUCKET_XP, min_xp_for_level)


def deconstruct_item_attachment(item: dict) -> tuple[ItemAttachmentType, None | int | UUID, None | str]:
    parent = item.get("parent")
    attach_slot = item.get("attachSlot")
    if not parent:
        return ItemAttachmentType.None_, None, attach_slot
    attachment_type = parent.get("attachmentType")
    if attachment_type == "Character":
        parent_archetype = parent.get("parentArchetype")
        if not parent_archetype or "id" not in parent_archetype:
            raise ValueError("No parentArchetype for Character attachment")
        return ItemAttachmentType.Character, to_native(parent_archetype["id"]), attach_slot
    if attachment_type == "ItemGuid":
        parent_guid = parent.get("parentGuid")
        if not parent_guid:
            raise ValueError("No parentGuid for ItemGuid attachment")
        return ItemAttachmentType.ItemGuid, parent_guid, attach_slot
    # TODO: What's the Item type?
    raise ValueError(f"Unsupported ItemAttachmentType type {attachment_type}")


def construct_item_attachment(item: dict, typ: ItemAttachmentType, parent: int | UUID = None, attach_slot: str = None):
    if typ == ItemAttachmentType.None_:
        item.pop("parent", None)
        item.pop("attachSlot", None)
        return
    if typ == ItemAttachmentType.Character:
        item["parent"] = dict(attachmentType="Character", parentArchetype=dict(id=Long(parent)))
    elif typ == ItemAttachmentType.ItemGuid:
        item["parent"] = dict(attachmentType="ItemGuid", parentGuid=parent)
    else:
        raise ValueError(f"Unsupported ItemAttachmentType type {typ}")

    if attach_slot is not None:
        item["attachSlot"] = attach_slot
    else:
        item.pop("attachSlot", None)


def item_attachment_to_string(item: dict):
    typ, parent, attach_slot = deconstruct_item_attachment(item)
    if parent:
        if typ == ItemAttachmentType.Character:
            parent = CharacterArchetype(parent).name
        return f"{typ.name} {parent}: {attach_slot}"
    return "Not Attached"


def force_complete_quest(save_game: VeilguardSaveGame, quest_key: PersistenceKey):
    save_game.set_persistence_property(
        PersistencePropertyDefinition(quest_key, 1, "Uint8", 0),
        EcoQuestRegisteredStateFlags.Eligible | EcoQuestRegisteredStateFlags.Completed,
    )
    save_game.set_persistence_property(PersistencePropertyDefinition(quest_key, 3, "Uint32", 0), 1)
