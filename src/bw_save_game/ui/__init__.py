#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import ctypes
import json
import sys
import typing  # noqa: F401
from uuid import UUID

from imgui_bundle import imgui, immapp, portable_file_dialogs

from bw_save_game import (
    __version__,
    dumps,
    loads,
    read_save_from_reader,
    write_save_to_writer,
)
from bw_save_game.db_object import Double, Long, from_raw_dict, to_native, to_raw_dict
from bw_save_game.db_object_codec import (
    double_struct,
    float_struct,
    int32_struct,
    int64_struct,
)
from bw_save_game.ui.widgets import show_searchable_combo_box

# imgui_bundle has automatically generated bindings that mishandle void*
# by requiring capsules instead of the raw bytes the actual imgui API wants.
PyCapsule_Destructor = ctypes.CFUNCTYPE(None, ctypes.py_object)
PyCapsule_New = ctypes.pythonapi.PyCapsule_New
PyCapsule_New.restype = ctypes.py_object
PyCapsule_New.argtypes = (ctypes.c_void_p, ctypes.c_char_p, PyCapsule_Destructor)

_NANOBIND_VOIDP_CAPSULE_TYPE = b"nb_handle"


def wrap_bytes_for_imgui(buffer: bytearray):
    raw = (ctypes.c_ubyte * len(buffer)).from_buffer(buffer)
    return PyCapsule_New(raw, _NANOBIND_VOIDP_CAPSULE_TYPE, PyCapsule_Destructor(0))


# https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python/9319832#9319832
def get_path(message, wildcard, is_save=False):
    if is_save:
        return portable_file_dialogs.save_file(title=message, filters=wildcard.split("|"))
    return portable_file_dialogs.open_file(title=message, filters=wildcard.split("|"))


def show_error(message: str):
    print(message)
    portable_file_dialogs.message("Error", message, portable_file_dialogs.choice.ok).ready(900)


_PERSISTENCE_TYPES = {
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


def get_or_create_persisted_value(family: dict, id: int, typ: str):
    key = f",{id}:{typ}"

    all_props = family["PropertyValueData"]["DefinitionProperties"]
    found_prop = None
    for prop in all_props:
        if key in prop:
            found_prop = prop
    if found_prop is None:
        found_prop = {key: _PERSISTENCE_TYPES[typ]()}
        all_props.append(found_prop)
    return found_prop, key


class State(object):
    def __init__(self):
        # UI state
        self.show_app_about = False
        self.open_csav_dialog = None  # type: typing.Optional[portable_file_dialogs.open_file]
        self.open_json_dialog = None  # type: typing.Optional[portable_file_dialogs.open_file]
        self.save_csav_dialog = None  # type: typing.Optional[portable_file_dialogs.save_file]
        self.save_json_dialog = None  # type: typing.Optional[portable_file_dialogs.save_file]

        # loaded save game
        self.active_filename = None  # type: typing.Optional[str]
        self.active_meta = None  # type: typing.Optional[dict]
        self.active_data = None  # type: typing.Optional[dict]

        with open("item_list.json", "r", encoding="utf-8") as f:
            self.item_list = json.load(f)

        self.item_id_to_index = {}
        for i, item in enumerate(self.item_list):
            item["key"] = f"{item['name' or 'NO NAME']} ({item['id']})"
            item["guid"] = UUID(item["guid"])
            self.item_id_to_index[item["id"]] = i

        with open("currencies.json", "r", encoding="utf-8") as f:
            self.currencies = json.load(f)

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

    def get_persisted_definition_family(self, family_id: int) -> typing.Optional[dict]:
        for family in self.get_persisted_definitions():
            if to_native(family["DefinitionId"]) == family_id:
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
            state.open_csav_dialog = get_path("Open Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav")

        clicked, selected = imgui.menu_item(label="Import JSON", shortcut="", p_selected=False)
        if clicked:
            state.open_json_dialog = get_path("Open JSON Save Game", "JSON document (*.json)|*.json")

        clicked, selected = imgui.menu_item(
            label="Save", shortcut="Ctrl+S", p_selected=False, enabled=state.active_filename is not None
        )
        if clicked and state.active_filename:
            state.save(state.active_filename)

        clicked, selected = imgui.menu_item(
            label="Save As...", shortcut="", p_selected=False, enabled=state.has_content()
        )
        if clicked:
            state.save_csav_dialog = get_path(
                "Write Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav", is_save=True
            )

        clicked, selected = imgui.menu_item(
            label="Export JSON", shortcut="", p_selected=False, enabled=state.has_content()
        )
        if clicked:
            state.save_json_dialog = get_path("Export JSON save game", "JSON document (*.json)|*.json", is_save=True)

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


def show_numeric_value_editor(obj, key, value):
    typ = None
    encoded_value = None
    if isinstance(value, int):
        if value < 0:
            encoded_value = int32_struct.pack(value)
            typ = imgui.DataType_.s32
        else:
            encoded_value = int64_struct.pack(value)
            typ = imgui.DataType_.s64
    if isinstance(value, Long):
        encoded_value = int64_struct.pack(value.value)
        typ = imgui.DataType_.s64
    if isinstance(value, float):
        encoded_value = float_struct.pack(value)
        typ = imgui.DataType_.float
    if isinstance(value, Double):
        encoded_value = double_struct.pack(value.value)
        typ = imgui.DataType_.double

    if typ is None:
        # not numeric
        return False, False

    new_value = bytearray(encoded_value)
    capsule = wrap_bytes_for_imgui(new_value)
    changed = imgui.input_scalar(f"##{key}", typ, capsule)
    if not changed:
        return True, False  # nothing to do

    if isinstance(value, int):
        if typ == imgui.DataType_.s64:
            obj[key] = int64_struct.unpack(new_value)[0]
        else:
            obj[key] = int32_struct.unpack(new_value)[0]
    if isinstance(value, Long):
        obj[key] = Long(int64_struct.unpack(new_value)[0])
    if isinstance(value, float):
        obj[key] = float_struct.unpack(new_value)[0]
    if isinstance(value, Double):
        obj[key] = Double(double_struct.unpack(new_value)[0])
    return True, True


def show_raw_value_editor(obj: typing.MutableMapping, key, value=None):
    if value is None:
        value = obj[key]

    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)

    supported = False
    if isinstance(value, bool):
        changed, new_value = imgui.checkbox(f"##{key}", value)
        if changed:
            obj[key] = new_value
        supported = True

    if not supported:
        supported, changed = show_numeric_value_editor(obj, key, value)

    if not supported and isinstance(value, str):
        changed, new_value = imgui.input_text(f"##{key}", value)
        if changed:
            obj[key] = new_value
        supported = True

    if not supported and isinstance(value, UUID):
        changed, new_value = imgui.input_text(f"##{key}", str(value))
        if changed:
            try:
                obj[key] = UUID(hex=new_value)
            except ValueError:
                # just ignore it, the user needs to know what they're doing here
                pass
        supported = True

    imgui.pop_item_width()

    if not supported:
        raise TypeError(f"Unsupported type {type(value)}")
    return changed


