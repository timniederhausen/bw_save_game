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
import re
from dataclasses import dataclass

from imgui_bundle import imgui


@dataclass
class ComboBoxState:
    search_pattern = None
    filtered_items: list[int] = None
    shown_this_frame = True


# retained state
used_combo_boxes = {}  # type: dict[int, ComboBoxState]


def clear_unused_retained_data():
    global used_combo_boxes
    used_combo_boxes = {k: v for k, v in used_combo_boxes.items() if v.shown_this_frame}
    for v in used_combo_boxes.values():
        v.shown_this_frame = False


def show_regex_input(label: str, pattern: str):
    changed, new_value = imgui.input_text(label, pattern)
    if changed:
        try:
            compiled_pattern = re.compile(new_value, re.IGNORECASE)
            return changed, new_value, compiled_pattern
        except re.error as e:
            imgui.text_colored((0.9, 0.01, 0.01, 1.0), f"REGEX ERROR: {e}")

    return False, None, None


def show_searchable_combo_box(
    label: str,
    items: list[str],
    current_item: int,
):
    ctx = imgui.get_current_context()

    window = imgui.internal.get_current_window()
    if window.skip_items:
        return False, current_item

    preview_value = items[current_item]

    id = window.get_id(label)
    popup_id = imgui.internal.im_hash_str("##ComboPopup", 0, id)

    global used_combo_boxes
    retained_data = used_combo_boxes.get(id)
    if retained_data is None:
        retained_data = ComboBoxState()
    else:
        retained_data.shown_this_frame = True

    is_already_open = imgui.internal.is_popup_open(popup_id, 0)

    if not imgui.begin_combo(label, preview_value, imgui.ComboFlags_.height_largest):
        used_combo_boxes[id] = retained_data

        # Show tooltips in case our preview value is too long for the inline preview
        if imgui.begin_item_tooltip():
            imgui.text(preview_value)
            imgui.end_tooltip()

        return False, current_item

    imgui.push_item_width(-imgui.FLT_MIN)
    imgui.push_style_color(imgui.Col_.frame_bg, (240 / 255, 240 / 255, 240 / 255, 1))
    imgui.push_style_color(imgui.Col_.text, (0, 0, 0, 1))

    # Now we handle searching in our dataset:
    search_pattern = retained_data.search_pattern
    if not is_already_open or search_pattern is None:
        search_pattern = ""

    if not is_already_open:
        imgui.set_keyboard_focus_here()
    changed, new_value, new_pattern_compiled = show_regex_input("##ComboWithFilter_inputText", search_pattern)
    if changed:
        if new_value:
            filtered_items = [i for i, item in enumerate(items) if new_pattern_compiled.search(item)]
            retained_data.filtered_items = filtered_items
        else:
            filtered_items = None
            retained_data.filtered_items = None
        retained_data.search_pattern = new_value
    else:
        filtered_items = retained_data.filtered_items

    imgui.pop_style_color(2)

    is_filtering = filtered_items is not None
    if is_filtering:
        num_items = len(filtered_items)
        try:
            actual_current_item = filtered_items.index(current_item)
        except ValueError:
            actual_current_item = None
    else:
        num_items = len(items)
        actual_current_item = current_item

    value_changed = False

    imgui.push_style_var(imgui.StyleVar_.frame_border_size, 0)

    # from ListBox()
    height_in_items_f = min(7, num_items) + 0.25
    height = imgui.get_text_line_height_with_spacing() * height_in_items_f + ctx.style.frame_padding.y * 2.0
    if imgui.begin_child("##ComboWithFilter_itemList", (0.0, height), imgui.ChildFlags_.frame_style):
        clipper = imgui.ListClipper()
        clipper.begin(num_items, imgui.get_text_line_height_with_spacing())
        if actual_current_item is not None:
            clipper.include_item_by_index(actual_current_item)
        while clipper.step():
            for idx in range(clipper.display_start, clipper.display_end):
                imgui.push_id(idx)
                if is_filtering:
                    label = items[filtered_items[idx]]
                else:
                    label = items[idx]

                is_selected = idx == actual_current_item
                if imgui.selectable(label, is_selected)[0]:
                    if is_filtering:
                        current_item = filtered_items[idx]
                    else:
                        current_item = idx
                    value_changed = True
                    imgui.close_current_popup()

                if is_selected:
                    imgui.set_item_default_focus()
                    if not is_already_open:
                        imgui.set_scroll_here_y()

                imgui.pop_id()

    imgui.end_child()

    if imgui.is_key_pressed(imgui.Key.escape):
        value_changed = False
        imgui.close_current_popup()

    imgui.pop_style_var()
    imgui.pop_item_width()
    imgui.end_combo()

    if value_changed:
        imgui.internal.mark_item_edited(ctx.last_item_data.id_)

    used_combo_boxes[id] = retained_data
    return value_changed, current_item
