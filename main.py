from operator import index
from engine import *

#  ONLY VARIABLES THAT NEED CHANGING  #
#######################################
ROLE = "tank"
JOB = "pld"
ENCOUNTER = "p4sp2"

PERFECT_PARSE = f"{SLN_PATH}/perfect/{ROLE}/{JOB}/{ENCOUNTER}.txt"
XIV_PARSE = f"{XIV_PATH}/jobs/{ROLE}/{JOB}/{ENCOUNTER}.txt"

PARSE = XIV_PARSE
#########################################

window = Engine()
actions = []
gcd_actions = []
ogcd_actions = []
foreground = []
ability_icons = {}

is_melee = []
is_mage = []
is_ogcd = []

timings = []

types = ["GCD", "oGCD", "Melee", "Mage"]

def load_images_from_txt(file_loc):
    with open(f"{JOBS_PATH}/{file_loc}/actions.txt") as role_file:
        for line in role_file:
            if any(x in line for x in types):
                continue
            image_name = line.replace(" ", "_").strip('\n')
            image_name += ".png"           
            ability_icons[line.strip('\n')] = window.factory.from_image(f"{SLN_PATH}/resources/{file_loc}/{image_name}")

def load_images(role, job):
    ability_icons["Activation"] = window.factory.from_image(f"{SLN_PATH}/resources/Activation.png")
    load_images_from_txt(f"{role}")
    load_images_from_txt(f"{role}/{job}")

def load_actions(role, job):
    isGCD = False
    isMelee = False

    with open(f"{JOBS_PATH}/{role}/actions.txt", 'r') as role_file:
        for line in role_file:
            line = line.rstrip()
            if line == "oGCD":
                continue
            is_ogcd.append(line)

    with open(f"{JOBS_PATH}/{role}/{job}/actions.txt", 'r') as job_file:
        for line in job_file:
            line = line.rstrip()
            if line == "GCD":
                isGCD = True
                continue
            if line == "oGCD":
                isGCD = False
                continue
            if line == "Melee":
                isMelee = True
                continue
            if line == "Mage":
                isMelee = False
                continue
            if isGCD == True and isMelee == True:
                is_melee.append(line)
            if isGCD == True and isMelee == False:
                is_mage.append(line)
            if isGCD == False:
                is_ogcd.append(line)

def load_timings(file):
    with open(f"{XIV_PATH}/jobs/{ROLE}/{JOB}/{ENCOUNTER}.txt") as timing_file:
        for line in timing_file:
            actions.append(line.rstrip())

    index = 0
    while index < len(actions):
        if any(x in actions[index] for x in is_melee):
            index += 1  
            timings.append(int(actions[index]))
            index += 1  

        if index < len(actions):
            if any(x in actions[index] for x in is_mage):
                index += 1
                timings.append(int(actions[index]))
                index += 1    

        if index < len(actions):
            if any(x in actions[index] for x in is_ogcd):
                index += 2

        if index < len(actions):
            if any(x in actions[index] for x in is_ogcd):
                index += 2 

    converted_to_seconds = [x / 1000 for x in timings]

    for i in range (1, len(converted_to_seconds)):
        timings[i] = converted_to_seconds[i] - converted_to_seconds[i-1]
    timings[0] = 2.45

def add_encounter_gcd(index, timeline, cast_type):
    if index < len(actions):
            if any(x in actions[index] for x in cast_type):
                timeline += float(timings.pop(0))
                gcd_actions.append(Entity(window, ability_icons[actions[index]], (ACTIVATION_TIME + COUNDOWN) + (timeline * MOVE_SPEED), 5))
                index += 1 
                return index, timeline
    return index, timeline

def add_encounter_ogcd(index, timeline, position):
    if index < len(actions):
        if any(x in actions[index] for x in is_ogcd):
            ogcd_actions.append(Entity(window, ability_icons[actions[index]], (ACTIVATION_TIME + COUNDOWN) + (timeline * MOVE_SPEED) + position, 5, 25, 25))
            index += 1
            return index
    return index

def load_encounter(window):
    foreground.append(Entity(window, ability_icons["Activation"], ACTIVATION_TIME, 0, 5, 50, (100,0,10,255)))
    del actions[1::2]   
    
    index, timeline = 0, 1
    while index < len(actions):
        index, timeline = add_encounter_gcd(index, timeline, is_melee)
        index, timeline = add_encounter_gcd(index, timeline, is_mage)
        index = add_encounter_ogcd(index, timeline, 50)
        index = add_encounter_ogcd(index, timeline, 85)

def remove_out_of_bounds_obj(action):
    if action:
        if action[0].rect.x < -50:
            action.pop(0)
            
@window.draw
def draw():
    [entity.draw() for entity in gcd_actions]
    [entity.draw() for entity in ogcd_actions]
    [entity.draw() for entity in foreground]

@window.update
def update(dt):
    [entity.update(MOVE_SPEED * dt) for entity in gcd_actions]
    [entity.update(MOVE_SPEED * dt) for entity in ogcd_actions]
    remove_out_of_bounds_obj(gcd_actions)
    remove_out_of_bounds_obj(ogcd_actions)

def main():
    load_images(ROLE, JOB)
    load_actions(ROLE, JOB)
    load_timings(PARSE)
    load_encounter(window)
    window.loop()

if __name__ == '__main__':
    main()