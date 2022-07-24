import http.client
import json
import os
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from seleniumwire import webdriver 
from time import sleep
import os

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

identifiers = {
  f"{Tank.PLD.name}": "Intervene",
  f"{Tank.GNB.name}": "Bloodfest",
  f"{Tank.DRK.name}": "Bloodspiller",
  f"{Tank.WAR.name}": "Maim"
}

JOB     = Tank.DRK
RAID_TIER = Pandaemonium
XIV_PATH = f"{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))}/xivanalysis"
IGNORE_ACTION = ["attack"]

members = [attr for attr in dir(RAID_TIER) if not callable(getattr(RAID_TIER, attr)) and not attr.startswith("__")]
actions = []

def load_url(fight_id):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(f"https://www.fflogs.com/zone/rankings/44#boss={fight_id.value}&metric=dps&class=Global&spec={JOB.value}")
    cookies = driver.find_element(by=By.XPATH ,value="/html/body/div[2]/div/div/div/div[2]/div/button[2]/span")
    sleep(1)
    cookies.click()
    top_player = driver.find_element(by=By.XPATH ,value="/html/body/div[3]/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[2]/div/div[1]/a[1]")
    sleep(1)
    top_player.click()

    fflog = driver.current_url[31:].partition("#")
    fight_url= fflog[0]
    fight_id = fflog[2][6:].partition("&")[0]

    driver.get(f"https://xivanalysis.com/fflogs/{fight_url}/{fight_id}")
    sleep(1)
    top_player = driver.find_element(by=By.XPATH ,value="/html/body/div/div[2]/div[2]/div/div[1]/div/a[1]/span[1]")
    top_player.click()
    sleep(2)

    api_url = "Not Found"
    for request in driver.requests:
        if request.response:
            if "https://xivanalysis.com/proxy/fflogs/report/events/" in request.url:
                api_url = request.url.partition("events/")[2]
    driver.quit()
    return api_url

def create_single_file(fight_name, override = False):
    if os.path.exists(f"{XIV_PATH}/jobs/{Tank.__qualname__}/{JOB.name}/{fight_name}.txt") and not override:
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
    url = load_url(RAID_TIER[fight_name])
    conn.request("GET", f"/proxy/fflogs/report/events/{url}", payload, headers)

    result = conn.getresponse()
    data = result.read()
    string = data.decode("utf-8")

    if "429 Too Many Requests" in string:
        sleep(5)
        create_single_file(fight_name, override)
        return

    encounter = json.loads(string)
    for entry in encounter['events']:
        try:
            if entry['ability']['name'] == identifiers[JOB.name]:
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

    action_output_path = f"{XIV_PATH}/jobs/{Tank.__qualname__}/{JOB.name}/{fight_name}.txt"
    with open(action_output_path, 'w') as f:
        for line in actions:
            f.write(f"{line}\n")
    actions.clear()

def create_raid_tier(force_refresh = False):
    amount_of_fights = (RAID_TIER[members[-1]].value + 1) - RAID_TIER[members[0]].value
    for x in range(amount_of_fights):
        create_single_file(members[x], force_refresh)

def main():
    #create_single_file("P4SP2", True)
    create_raid_tier()

if __name__ == '__main__':
    main()