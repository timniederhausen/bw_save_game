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

from __future__ import absolute_import

import json
import os.path
import sys
import typing  # noqa: F401
from uuid import UUID, uuid1

from imgui_bundle import glfw_utils, imgui, immapp

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
    CHARACTER_GENERATOR_FACTION,
    CHARACTER_GENERATOR_FACTION_LABELS,
    CHARACTER_GENERATOR_FACTION_VALUES,
    CHARACTER_GENERATOR_LINEAGE,
    CHARACTER_GENERATOR_LINEAGE_LABELS,
    CHARACTER_GENERATOR_LINEAGE_VALUES,
    CLASS_KEYBINDING_LABELS,
    CLASS_KEYBINDING_VALUES,
    DIFFICULTY_COMBAT_PRESET_LABELS,
    DIFFICULTY_COMBAT_PRESET_VALUES,
    DIFFICULTY_EXPLORATION_PRESET_LABELS,
    DIFFICULTY_EXPLORATION_PRESET_VALUES,
    ITEM_ATTACHMENT_SLOT_NAMES,
    ITEM_ATTACHMENT_SLOT_VALUES,
    KNOWN_CHARACTER_ARCHETYPE_LABELS,
    KNOWN_CHARACTER_ARCHETYPE_VALUES,
    LOOT_RARITY_NAMES,
    PAST_DA_INQUISITOR_ROMANCE_LABELS,
    PAST_DA_INQUISITOR_ROMANCE_PROPERTY,
    PAST_DA_INQUISITOR_ROMANCE_VALUES,
    PAST_DA_SHOULD_REFERENCE_PROPERTY,
    ItemAttachmentType,
    VeilguardSaveGame,
    construct_item_attachment,
    deconstruct_item_attachment,
    item_attachment_to_string,
)

# The UI needs some additional per-item data, pre-compute that here:
_ITEM_ID_TO_INDEX = {item["id"]: i for i, item in enumerate(ALL_ITEMS)}
_ITEM_KEYS = [item["key"] for item in ALL_ITEMS]


class State(object):
    def __init__(self):
        # UI state
        self.show_app_about = False
        self.add_item_object = None  # type: typing.Optional[dict]

        self.default_save_path = os.path.expandvars(
            "%USERPROFILE%/Documents/BioWare/Dragon Age The Veilguard/save games"
        )

        # loaded save game
        self.active_filename = None  # type: typing.Optional[str]
        self.save_game = None  # type: typing.Optional[VeilguardSaveGame]

    def has_content(self):
        return self.save_game is not None

    def load(self, filename: str):
        try:
            with open(filename, "rb") as f:
                m, d = read_save_from_reader(f)
            m = loads(m)
            d = loads(d)
        except Exception as e:
            show_error(f"Cannot load {filename}: {repr(e)}")
            return False

        self.active_filename = filename
        self.save_game = VeilguardSaveGame(m, d)
        return True

    def save(self, filename: str):
        try:
            m = dumps(self.save_game.meta)
            d = dumps(self.save_game.data)
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
        self.save_game = VeilguardSaveGame(m, d)

    def export_json(self, filename: str):
        try:
            root = dict(
                meta=self.save_game.meta, data=self.save_game.data, exporter=dict(version=__version__, format=1)
            )
            with open(filename, "w", encoding="utf-8") as f:
                # TODO: do we want sort keys on?
                json.dump(root, f, ensure_ascii=False, indent=2, default=to_raw_dict)
        except Exception as e:
            show_error(f"Cannot save {filename}: {repr(e)}")
            return


def show_app_about(state: State):
    if imgui.begin_popup("About BWSaveGameEditor", imgui.WindowFlags_.always_auto_resize):
        imgui.text("BWSaveGameEditor " + __version__)
        imgui.separator()
        imgui.text("By Tim & mons.")
        imgui.text("BWSaveGameEditor is licensed under GNU General Public License v3.0.")
        imgui.separator()
        imgui.text("Using ImGui v" + imgui.get_version())
        imgui.end_popup()


def ask_for_open(state: State):
    path = ask_for_file_to_open(
        "Open Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav", state.default_save_path
    )
    if path:
        if state.load(path):
            glfw_win = glfw_utils.glfw_window_hello_imgui()
            glfw_utils.glfw.set_window_title(glfw_win, path)


def show_main_menu_bar(state: State):
    if not imgui.begin_main_menu_bar():
        return

    if imgui.begin_menu("File", True):
        clicked, selected = imgui.menu_item(label="Open", shortcut="Ctrl+O", p_selected=False)
        if clicked:
            ask_for_open(state)

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

    # https://github.com/ocornut/imgui/issues/331
    need_about_open = False
    if imgui.begin_menu("Help", True):
        clicked, selected = imgui.menu_item(label="About BWSaveGameEditor", shortcut="", p_selected=False)
        if clicked:
            need_about_open = True
        imgui.end_menu()

    imgui.end_main_menu_bar()

    if need_about_open:
        imgui.open_popup("About BWSaveGameEditor")


