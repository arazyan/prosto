from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument(r'user-data-dir=/home/sad/git/prosto/whatsapp_sender/profile') # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--profiling-flush=n')
options.add_argument('--enable-aggressive-domstorage-flushing')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)


# numbers = ["+70000000000", "+70000000001"]
numbers = ["+79036508174", "+79516476056", "+79806401418"]
text = "Привет+мир!"
# xpathbtn = "//button[@data-testid='compose-btn-send']"
xpathbtn = """//div[@class='_ak1t _ak1u']"""

for number in numbers:

    url = f"https://web.whatsapp.com/send?phone={number}&text={text}"
    driver.get(url)
    # sleep(50)

    wait.until(EC.element_to_be_clickable((By.XPATH, xpathbtn)))
    driver.find_element(By.XPATH, xpathbtn).click()
    sleep(1)
