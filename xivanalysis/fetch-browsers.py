from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from seleniumwire import webdriver 
from time import sleep

class Pandaemonium(Enum):
    P1S =   78
    P2S =   79
    P3S =   80
    P4SP1 = 81
    P4SP2 = 82

class Jobs(Enum):
    PLD = "Paladin"
    GNB = "Gunbreaker"

JOB     = Jobs.GNB
RAID_TIER = Pandaemonium.__qualname__
api_list = []

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for x in range(Pandaemonium.P1S.value, Pandaemonium.P4SP2.value + 1):
    driver.get(f"https://www.fflogs.com/zone/rankings/44#boss={x}&metric=dps&class=Global&spec={JOB.value}")
    if x is 78:
        cookies = driver.find_element(by=By.XPATH ,value="/html/body/div[2]/div/div/div/div[2]/div/button[2]/span")
        sleep(1)
        cookies.click()
    top_player = driver.find_element(by=By.XPATH ,value="/html/body/div[3]/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[2]/div/div[1]/a[1]")
    sleep(1)
    top_player.click()

    fflog = driver.current_url
    fflog = fflog[31:]
    fflog = fflog.partition("#")
    fight_url= fflog[0]
    fflog = fflog[2]
    fflog = fflog[6:]
    fflog = fflog.partition("&")
    fight_id = int(fflog[0])

    driver.get(f"https://xivanalysis.com/fflogs/{fight_url}/{fight_id}")
    sleep(1)
    top_player = driver.find_element(by=By.XPATH ,value="/html/body/div/div[2]/div[2]/div/div[1]/div/a[1]/span[1]")
    top_player.click()
    sleep(2)

for request in driver.requests:
    if request.response:
        if "https://xivanalysis.com/proxy/fflogs/report/events/" in request.url:
            api_url = request.url.partition("events/")
            api_list.append(f"{api_url[2]}\n")
driver.quit()

with open(f"{RAID_TIER}.txt", 'w') as f:
    for line in api_list:
        f.write(line)