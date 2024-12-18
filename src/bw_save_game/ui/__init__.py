#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import sys
import typing  # noqa: F401
from uuid import UUID

from imgui_bundle import imgui, immapp

from bw_save_game import (
    __version__,
    dumps,
    loads,
    read_save_from_reader,
    write_save_to_writer,
)
from bw_save_game.db_object import Long, from_raw_dict, to_native, to_raw_dict
from bw_save_game.persistence import (
    PersistencePropertyDefinition,
    get_or_create_persisted_value,
)
from bw_save_game.ui.editors import (
    show_json_editor,
    show_key_value_options_editor,
    show_raw_key_value_editor,
    show_raw_value_editor,
    show_uuid_editor,
)
from bw_save_game.ui.utils import ask_for_file_to_open, ask_for_file_to_save, show_error
from bw_save_game.ui.widgets import (
    clear_unused_retained_data,
    show_searchable_combo_box,
)
from bw_save_game.veilguard import (
    ALL_CURRENCIES,
    ALL_ITEMS,
    CLASS_KEYBINDING_LABELS,
    CLASS_KEYBINDING_VALUES,
    DIFFICULTY_COMBAT_PRESET_LABELS,
    DIFFICULTY_COMBAT_PRESET_VALUES,
    DIFFICULTY_EXPLORATION_PRESET_LABELS,
    DIFFICULTY_EXPLORATION_PRESET_VALUES,
    ITEM_ATTACHMENT_SLOT_NAMES,
    KNOWN_CHARACTER_ARCHETYPE_LABELS,
    KNOWN_CHARACTER_ARCHETYPE_VALUES,
    PAST_DA_INQUISITOR_ROMANCE_DEFAULT_INDEX,
    PAST_DA_INQUISITOR_ROMANCE_LABELS,
    PAST_DA_INQUISITOR_ROMANCE_PROPERTY,
    PAST_DA_INQUISITOR_ROMANCE_VALUES,
    PAST_DA_SHOULD_REFERENCE_PROPERTY,
    ItemAttachmentType,
    construct_item_attachment,
    deconstruct_item_attachment,
    item_attachment_to_string,
)


