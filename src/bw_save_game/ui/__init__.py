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
from bw_save_game.db_object import Double, Long, from_raw_dict, to_raw_dict
from bw_save_game.db_object_codec import (
    double_struct,
    float_struct,
    int32_struct,
    int64_struct,
)

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
    def get_server_extents(self):
        return filter(lambda c: c["name"] == "RPGPlayerExtent", self.active_data["server"]["contributors"])

    def get_items(self):
        for extent in self.get_server_extents():
            if "items" in extent["data"]:
                return extent["data"]["items"]
        raise ValueError("Server section doesn't have items")


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
        return False

    new_value = bytearray(encoded_value)
    capsule = wrap_bytes_for_imgui(new_value)
    changed = imgui.input_scalar(f"##{key}", typ, capsule)
    if not changed:
        return True  # nothing to do

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
    return True


def show_simple_value_editor(obj: typing.MutableMapping, key, value=None):
    if value is None:
        value = obj[key]

    # https://github.com/ocornut/imgui/issues/623
    imgui.push_item_width(-1)

    supported = show_numeric_value_editor(obj, key, value)
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


def _ordered_keys(value: dict):
    return sorted(value.keys(), key=lambda x: (isinstance(value[x], dict), x))


def show_value_editor(obj, key):
    value = obj[key]
    label = str(key)

    if isinstance(value, (dict, list)):
        is_open, is_removed = imgui.collapsing_header(label, True, imgui.TreeNodeFlags_.allow_overlap)
        if not is_open:
            return

        imgui.indent()
        if isinstance(value, dict):
            for sub_key in value:
                imgui.push_id(sub_key)
                show_value_editor(value, sub_key)
                imgui.pop_id()
        if isinstance(value, list):
            for sub_key in range(len(value)):
                imgui.push_id(str(sub_key))
                show_value_editor(value, sub_key)
                imgui.pop_id()
        imgui.unindent()
        return

    imgui.columns(2)
    imgui.text(label)
    imgui.next_column()

    show_simple_value_editor(obj, key, value)

    imgui.columns(1)


def show_editor_raw_data(state: State):
    if imgui.collapsing_header("Metadata", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in state.active_meta:
            imgui.push_id(key)
            show_value_editor(state.active_meta, key)
            imgui.pop_id()
    imgui.separator()
    if imgui.collapsing_header("Content", imgui.TreeNodeFlags_.default_open | imgui.TreeNodeFlags_.allow_overlap):
        for key in state.active_data.keys():
            imgui.push_id(key)
            show_value_editor(state.active_data, key)
            imgui.pop_id()


def show_editor_inventories(state):
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
            imgui.push_id(str(i))
            imgui.table_next_row()
            imgui.table_next_column()
            show_simple_value_editor(item, "itemDataId")
            imgui.table_next_column()
            imgui.text(str(item["parent"]))
            imgui.table_next_column()
            show_simple_value_editor(item, "attachSlot")
            imgui.table_next_column()
            if "stackCount" in item:
                show_simple_value_editor(item, "stackCount")
            else:
                imgui.text("n/a")
            imgui.table_next_column()
            imgui.text(str(item.get("rarity")))
            imgui.pop_id()
        imgui.end_table()


def show_editor_content(state: State):
    if not imgui.begin_tab_bar("editors"):
        return

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
