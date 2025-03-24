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

import os.path
import re
import sys
import typing  # noqa: F401
from uuid import UUID, uuid1

from imgui_bundle import glfw_utils, imgui, immapp

from bw_save_game import __version__
from bw_save_game.db_object import Long, to_native
from bw_save_game.persistence import (
    PersistenceKey,
    PersistencePropertyDefinition,
    get_persisted_value,
    registered_persistence_key,
    set_persisted_value,
)
from bw_save_game.ui.editors import (
    show_bit_flags_editor,
    show_json_editor,
    show_labeled_bit_flags_editor,
    show_labeled_options_editor,
    show_labeled_options_editor_in_place,
    show_labeled_value_editor,
    show_labeled_value_editor_in_place,
    show_uuid_editor,
    show_value_editor,
    show_value_editor_in_place,
    show_value_tree_editor_in_place,
)
from bw_save_game.ui.utils import (
    ask_for_file_to_open,
    ask_for_file_to_save,
    push_int_id,
    show_error,
)
from bw_save_game.ui.widgets import (
    clear_unused_retained_data,
    show_regex_input,
    show_searchable_combo_box,
)
from bw_save_game.veilguard import (
    ALL_CURRENCIES,
    ALL_ITEMS,
    ALL_PERSISTENCE_DEFINITIONS,
    ARCHETYPE_TO_SKILL_DATA,
    CARETAKERPROGRESSION_XP,
    CHARACTER_GENDER_LABELS,
    CHARACTER_GENDER_VALUES,
    CHARACTER_GENERATOR_FACTION,
    CHARACTER_GENERATOR_FACTION_LABELS,
    CHARACTER_GENERATOR_FACTION_VALUES,
    CHARACTER_GENERATOR_GENDER,
    CHARACTER_GENERATOR_IS_TRANS,
    CHARACTER_GENERATOR_LINEAGE,
    CHARACTER_GENERATOR_LINEAGE_LABELS,
    CHARACTER_GENERATOR_LINEAGE_VALUES,
    CHARACTER_GENERATOR_PRONOUN_OPTION_LABELS,
    CHARACTER_GENERATOR_PRONOUN_OPTION_VALUES,
    CHARACTER_GENERATOR_PRONOUNS,
    CHARACTER_GENERATOR_VOICE,
    CHARACTER_GENERATOR_VOICE_LABELS,
    CHARACTER_GENERATOR_VOICE_TONE,
    CHARACTER_GENERATOR_VOICE_TONE_LABELS,
    CHARACTER_GENERATOR_VOICE_TONE_VALUES,
    CHARACTER_GENERATOR_VOICE_VALUES,
    CLASS_KEYBINDING_LABELS,
    CLASS_KEYBINDING_VALUES,
    COLLECTIBLE_LABELS,
    COLLECTIBLES,
    DIFFICULTY_COMBAT_PRESET_LABELS,
    DIFFICULTY_COMBAT_PRESET_VALUES,
    DIFFICULTY_EXPLORATION_PRESET_LABELS,
    DIFFICULTY_EXPLORATION_PRESET_VALUES,
    EMMRICH_AND_STRIFE_PROPERTIES,
    EMMRICH_M23_LICHBECOMING,
    EMMRICH_M23_MANFREDREVIVE,
    FACTION_ANTIVANCROWS_PROPERTIES,
    FACTION_GREYWARDENS_PROPERTIES,
    FACTION_LORDSOFFORTUNE_PROPERTIES,
    FACTION_MOURNWATCH_PROPERTIES,
    FACTION_SHADOWDRAGONS_PROPERTIES,
    FACTION_VEILJUMPERS_PROPERTIES,
    FOLLOWER_IDS,
    FOLLOWER_LABELS,
    HARDING_AND_TASH_PROPERTIES,
    ITEM_ATTACHMENT_SLOT_NAMES,
    KNOWN_CHARACTER_ARCHETYPE_LABELS,
    KNOWN_CHARACTER_ARCHETYPE_VALUES,
    LOOT_RARITY_NAMES,
    LUCANIS_AND_NEVE_PROPERTIES,
    LUCANIS_M21,
    LUCANIS_M23,
    PERSISTENCE_DEFINITION_LABELS,
    PERSISTENCE_DEFINITION_TO_QUEST,
    PROGRESSION_BELLARA_PROPERTIES,
    PROGRESSION_DAVRIN_PROPERTIES,
    PROGRESSION_EMMRICH_PROPERTIES,
    PROGRESSION_HARDING_PROPERTIES,
    PROGRESSION_LUCANIS_PROPERTIES,
    PROGRESSION_NEVE_PROPERTIES,
    PROGRESSION_TAASH_PROPERTIES,
    ROMANCE_BELLARA_PROPERTIES,
    ROMANCE_DAVRIN_PROPERTIES,
    ROMANCE_EMMRICH_PROPERTIES,
    ROMANCE_HARDING_PROPERTIES,
    ROMANCE_LUCANIS_PROPERTIES,
    ROMANCE_NEVE_PROPERTIES,
    ROMANCE_TAASH_PROPERTIES,
    SKILL_GRAPHS,
    TRANSITION_START_POINTS,
    BWFollowerStateFlag,
    CharacterArchetype,
    CollectibleSetFlag,
    EcoQuestRegisteredStateFlags,
    INQUISITION_CHOICES_Inquisitor_Gender,
    INQUISITION_CHOICES_Inquisitor_Gender_LABELS,
    INQUISITION_CHOICES_Inquisitor_Gender_VALUES,
    INQUISITION_CHOICES_Inquisitor_Lineage,
    INQUISITION_CHOICES_Inquisitor_Lineage_LABELS,
    INQUISITION_CHOICES_Inquisitor_Lineage_VALUES,
    INQUISITION_CHOICES_Inquisitor_Voice,
    INQUISITION_CHOICES_Inquisitor_Voice_LABELS,
    INQUISITION_CHOICES_Inquisitor_Voice_VALUES,
    INQUISITION_CHOICES_Keep_Inquisition,
    INQUISITION_CHOICES_Keep_Inquisition_LABELS,
    INQUISITION_CHOICES_Keep_Inquisition_VALUES,
    INQUISITION_CHOICES_Keep_Romance,
    INQUISITION_CHOICES_Keep_Romance_LABELS,
    INQUISITION_CHOICES_Keep_Romance_VALUES,
    INQUISITION_CHOICES_Keep_Trespasser,
    INQUISITION_CHOICES_Keep_Trespasser_LABELS,
    INQUISITION_CHOICES_Keep_Trespasser_VALUES,
    INQUISITION_CHOICES_LegacyReferences,
    ItemAttachmentType,
    PROGRESSION_CurrentLevel,
    VeilguardSaveGame,
    construct_item_attachment,
    deconstruct_item_attachment,
    force_complete_quest,
    item_attachment_to_string,
)

