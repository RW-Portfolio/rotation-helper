import http.client
import json
import os


#       HOW TO USE        #
#                         #
#   Change config.txt     #
#   - Source ID           #
#   - Input/Output        #

#  ONLY VARIABLES THAT NEED CHANGING  #
#######################################
ROLE = "tank"
JOB = "pld"
XIV_PATH = "C:/Users/Ryan/Documents/Git/rotation-helper/xivanalysis"
CONFIG_PATH = f"{XIV_PATH}/config.txt"
IGNORE_ACTION = ["attack", "Iron Will", "Provoke", "Hallowed Ground", "Intervention"]
#######################################

actions = []
config = []

def retrieve_log(fight_id):
    conn = http.client.HTTPSConnection("xivanalysis.com")

    payload = ""

    headers = {
        'authority': "xivanalysis.com",
        'accept': "application/json",
        'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
        'referer': "https://xivanalysis.com/fflogs/N6nvcKYmQC2d3M4W/4/1",
        'sec-ch-ua': "^\^.Not/A",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "^\^Windows^^",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

    conn.request("GET", f"/proxy/fflogs/report/events/{fight_id}?start=1994517&end=2406988&translate=true", payload, headers)

    result = conn.getresponse()
    data = result.read()
    string = data.decode("utf-8")
    file = open(f"{XIV_PATH}/temp.json", "w")
    file.write(string)
    file.close()

def clean():
    os.remove(f"{XIV_PATH}/temp.json")

def main():

    with open(CONFIG_PATH) as file:
        for line in file:
            text = line.rstrip('\n')
            config.append(text)

    sourceID = int(config[0])
    input_path = f"{XIV_PATH}/temp.json"
    output_path = f"{XIV_PATH}/jobs/{ROLE}/{JOB}/parsed/{config[1]}.txt"
    
    retrieve_log(config[2])

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
    clean()