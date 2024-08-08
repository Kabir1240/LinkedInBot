import time
import os
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import json

load_dotenv()
user_data_dir = os.environ.get("USER_DATA_DIR")
url = "https://www.linkedin.com/"


SLEEP_TIME_BETWEEN_PAGES = 1
LINKEDIN_CREDS_PATH = "linkedin_creds.json"
JOBS_TO_SEARCH_PATH = "jobs_to_search.json"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
# chrome_options.add_argument("--incognito")


def login():
    with open (LINKEDIN_CREDS_PATH, 'r') as file:
        linkedin_creds = json.load(file)
    try:
        login_button = driver.find_element(By.CSS_SELECTOR, ".nav__button-secondary.btn-md.btn-secondary-emphasis")
    except NoSuchElementException as e:
        login_button = driver.find_element(By.CSS_SELECTOR, ".nav__button-secondary.btn-sm.btn-primary")
    finally:
        login_button.click()
        time.sleep(SLEEP_TIME_BETWEEN_PAGES)
    
    email_field = driver.find_element(By.ID, "username")
    email_field.send_keys(linkedin_creds["email"])
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(linkedin_creds["password"])
    
    login_button_2 = driver.find_element(By.CSS_SELECTOR, ".btn__primary--large.from__button--floating")
    login_button_2.click()
    

def search_for_jobs(keyword, location):
    time.sleep(5)
    fields = driver.find_elements(By.CSS_SELECTOR, "div.jobs-search-box__inner div.relative")
    fields[0].find_element(By.CSS_SELECTOR, "input").clear()
    fields[0].find_element(By.CSS_SELECTOR, "input").send_keys(keyword)
    
    fields[1].find_element(By.CSS_SELECTOR, "input").clear()
    fields[1].find_element(By.CSS_SELECTOR, "input").send_keys(location, Keys.ENTER)
    
    time.sleep(SLEEP_TIME_BETWEEN_PAGES * 3)
    

def apply_to_all():
    jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")
    
    # since linkedin is dynamic, we can only apply to the first 4 jobs that appear
    for job in jobs[0:5]:
        # scrolls button into view if hidden
        driver.execute_script("arguments[0].scrollIntoView(true);", job)
        job.click()
        
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary ember-view")
        apply_button.click()
        
        
    
    
driver = webdriver.Chrome(options=chrome_options)

# # Open a new tab with JavaScript
driver.execute_script("window.open('');")

# # Switch to the new tab
driver.switch_to.window(driver.window_handles[-1])

# goto the website (linkedin)
driver.get(url)
time.sleep(SLEEP_TIME_BETWEEN_PAGES)
# login()
# time.sleep(SLEEP_TIME_BETWEEN_PAGES * 3)

# this takes you to the jobs page
primary_buttons = driver.find_elements(By.CSS_SELECTOR, ".app-aware-link.global-nav__primary-link")
primary_buttons[2].click()
    
with open(JOBS_TO_SEARCH_PATH, 'r') as file:
    jobs_to_search_for = json.load(file)

easy_apply = False
for job in jobs_to_search_for:
    search_for_jobs(job["keyword"], job["location"])
    
    # if easy apply is not on, turn it on. Runs the first time only
    if not easy_apply:
        easy_apply_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Easy Apply filter."]')
        easy_apply_button.click()
        easy_apply = True
        time.sleep(SLEEP_TIME_BETWEEN_PAGES*3)
        
    apply_to_all()
