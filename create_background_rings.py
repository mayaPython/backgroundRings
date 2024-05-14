'''
written by Emily Pollacchi
  	file name Create_Background_Rings
  	Copyright (C) 2024 by Emily Pollacchi
  	epollacchi@gmail.com
'''

import maya.cmds as cmds

# Change perspective clip plane
cmds.viewClipPlane("perspShape", farClipPlane = 100000)

# Set up naming loop

matteNames = ("g_foreground", "g_midground", "g_background")

inc = 0

# Create rings

for ring in range(3):
    
    newRing = cmds.polyCylinder(n = matteNames[inc], sx=24, sy=3, sz=0, radius=3000, h=2000)
    cmds.move(340, y=True)
    cmds.polyNormal(nm=0)
        
    inc = inc + 1

# Adjust the scale
cmds.setAttr("polyCylinder2.radius", 3440)
cmds.setAttr("polyCylinder3.radius", 3880)

# Delete caps on all cylinders
cmds.delete("g_foreground.f[72:73]", "g_midground.f[72:73]", "g_background.f[72:73]")

# Set up ctrl naming loop
ctrlNames = ("c_ForegroundMatte", "c_MidgroundMatte", "c_BackgroundMatte")

# Create controls

inc = 0

for ctrl in range(3):
    
    newCtrl = cmds.circle(n=ctrlNames[inc], r = 3000)    
    cmds.rotate('90deg', 0, 0, r=True )
    cmds.move(0, 1500, 0)
    
    inc = inc + 1

# Adjust the scale

cmds.setAttr("makeNurbCircle2.radius", 3440)
cmds.setAttr("makeNurbCircle3.radius", 3880)
    
# Change colour of the control rings

cmds.color("c_ForegroundMatte", rgb=(1, 0.5, 0.5))
cmds.color("c_MidgroundMatte",  rgb=(1, 0.5, 1))
cmds.color("c_BackgroundMatte", rgb=(0, 1, 2))

# Create a square control
cmds.circle(n="POS", nr = (0,1,0,), d = 1, s=4, r = 1)
cmds.scale(7876, 7876, 7876, "POS")
cmds.rotate(0, "45deg", 0,  "POS")

# Select backgrounds and the controls
cmds.select(matteNames, ctrlNames, "POS", r=True )
#Freeze transformations
cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
#Delete history
cmds.bakePartialHistory(matteNames, ctrlNames, "POS", prePostDeformers=True)
# Clear selection
cmds.select(clear=True)

# Parent cylinders to controls

inc = 0

for item in range(3):
    
    connection = cmds.parentConstraint(ctrlNames[inc], matteNames[inc], mo=True, weight=1)
    cmds.scaleConstraint(ctrlNames[inc], matteNames[inc], mo=True, weight=1)
    inc = inc + 1
         
# Group the geo
cmds.group(matteNames, n="GEO_fixed")

# Group the controls
cmds.group(ctrlNames, n="Controls")

# Parent groups to main control
cmds.select("Controls", "GEO_fixed", "POS")
cmds.parent()
# Create a main background group
cmds.select("POS")
cmds.group(n="ma_backgrounds_day")

#Frame all

cmds.viewFit()