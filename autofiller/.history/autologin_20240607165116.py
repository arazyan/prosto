from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import time
# api.prostospb.team credentials
# https://api.prostospb.team/auth/
username = "kolbasovaann@gmail.com"
password = "12345678"

# initialize the Chrome driver
driver = webdriver.Chrome(executable_path="C:\Users\prosto_coworker\Documents\Desktop\Компаратор\chromedriver.exe")

# head to login page
driver.get("https://api.prostospb.team/auth/")
time.sleep(30)