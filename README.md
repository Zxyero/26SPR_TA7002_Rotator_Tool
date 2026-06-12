# 26SPR_TA7002_Rotator_Tool
Random Rotation Tool for UE5

# Use : 
This is a tool that will randomly rotate selected meshes/actors at a set range in Unreal Engine 5. 

Select your mesh/actors in the Unreal Engine viewport (can select multiple) and enter the minimium and maximum angles on pitch, roll, and yawn (y, x, z) axis. 
This will apply a new rotation to selected actors that is randomised.

Helpful tool when building large enviroments and creating variation in scenes quickly.


# Instructions :

**Setting up Unreal for Python Scripts**
- In Unreal go to plugins -> Python Editor Script Plugin -> select on -> restart editor
- Go to Tools menu bar -> select 'Exacute Python Script', locate and select 'Rotate_test_5'

- To run this script again, select 'Recent Python Scripts' in Unreal Engine Tool bar, and select 'Rotate_tes_5' (note to self update file name)


# Set-up requirements :
- Unreal Engine 5
- pySide6 (?)

  
# Known bugs and workarounds :
- Undo (Ctrl-Z) doesnt apply to rotation changes made with tool, can undo random rotation changes by following 'clear rotation' instruction below.

- Can repeat a new randomised rotation by re-applying the 'apply change to selected' button
- **Clear Rotation** (returns to actors original applied  rotation) by unchecking all checkboxes and selecting the 'apply change to selected' button = clear rotation.
