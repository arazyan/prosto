from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
start = time.time()

from standartize import old_to_new
import qr

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
  return username.strip(), 'Новый пользователь (подтверждение профиля)'


def extract_user(qr_link: str):
  """Извлекает данные пользователя коворкинга или мероприятия."""
  driver.get(qr_link)

  page_waiting()

  text = driver.find_element("xpath", "//div[@class='alert alert-danger']").text

  meetup = text.split('на мероприятие ')[-1].replace("\'", "").strip()
  username = text[text.find('Пользователь')+len('Пользователь '): text.find(' уже отмечен')]

  return username, meetup


def get_username(qr_link: str):
  try:
    if 'confirm_user' in qr_link:
      return extract_from_new_user(qr_link)
    elif 'form_participation' in qr_link:
      return extract_user(qr_link)
  except Exception as err:
    # лучше бы записывать все в файлик
    # print(err)
    print(qr_link)
  return qr_link, 'Не удалось распознать qr'

# бот будет выглядеть как поросенок
# порося бот

output = qr.inputs

quars = [x.strip() for x in output.split('\n')]


username_meetups = []
for quar in quars:
  if '.xn--' in quar:
    quar = old_to_new(quar)

  username_meetups.append(get_username(quar))

answer = {}
unique_answer = set()

for username, meetup in username_meetups:
  if meetup not in answer:
    answer[meetup] = set() 
  answer[meetup].add(username)

def beauty_res_output(s):
  with open('detailed.txt', 'w') as file:
    for k in s:
      if k == "Некорректные данные":
        s.remove(k)
        continue
      intro = f'----{k}----'
      outro = '-'*len(intro)

      file.write(f'{intro}\n')

      for person in s[k]: file.write(f'{person}\n') 

      file.write(f'\nВсего: {len(s[k])}\n')
      file.write(f'{outro}\n\n')



for k in answer:
  if k == 'Не удалось распознать qr':
    continue
  for v in answer[k]:
    unique_answer.add(v)

beauty_res_output(answer)

# unique_answer_sorted = sorted(list(unique_answer))
unique_answer_sorted = list(unique_answer)
print(f'\n\tСписок для вставки в таблицу\n\t{'-'*28}')
for x in unique_answer_sorted: print(x)

# дополнительная инфа
print()
print(f'{len(unique_answer_sorted)} записей')
print()
print(f'{int(time.time() - start)} сек.')