class State(object):
    def __init__(self):
        # UI state
        self.show_app_about = False

        # loaded save game
        self.active_filename = None  # type: typing.Optional[str]
        self.active_meta = None  # type: typing.Optional[dict]
        self.active_data = None  # type: typing.Optional[dict]

        self.item_list = ALL_ITEMS

        self.item_id_to_index = {}
        for i, item in enumerate(self.item_list):
            item["key"] = f"{item['name' or 'NO NAME']} ({item['id']})"
            item["guid"] = UUID(item["guid"])
            self.item_id_to_index[item["id"]] = i
        self.item_keys = [item["key"] for item in self.item_list]

        self.currencies = ALL_CURRENCIES

    def has_content(self):
        return self.active_meta is not None and self.active_data is not None

    def load(self, filename: str):
        try:
            with open(filename, "rb") as f:
                m, d = read_save_from_reader(f)
            m = loads(m)
            d = loads(d)
        except Exception as e:
            show_error(f"Cannot load {filename}: {repr(e)}")
            return

        self.active_filename = filename
        self.active_meta = m
        self.active_data = d

    def save(self, filename: str):
        try:
            m = dumps(self.active_meta)
            d = dumps(self.active_data)
            with open(filename, "wb") as f:
                write_save_to_writer(f, m, d)
        except Exception as e:
            show_error(f"Cannot save {filename}: {repr(e)}")
            return
        self.active_filename = filename

    def import_json(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                doc = json.load(f, object_hook=from_raw_dict)
        except Exception as e:
            show_error(f"Cannot load {filename}: {repr(e)}")
            return

        try:
            m = doc["meta"]
            d = doc["data"]
        except KeyError as e:
            show_error(f"{filename} doesn't have the correct JSON structure.\n{e} is missing.")
            return

        self.active_filename = None
        self.active_meta = m
        self.active_data = d

    def export_json(self, filename: str):
        try:
            root = dict(meta=self.active_meta, data=self.active_data, exporter=dict(version=__version__, format=1))
            with open(filename, "w", encoding="utf-8") as f:
                # TODO: do we want sort keys on?
                json.dump(root, f, ensure_ascii=False, indent=2, default=to_raw_dict)
        except Exception as e:
            show_error(f"Cannot save {filename}: {repr(e)}")
            return

    # Easy data accessors
    def get_client_rpg_extents(self, loadpass=0) -> dict:
        for c in self.active_data["client"]["contributors"]:
            if c["name"] == "RPGPlayerExtent" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No client RPGPlayerExtent with loadpass {loadpass}")

    def get_server_rpg_extents(self, loadpass=0) -> dict:
        for c in self.active_data["server"]["contributors"]:
            if c["name"] == "RPGPlayerExtent" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No server RPGPlayerExtent with loadpass {loadpass}")

    def get_client_difficulty(self, loadpass=0) -> dict:
        for c in self.active_data["client"]["contributors"]:
            if c["name"] == "DifficultyOptions" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No client DifficultyOptions with loadpass {loadpass}")

    def get_currencies(self):
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("currencies", []), first_extent.setdefault("discoveredCurrencies", [])

    def get_items(self) -> list:
        first_extent = self.get_server_rpg_extents(0)
        return first_extent.setdefault("items", [])

    def get_registered_persistence(self, loadpass=0) -> dict:
        for c in self.active_data["server"]["contributors"]:
            if c["name"] == "RegisteredPersistence" and to_native(c["loadpass"]) == loadpass:
                return c["data"]
        raise ValueError(f"No RegisteredPersistence with loadpass {loadpass}")

    def get_persisted_definitions(self) -> typing.List[dict]:
        return self.get_registered_persistence()["RegisteredData"]["Persistence"]

    def get_persisted_definition(self, definition_id: int) -> typing.Optional[dict]:
        for family in self.get_persisted_definitions():
            if to_native(family["DefinitionId"]) == definition_id:
                return family
        return None


def show_app_about(state: State):
    if not state.show_app_about:
        return  # nothing to do

    is_expand, is_show_app_about = imgui.begin(
        name="About BWSaveGameEditor",
        p_open=state.show_app_about,
        flags=imgui.WindowFlags_.always_auto_resize | imgui.WindowFlags_.no_collapse,
    )
    if is_show_app_about is not None:
        state.show_app_about = is_show_app_about
    if is_expand:
        imgui.text("BWSaveGameEditor " + __version__)
        imgui.separator()
        imgui.text("By Tim and mons.")
        imgui.text("BWSaveGameEditor is licensed under GNU General Public License v3.0.")
        imgui.separator()
        imgui.text("Using ImGui v" + imgui.get_version())
    imgui.end()


def show_main_menu_bar(state: State):
    if not imgui.begin_main_menu_bar():
        return

    if imgui.begin_menu("File", True):
        clicked, selected = imgui.menu_item(label="Open", shortcut="Ctrl+O", p_selected=False)
        if clicked:
            path = ask_for_file_to_open("Open Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav")
            if path:
                state.load(path)

        clicked, selected = imgui.menu_item(label="Import JSON", shortcut="", p_selected=False)
        if clicked:
            path = ask_for_file_to_open("Open JSON Save Game", "JSON document (*.json)|*.json")
            if path:
                state.import_json(path)

        clicked, selected = imgui.menu_item(
            label="Save", shortcut="Ctrl+S", p_selected=False, enabled=state.active_filename is not None
        )
        if clicked and state.active_filename:
            state.save(state.active_filename)

        clicked, selected = imgui.menu_item(
            label="Save As...", shortcut="", p_selected=False, enabled=state.has_content()
        )
        if clicked:
            path = ask_for_file_to_save("Write Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav")
            if path:
                state.save(path)

        clicked, selected = imgui.menu_item(
            label="Export JSON", shortcut="", p_selected=False, enabled=state.has_content()
        )
        if clicked:
            path = ask_for_file_to_save("Export JSON save game", "JSON document (*.json)|*.json")
            if path:
                state.export_json(path)

        clicked, selected = imgui.menu_item("Quit", "Cmd+Q", False, True)
        if clicked:
            sys.exit(0)

        imgui.end_menu()

    if imgui.begin_menu("Help", True):
        clicked, state.show_app_about = imgui.menu_item(
            label="About BWSaveGameEditor", shortcut="", p_selected=state.show_app_about
        )
        imgui.end_menu()

    imgui.end_main_menu_bar()


def show_item_id_editor(state: State, obj):
    index = state.item_id_to_index.get(to_native(obj["itemDataId"]))
    if index is not None:
        # https://github.com/ocornut/imgui/issues/623
        imgui.push_item_width(-1)
        changed, new_index = show_searchable_combo_box("##itemDataId", state.item_keys, index)
        imgui.pop_item_width()

        if changed:
            data = state.item_list[new_index]
            obj["itemDataId"] = Long(data["id"])
            obj["dataGuid"] = data["guid"]
    else:
        imgui.text(f"Unsupported item: {to_native(obj["itemDataId"])}")
        # oh well
        # show_simple_value_editor(obj, "itemDataId")


def show_persisted_value_editor(state: State, label: str, prop: PersistencePropertyDefinition):
    definition = state.get_persisted_definition(prop.definition.definitionId)
    if not definition:
        return

    obj, key = get_or_create_persisted_value(definition, prop.propertyId, prop.propertyType)
    show_raw_key_value_editor(obj, key, label)


def show_persisted_value_options_editor(
    state: State,
    label: str,
    prop: PersistencePropertyDefinition,
    option_values: list,
    option_names: list[str],
    default_option_index: int = 0,
):
    definition = state.get_persisted_definition(prop.definition.definitionId)
    if not definition:
        return

    obj, key = get_or_create_persisted_value(definition, prop.propertyId, prop.propertyType)
    show_key_value_options_editor(label, obj, key, option_values, option_names, default_option_index)


def show_editor_raw_data(state: State):
    if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in state.active_meta:
            imgui.push_id(key)
            show_raw_key_value_editor(state.active_meta, key)
            imgui.pop_id()
    imgui.separator()
    if imgui.collapsing_header("Content", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in state.active_data.keys():
            imgui.push_id(key)
            show_raw_key_value_editor(state.active_data, key)
            imgui.pop_id()


def show_item_attachment_editor(state: State, item: dict):
    preview_value = item_attachment_to_string(item)

    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)
    is_open = imgui.begin_combo("##itemAttachment", preview_value, imgui.ComboFlags_.height_largest)
    if not is_open:
        imgui.pop_item_width()
        return

    typ, parent, attach_slot = deconstruct_item_attachment(item)

    if imgui.radio_button("None", typ == ItemAttachmentType.None_):
        construct_item_attachment(item, ItemAttachmentType.None_)
    imgui.same_line()
    if imgui.radio_button("Character", typ == ItemAttachmentType.Character):
        construct_item_attachment(item, ItemAttachmentType.Character, KNOWN_CHARACTER_ARCHETYPE_VALUES[0], attach_slot)
    imgui.same_line()
    if imgui.radio_button("ItemGuid", typ == ItemAttachmentType.ItemGuid):
        construct_item_attachment(item, ItemAttachmentType.ItemGuid, UUID(int=0), attach_slot)

    if typ == ItemAttachmentType.None_:
        imgui.end_combo()
        imgui.pop_item_width()
        return

    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)

    if typ == ItemAttachmentType.Character:
        try:
            current_item = KNOWN_CHARACTER_ARCHETYPE_VALUES.index(parent)
            imgui.text("Character archetype:")
            changed, new_item = imgui.list_box("##Character", current_item, KNOWN_CHARACTER_ARCHETYPE_LABELS)
            if changed:
                construct_item_attachment(
                    item, ItemAttachmentType.Character, KNOWN_CHARACTER_ARCHETYPE_VALUES[new_item], attach_slot
                )
        except ValueError:
            imgui.text_colored((1.0, 0.0, 0.0, 1.0), f"Unknown archetype {parent}")
    if typ == ItemAttachmentType.ItemGuid:
        imgui.text("Item UUID:")
        changed, new_value = show_uuid_editor("##ItemGuid", parent)
        if changed:
            construct_item_attachment(item, ItemAttachmentType.ItemGuid, new_value, attach_slot)

    try:
        current_item = ITEM_ATTACHMENT_SLOT_NAMES.index(attach_slot or "None")
        imgui.text("Attach slot:")
        changed, new_item = imgui.list_box("##AttachSlot", current_item, ITEM_ATTACHMENT_SLOT_NAMES)
        if changed:
            construct_item_attachment(item, typ, parent, ITEM_ATTACHMENT_SLOT_NAMES[new_item])
    except ValueError:
        imgui.text_colored((1.0, 0.0, 0.0, 1.0), f"Unknown attach slot {attach_slot}")

    imgui.pop_item_width()
    imgui.end_combo()
    imgui.pop_item_width()


