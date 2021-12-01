import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from cleantext import clean
from tqdm import tqdm


driver = webdriver.Chrome(ChromeDriverManager().install())

df = pd.read_csv('raw_all_profiles.csv')

profile_links = df['profile_link'].to_list()

detailed_profiles = pd.DataFrame()


for profile_link in tqdm(profile_links):

    driver.get(profile_link)

    try:
        education = driver.find_element(By.XPATH, '//div[@class="field field--name-field-education field--type-entity-reference-revisions field--label-above"]')
        education_list = education.find_elements(By.XPATH, './/div[@class="paragraph paragraph--type--education paragraph--view-mode--default"]')
        education_list = [clean(x.text, fix_unicode=True, to_ascii=True, no_line_breaks=True, lower=False, no_punct=False) for x in education_list]
    except:
        education_list = []

    try:
        bars_and_ccourts = driver.find_element(By.XPATH, '//div[@class="field field--name-field-admissions field--type-entity-reference field--label-above"]')
        bars_and_ccourts_list = bars_and_ccourts.find_elements(By.XPATH, './/div[@class="field--item"]')
        bars_and_ccourts_list = [clean(x.text, fix_unicode=True, to_ascii=True, no_line_breaks=True, lower=False, no_punct=False) for x in bars_and_ccourts_list]
    except:
        bars_and_ccourts_list = []

    try:
        languages = driver.find_element(By.XPATH, '//div[@class="field field--name-field-spoken-languages field--type-entity-reference field--label-above"]')
        languages_list = languages.find_elements(By.XPATH, './/div[@class="field--item"]')
        languages_list = [clean(x.text, fix_unicode=True, to_ascii=True, no_line_breaks=True, lower=False, no_punct=False) for x in languages_list]
    except:
        languages_list = []

    detailed_profiles = detailed_profiles.append(pd.DataFrame([
        {
            'profile_link': profile_link,
            'education': education_list,
            'bar_court': bars_and_ccourts_list,
            'language': languages_list
        }
    ]))

education = detailed_profiles[['profile_link','education']].explode('education')
languages = detailed_profiles[['profile_link','language']].explode('language')
bar_court = detailed_profiles[['profile_link','bar_court']].explode('bar_court')

education.to_csv('education.csv', index=False)
languages.to_csv('languages.csv', index=False)
bar_court.to_csv('bar_court.csv', index=False)
