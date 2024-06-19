from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import mytime

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

# бот будет выглядеть как поросенок
# порося бот

output = qr.inputs

quars = [x.strip() for x in output.split('\n')]
# quars = quars[:30]


username_meetup_time = []
times = mytime.export_time('exported.csv')

available_size = min(len(quars), len(times))
quars = quars[:available_size+1]
times = times[:available_size+1]

time.sleep(5)

for i, quar in enumerate(quars):
  if '.xn--' in quar:
    quar = old_to_new(quar)

  try:
    username_meetup = get_username(quar)
    username_meetup.append(times[i])
    username_meetup_time.append(username_meetup)
  except:
    print('опа, несовпады размерностей куаров и часиков')
    print(len(times))
    print(len(quars))
    print(i)
    exit(1)

username_meetup_time = username_meetup_time[::-1]
print()
print(username_meetup_time)
time.sleep(5)

# мэйн ответ ------------------------------------------------
username_time = []
in_list = {}
for username, meetup, time in username_meetup_time:
  if meetup == 'Не удалось распознать qr': continue
  
  if not in_list.get(username, False):
    username_time.append(f'{username},{time}\n')
    in_list[username] = True

with open('result.csv', 'w') as file:
  file.writelines(username_time)
# print(username_time)
# time.sleep(5)
# for sublist in username_meetup_time:
  # print(sublist)

answer = {}
unique_answer = set()

# print(username_meetup_time)


# считываем имя, мероприятие и время посещения
# это нужно, чтобы учитывать дубли
for username, meetup, time in username_meetup_time:
  # print(answer)
  # print(username, meetup, time)
  if meetup not in answer:
    answer[meetup] = {}
  if username not in answer[meetup]:
    answer[meetup][username] = time

# answer это уникальный список
# подготовим столбцы для будущего датафрейма
nums_column = []
name_column = []
time_column = []

num = 1
for meetup in answer:
  if meetup == 'Не удалось распознать qr':
    continue
  nums_column.append(None)
  nums_column.append(None)
  nums_column.append(None)
  name_column.append('-'*len(meetup))
  name_column.append(meetup)
  name_column.append('-'*len(meetup))
  time_column.append(None)
  time_column.append(None)
  time_column.append(None)

  for username in answer[meetup]:
    nums_column.append(num)
    name_column.append(username)
    time_column.append(time)

    num += 1
  # добавляем пропуски для читабельности
  nums_column.append(None)
  name_column.append(None)
  time_column.append(None)

print(len(nums_column))
print(len(name_column))
print(len(time_column))

print()

# добавим список неудавшихся куаров
try:
  answer['Не удалось распознать qr']

  nums_column.append(None)
  nums_column.append(None)
  nums_column.append(None)
  name_column.append('-'*len('Не удалось распознать qr'))
  name_column.append('Не удалось распознать qr')
  name_column.append('-'*len('Не удалось распознать qr'))
  time_column.append(None)
  time_column.append(None)
  time_column.append(None)

  nums_column.extend([None]*len(answer['Не удалось распознать qr']))
  name_column.extend(list(answer['Не удалось распознать qr']))
  time_column.extend([None]*len(answer['Не удалось распознать qr']))
except:
  pass

# сохраняем датафрейм
import pandas as pd
df = pd.DataFrame()

df['Num']         = [str(x) if x != None else None for x in nums_column]
df['Name/Meetup'] = name_column
df['Time']        = time_column

df.to_csv('test.csv')
# print(df)




# -------------------
# print(answer)
# красивый вывод
# for meetup in answer:
#   intro = f'----{meetup}----'
#   outro = '-'*len(intro)
#
#   print(intro)
#
#   for username in answer[meetup]:
#     print(f'{username}  {answer[meetup][username]}')
#
#   print(outro)
# # -------------------


# exit(1)

def beauty_res_output(s):
  with open('detailed.txt', 'w') as file:
    for k in s:
      if k == "Некорректные данные":
        s.remove(k)
        continue
      intro = f'----{k}----'
      outro = '-'*len(intro)

      file.write(f'{intro}\n')

      for person in s[k]: 
        file.write(f'{person}\n') 

      file.write(f'\nВсего: {len(s[k])}\n')
      file.write(f'{outro}\n\n')

# beauty_res_output(answer)

# коды, которые не распознались, можно как-нибудь отдельно выделить
for meetup in answer:
  if meetup == 'Не удалось распознать qr':
    continue
  for subset in answer[meetup]:
    for username in subset:
      # make_csv.create_csv()
      pass


# print(unique_answer)
# printpas
# print(answer)
# beauty_res_output(answer)

# unique_answer_sorted = sorted(list(unique_answer))

unique_answer_list = list(unique_answer)
# print(f'\n\tСписок для вставки в таблицу\n\t{'-'*28}')
# for x in unique_answer_list: print(x)

# дополнительная инфа
# print()
# print(f'{len(unique_answer_list)} записей')
# print()
# print(f'{int(time.time() - start)} сек.')
