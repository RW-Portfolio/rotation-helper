import json
from engine import *

world = Engine()
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

#sln_path = "C:/Users/ryanw/Documents/GitHub/rotation-helper"
sln_path = "C:/Users/Ryan/Documents/Git/rotation-helper"
rel_fight_path = f"{sln_path}/fight.txt"
rel_encounter_path = f"{sln_path}/encounters.json"
rel_jobs_path = f"{sln_path}/xivanalysis/jobs"

matchesMelee = []
matchesMage = []
matchesOgcd = []

pngDict = {
  "Fast Blade":         "Fast_Blade.png",
  "Riot Blade":         "Riot_Blade.png",
  "Goring Blade":       "Goring_Blade.png",
  "Royal Authority":    "Royal_Authority.png",
  "Atonement":          "Attonement.png",
  "Holy Spirit":        "Holy_Spirit.png",
  "Confiteor":          "Confiteor.png",
  "Blade of Faith":     "Blade_of_Faith.png",
  "Blade of Truth":     "Blade_of_Truth.png",
  "Blade of Valor":     "Blade_of_Valor.png",
  "Fight or Flight":    "Flight_or_Fight.png",
  "Circle of Scorn":    "Circle_of_Scorn.png",
  "Expiacion":          "Expiacion.png",
  "Medicated":          "Pot.png",
  "Requiescat":         "Requiescat.png",
  "Intervene":          "Intervene.png",
  "Holy Sheltron":      "Holy_Sheltron.png",
  "Reprisal":           "Reprisal.png",
  "Divine Veil":        "Divine_Veil.png",
  "Sentinel":           "Sentinel.png",
  "Shirk":              "Shirk.png",
  "Sprint":             "Sprint.png",
  "Rampart":            "Rampart.png"
}

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

def load_encounter(wrld, fight):
    foreground.append(Entity(wrld, "Activation.png", activation_time, 0, 5, 50, (100,0,10,255)))
    
    with open(rel_encounter_path) as json_file:
        encounter = json.load(json_file)

        index = 0
        for entry in encounter[fight]:
            if entry['name'] == "GCD":
                gcd_actions.append(Entity(wrld, entry['skill'], (activation_time + 600) + (index * melee_gcd_gap), 5))

            if entry['name'] == "oGCD":
                index -= 1
                if entry['skill1'] != "none":
                    ogcd_actions.append(Entity(wrld, entry['skill1'], (activation_time + 600) + (index * melee_gcd_gap) + 50, 5, 25, 25))
                if entry['skill2'] != "none":
                    ogcd_actions.append(Entity(wrld, entry['skill2'], (activation_time + 600) + (index * melee_gcd_gap) + 85, 5, 25, 25))
            index += 1


test_actions = []
def load_encounter_txt(wrld):
    global test_actions
    foreground.append(Entity(wrld, "Activation.png", activation_time, 0, 5, 50, (100,0,10,255)))
   
    with open(f"{sln_path}/xivanalysis/output.txt") as file:
        for line in file:
            test_actions.append(line.rstrip())

    index = 0
    gcd_gap_index = 1
    timeline = 1
    while index < len(test_actions):
        if any(x in test_actions[index] for x in matchesMelee):
            timeline += 2.45
            gcd_actions.append(Entity(wrld, pngDict[test_actions[index]], (activation_time + 600) + (timeline * move_speed), 5))
            index += 1

        if any(x in test_actions[index] for x in matchesMage):
            timeline += 2.45
            gcd_actions.append(Entity(wrld, pngDict[test_actions[index]], (activation_time + 600) + (timeline * move_speed), 5))
            index += 1

        if index < len(test_actions):
            if any(x in test_actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pngDict[test_actions[index]], (activation_time + 600) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1

        if index < len(test_actions):
            if any(x in test_actions[index] for x in matchesOgcd):
                ogcd_actions.append(Entity(wrld, pngDict[test_actions[index]], (activation_time + 600) + (timeline * move_speed) + 50, 5, 25, 25))
                index += 1 

        gcd_gap_index += 1

load_actions("pld")
load_encounter_txt(world)

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

world.loop()