def show_editor_inventories(state: State):
    items = state.get_items()

    imgui.text(f"Number of items: {len(items)}")
    if imgui.begin_table("Items", 5, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        imgui.table_setup_column("Item")
        imgui.table_setup_column("Attached to")
        imgui.table_setup_column("Amount")
        imgui.table_setup_column("Rarity")
        imgui.table_headers_row()
        for i, item in enumerate(items):
            imgui.push_id(i)
            imgui.table_next_row()
            imgui.table_next_column()
            show_item_id_editor(state, item)
            imgui.table_next_column()
            show_item_attachment_editor(state, item)
            imgui.table_next_column()
            if "stackCount" in item:
                show_raw_value_editor(item, "stackCount")
            else:
                imgui.text("1")
            imgui.table_next_column()
            imgui.text(str(item.get("rarity")))
            imgui.pop_id()
        imgui.end_table()


def show_currency_editor(state: State):
    if not imgui.begin_table("Currencies", 3, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        return

    imgui.table_setup_column("Currency")
    imgui.table_setup_column("Discovered?")
    imgui.table_setup_column("Amount")
    imgui.table_headers_row()
    currencies, discovered_currencies = state.get_currencies()
    for currency_def in state.currencies:
        imgui.push_id(currency_def["id"])
        imgui.table_next_row()
        imgui.table_next_column()
        imgui.text(f"{currency_def['name']} ({currency_def['id']})")
        imgui.table_next_column()
        changed, new_value = imgui.checkbox("##discovered?", currency_def["id"] in discovered_currencies)
        if changed:
            if new_value:
                discovered_currencies.append(currency_def["id"])
            else:
                discovered_currencies.remove(currency_def["id"])
        imgui.table_next_column()
        obj = next((c for c in currencies if c["currency"] == currency_def["id"]), None)
        if obj is None:
            currencies.append(dict(currency=currency_def["id"], value=0))
            obj = currencies[-1]
        show_raw_value_editor(obj, "value")
        imgui.pop_id()
    imgui.end_table()


def show_editor_main(state: State):
    imgui.columns(2)

    if imgui.begin_child("##first column"):
        if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
            show_raw_key_value_editor(state.active_meta, "description", "Description")

        if imgui.collapsing_header(
            "Player character", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            show_key_value_options_editor(
                "Class keybinding profile",
                state.active_meta["projdata"],
                "keybindingprofile",
                CLASS_KEYBINDING_VALUES,
                CLASS_KEYBINDING_LABELS,
            )

        if imgui.collapsing_header(
            "Currencies", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            show_currency_editor(state)
    imgui.end_child()

    imgui.next_column()

    if imgui.begin_child("##second column"):
        if imgui.collapsing_header(
            "Difficulty", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            difficulty = state.get_client_difficulty()
            if show_key_value_options_editor(
                "Combat Difficulty",
                difficulty,
                "difficultyIndex",
                DIFFICULTY_COMBAT_PRESET_VALUES,
                DIFFICULTY_COMBAT_PRESET_LABELS,
            ):
                # value is duplicated!
                state.active_meta["projdata"]["difficulty"] = difficulty["difficultyIndex"]
            show_key_value_options_editor(
                "Exploration Difficulty",
                difficulty,
                "explorationIndex",
                DIFFICULTY_EXPLORATION_PRESET_VALUES,
                DIFFICULTY_EXPLORATION_PRESET_LABELS,
            )

        if imgui.collapsing_header(
            "Inquisitor", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            show_persisted_value_editor(state, "Reference past DA?", PAST_DA_SHOULD_REFERENCE_PROPERTY)
            show_persisted_value_options_editor(
                state,
                "Romance option",
                PAST_DA_INQUISITOR_ROMANCE_PROPERTY,
                PAST_DA_INQUISITOR_ROMANCE_VALUES,
                PAST_DA_INQUISITOR_ROMANCE_LABELS,
                PAST_DA_INQUISITOR_ROMANCE_DEFAULT_INDEX,
            )
    imgui.end_child()

    imgui.columns(1)


def show_editor_appearances(state: State):
    data = state.get_client_rpg_extents(2)

    imgui.text_wrapped(
        "You can manually edit the following JSON documents or copy them from another save game!\n"
        + "Hint: It is probably easier to make a new character with the desired player or inquisitor appearance "
        + "and copy their appearance documents over than trying to modify the values below."
    )

    if imgui.collapsing_header(
        "Player appearance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        # https://github.com/ocornut/imgui/issues/623
        imgui.push_item_width(-1)
        changed, new_value = show_json_editor("##Player", data["playerData"])
        if changed:
            data["playerData"] = new_value
        imgui.pop_item_width()

    if imgui.collapsing_header(
        "Inquisitor appearance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        # https://github.com/ocornut/imgui/issues/623
        imgui.push_item_width(-1)
        changed, new_value = show_json_editor("##Inquisitor", data["inquisitorData"])
        if changed:
            data["inquisitorData"] = new_value
        imgui.pop_item_width()


def show_editor_content(state: State):
    if not imgui.begin_tab_bar("editors"):
        return

    if imgui.begin_tab_item("Main")[0]:
        show_editor_main(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Appearances")[0]:
        show_editor_appearances(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Inventories")[0]:
        show_editor_inventories(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Raw Data")[0]:
        show_editor_raw_data(state)
        imgui.end_tab_item()

    imgui.end_tab_bar()


def show_empty_warning():
    imgui.push_style_var(imgui.StyleVar_.selectable_text_align, (0.5, 0.5))
    imgui.selectable("No save file loaded!", False)
    imgui.pop_style_var()


def show_editor_window(state: State):
    vp = imgui.get_main_viewport()

    imgui.set_next_window_pos(vp.work_pos)
    imgui.set_next_window_size(vp.work_size)

    if imgui.begin(
        "editor_content",
        None,
        imgui.WindowFlags_.no_title_bar | imgui.WindowFlags_.no_resize | imgui.WindowFlags_.no_collapse,
    ):
        if state.has_content():
            show_editor_content(state)
        else:
            show_empty_warning()

    imgui.end()


WINDOW_TITLE = "Dragon Age: The Veilguard save editor by Tim & mons"


def show_ui(state: State):
    show_main_menu_bar(state)
    show_app_about(state)
    show_editor_window(state)

    clear_unused_retained_data()


def main():
    state = State()
    immapp.run(gui_function=lambda: show_ui(state), window_title=WINDOW_TITLE)
