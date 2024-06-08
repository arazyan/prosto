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
    tag = soup.find(class_='alert alert-danger')
    file.write(tag.text)

with open('output.txt', 'r') as file:
    temp = file.read()
    
    l, r = temp.find('Пользователь '), temp.find('уже отмечен')
    print(temp[l+1:r])
    if l != -1 and r != -1:
        file.write(temp[l+1:r])

        

