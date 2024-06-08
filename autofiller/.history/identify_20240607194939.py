from bs4 import BeautifulSoup

page = None

with open('assets/signed.html', 'r') as file:
    page = file.read()

# Заголовки, чтобы замаскироваться под браузер
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Парсим HTML при помощи Beautiful Soup
soup = BeautifulSoup(page, 'html.parser')

with open('output.txt', 'w') as file:
    file.write(repr(soup.find_all(class_='alert alert-danger')))
print(soup.find_all(class_='alert alert-danger'))