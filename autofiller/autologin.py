from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
# api.prostospb.team credentials
# https://api.prostospb.team/auth/
#
#
# есть два случая
# - чувак уже был у нас
# - чувака у нас еще не было
#
#
#
#
username = "kolbasovaann@gmail.com"
password = "12345678"

# initialize the Chrome driver
# in a new selenium version there is no need to install chromedriver
# just import it
driver = webdriver.Chrome()

# head to login page
driver.get("https://api.prostospb.team/auth/")
quar_link = "https://api.prostospb.team/api/form_participation.php?user_id=139627&event_id=9706"
quar_link2 = "https://api.prostospb.team/api/form_participation.php?user_id=115123&event_id=9706"

# find =login field and send the username itself to the input field
driver.find_element("id", "username").send_keys(username)
# find password input field and insert password as well
driver.find_element("id", "password").send_keys(password)
# time.sleep(3)
# click login button
driver.find_element("name", "AUTH_ACTION").click()

# waiting for page to be downloaded
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


def get_username(quar_link: str) -> str:
  # начинаем проходку по куарам
  driver.get(quar_link)

  # ждем чтобы все загрузилось
  WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
  )

  # собираем данные
  ## ждем пока страница загрузится полностью
  wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
  wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
  #
  text = driver.find_element("xpath", "//div[@class='alert alert-danger']").text
  username = text[text.find('Пользователь')+len('Пользователь '): text.find(' уже отмечен')]
  return username

output = """https://api.prostospb.team/api/form_participation.php?user_id=120155&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=139627&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=27419&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=140925&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=141770&event_id=9706 
https://api.prostospb.team/confirm_user?verification_id=156308 
https://api.prostospb.team/api/form_participation.php?user_id=156308&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=147904&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=128770&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=44918&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=137744&event_id=9706 
https://api.prostospb.team/api/form_participation.php?user_id=127467&event_id=11974 
https://api.prostospb.team/api/form_participation.php?user_id=115123&event_id=9706
"""

a = [x.strip() for x in output.split('\n') if 'verification' not in x]


quar_links = a

for quar in quar_links:
  try:
    print(get_username(quar))
  except:
    print(quar)

