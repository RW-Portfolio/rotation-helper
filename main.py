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

sln_path = "C:/Users/ryanw/Documents/GitHub/personal-tts"
rel_fight_path = f"{sln_path}/fight.txt"
rel_encounter_path = f"{sln_path}/encounters.json"

def load_encounter(wrld, fight):
    with open(rel_encounter_path) as json_file:
        encounter = json.load(json_file)

        for entry in encounter[fight]:
            #array.append({"name" : entry['name'], "time" : entry['time']})
            pass
    foreground.append(Entity(wrld, activation_time, 0, 5, 50, (100,0,10,255)))
    [gcd_actions.append(Entity(world, (activation_time + 600) + ( i * melee_gcd_gap), 5)) for i in range(100)]

    for i in range(100):
        ogcd_actions.append(Entity(wrld, (activation_time + 600) + ( i * melee_gcd_gap) + 50, 5, 25, 25))
        ogcd_actions.append(Entity(wrld, (activation_time + 600) + ( i * melee_gcd_gap) + 85, 5, 25, 25))
        
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