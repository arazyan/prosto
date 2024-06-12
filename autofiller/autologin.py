from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

driver = webdriver.Chrome()
meetups = {}

def auth():
  username = "kolbasovaann@gmail.com"
  password = "12345678"

  # initialize the Chrome driver
  # in a new selenium version there is no need to install chromedriver
  # just import it

  # head to login page
  driver.get("https://api.prostospb.team/auth/")

  # find =login field and send the username itself to the input field
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


# входим в аккаунт
auth()

# не точно
# cowork - starts on 9
# meets  - starts on 11 
#
# Аутпут должен содержать ответ вида
#
# ----Коворкинг----
# имя фамилия 1
# имя фамилия 2
# имя фамилия 3
# ...
#
#
# ----Мероприятие A----
# имя фамилия 1
# имя фамилия 2
# имя фамилия 3
# ...
#
# ----Мероприятие B----
# имя фамилия 1
# имя фамилия 2
# имя фамилия 3
# ...

# есть три типа ссылок: 
# - неподтвержденный профиль (confirm user)
# - обычная ссылка, когда человек у нас уже был 
# - мероприятия
#
#
# А если не получилось вернуть строку, то нужно вывести этот куар и сказать что не получилось
#

def page_waiting():
  """Ожидает пока веб-страница загрузится."""
  WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
  )

  wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
  wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


def extract_from_new_user(qr_link: str):
  """Извлекает данные нового пользователя (неподтвержденный профиль)."""
  driver.get(qr_link)

  page_waiting()
  form_inputs = driver.find_elements(By.CLASS_NAME, 'form-control')[0:3]

  # вычленяем имя из тегов input'а
  username = ''
  for x in form_inputs:
    name = x.get_attribute("value")
    if isinstance(name, str) and len(name) > 1:
      username += (' ' + name)

  return username.strip(), 'Новый пользователь (подтверждение профиля)'


def extract_user(qr_link: str):
  """Извлекает данные пользователя коворкинга или мероприятия."""
  # начинаем проходку по куарам
  driver.get(qr_link)

  page_waiting()

  text = driver.find_element("xpath", "//div[@class='alert alert-danger']").text

  meetup = text.split('на мероприятие ')[-1].strip()
  username = text[text.find('Пользователь')+len('Пользователь '): text.find(' уже отмечен')]

  return username, meetup



def get_username(qr_link: str):
  if 'confirm_user' in qr_link:
    return extract_from_new_user(qr_link)
  elif 'form_participation' in qr_link:
    return extract_user(qr_link)
  else:
    return qr_link, 'Не удалось распознать qr'


# api.prostospb.team credentials
# https://api.prostospb.team/auth/
#
#
# есть два случая
# - чувак уже был у нас
# - чувака у нас еще не было
# - конфирмация
# - работает ли со старым куаром?
# - куары с иксами
# бот будет выглядеть как поросенок
# порося бот
#
#
#
#





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
asdflkajds.return asldfkjsakfd
asldkfjlkdsajf
lkj"""

output = """https://www.prostospb.team/events?eventId=11917&utm_source=prosto&utm_medium=adminka&utm_campaign=pablik 
https://www.prostospb.team/proprod2?utm_source=prosto&utm_medium=adminka&utm_campaign=proPROD 
https://blackmesait.ru/yaroslav-ilchenko 
https://api.prostospb.team/api/form_participation.php?user_id=123788&event_id=9707 
https://api.prostospb.team/api/form_participation.php?user_id=147958&event_id=9707 
https://api.prostospb.team/api/form_participation.php?user_id=124855&event_id=9707 
https://api.prostospb.team/confirm_user?verification_id=156357 
https://api.prostospb.team/api/form_participation.php?user_id=156357&event_id=9707"""
# проверить, что будет на случай, если человек зарегался и впервые с неподтвержденным профилем пришел на меро
quars = [x.strip() for x in output.split('\n')]


username_meetups = []
for quar in quars:
  username_meetups.append(get_username(quar))

answer = {}
for username, meetup in username_meetups:
  if meetup not in answer:
    answer[meetup] = set() 
  answer[meetup].add(username)

def beauty_set_output(s: set):
  for k in s:
    print(f'----{k}----')
    for elem in s[k]:
      print(elem)
    print('---------')

beauty_set_output(answer)
