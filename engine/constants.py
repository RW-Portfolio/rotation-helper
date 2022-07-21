import os 
SLN_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
XIV_PATH = f"{SLN_PATH}/xivanalysis"
JOBS_PATH = f"{SLN_PATH}/game/roles"
MOVE_SPEED = 60
ACTIVATION_TIME = 100
COUNDOWN = (60 * 5) - 30 # 8 seconds - Use on 10s pre pull