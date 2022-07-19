import csv
from re import I
from engine import *

#  ONLY VARIABLES THAT NEED CHANGING  #
#######################################

ROLE = "tank"
JOB = "pld"
ENCOUNTER = "p3s-test"

PERFECT_PARSE = f"{SLN_PATH}/perfect/{ROLE}/{JOB}/{ENCOUNTER}.txt"
XIV_PARSE = f"{XIV_PATH}/jobs/{ROLE}/{JOB}/{ENCOUNTER}.txt"

PARSE = XIV_PARSE

#########################################

window = Engine()
actions = []
gcd_actions = []
ogcd_actions = []
background = []
foreground = []
ability_icons = {}

is_melee = []
is_mage = []
is_ogcd = []

fight_path = f"{SLN_PATH}/fight.txt"
encounter_path = f"{SLN_PATH}/encounters.json"
jobs_path = f"{SLN_PATH}/game/roles/"

move_speed = 60 # 60 == 1s
melee_gcd = 2.45
melee_gcd_gap = move_speed * melee_gcd
mage_gcd = 2.50
mage_gcd_gap = move_speed * mage_gcd

activation_time = 100
countdown = (60 * 5) - 30 # 8 seconds - Use on 10s pre pull

half_second = "Half-Second"
half_tenth = "Half-Tenth"

gcd_times = []
timings = []

def load_images(role, job):
    factory = window.factory
    ability_icons["Activation"] = factory.from_image(f"{SLN_PATH}/resources/Activation.png")

    with open(f"{jobs_path}/{role}/icon_map.csv") as role_file:
        next(role_file)
        csv_reader = csv.reader(role_file, delimiter=',')
        for row in csv_reader:
                ability_icons[row[0]] = factory.from_image(f"{SLN_PATH}/resources/{role}/{row[1]}")
    
    with open(f"{jobs_path}/{role}/{job}/icon_map.csv") as job_file:
        next(job_file)
        csv_reader = csv.reader(job_file, delimiter=',')
        for row in csv_reader:
            ability_icons[row[0]] = factory.from_image(f"{SLN_PATH}/resources/{role}/{job}/{row[1]}")

def load_actions(role, job):
    isGCD = False
    isMelee = False

    with open(f"{jobs_path}/{role}/actions.txt", 'r') as role_file:
        for line in role_file:
            line = line.rstrip()
            if line == "oGCD":
                continue
            is_ogcd.append(line)

    with open(f"{jobs_path}/{role}/{job}/actions.txt", 'r') as job_file:
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
            timings.append(["melee" ,int(actions[index])/1000])
            index += 1  

        if index < len(actions):
            if any(x in actions[index] for x in is_mage):
                index += 1
                timings.append(["mage", int(actions[index])/1000])
                index += 1    

        if index < len(actions):
            if any(x in actions[index] for x in is_ogcd):
                index += 2

        if index < len(actions):
            if any(x in actions[index] for x in is_ogcd):
                index += 2 

def load_encounter(window, file):
    global actions
    foreground.append(Entity(window, ability_icons["Activation"], activation_time, 0, 5, 50, (100,0,10,255)))
    
    with open(file) as action_file:
        for line in action_file:
            actions.append(line.rstrip())

    del actions[1::2]
    index = 0
    timeline = 1
    while index < len(actions):
        if any(x in actions[index] for x in is_melee):
            gcd_actions.append(Entity(window, ability_icons[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
            index += 1
            timeline += melee_gcd

        if index < len(actions):
            if any(x in actions[index] for x in is_mage):
                gcd_actions.append(Entity(window, ability_icons[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
                index += 1 
                timeline += mage_gcd

        if index < len(actions):
            if any(x in actions[index] for x in is_ogcd):
                ogcd_actions.append(Entity(window, ability_icons[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1

        if index < len(actions):
            if any(x in actions[index] for x in is_ogcd):
                ogcd_actions.append(Entity(window, ability_icons[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 85, 5, 25, 25))
                index += 1 

@window.draw
def draw():
    [entity.draw() for entity in background]
    [entity.draw() for entity in gcd_actions]
    [entity.draw() for entity in ogcd_actions]
    [entity.draw() for entity in foreground]

@window.update
def update(dt):
    [entity.update(move_speed * dt) for entity in gcd_actions]
    [entity.update(move_speed * dt) for entity in ogcd_actions]
    if gcd_actions:
        if gcd_actions[0].rect.x < -50:
            gcd_actions.pop(0)
    if ogcd_actions:
        if ogcd_actions[0].rect.x < -50:
            ogcd_actions.pop(0)

def main():
    load_images(ROLE, JOB)
    load_actions(ROLE, JOB)
    load_timings(PARSE)
    load_encounter(window, PARSE)
    window.loop()

if __name__ == '__main__':
    main()