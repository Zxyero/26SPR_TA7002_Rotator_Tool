# 26SPR_TA7002_Rotator_Tool
Random Rotation Tool for UE5

# Use :: 


# Instructions ::

**Setting up Unreal for Python Scripts**
- In Unreal go to plugins -> Python Editor Script Plugin -> select on -> restart editor
- Go to Tools menu bar -> select 'Exacute Python Script', locate and select 'Rotate_test_5'

- to run this script again, select 'Recent Python Scripts' in Unreal Engine Tool bar, and select 'Rotate_tes_5' (note to self update file name)


# Set-up requirements ::
- Unreal Engine 5
- pySide6 (?)
- 
# Known bugs and workarounds :: 
- Undo (Ctrl-Z) doesnt apply to rotation changes made with tool, can undo random rotation changes by following 'clear rotation' instruction below.

- can repeat rotation by re-applying the 'apply change to selected' button
- **clear rotation** (returns to actors original applied  rotation) by unchecking all checkboxes and selected 'apply change to selected' button = clear rotation.