def show_raw_key_value_editor(obj, key, label=None):
    value = obj[key]
    if label is None:
        label = str(key)

    if isinstance(value, (dict, list)):
        is_open, is_removed = imgui.collapsing_header(label, True, imgui.TreeNodeFlags_.allow_overlap)
        if not is_open:
            return

        imgui.indent()
        if isinstance(value, dict):
            for sub_key in value:
                imgui.push_id(sub_key)
                show_raw_key_value_editor(value, sub_key)
                imgui.pop_id()
        if isinstance(value, list):
            for sub_key in range(len(value)):
                imgui.push_id(sub_key)
                show_raw_key_value_editor(value, sub_key)
                imgui.pop_id()
        imgui.unindent()
        return

    imgui.columns(2)
    imgui.text(label)
    imgui.next_column()

    show_raw_value_editor(obj, key, value)

    imgui.columns(1)


def show_key_value_options_editor(label: str, obj, key, options: typing.List[dict], default: int = 0):
    value = obj[key]
    native_value = to_native(value)

    imgui.columns(2)
    imgui.text(label)
    imgui.next_column()

    current_item = None
    for i, option in enumerate(options):
        if to_native(option["value"]) == native_value:
            current_item = i

    if current_item is None:
        current_item = default

    changed, current_item = show_searchable_combo_box(f"##{key}", options, lambda o: o["label"], current_item)
    if changed:
        obj[key] = options[current_item]["value"]

    imgui.columns(1)


def show_item_id_editor(state: State, obj):
    index = state.item_id_to_index.get(to_native(obj["itemDataId"]))
    if index is not None:
        # https://github.com/ocornut/imgui/issues/623
        imgui.push_item_width(-1)
        changed, new_index = show_searchable_combo_box("##itemDataId", state.item_list, lambda item: item["key"], index)
        imgui.pop_item_width()

        if changed:
            data = state.item_list[new_index]
            obj["itemDataId"] = Long(data["id"])
            obj["dataGuid"] = data["guid"]
    else:
        imgui.text(to_native(obj["itemDataId"]))
        # oh well
        # show_simple_value_editor(obj, "itemDataId")


def show_persisted_value_editor(state: State, label: str, family_id: int, id: int, typ: str):
    family = state.get_persisted_definition_family(family_id)
    if not family:
        return

    obj, key = get_or_create_persisted_value(family, id, typ)
    show_raw_key_value_editor(obj, key, label)


def show_persisted_value_options_editor(
    state: State, label: str, family_id: int, id: int, typ: str, options: typing.List[dict], default: int = 0
):
    family = state.get_persisted_definition_family(family_id)
    if not family:
        return

    obj, key = get_or_create_persisted_value(family, id, typ)
    show_key_value_options_editor(label, obj, key, options, default)


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


