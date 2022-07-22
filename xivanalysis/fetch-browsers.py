from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from seleniumwire import webdriver 
from time import sleep

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.fflogs.com/zone/rankings/44#boss=79&metric=dps&class=Global&spec=Gunbreaker")
element = driver.find_element(by=By.XPATH ,value="/html/body/div[2]/div/div/div/div[2]/div/button[2]/span")
element.click()
driver.implicitly_wait(1)
element = driver.find_element(by=By.XPATH ,value="/html/body/div[3]/div[3]/div[2]/div[2]/div/div[4]/div[2]/table/tbody/tr[1]/td[2]/div/div[1]/a[1]")
element.click()

fflog = driver.current_url
fflog = fflog[31:]
fflog = fflog.partition("#")
fight_url= fflog[0]
fflog = fflog[2]
fflog = fflog[6:]
fflog = fflog.partition("&")
fight_id = int(fflog[0])

driver.get(f"https://xivanalysis.com/fflogs/{fight_url}/{fight_id}")
element = driver.find_element(by=By.XPATH ,value="/html/body/div/div[2]/div[2]/div/div[1]/div/a[1]/span[1]")
element.click()
sleep(2)

for request in driver.requests:
    if request.response:
        if "https://xivanalysis.com/proxy/fflogs/report/events/" in request.url:
            sides = request.url.partition("events/")
            print(sides[2])  

driver.quit()