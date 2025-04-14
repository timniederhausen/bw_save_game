=========
Changelog
=========

Version 1.5.0
=============

* feat(ui): Support editing a save game's associated career
* feat(ui): Support multiple persistence instances for a definition
* chore(ui): Use re.search() to simplify regex use for users
* feat(veilguard): Support multiple persistence instances with the same DefId
* chore: Code cleanup
* fix: Make new persistence editor UI more consistent
* feat(ui): Make item popups resize-able
* feat: Add full-blown editor for all persistence definitions
* feat(ui): Support using Python regular expressions for filtering

Version 1.4.2
=============

* fix(ui): Change player XP when the level is changed
* feat: Better support for changing levels & XP

Version 1.4.1
=============

* chore(ui): Disable general editor for now & bring back IsleOfTheGods options

Version 1.4.0
=============

* feat: Add complete transition point & map list
* feat: Add editors for voice & voice tone
* feat(ui): Add tab for player skills
* fix: Add missing "None" option for inquisitor romance
* feat(ui): Add quick action to grant all normal appearance collectibles
* feat(ui): Allow editing all collectible flags
* chore(ui): Make bit flag editors more compact
* feat: Support changing the current transition spawn point
* feat(ui): Add text search / filter for the inventory list
* feat: Support editing the active follower party
* fix(ui): Don't ignore currency changes if previous value was default
* chore: Change README heading for now
* feat: Add general quest state editor

Version 1.3.0
=============

* chore: Re-normalize line endings after .gitattributes introduction
* refactor!: Add more data files and move them to LFS
* chore: Add .gitattributes and start storing data files in LFS
* fix(ui): Don't crash when encountering primitive arrays in raw view
* feat: Add scripts & properties for Isle of the Gods and Soul of a City
* feat: Add Emmrich sacrifice choices
* fix(ui): Don't fail for non-string keys in raw data (e.g. array indices)
* feat: Add scripts for force-starting Emmrich Lich/Manfred quests
* feat(ui): Support editing definitions the game hasn't loaded yet
* feat(ui): Add editors for follower states (available, dead, hardened, etc.)

Version 1.2.2
=============

* fix: Correct some wrong defaults in CharacterGenerator_RDA_1647819227
* refactor!(ui): Split our custom editors into normal & in-place variants

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
