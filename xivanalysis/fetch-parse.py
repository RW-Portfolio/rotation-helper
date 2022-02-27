import json

role = "tank"
job = "drk"
actionsToIgnore = ["attack", "Iron Will", "Provoke", "Hallowed Ground", "Intervention"]
actions = []

XIV_PATH = "C:/Users/Ryan/Documents/Git/rotation-helper/xivanalysis"
config_path = f"{XIV_PATH}/config.txt"

#   1. Source ID
#   2. Input File
#       - data.json - open xivanalysis open network inspector refresh open largest file in new tab, copy to data.json file
config = []
with open(config_path) as file:
    for line in file:
        text = line.rstrip('\n')
        config.append(text)

sourceID = int(config[0])
input_path = f"{XIV_PATH}/jobs/{role}/{job}/json/{config[1]}.json"
output_path = f"{XIV_PATH}/jobs/{role}/{job}/parsed/{config[1]}.txt"

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
            not any(x in entry["ability"]["name"] for x in actionsToIgnore)
        ):    
            actions.append(entry["ability"]["name"])

with open(output_path, 'w') as f:
    f.write('\n'.join(actions))