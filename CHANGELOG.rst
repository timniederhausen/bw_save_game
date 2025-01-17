=========
Changelog
=========

Version 1.2.1
=============

- fix: Consistently use Long for Uint32 persistence properties

Version 1.2.0
=============

- feat: Add editor for Emmrich & Strife romance properties
- feat: Add script for force-starting Lucanis' A Moment's Peace quest
- fix: Prevent circular imports in `veilguard` package
- fix(ui): Always create "Inquisition Choices" definition instance
- fix: Use correct type for quest completion count
- chore: Make install / usage instructions less ambiguous
- refactor!: Split `veilguard` into multiple smaller modules
- chore: Use dict comprehension for persistence key <> instance cache
- feat: Add editors for Gender and is-trans state
- chore(ui): Make appearance JSON editors scale with window size
- feat: Add script to force-complete "Inner Demons" pre-reqs
- feat: Support editing NPC romances (Luc & Neve, Harding & Taash)
- feat: Support faction XP editing
- feat: Support more inquisition choices (lineage, gender, voice, fate)
- feat(ui): Accept save file to open as first command-line argument
- feat: Add Inquisitor objective
- feat: Support changing pronouns

Version 1.0.1
=============

- feat: Grant class default skills on archetype change
- fix(ui): Use SHGetFolderPathW on Windows & ensure "Open" start paths are valid
- fix: Correct edge case handling for Integer to Long upgrade
- fix(ui): Support the full uint64 range for positive numbers in the UI

Version 1.0.0
=============

- Initial public release of a ImGui-based graphical user interface.

Version 0.2.0
=============

- Fixed a serialization issue that caused VarInts to be used in places where they are not supported by the game.

Version 0.1.0
=============

- Initial release
