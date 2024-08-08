import time
import os
from selenium import  webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import json

load_dotenv()
user_data_dir = os.environ.get("USER_DATA_DIR")
url = "https://www.linkedin.com/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--incognito")


def login():
    pass

driver = webdriver.Chrome(options=chrome_options)

# goto the cookie clicker site
driver.get(url)
login()