import csv
import sdl2
from engine import *

world = Engine()
actions = []
gcd_actions = []
ogcd_actions = []
background = []
foreground = []

# 60 == 1s
move_speed = 60
melee_gcd = 2.45
melee_gcd_gap = move_speed * melee_gcd
mage_gcd = 2.50
mage_gcd_gap = move_speed * mage_gcd

activation_time = 100
# 0 is about ~ 3seconds ish
countdown = 60 * 0

rel_fight_path = f"{SLN_PATH}/fight.txt"
rel_encounter_path = f"{SLN_PATH}/encounters.json"
rel_jobs_path = f"{SLN_PATH}/game/roles/"

matchesMelee = []
matchesMage = []
matchesOgcd = []

pictures = {}

def load_images(role, job):
    factory = world.factory
    pictures["Activation"] = factory.from_image(f"{SLN_PATH}/resources/Activation.png")

    with open(f"{rel_jobs_path}/{role}/icon_map.csv") as tank_file:
        next(tank_file)
        csv_reader = csv.reader(tank_file, delimiter=',')
        for row in csv_reader:
                pictures[row[0]] = factory.from_image(f"{SLN_PATH}/resources/{role}/{row[1]}")
    
    with open(f"{rel_jobs_path}/{role}/{job}/icon_map.csv") as job_file:
        next(job_file)
        csv_reader = csv.reader(job_file, delimiter=',')
        for row in csv_reader:
            pictures[row[0]] = factory.from_image(f"{SLN_PATH}/resources/{role}/{job}/{row[1]}")

def load_actions(role, job):
    isGCD = False
    isMelee = False

    with open(f"{rel_jobs_path}/{role}/actions.txt", 'r') as file1:
        for line in file1:
            line = line.rstrip()
            if line == "oGCD":
                continue
            matchesOgcd.append(line)

    with open(f"{rel_jobs_path}/{role}/{job}/actions.txt", 'r') as file:
        for line in file:
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
                matchesMelee.append(line)
            if isGCD == True and isMelee == False:
                matchesMage.append(line)
            if isGCD == False:
                matchesOgcd.append(line)

def load_encounter_xivanalysis(wrld, role, job, file):
    global actions
    foreground.append(Entity(wrld, pictures["Activation"], activation_time, 0, 5, 50, (100,0,10,255)))
   
    with open(f"{XIV_PATH}/jobs/{role}/{job}/parsed/{file}.txt") as file:
        for line in file:
            actions.append(line.rstrip())
            
    index = 0
    gcd_gap_index = 1
    timeline = 1
    while index < len(actions):
        if any(x in actions[index] for x in matchesMelee):
            timeline += 2.45
            gcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
            index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesMage):
                timeline += 2.50
                gcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
                index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 85, 5, 25, 25))
                index += 1 

        gcd_gap_index += 1

def load_encounter_personal(wrld, role, job, file):
    global actions
    foreground.append(Entity(wrld, pictures["Activation"], activation_time, 0, 5, 50, (100,0,10,255)))
    
    with open(f"{SLN_PATH}/perfect/{role}/{job}/{file}.txt") as file:
        for line in file:
            actions.append(line.rstrip())

    index = 0
    gcd_gap_index = 1
    timeline = 1
    while index < len(actions):
        if any(x in actions[index] for x in matchesMelee):
            timeline += 2.45
            gcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
            index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesMage):
                timeline += 2.50
                gcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
                index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 85, 5, 25, 25))
                index += 1 

        gcd_gap_index += 1

@world.draw
def draw():
    [entity.draw() for entity in background]
    [entity.draw() for entity in gcd_actions]
    [entity.draw() for entity in ogcd_actions]
    [entity.draw() for entity in foreground]

@world.update
def update(dt):
    [entity.update(move_speed * dt) for entity in gcd_actions]
    [entity.update(move_speed * dt) for entity in ogcd_actions]
    if gcd_actions:
        if gcd_actions[0].rect.x < -50:
            gcd_actions.pop(0)

role = "tank"
job = "pld"

load_images(role, job)
load_actions(role, job)
#load_encounter_xivanalysis(world, role, job, "p1s")
load_encounter_personal(world, role, job, "p1s")

world.loop()