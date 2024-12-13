import typing

from imgui_bundle import imgui

# retained state
used_combo_boxes = {}


def clear_unused_retained_data():
    global used_combo_boxes
    used_combo_boxes = {k: v for k, v in used_combo_boxes.items() if v["shown_this_frame"]}
    for v in used_combo_boxes.values():
        v["shown_this_frame"] = False


def show_searchable_combo_box(
    label: str,
    items: typing.List[typing.Any],
    to_text: typing.Callable[[typing.Any], str],
    current_item: typing.Optional[int] = None,
):
    ctx = imgui.get_current_context()

    window = imgui.internal.get_current_window()
    if window.skip_items:
        return False, current_item

    preview_value = to_text(items[current_item])

    id = window.get_id(label)
    popup_id = imgui.internal.im_hash_str("##ComboPopup", 0, id)

    global used_combo_boxes
    retained_data = used_combo_boxes.get(id)
    if retained_data is None:
        retained_data = dict(shown_this_frame=True, search_pattern="", filtered_items=None)
    else:
        retained_data["shown_this_frame"] = True

    search_pattern = retained_data["search_pattern"]

    is_already_open = imgui.internal.is_popup_open(popup_id, 0)

    if not imgui.begin_combo(label, preview_value, imgui.ComboFlags_.height_largest):
        used_combo_boxes[id] = retained_data
        return False, current_item

    if not is_already_open:
        search_pattern = ""

    imgui.push_style_color(imgui.Col_.frame_bg, (240 / 255, 240 / 255, 240 / 255, 1))
    imgui.push_style_color(imgui.Col_.text, (0, 0, 0, 1))
    imgui.push_item_width(-imgui.FLT_MIN)

    if not is_already_open:
        imgui.set_keyboard_focus_here()
    changed, new_value = imgui.input_text("##ComboWithFilter_inputText", search_pattern)
    if changed:
        search_pattern = new_value

    imgui.pop_style_color(2)

    is_filtering = is_already_open and search_pattern
    if is_filtering:
        if search_pattern != retained_data["search_pattern"] or not retained_data["filtered_items"]:
            filtered_items = [i for (i, item) in enumerate(items) if search_pattern in to_text(item)]
            retained_data["filtered_items"] = filtered_items
        else:
            filtered_items = retained_data["filtered_items"]
        num_items = len(filtered_items)
        try:
            filtered_current_item = filtered_items.index(current_item)
        except ValueError:
            filtered_current_item = None
    else:
        num_items = len(items)

    retained_data["search_pattern"] = search_pattern

    actual_current_item = filtered_current_item if is_filtering else current_item
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
                if imgui.selectable(to_text(label), is_selected)[0]:
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
