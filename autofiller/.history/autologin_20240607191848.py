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
# find login field and send the username itself to the input field
driver.find_element("id", "username").send_keys(username)
# find password input field and insert password as well
driver.find_element("id", "password").send_keys(password)
# click login button
driver.find_element("name", "AUTH_ACTION").click()

# wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
# get the errors (if there are)
errors = driver.find_elements("css selector", ".flash-error")
# print the errors optionally
# for e in errors:
#     print(e.text)
# if we find that error message within errors, then login is failed
if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")

