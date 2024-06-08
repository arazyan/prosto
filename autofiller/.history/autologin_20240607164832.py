from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# api.prostospb.team credentials
# https://api.prostospb.team/auth/
username = "kolbasovaann@gmail.com"
password = "12345678"

# initialize the Chrome driver
driver = webdriver.Chrome("chromedriver")
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver/", options=chrome_options )


# head to login page
driver.get("https://api.prostospb.team/auth/")
