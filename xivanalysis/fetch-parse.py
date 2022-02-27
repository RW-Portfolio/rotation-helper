import json

#       HOW TO USE        #
#                         #
#   Change config.txt     #
#   - Source ID           #
#   - Input/Output        #

#  ONLY VARIABLES THAT NEED CHANGING  #
#######################################
ROLE = "tank"
JOB = "drk"
XIV_PATH = "C:/Users/Ryan/Documents/Git/rotation-helper/xivanalysis"
CONFIG_PATH = f"{XIV_PATH}/config.txt"
IGNORE_ACTION = ["attack", "Iron Will", "Provoke", "Hallowed Ground", "Intervention"]
#######################################

actions = []
config = []

def main():
    with open(CONFIG_PATH) as file:
        for line in file:
            text = line.rstrip('\n')
            config.append(text)

    sourceID = int(config[0])
    input_path = f"{XIV_PATH}/jobs/{ROLE}/{JOB}/json/{config[1]}.json"
    output_path = f"{XIV_PATH}/jobs/{ROLE}/{JOB}/parsed/{config[1]}.txt"

    with open(input_path) as json_file:
        encounter = json.load(json_file)
        for entry in encounter['events']:
            try:
                entry["sourceID"] == sourceID
            except:
                continue
            if (
                entry["type"] == "cast" and
                entry["sourceID"] == sourceID and
                not any(x in entry["ability"]["name"] for x in IGNORE_ACTION)
            ):    
                actions.append(entry["ability"]["name"])

    with open(output_path, 'w') as f:
        f.write('\n'.join(actions))

if __name__ == '__main__':
    main()