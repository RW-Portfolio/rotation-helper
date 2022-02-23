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

#sln_path = "C:/Users/ryanw/Documents/GitHub/rotation-helper"
sln_path = "C:/Users/Ryan/Documents/Git/rotation-helper"
rel_fight_path = f"{sln_path}/fight.txt"
rel_encounter_path = f"{sln_path}/encounters.json"
rel_jobs_path = f"{sln_path}/xivanalysis/jobs"

matchesMelee = []
matchesMage = []
matchesOgcd = []

pictures = {}

def load_actions(job):
    isGCD = False
    isMelee = False
    with open(f"{rel_jobs_path}/{job}/actions.txt", 'r') as file:
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

def load_encounter(wrld):
    global actions
    foreground.append(Entity(wrld, pictures["Activation"], activation_time, 0, 5, 50, (100,0,10,255)))
   
    with open(f"{sln_path}/xivanalysis/output.txt") as file:
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

        if any(x in actions[index] for x in matchesMage):
            timeline += 2.45
            gcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed), 5))
            index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + countdown) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1

        if index < len(actions):
            if any(x in actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pictures[actions[index]], (activation_time + 600) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1 

        gcd_gap_index += 1

def load_images():
    #RESOURCES = sdl2.ext.Resources("c:/Users/ryanw/Documents/GitHub/rotation-helper/", "resources")
    RESOURCES = sdl2.ext.Resources("C:/Users/Ryan/Documents/Git/rotation-helper", "resources")
    factory = world.factory

    pictures["Activation"] = factory.from_image(RESOURCES.get_path("Activation.png"))
    with open(f"{rel_jobs_path}/pld/pictures.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            pictures[row[0]] = factory.from_image(RESOURCES.get_path(row[1]))

@world.draw
def draw():
    [entity.draw() for entity in background]
    [entity.draw() for entity in gcd_actions]
    [entity.draw() for entity in ogcd_actions]
    [entity.draw() for entity in foreground]

@world.update
def update(dt):
    [entity.set_pos(entity.get_x() - (move_speed * dt), entity.get_y()) for entity in gcd_actions]
    [entity.set_pos(entity.get_x() - (move_speed * dt), entity.get_y()) for entity in ogcd_actions]
    if gcd_actions:
        if gcd_actions[0].get_x() < -50:
            gcd_actions.pop(0)

load_images()
load_actions("pld")
load_encounter(world)

world.loop()