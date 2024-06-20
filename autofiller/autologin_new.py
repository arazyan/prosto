from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

import dataframe

start = time.time()

from standartize import old_to_new
# import qr

driver = webdriver.Chrome()
# meetups = {}

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
  errors = driver.find_elements("css selector", ".flash-error")
  if any(error_message in e.text for e in errors):
    print("[!] Login failed")
  else:
    print("[+] Login successful")


# входим в аккаунт
auth()


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
      username += (' ' + name.strip())

  tmp = username.strip().split() 
  username = tmp[1] + ' ' + tmp[0]
  return [username.strip(), 'Новый пользователь (подтверждение профиля)']


def extract_user(qr_link: str):
  """Извлекает данные пользователя коворкинга или мероприятия."""
  driver.get(qr_link)

  page_waiting()

  text = driver.find_element("xpath", "//div[@class='alert alert-danger']").text

  meetup = text.split('на мероприятие ')[-1].replace("\'", "").strip()
  username = text[text.find('Пользователь')+len('Пользователь '): text.find(' уже отмечен')]

  return [username, meetup]


def get_username(qr_link: str):
  """Получить имя. Если не удается распарсить, возвращает неудачу."""
  try:
    if 'confirm_user' in qr_link:
      return extract_from_new_user(qr_link)
    elif 'form_participation' in qr_link:
      return extract_user(qr_link)
  except:
    # лучше бы записывать все в файлик
    # print(err)
    print(qr_link)
  return [qr_link, 'Не удалось распознать qr']


def quars_regularization(quar_time_pairs):
  """Стандартизирует куар-коды в единый вид."""
  for i in range(len(quar_time_pairs)):
    if '.xn--' in quar_time_pairs[i][0]:
      quar_time_pairs[i][0] = old_to_new(quar_time_pairs[i][0])


def fill_structrues(quar_time_pairs):
  """Заполняет объекты данными."""
  i = 0
  for quar, time in quar_time_pairs:
    GOFORWARD = True
    name, meetup = get_username(quar)
    if meetup.startswith('Не удалось'):
      brokens.append(i)
      GOFORWARD = False

    # записываем отдельно меру и имя
    if meetup not in meetup_names:
      meetup_names[meetup] = set()
    meetup_names[meetup].add(name)

    if 'с ID=' in name:
      try:
        answer.pop(name)
      except:
        pass   # записываем человека и во сколько он пришел
      continue

    # сохраняем только людей, которые пришли в коворкинг на карповку
    # потому как в табличке нужно записывать по факту пришедших в коворк
    if GOFORWARD and 'ПРОСТО на Карповке'.lower() in meetup.lower() or 'Новый пользователь'.lower() in meetup.lower():
      if name not in answer:
        answer[name] = time
        # for debug:
        # answer[name] = [time, quar]
      else:
        # print(answer[name])
        # print(time, quar)
        repeats.append(i)


    i += 1

  print(f'answer length: {len(answer)}')


def save_table(filename: str):
  """Выгрузка"""
  with open(filename, 'w') as file:
    for name in answer:
      file.write(f'{name}\n')

    file.write('\n')

    for name in answer:
      file.write(f'{answer[name]}\n')


def save_details(filename: str):
  """Детали"""
  with open(filename, 'w') as file:
    for meetup in meetup_names:
      file.write('-'*len(meetup) + '\n')
      file.write(f'{meetup}'     + '\n')
      file.write('-'*len(meetup) + '\n')
      
      for name in meetup_names[meetup]:
        file.write(name + '\n')

      file.write('\n')
# ------------------------------------------------------------------------------------------------------
# Конец функционального блока
# ------------------------------------------------------------------------------------------------------

quar_time = dataframe.qr_time_sorted
# quar_time = quar_time[30:60]

# стандартизируем куары
quars_regularization(quar_time_pairs=quar_time)

meetup_names = {}
answer = {}
repeats = []
brokens = []

fill_structrues(quar_time_pairs=quar_time)

save_table('выгрузка.txt')
save_details('детали.txt')



# print(len(quar_time))
# print(len(answer))
# print(answer)
# for idx, pair in enumerate(quar_time):
  # print(idx, pair)

# print(brokens)
# посмотрим на не куары
# for broken_idx in brokens:
  # print(quar_time[broken_idx])
# print(repeats)



