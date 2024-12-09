#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import sys
import typing  # noqa: F401
from uuid import UUID

import imgui
import pyglet
import wx

# Note that we could explicitly choose to use PygletFixedPipelineRenderer
# or PygletProgrammablePipelineRenderer, but create_renderer handles the
# version checking for us.
from imgui.integrations.pyglet import create_renderer

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


# https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python/9319832#9319832
def get_path(message, wildcard, is_save=False):
    style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT if is_save else wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, message, wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path


class State(object):
    def __init__(self):
        self.app = wx.App(None)

        # UI state
        self.show_app_about = False

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
            wx.MessageBox(f"Cannot load {filename}: {repr(e)}")
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
            wx.MessageBox(f"Cannot save {filename}: {repr(e)}")
            return
        self.active_filename = filename

    def import_json(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                doc = json.load(f, object_hook=from_raw_dict)
        except Exception as e:
            wx.MessageBox(f"Cannot load {filename}: {repr(e)}")
            return

        try:
            m = doc["meta"]
            d = doc["data"]
        except KeyError as e:
            wx.MessageBox(f"{filename} doesn't have the correct JSON structure.\n{e} is missing.")
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
            wx.MessageBox(f"Cannot save {filename}: {repr(e)}")
            return


def show_app_about(state: State):
    if not state.show_app_about:
        return  # nothing to do

    is_expand, state.show_app_about = imgui.begin(
        label="About BWSaveGameEditor",
        closable=state.show_app_about,
        flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE,
    )
    if is_expand:
        imgui.text("BWSaveGameEditor " + __version__)
        imgui.separator()
        imgui.text("By Tim and mons.")
        imgui.text("BWSaveGameEditor is licensed under GNU General Public License v3.0.")
        imgui.separator()
        imgui.text("Using ImGui, " + imgui.get_version())
    imgui.end()


def show_main_menu_bar(state: State):
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked, selected = imgui.menu_item(label="Open", shortcut="Ctrl+O")
            if clicked:
                path = get_path("Open Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav")
                if path:
                    state.load(path)

            clicked, selected = imgui.menu_item(label="Import JSON")
            if clicked:
                path = get_path("Open JSON Save Game", "JSON document (*.json)|*.json")
                if path:
                    state.import_json(path)

            clicked, selected = imgui.menu_item(
                label="Save", shortcut="Ctrl+S", enabled=state.active_filename is not None
            )
            if clicked and state.active_filename:
                state.save(state.active_filename)

            clicked, selected = imgui.menu_item(label="Save As...", enabled=state.has_content())
            if clicked:
                path = get_path("Write Save Game", "Dragon Age: Veilguard save files (*.csav)|*.csav", is_save=True)
                if path:
                    state.save(path)

            clicked, selected = imgui.menu_item(label="Export JSON", enabled=state.has_content())
            if clicked:
                path = get_path("Export JSON save game", "JSON document (*.json)|*.json", is_save=True)
                if path:
                    state.export_json(path)

            clicked, selected = imgui.menu_item("Quit", "Cmd+Q", False, True)
            if clicked:
                sys.exit(0)

            imgui.end_menu()
        if imgui.begin_menu("Help", True):
            clicked, state.show_app_about = imgui.menu_item(
                label="About BWSaveGameEditor", shortcut=None, selected=state.show_app_about
            )
            imgui.end_menu()

        imgui.end_main_menu_bar()


def show_numeric_value_editor(obj, key, value, label: str):
    typ = None
    encoded_value = None
    if isinstance(value, int):
        if value < 0:
            encoded_value = int32_struct.pack(value)
            typ = imgui.DATA_TYPE_S32
        else:
            encoded_value = int64_struct.pack(value)
            typ = imgui.DATA_TYPE_S64
    if isinstance(value, Long):
        encoded_value = int64_struct.pack(value.value)
        typ = imgui.DATA_TYPE_S64
    if isinstance(value, float):
        encoded_value = float_struct.pack(value)
        typ = imgui.DATA_TYPE_FLOAT
    if isinstance(value, Double):
        encoded_value = double_struct.pack(value.value)
        typ = imgui.DATA_TYPE_DOUBLE

    if typ is None:
        # not numeric
        return False

    changed, new_value = imgui.input_scalar(
        f"##{key}",
        typ,
        encoded_value,
        flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE,
    )
    if not changed:
        return True  # nothing to do

    if isinstance(value, int):
        if typ == imgui.DATA_TYPE_S64:
            obj[key] = int64_struct.unpack(new_value)[0]
        else:
            obj[key] = int32_struct.unpack(new_value)[0]
    if isinstance(value, Long):
        obj[key] = Long(int64_struct.unpack(new_value)[0])
    if isinstance(value, float):
        obj[key] = float_struct.unpack(new_value)[0]
    if isinstance(value, Double):
        obj[key] = Double(double_struct.unpack(new_value)[0])


def show_simple_value_editor(key, label, obj, value):
    supported = show_numeric_value_editor(obj, key, value, label)
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
    if not supported:
        raise TypeError(f"Unsupported type {type(value)}")


def _ordered_keys(value: dict):
    return sorted(value.keys(), key=lambda x: (isinstance(value[x], dict), x))


def show_value_editor(obj, key):
    value = obj[key]
    label = str(key)

    if isinstance(value, (dict, list)):
        is_open, is_removed = imgui.collapsing_header(label, True, imgui.TREE_NODE_ALLOW_ITEM_OVERLAP)
        if not is_open:
            return

        imgui.indent()
        if isinstance(value, dict):
            for sub_key in _ordered_keys(value):
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

    show_simple_value_editor(key, label, obj, value)

    imgui.columns(1)


def show_editor_raw_data(state: State):
    if imgui.collapsing_header("Metadata", None, imgui.TREE_NODE_DEFAULT_OPEN | imgui.TREE_NODE_ALLOW_ITEM_OVERLAP)[0]:
        for key in state.active_meta.keys():
            show_value_editor(state.active_meta, key)
    imgui.separator()
    if imgui.collapsing_header("Content", None, imgui.TREE_NODE_DEFAULT_OPEN | imgui.TREE_NODE_ALLOW_ITEM_OVERLAP)[0]:

        for key in state.active_data.keys():
            show_value_editor(state.active_data, key)


def show_editor_content(state: State):
    with imgui.begin_tab_bar("editors") as tab_bar:
        if not tab_bar.opened:
            return

        with imgui.begin_tab_item("Raw Data") as raw_data:
            if raw_data.selected:
                show_editor_raw_data(state)


def show_empty_warning():
    imgui.push_style_var(imgui.STYLE_SELECTABLE_TEXT_ALIGN, (0.5, 0.5))
    imgui.selectable("No save file loaded!")
    imgui.pop_style_var()


def show_editor_window(state: State):
    vp = imgui.get_main_viewport()

    imgui.set_next_window_position(*vp.work_pos)
    imgui.set_next_window_size(*vp.work_size)

    if imgui.begin(
        "editor_content", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE
    ):
        if state.has_content():
            show_editor_content(state)
        else:
            show_empty_warning()

        imgui.end()


WINDOW_TITLE = "Dragon Age: The Veilguard save editor by Tim & mons"


def main():
    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    pyglet.gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = create_renderer(window)

    state = State()

    # from testwindow import show_test_window
    def update(dt):
        impl.process_inputs()
        imgui.new_frame()

        show_main_menu_bar(state)
        show_app_about(state)
        show_editor_window(state)
        # show_test_window()

        active_caption = state.active_filename if state.active_filename else WINDOW_TITLE
        if window.caption != active_caption:
            window.set_caption(active_caption)

    def draw(dt):
        update(dt)
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.clock.schedule_interval(draw, 1 / 120.0)
    pyglet.app.run()
    impl.shutdown()


if __name__ == "__main__":
    main()
