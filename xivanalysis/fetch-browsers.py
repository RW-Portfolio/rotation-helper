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

JOB     = Tank.PLD
RAID_TIER = Pandaemonium

XIV_PATH = f"{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))}/xivanalysis"
members = [attr for attr in dir(RAID_TIER) if not callable(getattr(RAID_TIER, attr)) and not attr.startswith("__")]
api_list = []

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for x in range(RAID_TIER[members[0]].value, RAID_TIER[members[-1]].value + 1):
    driver.get(f"https://www.fflogs.com/zone/rankings/44#boss={x}&metric=dps&class=Global&spec={JOB.value}")
    if x == RAID_TIER[members[0]].value:
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
    sleep(1)

for request in driver.requests:
    if request.response:
        if "https://xivanalysis.com/proxy/fflogs/report/events/" in request.url:
            api_url = request.url.partition("events/")
            api_list.append(f"{api_url[2]}\n")
driver.quit()

with open(f"{XIV_PATH}/jobs/{Tank.__qualname__}/{JOB.name}/{RAID_TIER.__qualname__}.txt", 'w') as f:
    for line in api_list:
        f.write(line)