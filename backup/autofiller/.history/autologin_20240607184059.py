from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import time
# api.prostospb.team credentials
# https://api.prostospb.team/auth/
username = "kolbasovaann@gmail.com"
password = "12345678"

# initialize the Chrome driver
driver = webdriver.Chrome('chromedriver.exe')

# head to login page
driver.get("https://api.prostospb.team/auth/")
time.sleep(30)

# head to github login page
driver.get("https://github.com/login")
# find username/email field and send the username itself to the input field
driver.find_element("id", "login_field").send_keys(username)
# find password input field and insert password as well
driver.find_element("id", "password").send_keys(password)
# click login button
driver.find_element("name", "commit").click()
