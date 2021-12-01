from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import os
import time
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

def scroll_down():
    # Get scroll height after first time page load
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_profiles():

    profiles = pd.DataFrame()

    bio_cards = driver.find_elements(By.XPATH, '//div[@class="bio-item-wrapper col-xs-12 col-sm-6"]')

    for card in bio_cards:
        name = card.find_element(By.XPATH, './/h4/a/span').text
        title_location = card.find_element(By.XPATH, './/div[@class="lawyer-role-offices"]').text
        try:
            telephone = card.find_element(By.XPATH, './/li').text
        except:
            telephone = None
        try:
            email = card.find_element(By.XPATH, './/div[@class="field field--name-field-email field--type-email field--label-hidden field--item"]').text
        except:
            email = None
        profile_link = card.find_element(By.XPATH, './/h4/a').get_attribute('href')
        image_link = card.find_element(By.XPATH, './/img').get_attribute('src')

        profile = pd.DataFrame([{
            'name': name,
            'title_location': title_location,
            'telephone': telephone,
            'email': email,
            'profile_link': profile_link,
            'image_link': image_link
        }])

        profiles = profiles.append(profile)

    return profiles


def main():

    all_profiles = pd.DataFrame()

    driver.get("https://www.whitecase.com/")

    driver.maximize_window()

    locations=["AU", "846", "856", "741", "746", "931", "CA", "CN", "946", "911", "921", "936", "DE", "731", "736", "961", "951", "826", "IN", "IL", "821", "916", "771", "886", "751", "851", "816", "876", "756", "94401", "841", "791", "896", "906", "796", "801", "891", "CH", "786", "75056", "866", "TW", "881", "TH", "811", "AE", "926", "941", "US", "836", "956", "901", "776", "726", "861", "831", "871", "781", "806"]

    location_urls = [
        f'https://www.whitecase.com/people/all/all/all/{location}/all/all/search_api_relevance/DESC'
        for location in locations
    ]

    for location in tqdm(location_urls):

        driver.get(location)
        scroll_down()
        profiles = scrape_profiles()

        all_profiles = all_profiles.append(profiles)

    all_profiles.drop_duplicates('email', inplace=True)
    all_profiles.to_csv('raw_all_profiles.csv', index=False)

if __name__ == "__main__":
    main()