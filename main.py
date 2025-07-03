from core import *
SCREENSHOT_AREA1 = (570, 262, 900, 290)  # Left, top, right, down
SCREENSHOT_AREA2 = (570, 302, 900, 330)
SCREENSHOT_AREA3 = (570, 342, 900, 370)
SCREENSHOT_AREA4 = (570, 381, 900, 410)
performInitial()
counter = 5129
for i in range(125):
    reroll()
    time.sleep(1.5)
    get_gt(str(counter),SCREENSHOT_AREA1)
    counter += 1
    get_gt(str(counter),SCREENSHOT_AREA2)
    counter += 1
    get_gt(str(counter),SCREENSHOT_AREA3)
    counter += 1
    get_gt(str(counter),SCREENSHOT_AREA4)
    counter += 1

#Elemental: Ice, Fire, Poison, Dark, Earth, Electric, Steel
#Do 250 of each i gues
#Completed: Ice has: 250, Earth has 250, Dark has 250, electric has 250, poison has 250,
