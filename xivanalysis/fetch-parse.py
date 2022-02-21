import json

# source ID - have this in another file to stop recompile?
# data.json - open xivanalysis open network inspector refresh open largest file in new tab, copy to data.json file
sln_path = "C:/Users/ryanw/Documents/GitHub/rotation-helper/xivanalysis"
rel_config_path = f"{sln_path}/config.txt"

matches = ["attack"]

#   1. Source ID
#   2. Input File
#   3. Output File
config = []
with open(rel_config_path) as file:
    for line in file:
        text = line.rstrip('\n')
        config.append(text)

sourceID = int(config[0])
rel_input_path = f"{sln_path}/{config[1]}.json"
rel_output_path = f"{sln_path}/{config[2]}.txt"

actions = []
with open(rel_input_path) as json_file:
    encounter = json.load(json_file)
    for entry in encounter['events']:
        if (
            entry["type"] == "cast" and
            entry["sourceID"] == sourceID and
            not any(x in entry["ability"]["name"] for x in matches)
        ):    
            actions.append(entry["ability"]["name"])

with open(rel_output_path, 'w') as f:
    f.write('\n'.join(actions))