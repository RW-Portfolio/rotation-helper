import http.client
import json

class Flag():
    SOURCEID = 0
    ENCOUNTER = 1
    URLREQUEST = 2
    ROLE = 3
    JOB = 4

#  ONLY VARIABLES THAT NEED CHANGING in Config.txt  #
#####################################################
XIV_PATH = "C:/Users/Ryan/Documents/Git/rotation-helper/xivanalysis"
CONFIG_PATH = f"{XIV_PATH}/config.txt"
IGNORE_ACTION = ["attack", "Iron Will", "Provoke", "Hallowed Ground", "Intervention", "Interject", "Shield Wall", "Stronghold", "Last Bastion", "Land Waker", "Dark Force", "Gunmetal Soul"]
#####################################################

actions = []
config = []

def main():

    with open(CONFIG_PATH) as file:
        for line in file:
            text = line.split(":",1)[1]
            text = text.strip()
            config.append(text)

    sourceID = int(config[Flag.SOURCEID])
    action_output_path = f"{XIV_PATH}/jobs/{config[Flag.ROLE]}/{config[Flag.JOB]}/{config[Flag.ENCOUNTER]}.txt"
    
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

    conn.request("GET", f"/proxy/fflogs/report/events/{config[Flag.URLREQUEST]}", payload, headers)

    result = conn.getresponse()
    data = result.read()
    string = data.decode("utf-8")

    encounter = json.loads(string)
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
            actions.append(entry["timestamp"])

    with open(action_output_path, 'w') as f:
        for line in actions:
            f.write(f"{line}\n")

if __name__ == '__main__':
    main()