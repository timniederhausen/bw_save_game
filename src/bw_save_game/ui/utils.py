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
from imgui_bundle import imgui, portable_file_dialogs


def ask_for_file_to_open(message, wildcard, default_path=""):
    dlg = portable_file_dialogs.open_file(title=message, filters=wildcard.split("|"), default_path=default_path)
    while not dlg.ready():
        pass
    res = dlg.result()
    if res:
        return res[0]
    return None


def ask_for_file_to_save(message, wildcard, default_path=""):
    dlg = portable_file_dialogs.save_file(title=message, filters=wildcard.split("|"), default_path=default_path)
    while not dlg.ready():
        pass
    return dlg.result()


def show_error(message):
    dlg = portable_file_dialogs.message("Error", message, portable_file_dialogs.choice.ok)
    while not dlg.ready():
        pass


def push_int_id(signed_id: int):
    # Make really sure our int value is signed - imgui_bundle only accepts signed int32 values for PushID(int)
    # XXX: could be a nanobind issue too?
    imgui.push_id(signed_id - (signed_id & (1 << 31)))
