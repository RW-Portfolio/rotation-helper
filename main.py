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

sln_path = "C:/Users/ryanw/Documents/GitHub/rotation-helper"
rel_fight_path = f"{sln_path}/fight.txt"
rel_encounter_path = f"{sln_path}/encounters.json"


# Need to incorporate the gap better between melee and
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

load_encounter(world, "p1s")

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