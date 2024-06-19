from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# api.prostospb.team credentials
# c
username = "kolbasovaann@gmail.com"
password = "12345678"

# initialize the Chrome driver
driver = webdriver.Chrome("chromedriver")

# head to login page
driver.get("https://github.com/login")
