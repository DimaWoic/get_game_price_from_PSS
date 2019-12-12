import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string


def send_mail(addr_to, body):
    addr_from = "svgetbot@yandex.ru"

    password = "zxcvbnM123"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Скидки на игры в PS4 Store'

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.yandex.com', 587)
    tls = server.starttls()
    print(tls)
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()

def game_price(url):
    page = requests.get(url)
    pagesoup = BeautifulSoup(page.text, 'html.parser')
    title = pagesoup.find('h2', class_='pdp__title').text
    price = pagesoup.find('h3', class_='price-display__price').text
    b = ''
    for num in price:
        if num.isdigit() == True:
            b = b+num
    if 1500 > int(b):
        item = title + " " + price + ' '
    else:
        item = None
    return item


def get_list_games(url):
    link = []
    page = requests.get(url)
    pagesoup = BeautifulSoup(page.text, 'html.parser')
    list_product = pagesoup.find('div', class_='grid-cell-container')
    all_link = list_product.findAll('a')
    for i in all_link:
        link_a = i.get('href')
        link.append('https://store.playstation.com' + link_a)
    return link


url = 'https://store.playstation.com/ru-ru/grid/search-game/1?gameContentType=games%2Cbundles&platform=ps4&query=assassin'
list_link = set(get_list_games(url))
list_games = ''
for i in list_link:
    if game_price(i) == None:
        pass
    else:
        list_games = (list_games + '<p>' + game_price(i) + '</p>')

send_mail('wdv85@mail.ru', list_games)



