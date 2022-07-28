import os
from enum import Enum

SLN_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
XIV_PATH = f"{SLN_PATH}/xivanalysis"
MOVE_SPEED = 60
ACTIVATION_TIME = 100
COUNDOWN = (60 * 5) - 30 # 8 seconds - Use on 10s pre pull

class Pandaemonium(Enum):
    P1S =   78
    P2S =   79
    P3S =   80
    P4SP1 = 81
    P4SP2 = 82

class Tank(Enum):
    PLD = "Paladin"
    GNB = "Gunbreaker"
    DRK = "DarkKnight"
    WAR = "Warrior"

class MeleeDps(Enum):
    MNK = "Monk"
    DRG = "Dragoon"
    NIN = "Ninja"
    SAM = "Samurai"
    RPR = "Reaper"

JOB     = Tank.PLD
RAID_TIER = Pandaemonium
RAID = Pandaemonium.P2S