
from core import *
import os
import sys
paddleocr_path = os.path.join(os.path.dirname(__file__), "PaddleOCR")
sys.path.append(paddleocr_path)
from image_recognition import trueOCR

#Opening up the CRK emulator and finding the area anchors
performInitial()
time.sleep(1)
regions = find_area()
time.sleep(2)

#In case we have a first roll of the day and three of the same on that roll we can bypass both menus
initial_three = False
initial_list = []
x = []
for region in regions:
    single_roll = trueOCR(region)
    initial_list.append(single_roll)
    
initial_roll = Roll(initial_list, x)
if initial_roll.three_check():
    initial_three = True
    print(initial_three)

#User input variables
num_lines = 3
target_stat = "Cooldown"
stat_amount = 12
max_rolls = 3
three_found = False
#Maybe change this to be like "It really doesnt matter if its elemental if the user does not want an elemental type anyways"
is_elemental = True
element_type = "Earth DMG"
    
#User inputs 0 or null, that means infinite rolls: Roll until found
if max_rolls == 0:
    max_rolls = float("inf")

#Main loop
for i in range(max_rolls):
    
    roll_list = []
    validity_list = []
    if i == 0 and initial_three:
        firstofday()
        threeofsame()
    elif i == 0 and not initial_three:
        firstofday()
        time.sleep(2)
    elif three_found:
        firstofday()
        time.sleep(2)
        three_found = None
    else:
        reroll()
        time.sleep(2)
    
    for region in regions:
        single_roll = trueOCR(region)
        valid = single_roll.isValid()
        if valid:
            validity_list.append(1)
        else:
            validity_list.append(0)
        
        if is_elemental and single_roll.stat == "":
            single_roll.set_stat(element_type)
    
        roll_list.append(single_roll)
    
    current_roll = Roll(roll_list, validity_list)
    table_add(current_roll)
    
    if not three_found:
        three_found = current_roll.three_check()
        
    sum_stat = current_roll.sumStats()
    if(sum_stat.get(target_stat, 0) >= stat_amount and current_roll.num_target(target_stat) <= num_lines): 
        #Target found
        print("Target found")
        break