# The UI needs some additional per-item data, pre-compute that here:
_ITEM_ID_TO_INDEX = {item["id"]: i for i, item in enumerate(ALL_ITEMS)}
_ITEM_KEYS = [item["key"] for item in ALL_ITEMS]

WINDOW_TITLE = "DA:V Save Editor - By Tim & mons"


def detect_save_game_path():
    if sys.platform.startswith("win"):
        # https://stackoverflow.com/a/3859336
        import ctypes.wintypes

        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Want current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
        full_path = f"{buf.value}/BioWare/Dragon Age The Veilguard/save games"
        if os.path.exists(full_path):
            return full_path
        return ""

    # TODO: maybe support Wine etc. here? I don't know how they map the Documents path.
    return ""


class State(object):
    def __init__(self):
        # UI state
        self.show_app_about = False
        self.add_item_object = None  # type: typing.Optional[dict]
        self.inventory_filter = ""
        self.inventory_filter_compiled = None  # type: typing.Optional[re.Pattern]
        self.selected_collectible_set_index = 0
        self.selected_definition_index = 0
        self.selected_instance_index = 0

        self.default_save_path = detect_save_game_path()

        # loaded save game
        self.active_filename = None  # type: typing.Optional[str]
        self.save_game = None  # type: typing.Optional[VeilguardSaveGame]

    def has_content(self):
        return self.save_game is not None

    def load(self, filename: str):
        try:
            with open(filename, "rb") as f:
                new_save_game = VeilguardSaveGame.from_file(f)
        except Exception as e:
            show_error(f"Cannot load {filename}: {repr(e)}")
            return False

        self.close()
        self.active_filename = filename
        self.save_game = new_save_game
        return True

    def save(self, filename: str):
        if not os.path.splitext(filename)[1]:
            filename += ".csav"
        try:
            with open(filename, "wb") as f:
                self.save_game.to_file(f)
        except Exception as e:
            show_error(f"Cannot save {filename}: {repr(e)}")
            return
        self.active_filename = filename

    def import_json(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                new_save_game = VeilguardSaveGame.from_json(f)
        except Exception as e:
            show_error(f"Cannot load {filename}: {repr(e)}")
            return

        self.close()
        self.save_game = new_save_game

    def export_json(self, filename: str):
        if not os.path.splitext(filename)[1]:
            filename += ".json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                self.save_game.to_json(f)
        except Exception as e:
            show_error(f"Cannot save {filename}: {repr(e)}")
            return

    def close(self):
        self.active_filename = None
        self.save_game = None
        self.inventory_filter = ""
        self.inventory_filter_compiled = None
        self.selected_collectible_set_index = 0
        self.selected_definition_index = 0
        self.selected_instance_index = 0


def set_window_title(title: str):
    glfw_win = glfw_utils.glfw_window_hello_imgui()
    glfw_utils.glfw.set_window_title(glfw_win, title)


DRAGON_AGE_CSAV_WILDCARD = "Dragon Age: Veilguard save file (*.csav)|*.csav"
DRAGON_AGE_JSON_WILDCARD = "JSON save document (*.json)|*.json"


def ask_for_open(state: State):
    path = ask_for_file_to_open("Open Save Game", DRAGON_AGE_CSAV_WILDCARD, state.default_save_path)
    if path:
        if state.load(path):
            set_window_title(f"{WINDOW_TITLE}: {path}")


def show_app_about(state: State):
    imgui.set_next_window_pos(imgui.get_main_viewport().get_center(), imgui.Cond_.appearing, (0.5, 0.5))
    if imgui.begin_popup("About", imgui.WindowFlags_.always_auto_resize):
        imgui.text("DA:V Editor " + __version__)
        imgui.separator()
        imgui.text("By Tim & mons.")
        imgui.text("Website:")
        imgui.same_line()
        imgui.text_link_open_url(
            "https://github.com/timniederhausen/bw_save_game", "https://github.com/timniederhausen/bw_save_game"
        )
        imgui.text("DA:V Editor is licensed under GNU General Public License v3.0.")
        imgui.separator()
        imgui.text("Using ImGui v" + imgui.get_version())
        imgui.end_popup()


def show_main_menu_bar(state: State):
    if not imgui.begin_main_menu_bar():
        return

    if imgui.begin_menu("File", True):
        clicked, selected = imgui.menu_item(label="Open", shortcut="Ctrl+O", p_selected=False)
        if clicked:
            ask_for_open(state)

        clicked, selected = imgui.menu_item(label="Import JSON", shortcut="", p_selected=False)
        if clicked:
            path = ask_for_file_to_open("Open JSON Save Game", DRAGON_AGE_JSON_WILDCARD)
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
            path = ask_for_file_to_save("Write Save Game", DRAGON_AGE_CSAV_WILDCARD)
            if path:
                state.save(path)
                set_window_title(path)

        clicked, selected = imgui.menu_item(
            label="Export JSON", shortcut="", p_selected=False, enabled=state.has_content()
        )
        if clicked:
            path = ask_for_file_to_save("Export JSON save game", DRAGON_AGE_JSON_WILDCARD)
            if path:
                state.export_json(path)

        clicked, selected = imgui.menu_item("Close", "", False, state.has_content())
        if clicked:
            state.close()
            set_window_title(WINDOW_TITLE)

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
        imgui.open_popup("About")


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
    push_int_id(prop.id)

    changed, new_value = show_labeled_value_editor(label, state.save_game.get_persistence_property(prop))
    if changed:
        state.save_game.set_persistence_property(prop, new_value)
    imgui.pop_id()
    return changed


def show_persisted_value_options_editor(
    state: State, label: str, prop: PersistencePropertyDefinition, option_values: list, option_names: list[str]
):
    push_int_id(prop.id)

    changed, new_value = show_labeled_options_editor(
        label,
        state.save_game.get_persistence_property(prop),
        option_values,
        option_names,
        option_values.index(prop.default),
    )
    if changed:
        state.save_game.set_persistence_property(prop, new_value)
    imgui.pop_id()


def show_editor_raw_data(game: VeilguardSaveGame):
    if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in game.meta:
            imgui.push_id(key)
            show_value_tree_editor_in_place(game.meta, key)
            imgui.pop_id()
    imgui.separator()
    if imgui.collapsing_header("Content", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in game.data:
            imgui.push_id(key)
            show_value_tree_editor_in_place(game.data, key)
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
            construct_item_attachment(item, typ, parent, ITEM_ATTACHMENT_SLOT_NAMES[new_item])
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


def _does_item_match(item, pattern: re.Pattern):
    item_def_index = _ITEM_ID_TO_INDEX.get(to_native(item["itemDataId"]))
    if item_def_index is not None:
        item_def = ALL_ITEMS[item_def_index]
        if pattern.search(item_def["key"]):
            return True

    typ, parent, attach_slot = deconstruct_item_attachment(item)
    if typ == ItemAttachmentType.None_:
        return False

    if pattern.search(attach_slot):
        return True

    if typ == ItemAttachmentType.Character:
        try:
            current_item = KNOWN_CHARACTER_ARCHETYPE_VALUES.index(parent)
            if pattern.search(KNOWN_CHARACTER_ARCHETYPE_LABELS[current_item]):
                return True
        except ValueError:
            pass

    return False


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

    imgui.set_next_window_size_constraints((400, 190), (imgui.FLT_MAX, imgui.FLT_MAX))
    if imgui.begin_popup_modal("Add Item", None)[0]:
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

    imgui.text("Filter:")
    imgui.same_line()
    imgui.set_next_item_width(-1)
    changed, new_value, new_value_compiled = show_regex_input("##filter", state.inventory_filter)
    if changed:
        state.inventory_filter = new_value
        state.inventory_filter_compiled = new_value_compiled

    filtered_items = enumerate(items)
    if state.inventory_filter:
        filtered_items = filter(
            lambda i_item: _does_item_match(i_item[1], state.inventory_filter_compiled), filtered_items
        )

    removed_items = []
    if imgui.begin_table("Items", 5, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        imgui.table_setup_column("Item")
        imgui.table_setup_column("Attached to")
        imgui.table_setup_column("Amount")
        imgui.table_setup_column("Rarity")
        imgui.table_setup_column("Level")
        imgui.table_headers_row()
        for i, item in filtered_items:
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
            imgui.push_id(currency_def["id"])
            changed, new_value = show_value_editor(0)
            imgui.pop_id()
            if changed:
                currencies.append(dict(currency=currency_def["id"], value=new_value))
        else:
            show_value_editor_in_place(obj, "value")
        imgui.pop_id()
    imgui.end_table()


def show_editor_main(state: State):
    imgui.columns(2)

    if imgui.begin_child("##first column", child_flags=imgui.ChildFlags_.auto_resize_y):
        if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
            show_labeled_value_editor_in_place("Description", state.save_game.meta, "description")
            show_labeled_value_editor_in_place("Unique Identifier", state.save_game.meta, "uid")
            show_labeled_options_editor_in_place(
                "Transition start point",
                state.save_game.meta["projdata"],
                "transitionpointname",
                TRANSITION_START_POINTS,
                TRANSITION_START_POINTS,
            )
            if show_labeled_value_editor_in_place("Career ID", state.save_game.meta, "activecareer"):
                difficulty = state.save_game.get_client_difficulty()
                difficulty["careerId"] = state.save_game.meta["activecareer"]

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
            if show_labeled_options_editor_in_place(
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
            show_labeled_options_editor_in_place(
                "Class keybinding profile",
                state.save_game.meta["projdata"],
                "keybindingprofile",
                CLASS_KEYBINDING_VALUES,
                CLASS_KEYBINDING_LABELS,
            )
            if show_persisted_value_editor(state, "Level:", PROGRESSION_CurrentLevel):
                state.save_game.change_level(state.save_game.get_persistence_property(PROGRESSION_CurrentLevel))
            if show_persisted_value_options_editor(
                state,
                "Voice",
                CHARACTER_GENERATOR_VOICE,
                CHARACTER_GENERATOR_VOICE_VALUES,
                CHARACTER_GENERATOR_VOICE_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["voice"] = state.save_game.get_persistence_property(
                    CHARACTER_GENERATOR_VOICE
                )
            if show_persisted_value_options_editor(
                state,
                "Voice tone",
                CHARACTER_GENERATOR_VOICE_TONE,
                CHARACTER_GENERATOR_VOICE_TONE_VALUES,
                CHARACTER_GENERATOR_VOICE_TONE_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["tone"] = state.save_game.get_persistence_property(
                    CHARACTER_GENERATOR_VOICE_TONE
                )
            if show_persisted_value_options_editor(
                state,
                "Gender",
                CHARACTER_GENERATOR_GENDER,
                CHARACTER_GENDER_VALUES,
                CHARACTER_GENDER_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["gender"] = state.save_game.get_persistence_property(
                    CHARACTER_GENERATOR_GENDER
                )
            if show_persisted_value_options_editor(
                state,
                "Pronouns",
                CHARACTER_GENERATOR_PRONOUNS,
                CHARACTER_GENERATOR_PRONOUN_OPTION_VALUES,
                CHARACTER_GENERATOR_PRONOUN_OPTION_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["pronoun"] = state.save_game.get_persistence_property(
                    CHARACTER_GENERATOR_PRONOUNS
                )
            show_persisted_value_editor(state, "Is Trans?", CHARACTER_GENERATOR_IS_TRANS)

        if imgui.collapsing_header(
            "Currencies", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            show_currency_editor(state)
    imgui.end_child()

    imgui.next_column()

    if imgui.begin_child("##second column", child_flags=imgui.ChildFlags_.auto_resize_y):
        if imgui.collapsing_header(
            "Difficulty", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            difficulty = state.save_game.get_client_difficulty()
            if show_labeled_options_editor_in_place(
                "Combat Difficulty",
                difficulty,
                "difficultyIndex",
                DIFFICULTY_COMBAT_PRESET_VALUES,
                DIFFICULTY_COMBAT_PRESET_LABELS,
            ):
                # value is duplicated!
                state.save_game.meta["projdata"]["difficulty"] = difficulty["difficultyIndex"]
            show_labeled_options_editor_in_place(
                "Exploration Difficulty",
                difficulty,
                "explorationIndex",
                DIFFICULTY_EXPLORATION_PRESET_VALUES,
                DIFFICULTY_EXPLORATION_PRESET_LABELS,
            )

        if imgui.collapsing_header(
            "Inquisitor", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            # XXX: Hacky for now: people always want the inquisition choices
            if not state.save_game.get_persistence_instance(INQUISITION_CHOICES_LegacyReferences.key):
                state.save_game.make_persistence_instance(INQUISITION_CHOICES_LegacyReferences.key)

            show_persisted_value_editor(state, "Reference past DA?", INQUISITION_CHOICES_LegacyReferences)
            show_persisted_value_options_editor(
                state,
                "Lineage",
                INQUISITION_CHOICES_Inquisitor_Lineage,
                INQUISITION_CHOICES_Inquisitor_Lineage_VALUES,
                INQUISITION_CHOICES_Inquisitor_Lineage_LABELS,
            )
            show_persisted_value_options_editor(
                state,
                "Gender",
                INQUISITION_CHOICES_Inquisitor_Gender,
                INQUISITION_CHOICES_Inquisitor_Gender_VALUES,
                INQUISITION_CHOICES_Inquisitor_Gender_LABELS,
            )
            show_persisted_value_options_editor(
                state,
                "Voice",
                INQUISITION_CHOICES_Inquisitor_Voice,
                INQUISITION_CHOICES_Inquisitor_Voice_VALUES,
                INQUISITION_CHOICES_Inquisitor_Voice_LABELS,
            )
            show_persisted_value_options_editor(
                state,
                "Romance option",
                INQUISITION_CHOICES_Keep_Romance,
                INQUISITION_CHOICES_Keep_Romance_VALUES,
                INQUISITION_CHOICES_Keep_Romance_LABELS,
            )
            show_persisted_value_options_editor(
                state,
                "Objective",
                INQUISITION_CHOICES_Keep_Trespasser,
                INQUISITION_CHOICES_Keep_Trespasser_VALUES,
                INQUISITION_CHOICES_Keep_Trespasser_LABELS,
            )
            show_persisted_value_options_editor(
                state,
                "Fate of Inquisition",
                INQUISITION_CHOICES_Keep_Inquisition,
                INQUISITION_CHOICES_Keep_Inquisition_VALUES,
                INQUISITION_CHOICES_Keep_Inquisition_LABELS,
            )

        if imgui.collapsing_header("Caretaker", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
            show_persisted_value_editor(state, "Caretaker XP", CARETAKERPROGRESSION_XP)

        if imgui.collapsing_header(
            "Current party", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            for i, follower_id_o in enumerate(state.save_game.get_party()):
                imgui.push_id(i)
                show_labeled_options_editor_in_place(
                    f"Follower {i + 1}", follower_id_o, "id", FOLLOWER_IDS, FOLLOWER_LABELS, 0
                )
                imgui.pop_id()

    imgui.end_child()

    imgui.columns(1)


def show_editor_appearances(state: State):
    data = state.save_game.get_client_rpg_extents(2)

    imgui.text_wrapped(
        "You can manually edit the following JSON documents or copy them from another save game!\n"
        + "Hint: It is probably easier to make a new character with the desired Player or Inquisitor appearance "
        + "and copy their appearance documents over than trying to modify the values below."
    )

    editor_size = (-1, imgui.get_window_size().y / 2 - 75)

    if imgui.collapsing_header(
        "Player appearance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        # https://github.com/ocornut/imgui/issues/623
        imgui.push_item_width(-1)
        changed, new_value = show_json_editor("##Player", data["playerData"], editor_size)
        if changed:
            data["playerData"] = new_value
        imgui.pop_item_width()

    if imgui.collapsing_header(
        "Inquisitor appearance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        # https://github.com/ocornut/imgui/issues/623
        imgui.push_item_width(-1)
        changed, new_value = show_json_editor("##Inquisitor", data["inquisitorData"], editor_size)
        if changed:
            data["inquisitorData"] = new_value
        imgui.pop_item_width()


def show_editor_progression(state: State, progression_properties: dict, header="Progression"):
    if header and not imgui.collapsing_header(
        header, imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        return

    for label, prop in progression_properties.items():
        if label == "State":
            changed, new_value = show_labeled_bit_flags_editor(
                label, BWFollowerStateFlag, state.save_game.get_persistence_property(prop)
            )
            if changed:
                state.save_game.set_persistence_property(prop, new_value)
        else:
            show_persisted_value_editor(state, label, prop)


def show_editor_scripts(scripts: dict, header="Scripts"):
    if header and not imgui.collapsing_header(
        header, imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        return

    for label, script in scripts.items():
        imgui.push_id(label)
        imgui.columns(2)
        imgui.text(label)
        imgui.next_column()

        imgui.set_next_item_width(-1)
        if imgui.button("Run"):
            script()

        imgui.columns(1)
        imgui.pop_id()


def show_editor_skills_list(state: State, graph: dict, persistence_key: PersistenceKey):
    if imgui.begin_table("Skills", 2, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        imgui.table_setup_column("Skill Name")
        imgui.table_setup_column("Unlocked?")
        imgui.table_headers_row()
        for skill in graph["skills"]:
            unlock_property = PersistencePropertyDefinition(
                persistence_key, skill["unlock_property_id"], "Boolean", False
            )
            imgui.push_id(skill["index"])
            imgui.table_next_row()
            imgui.table_next_column()
            imgui.text(skill["name"])
            imgui.table_next_column()
            show_persisted_value_editor(state, "", unlock_property)
            imgui.pop_id()
        imgui.end_table()


def show_editor_skills(state: State, archetype: CharacterArchetype):
    graph_id, persistence_key = ARCHETYPE_TO_SKILL_DATA[archetype]

    # see BELLARA_SKILLS_SkillPoints, ...
    skill_points = PersistencePropertyDefinition(persistence_key, 2271481620, "Uint32", 0)

    show_persisted_value_editor(state, "Skill points:", skill_points)
    show_editor_skills_list(state, SKILL_GRAPHS[graph_id], persistence_key)


def show_editor_companion_skills(state: State, archetype: CharacterArchetype):
    if imgui.collapsing_header("Skills", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        show_editor_skills(state, archetype)


def show_editor_companion_romance(state: State, romance_properties: dict):
    if imgui.collapsing_header("Romance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for label, prop in romance_properties.items():
            show_persisted_value_editor(state, label, prop)


def show_editor_companions(state: State):
    if not imgui.begin_tab_bar("companions"):
        return

    if imgui.begin_tab_item("Neve")[0]:
        show_editor_progression(state, PROGRESSION_NEVE_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_NEVE_PROPERTIES)
        show_editor_companion_skills(state, CharacterArchetype.Follower_Neve)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Davrin")[0]:
        show_editor_progression(state, PROGRESSION_DAVRIN_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_DAVRIN_PROPERTIES)
        show_editor_companion_skills(state, CharacterArchetype.Follower_Davrin)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Bellara")[0]:
        show_editor_progression(state, PROGRESSION_BELLARA_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_BELLARA_PROPERTIES)
        show_editor_companion_skills(state, CharacterArchetype.Follower_Bellara)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Taash")[0]:
        show_editor_progression(state, PROGRESSION_TAASH_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_TAASH_PROPERTIES)
        show_editor_companion_skills(state, CharacterArchetype.Follower_Taash)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Emmrich")[0]:
        show_editor_progression(state, PROGRESSION_EMMRICH_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_EMMRICH_PROPERTIES)
        show_editor_scripts(
            {
                'Force-start "Will and Testament" quest': lambda: force_complete_quest(
                    state.save_game, EMMRICH_M23_LICHBECOMING
                ),
                'Force-start "Heir to the Dead" quest': lambda: force_complete_quest(
                    state.save_game, EMMRICH_M23_MANFREDREVIVE
                ),
            }
        )
        show_editor_companion_skills(state, CharacterArchetype.Follower_Emmrich)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Harding")[0]:
        show_editor_progression(state, PROGRESSION_HARDING_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_HARDING_PROPERTIES)
        show_editor_companion_skills(state, CharacterArchetype.Follower_Harding)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Lucanis")[0]:
        show_editor_progression(state, PROGRESSION_LUCANIS_PROPERTIES)
        show_editor_companion_romance(state, ROMANCE_LUCANIS_PROPERTIES)
        show_editor_scripts(
            {
                'Force-start "Inner Demons" quest': lambda: force_complete_quest(state.save_game, LUCANIS_M21),
                'Force-start "A Moment\'s Peace" quest': lambda: force_complete_quest(state.save_game, LUCANIS_M23),
            }
        )
        show_editor_companion_skills(state, CharacterArchetype.Follower_Lucanis)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Misc")[0]:
        if imgui.collapsing_header(
            "Harding & Taash", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            for label, prop in HARDING_AND_TASH_PROPERTIES.items():
                show_persisted_value_editor(state, label, prop)
        if imgui.collapsing_header(
            "Lucanis & Neve", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            for label, prop in LUCANIS_AND_NEVE_PROPERTIES.items():
                show_persisted_value_editor(state, label, prop)
        if imgui.collapsing_header(
            "Emmrich & Strife", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            for label, prop in EMMRICH_AND_STRIFE_PROPERTIES.items():
                show_persisted_value_editor(state, label, prop)
        imgui.end_tab_item()

    imgui.end_tab_bar()


def show_editor_collectibles(state: State):
    imgui.text_wrapped(
        "All collectibles (appearances, ...) are organized into sets. "
        + "Select the appropriate set to view & edit all collectibles inside.\n"
        + "Note: This includes many quest / storyline items and states that you probably shouldn't touch."
    )

    imgui.text_disabled("Quick actions:")
    imgui.same_line()
    if imgui.button("Grant all appearances"):
        for collectibles_set in COLLECTIBLES:
            if collectibles_set["name"].startswith("CollectibleAppearanceParts"):
                persistence_key = registered_persistence_key(collectibles_set["definition_id"])
                for collectible in collectibles_set["collectibles"]:
                    flags_property = PersistencePropertyDefinition(persistence_key, collectible["id"], "Uint8", 0)
                    flags = state.save_game.get_persistence_property(flags_property) or 0
                    flags |= CollectibleSetFlag.IsCollected
                    state.save_game.set_persistence_property(flags_property, flags)

    imgui.text_disabled("Collectibles Set:")
    imgui.same_line()
    imgui.set_next_item_width(-1)
    changed, new_index = show_searchable_combo_box(
        "##CollectiblesSet", COLLECTIBLE_LABELS, state.selected_collectible_set_index
    )
    if changed:
        state.selected_collectible_set_index = new_index

    collectibles_set = COLLECTIBLES[state.selected_collectible_set_index]
    persistence_key = registered_persistence_key(collectibles_set["definition_id"])

    if not imgui.begin_table("Collectibles", 2, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        return

    imgui.table_setup_column("Collectible Name")
    imgui.table_setup_column("Is collected?")
    imgui.table_headers_row()
    for collectible in collectibles_set["collectibles"]:
        flags_property = PersistencePropertyDefinition(persistence_key, collectible["id"], "Uint8", 0)
        flags = state.save_game.get_persistence_property(flags_property) or 0

        push_int_id(collectible["id"])
        imgui.table_next_row()
        imgui.table_next_column()
        imgui.text(collectible["name"])
        imgui.table_next_column()
        changed, new_value = show_bit_flags_editor(CollectibleSetFlag, flags)
        if changed:
            state.save_game.set_persistence_property(flags_property, new_value)
        imgui.pop_id()

    imgui.end_table()


def show_editor_factions(state: State):
    if not imgui.begin_tab_bar("factions"):
        return

    if imgui.begin_tab_item("The Mourn Watch")[0]:
        show_editor_progression(state, FACTION_MOURNWATCH_PROPERTIES)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Antivan Crows")[0]:
        show_editor_progression(state, FACTION_ANTIVANCROWS_PROPERTIES)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Lords Of Fortune")[0]:
        show_editor_progression(state, FACTION_LORDSOFFORTUNE_PROPERTIES)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Veil Jumpers")[0]:
        show_editor_progression(state, FACTION_VEILJUMPERS_PROPERTIES)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Grey Wardens")[0]:
        show_editor_progression(state, FACTION_GREYWARDENS_PROPERTIES)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Shadow Dragons")[0]:
        show_editor_progression(state, FACTION_SHADOWDRAGONS_PROPERTIES)
        imgui.end_tab_item()

    imgui.end_tab_bar()


def show_editor_persistence(state: State):
    imgui.text_wrapped(
        "This list contains all persistence objects the game contains.\n"
        + "Note: This includes many internal quests and states that you probably shouldn't touch."
    )

    imgui.text_disabled("Persistence definition:")
    imgui.same_line()
    imgui.set_next_item_width(-1)
    changed, new_index = show_searchable_combo_box(
        "##PersistenceDefinitions", PERSISTENCE_DEFINITION_LABELS, state.selected_definition_index
    )
    if changed:
        state.selected_definition_index = new_index
        state.selected_instance_index = 0

    persistence_definition = ALL_PERSISTENCE_DEFINITIONS[state.selected_definition_index]
    def_id = persistence_definition["id"]
    quest_info = PERSISTENCE_DEFINITION_TO_QUEST.get(def_id)

    # display some properties:
    imgui.text_disabled("Definition Id:")
    imgui.same_line()
    imgui.text(str(def_id))

    imgui.text_disabled("Definition Version:")
    imgui.same_line()
    imgui.text(str(persistence_definition["version"]))

    if quest_info:
        imgui.text_disabled("Quest Id:")
        imgui.same_line()
        imgui.text(str(quest_info["id"]))
        imgui.text_disabled("Journal Id:")
        imgui.same_line()
        imgui.text(str(quest_info["journal_id"]))
    # end of properties

    persistence_instances = state.save_game.get_persistence_instances_by_id(def_id)
    persistence_instance = None
    if len(persistence_instances) > 1:
        imgui.text_disabled("Persistence instance:")
        imgui.same_line()
        imgui.set_next_item_width(-1)
        changed, new_index = show_searchable_combo_box(
            "##PersistenceInstances", [pi["Key"] for pi in persistence_instances], state.selected_instance_index
        )
        if changed:
            state.selected_instance_index = new_index
        persistence_instance = persistence_instances[state.selected_instance_index]
    elif persistence_instances:
        persistence_instance = persistence_instances[0]

    if not imgui.begin_table("Properties", 2, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        return

    imgui.table_setup_column("Property name")
    imgui.table_setup_column("Value")
    imgui.table_headers_row()
    for property_info in persistence_definition["properties"]:
        prop_id = property_info["id"]
        prop_type = property_info["type"]
        prop_default = property_info["default"]

        push_int_id(prop_id)

        imgui.table_next_row()
        imgui.table_next_column()
        imgui.text(property_info["name"])
        imgui.table_next_column()

        value = prop_default
        if persistence_instance is not None:
            value = get_persisted_value(persistence_instance, prop_id, prop_type, prop_default)

        if quest_info and property_info["name"] == "_QuestState":
            changed, new_value = show_bit_flags_editor(EcoQuestRegisteredStateFlags, value)
        else:
            changed, new_value = show_value_editor(value)

        if changed:
            if persistence_instance is None:
                persistence_instance = state.save_game.make_persistence_instance(registered_persistence_key(def_id))
            set_persisted_value(persistence_instance, prop_id, prop_type, new_value)

        imgui.pop_id()

    imgui.end_table()


def show_editor_content(state: State):
    if not imgui.begin_tab_bar("editors"):
        return

    if imgui.begin_tab_item("Main")[0]:
        show_editor_main(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Skills")[0]:
        show_editor_skills(state, state.save_game.meta["projdata"]["archetype"])
        imgui.end_tab_item()

    if imgui.begin_tab_item("Appearances")[0]:
        show_editor_appearances(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Companions")[0]:
        show_editor_companions(state)
        imgui.end_tab_item()

    # This isn't just "Quests" but people might find that label easier!
    if imgui.begin_tab_item("Quests")[0]:
        show_editor_persistence(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Inventories")[0]:
        show_editor_inventories(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Collectibles")[0]:
        show_editor_collectibles(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Factions")[0]:
        show_editor_factions(state)
        imgui.end_tab_item()

    if imgui.begin_tab_item("Raw Data")[0]:
        show_editor_raw_data(state.save_game)
        imgui.end_tab_item()

    imgui.end_tab_bar()


def show_empty_warning(state: State):
    imgui.push_style_var(imgui.StyleVar_.selectable_text_align, (0.5, 0.5))

    default_save_path_message = "No Dragon Age: Veilguard save games have been found."
    if state.default_save_path:
        default_save_path_message = "Your Dragon Age: Veilguard save games can be found at:\n"
        default_save_path_message += os.path.normpath(state.default_save_path)

    if imgui.selectable(
        "Welcome to the DA:V Save Editor - By Tim & mons\n\n"
        + "No save file loaded!\nClick here or use the menu to load or import files.\n\n"
        + default_save_path_message,
        False,
    )[0]:
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


def main():
    state = State()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        state.load(filename)

    immapp.run(gui_function=lambda: show_ui(state), window_title=WINDOW_TITLE)
