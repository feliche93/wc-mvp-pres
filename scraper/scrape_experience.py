import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from cleantext import clean
from tqdm import tqdm

def main():

    driver = webdriver.Chrome(ChromeDriverManager().install())

    df = pd.read_csv("raw_all_profiles.csv")

    profile_links = df["profile_link"].to_list()
    experience_links = [link + "#experience" for link in profile_links]

    experiences = pd.DataFrame()

    for experience_link in tqdm(experience_links):

        driver.get(experience_link)

        try:
            experience = driver.find_element(
                By.XPATH,
                '//div[@class="field field--name-field-personal-projects field--type-text-long field--label-hidden field--items"]',
            )
            experience = clean(
                experience.text, fix_unicode=True, to_ascii=True, no_line_breaks=True, lower=False, no_punct=False
            )
        except:
            experience = ""

        experience = pd.DataFrame(
            [
                {
                    "profile_link": experience_link.split("#")[0],
                    "experience": experience,
                }
            ]
        )

        experiences = experiences.append(experience)

    experiences.to_csv("raw_experiences.csv", index=False)


if __name__ == "__main__":
    main()