def show_editor_inventories(state: State):
    items = state.get_items()

    imgui.text(f"Number of items: {len(items)}")
    if imgui.begin_table("Items", 5, imgui.TableFlags_.resizable | imgui.TableFlags_.borders):
        imgui.table_setup_column("Item")
        imgui.table_setup_column("Parent")
        imgui.table_setup_column("Slot")
        imgui.table_setup_column("Amount")
        imgui.table_setup_column("Rarity")
        imgui.table_headers_row()
        for i, item in enumerate(items):
            imgui.push_id(i)
            imgui.table_next_row()
            imgui.table_next_column()
            show_item_id_editor(state, item)
            imgui.table_next_column()
            imgui.text(str(item.get("parent")))
            imgui.table_next_column()
            if "attachSlot" in item:
                show_raw_value_editor(item, "attachSlot")
            else:
                imgui.text("n/a")
            imgui.table_next_column()
            if "stackCount" in item:
                show_raw_value_editor(item, "stackCount")
            else:
                imgui.text("n/a")
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


# Globals/Persistence/InquisitorGeneratorDataAsset
_PAST_DA_INQUISITOR_FAMILY_ID = 1250272560
# DesignContent/PlotLogic/Global/PastDAChoices/UseReferences/Reference_Past_DA_fc
_PAST_DA_SHOULD_REFERENCE_PROPERTY_ID = 746726984, "Boolean"
_PAST_DA_INQUISITOR_ROMANCE_PROPERTY_ID = 3170937725, "Int32"
_PAST_DA_INQUISITOR_ROMANCE_OPTIONS = [
    # DesignContent/PlotLogic/Global/PastDAChoices/InquisitorRomance/...
    dict(value=1, label="Blackwall"),
    dict(value=2, label="Cassandra"),
    dict(value=3, label="Cullen"),
    dict(value=4, label="Dorian"),
    dict(value=5, label="IronBull"),
    dict(value=6, label="Josephine"),
    dict(value=7, label="Sera"),
    dict(value=8, label="Solas"),
]


def show_editor_main(state: State):
    imgui.columns(2)

    if imgui.begin_child("##first column"):
        if imgui.collapsing_header(
            "Player character", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            imgui.text("TODO")

        if imgui.collapsing_header(
            "Currencies", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            show_currency_editor(state)
    imgui.end_child()

    imgui.next_column()

    if imgui.begin_child("##second column"):
        if imgui.collapsing_header(
            "Inquisitor", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
        ):
            show_persisted_value_editor(
                state, "Reference past DA?", _PAST_DA_INQUISITOR_FAMILY_ID, *_PAST_DA_SHOULD_REFERENCE_PROPERTY_ID
            )
            show_persisted_value_options_editor(
                state,
                "Romance option",
                _PAST_DA_INQUISITOR_FAMILY_ID,
                *_PAST_DA_INQUISITOR_ROMANCE_PROPERTY_ID,
                _PAST_DA_INQUISITOR_ROMANCE_OPTIONS,
                7,
            )
    imgui.end_child()

    imgui.columns(1)


def show_editor_appearances(state: State):
    data = state.get_client_rpg_extents(2)

    if imgui.collapsing_header(
        "Player appearance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        imgui.push_item_width(-1)
        changed, new_value = imgui.input_text_multiline(
            "##Player", json.dumps(data["playerData"], indent=2, default=to_raw_dict)
        )
        imgui.pop_item_width()
        if changed:
            data["playerData"] = json.loads(new_value, object_hook=from_raw_dict)

    if imgui.collapsing_header(
        "Inquisitor appearance", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap
    ):
        imgui.push_item_width(-1)
        changed, new_value = imgui.input_text_multiline(
            "##Inquisitor", json.dumps(data["inquisitorData"], indent=2, default=to_raw_dict)
        )
        imgui.pop_item_width()
        if changed:
            data["playerData"] = json.loads(new_value, object_hook=from_raw_dict)


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

    def process_open_dialog(dlg: portable_file_dialogs.open_file, fn):
        if dlg and dlg.ready():
            res = dlg.result()
            if res:
                print(res)
                fn(res[0])
            return True
        return False

    def process_save_dialog(dlg: portable_file_dialogs.save_file, fn):
        if dlg and dlg.ready():
            res = dlg.result()
            if res:
                print(res)
                fn(res)
            return True
        return False

    if process_open_dialog(state.open_csav_dialog, state.load):
        state.open_csav_dialog = None
    if process_open_dialog(state.open_json_dialog, state.import_json):
        state.open_json_dialog = None
    if process_save_dialog(state.save_csav_dialog, state.save):
        state.save_csav_dialog = None
    if process_save_dialog(state.save_json_dialog, state.export_json):
        state.save_json_dialog = None


def main():
    state = State()
    immapp.run(gui_function=lambda: show_ui(state), window_title=WINDOW_TITLE)


if __name__ == "__main__":
    main()
