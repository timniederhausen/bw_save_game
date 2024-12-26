import ctypes
import json
import typing
from uuid import UUID

from imgui_bundle import imgui

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


def _wrap_bytes_for_imgui(buffer: bytearray):
    raw = (ctypes.c_ubyte * len(buffer)).from_buffer(buffer)
    return PyCapsule_New(raw, _NANOBIND_VOIDP_CAPSULE_TYPE, PyCapsule_Destructor(0))


def show_json_editor(label: str, value):
    changed, new_value = imgui.input_text_multiline(label, json.dumps(value, indent=2, default=to_raw_dict))
    error = None
    if changed:
        try:
            return True, json.loads(new_value, object_hook=from_raw_dict)
        except ValueError as e:
            error = repr(e)
    if error is not None:
        imgui.text_colored((0.9, 0.01, 0.01, 1.0), f"ERROR: {error}")
    return False, None


def show_uuid_editor(label: str, value: UUID):
    changed, new_value = imgui.input_text(label, str(value))
    error = None
    if changed:
        try:
            return True, UUID(hex=new_value)
        except ValueError as e:
            error = repr(e)
    if error is not None:
        imgui.text_colored((0.9, 0.01, 0.01, 1.0), f"ERROR: {error}")
    return False, None


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
    capsule = _wrap_bytes_for_imgui(new_value)
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
        changed, new_value = show_uuid_editor(f"##{key}", value)
        if changed:
            obj[key] = new_value
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

    changed = show_raw_value_editor(obj, key, value)

    imgui.columns(1)
    return changed


def show_key_value_options_editor(
    label: str, obj, key, option_values: list, option_names: list[str], default_option_index: int = 0
):
    value = obj.get(key)
    if value is None:
        value = option_values[default_option_index]
    native_value = to_native(value)

    imgui.columns(2)
    imgui.text(label)
    imgui.next_column()

    current_item = None
    for i, option in enumerate(option_values):
        if option == native_value:
            current_item = i

    if current_item is None:
        current_item = default_option_index

    changed, current_item = show_searchable_combo_box(f"##{key}", option_names, current_item)
    if changed:
        obj[key] = option_values[current_item]

    imgui.columns(1)
    return changed