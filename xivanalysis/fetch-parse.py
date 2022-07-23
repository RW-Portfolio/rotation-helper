import http.client
import json
import os

class Flag():
    SOURCEID = 0
    ENCOUNTER = 1
    URLREQUEST = 2
    ROLE = 3
    JOB = 4

#  ONLY VARIABLES THAT NEED CHANGING in Config.txt  #
#####################################################
XIV_PATH = f"{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))}/xivanalysis"
IGNORE_ACTION = ["attack", "Iron Will", "Provoke", "Hallowed Ground", "Intervention", "Interject", "Shield Wall", "Stronghold", "Last Bastion", "Land Waker", "Dark Force", "Gunmetal Soul"]
#####################################################

actions = []
config = []

identifiers = {
  "pld": "Intervene"
}

ROLE = "tank"
JOB  = "pld"

def single_file(fight_name, fight_url, override = False):

    if os.path.exists(f"{XIV_PATH}/jobs/{ROLE}/{JOB}/{fight_name}.txt") and not override:
        print(f"{fight_name} file already exists!")
        return

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
    conn.request("GET", f"/proxy/fflogs/report/events/{fight_url}", payload, headers)

    result = conn.getresponse()
    data = result.read()
    string = data.decode("utf-8")

    encounter = json.loads(string)
    for entry in encounter['events']:
        try:
            if entry['ability']['name'] == identifiers[JOB]:
                sourceID = entry["sourceID"]
                break
        except:
            continue

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

    action_output_path = f"{XIV_PATH}/jobs/{ROLE}/{JOB}/{fight_name}.txt"
    with open(action_output_path, 'w') as f:
        for line in actions:
            f.write(f"{line}\n")
    actions.clear()

def raid_tier():
    single_file("p1s", "N6nvcKYmQC2d3M4W?start=1994517&end=2406988&translate=true")
    single_file("p2s", "W6Avqfd1T9mx3FGg?start=450362&end=991804&translate=true")
    single_file("p3s", "wZKRXbpP7knF1TQY?start=971086&end=1516533&translate=true")
    single_file("p4sp1", "JfG2yaQPLHYgqR8c?start=216064&end=606434&translate=true")

def main():
    #single_file("p1s", "N6nvcKYmQC2d3M4W?start=1994517&end=2406988&translate=true")
    raid_tier()

if __name__ == '__main__':
    main()