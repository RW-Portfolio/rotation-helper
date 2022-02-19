from re import X
from engine import *
import sys
import os

gameEngine = Engine()

entity = Entity(gameEngine, 800, 12, 50, 50)
entity1 = Entity(gameEngine, 900, 12, 50, 50)
entity2 = Entity(gameEngine, 1000, 12, 50, 50)
entity3 = Entity(gameEngine, 1100, 12, 50, 50)

move = 50

@gameEngine.draw
def draw():
    entity.draw()
    entity1.draw()
    entity2.draw()
    entity3.draw()


@gameEngine.update
def update(dt):
    entity.set_pos(entity.get_x() - (move * dt), entity.get_y())
    entity1.set_pos(entity1.get_x() - (move * dt), entity1.get_y())
    entity2.set_pos(entity2.get_x() - (move * dt), entity2.get_y())
    entity3.set_pos(entity3.get_x() - (move * dt), entity3.get_y())


gameEngine.loop()

