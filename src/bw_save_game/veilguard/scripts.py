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
