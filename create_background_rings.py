'''
written by Emily Pollacchi
  	file name create_background_rings
  	Copyright (C) 2016 by Emily Pollacchi
  	epollacchi@gmail.com
'''

import maya.cmds as mc

#change perspective clip plane
mc.viewClipPlane("perspShape", farClipPlane = 100000)

#set up naming loop

matteNames = ("g_foreground", "g_midground", "g_background")

inc = 0

#create rings

for ring in range(3):
    
    newRing = mc.polyCylinder(n = matteNames[inc], sx=24, sy=3, sz=0, radius=3000, h=2000)
    mc.move(340, y=True)
    mc.polyNormal(nm=0)
        
    inc = inc + 1

#adjust the scale
mc.setAttr("polyCylinder2.radius", 3440)
mc.setAttr("polyCylinder3.radius", 3880)

#delete caps on all cylinders
mc.delete("g_foreground.f[72:73]", "g_midground.f[72:73]", "g_background.f[72:73]")

#set up ctrl naming loop
ctrlNames = ("c_ForegroundMatte", "c_MidgroundMatte", "c_BackgroundMatte")

#create controls

inc = 0

for ctrl in range(3):
    
    newCtrl = mc.circle(n=ctrlNames[inc], r = 3000)    
    mc.rotate('90deg', 0, 0, r=True )
    mc.move(0, 1500, 0)
    
    inc = inc + 1

#adjust the scale

mc.setAttr("makeNurbCircle2.radius", 3440)
mc.setAttr("makeNurbCircle3.radius", 3880)
    
#change colour of the control rings

mc.color("c_ForegroundMatte", rgb=(1, 0.5, 0.5))
mc.color("c_MidgroundMatte",  rgb=(1, 0.5, 1))
mc.color("c_BackgroundMatte", rgb=(0, 1, 2))

#create a square control
mc.circle(n="POS", nr = (0,1,0,), d = 1, s=4, r = 1)
mc.scale(7876, 7876, 7876, "POS")
mc.rotate(0, "45deg", 0,  "POS")

# select backgrounds and the controls
mc.select(matteNames, ctrlNames, "POS", r=True )
#freeze transformations
mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
#delete history
mc.bakePartialHistory(matteNames, ctrlNames, "POS", prePostDeformers=True)
# clear selection
mc.select(clear=True)

#parent cylinders to controls

inc = 0

for item in range(3):
    
    connection = mc.parentConstraint(ctrlNames[inc], matteNames[inc], mo=True, weight=1)
    mc.scaleConstraint(ctrlNames[inc], matteNames[inc], mo=True, weight=1)
    inc = inc + 1
         
#group the geo
mc.group(matteNames, n="GEO_fixed")

#group the controls
mc.group(ctrlNames, n="Controls")

#parent groups to main control
mc.select("Controls", "GEO_fixed", "POS")
mc.parent()
#create a main background group
mc.select("POS")
mc.group(n="ma_backgrounds_day")