def show_item_id_editor(obj):
    # https://github.com/ocornut/imgui/issues/623
    imgui.set_next_item_width(-1)

    index = _ITEM_ID_TO_INDEX.get(to_native(obj["itemDataId"]))
    if index is not None:
        # https://github.com/ocornut/imgui/issues/623
        changed, new_index = show_searchable_combo_box("##itemDataId", _ITEM_KEYS, index)
        if changed:
            data = ALL_ITEMS[new_index]
            obj["itemDataId"] = Long(data["id"])
            obj["dataGuid"] = data["guid"]
        return

    preview_value = f"Unsupported item: {to_native(obj['itemDataId'])}"

    is_open = imgui.begin_combo("##itemDataId", preview_value, imgui.ComboFlags_.height_largest)
    if not is_open:
        if imgui.begin_item_tooltip():
            imgui.text(preview_value)
            imgui.end_tooltip()
        return

    # TODO: Show something better!
    # show_simple_value_editor(obj, "itemDataId")


def show_persisted_value_editor(state: State, label: str, prop: PersistencePropertyDefinition):
    def_instance = state.save_game.get_persistence_instance(prop.key)
    if not def_instance:
        return False

    obj, key = get_or_create_persisted_value(def_instance, prop.id, prop.type, prop.default)
    return show_raw_key_value_editor(obj, key, label)


def show_persisted_value_options_editor(
    state: State, label: str, prop: PersistencePropertyDefinition, option_values: list, option_names: list[str]
):
    def_instance = state.save_game.get_persistence_instance(prop.key)
    if not def_instance:
        return False

    obj, key = get_or_create_persisted_value(def_instance, prop.id, prop.type, prop.default)
    return show_key_value_options_editor(
        label, obj, key, option_values, option_names, option_values.index(prop.default)
    )


def show_editor_raw_data(game: VeilguardSaveGame):
    if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in game.meta:
            imgui.push_id(key)
            show_raw_key_value_editor(game.meta, key)
            imgui.pop_id()
    imgui.separator()
    if imgui.collapsing_header("Content", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in game.data:
            imgui.push_id(key)
            show_raw_key_value_editor(game.data, key)
            imgui.pop_id()


def show_item_attachment_editor(item: dict):
    preview_value = item_attachment_to_string(item)

    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)
    is_open = imgui.begin_combo("##itemAttachment", preview_value, imgui.ComboFlags_.height_largest)
    if not is_open:
        if imgui.begin_item_tooltip():
            imgui.text(preview_value)
            imgui.end_tooltip()

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
            construct_item_attachment(item, typ, parent, ITEM_ATTACHMENT_SLOT_VALUES[new_item])
    except ValueError:
        imgui.text_colored((1.0, 0.0, 0.0, 1.0), f"Unknown attach slot {attach_slot}")

    imgui.pop_item_width()
    imgui.end_combo()
    imgui.pop_item_width()


def show_item_rarity_editor(item: dict):
    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)

    rarity = item.get("rarity")
    try:
        current_item = LOOT_RARITY_NAMES.index(rarity or "Rarity_None")
        changed, new_item = imgui.combo("##Rarity", current_item, LOOT_RARITY_NAMES)
        if changed:
            item["rarity"] = LOOT_RARITY_NAMES[new_item]
    except ValueError:
        imgui.text_colored((1.0, 0.0, 0.0, 1.0), f"Unknown: {rarity}")

    imgui.pop_item_width()


def show_item_stack_count_editor(item: dict):
    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)

    removed = False
    count = to_native(item.get("stackCount", 1))
    changed, new_count = imgui.input_int("##StackCount", count)
    if changed:
        item["stackCount"] = new_count
        removed = new_count == 0

    imgui.pop_item_width()
    return removed


def show_item_level_editor(item: dict):
    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)

    level = to_native(item.get("level", 1))
    changed, new_level = imgui.input_int("##Level", level)
    if changed:
        item["level"] = new_level

    imgui.pop_item_width()


