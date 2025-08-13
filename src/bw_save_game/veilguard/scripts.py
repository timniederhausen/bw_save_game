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
from .highlevel import VeilguardSaveGame
from .persistence import (
    QST_SHD_2_1_SOULOFACITY_ACQUISITION__QuestState,
    QST_SHD_2_1_SOULOFACITY_DOCKTOWN__QuestState,
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__QuestState,
    QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION_HasSeenNote,
)
from .types import EcoQuestRegisteredStateFlags


def force_start_soul_of_a_city(save_game: VeilguardSaveGame):
    save_game.set_persistence_property(
        QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION__QuestState, EcoQuestRegisteredStateFlags.Completed
    )
    save_game.set_persistence_property(QST_SHD_2_1_SOULOFACITY_LIGHTHOUSE_ACQUISITION_HasSeenNote, True)

    save_game.set_persistence_property(
        QST_SHD_2_1_SOULOFACITY_ACQUISITION__QuestState, EcoQuestRegisteredStateFlags.Completed
    )

    save_game.set_persistence_property(
        QST_SHD_2_1_SOULOFACITY_DOCKTOWN__QuestState, EcoQuestRegisteredStateFlags.Eligible
    )