def show_editor_inventories(state: State):
    items = state.save_game.get_items()

    imgui.text(f"Number of items: {len(items)}")
    imgui.same_line()
    if imgui.button("Add Item"):
        default_item_data = ALL_ITEMS[0]
        state.add_item_object = dict(
            itemDataId=Long(default_item_data["id"]), dataGuid=default_item_data["guid"], instanceGuid=uuid1()
        )
        imgui.open_popup("Add Item")

    if imgui.begin_popup_modal("Add Item", None, imgui.WindowFlags_.always_auto_resize)[0]:
        item = state.add_item_object

        imgui.text_disabled("Item: ")
        imgui.same_line()
        show_item_id_editor(item)

        imgui.text_disabled("Attached to: ")
        imgui.same_line()
        show_item_attachment_editor(item)

        imgui.text_disabled("Stack count: ")
        imgui.same_line()
        show_item_stack_count_editor(item)

        imgui.text_disabled("Rarity: ")
        imgui.same_line()
        show_item_rarity_editor(item)

        imgui.text_disabled("Level: ")
        imgui.same_line()
        show_item_level_editor(item)

        if imgui.button("OK", (120, 0)):
            items.append(item)
            imgui.close_current_popup()
        imgui.set_item_default_focus()
        imgui.same_line()
        if imgui.button("Cancel", (120, 0)):
            imgui.close_current_popup()
        imgui.end_popup()

    removed_items = []
    if imgui.begin_table("Items", 5, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        imgui.table_setup_column("Item")
        imgui.table_setup_column("Attached to")
        imgui.table_setup_column("Amount")
        imgui.table_setup_column("Rarity")
        imgui.table_setup_column("Level")
        imgui.table_headers_row()
        for i, item in enumerate(items):
            imgui.push_id(i)
            imgui.table_next_row()
            imgui.table_next_column()
            show_item_id_editor(item)
            imgui.table_next_column()
            show_item_attachment_editor(item)
            imgui.table_next_column()
            if show_item_stack_count_editor(item):
                removed_items.append(i)
            imgui.table_next_column()
            show_item_rarity_editor(item)
            imgui.table_next_column()
            show_item_level_editor(item)
            imgui.pop_id()
        imgui.end_table()

    # Actually remove the items from our list - in reverse order of index
    if removed_items:
        removed_items = sorted(removed_items, reverse=True)
        for i in removed_items:
            del items[i]


def show_currency_editor(state: State):
    if not imgui.begin_table("Currencies", 3, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        return

    imgui.table_setup_column("Currency")
    imgui.table_setup_column("Discovered?")
    imgui.table_setup_column("Amount")
    imgui.table_headers_row()
    currencies, discovered_currencies = state.save_game.get_currencies()
    for currency_def in ALL_CURRENCIES:
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
            tmp = dict(currency=currency_def["id"], value=0)
            if show_raw_value_editor(tmp, "value"):
                currencies.append(tmp)
        else:
            show_raw_value_editor(obj, "value")
        imgui.pop_id()
    imgui.end_table()


def show_editor_main(state: State):
    imgui.columns(2)

    if imgui.begin_child("##first column"):
        if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
            show_raw_key_value_editor(state.save_game.meta, "description", "Description")

        if imgui.collapsing_header(
            "Player character", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            if show_persisted_value_options_editor(
                state,
                "Lineage",
                CHARACTER_GENERATOR_LINEAGE,
                CHARACTER_GENERATOR_LINEAGE_VALUES,
                CHARACTER_GENERATOR_LINEAGE_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["lineage"] = state.save_game.get_persistence_property(
                    CHARACTER_GENERATOR_LINEAGE
                )
            if show_persisted_value_options_editor(
                state,
                "Faction",
                CHARACTER_GENERATOR_FACTION,
                CHARACTER_GENERATOR_FACTION_VALUES,
                CHARACTER_GENERATOR_FACTION_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["faction"] = state.save_game.get_persistence_property(
                    CHARACTER_GENERATOR_FACTION
                )
            if show_key_value_options_editor(
                "Class",
                state.save_game.meta["projdata"],
                "archetype",
                KNOWN_CHARACTER_ARCHETYPE_VALUES,
                KNOWN_CHARACTER_ARCHETYPE_LABELS,
            ):
                old_archetype = to_native(state.save_game.get_server_rpg_extents(loadpass=0)["archetype"])
                state.save_game.replace_character_archetype(
                    old_archetype, state.save_game.meta["projdata"]["archetype"]
                )
            show_key_value_options_editor(
                "Class keybinding profile",
                state.save_game.meta["projdata"],
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
            difficulty = state.save_game.get_client_difficulty()
            if show_key_value_options_editor(
                "Combat Difficulty",
                difficulty,
                "difficultyIndex",
                DIFFICULTY_COMBAT_PRESET_VALUES,
                DIFFICULTY_COMBAT_PRESET_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["difficulty"] = difficulty["difficultyIndex"]
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
            )
    imgui.end_child()

    imgui.columns(1)


def show_editor_appearances(state: State):
    data = state.save_game.get_client_rpg_extents(2)

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
        show_editor_raw_data(state.save_game)
        imgui.end_tab_item()

    imgui.end_tab_bar()


def show_empty_warning(state: State):
    imgui.push_style_var(imgui.StyleVar_.selectable_text_align, (0.5, 0.5))
    if imgui.selectable("No save file loaded!", False)[0]:
        ask_for_open(state)
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
            show_empty_warning(state)

    imgui.end()


def show_ui(state: State):
    show_main_menu_bar(state)
    show_app_about(state)
    show_editor_window(state)

    clear_unused_retained_data()


WINDOW_TITLE = "Dragon Age: The Veilguard save editor - By Tim & mons"


def main():
    state = State()
    immapp.run(gui_function=lambda: show_ui(state), window_title=WINDOW_TITLE)
