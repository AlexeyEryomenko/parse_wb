# name, shop, price, old_price, grade, url_to_photo, url


from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/116.0.0.0 Safari/537.36')
options_chrome.add_argument('--disable-blink-features=AutomationControlled')


headers = ['name', 'shop', 'price', 'old_price', 'grade', 'url_to_photo', 'url']

search = input('Enter what you want to parse from wildberries site')
name = input('Enter the name of the file to which you want to write the data')


def open_browser(search, page):
    with webdriver.Chrome(options=options_chrome) as browser:
        browser.get(f'https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search={search}')

        time.sleep(4)
        for _ in range(100):
            browser.execute_script("window.scrollBy(0, 300)")

        items = browser.find_elements(By.CLASS_NAME, 'product-card__wrapper')
        list_inf = []

        for item in items:
            url = item.find_element(By.CLASS_NAME, 'product-card__link').get_attribute('href')
            price = item.find_element(By.CLASS_NAME, 'price__lower-price').text
            old_price = item.find_element(By.CLASS_NAME, 'price__wrap').find_element(By.TAG_NAME, 'del').text
            shop = item.find_element(By.CLASS_NAME, 'product-card__brand').text
            name = item.find_element(By.CLASS_NAME, 'product-card__name').text
            grade = item.find_element(By.CLASS_NAME, 'address-rate-mini').text
            photos = item.find_element(By.CLASS_NAME, 'product-card__img-wrap')
            photo_main = photos.find_element(By.CLASS_NAME, 'j-thumbnail').get_attribute('src')
            additional_photos = [i.get_attribute('href') for i in photos.find_elements(By.CLASS_NAME, 'thumbnail')]
            print([name, shop, price, old_price, grade, photo_main, url])
            list_inf.append([name, shop, price, old_price, grade, photo_main, url])

        return list_inf


def create_csv_file(name):
    with open(f'{name}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)


def filling_csv_file(name, list_inf_items):
    with open(f'{name}.csv', 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for info in list_inf_items:
            writer.writerow(info)


def main():
    create_csv_file(name)

    for i in range(1, 1001):
        try:
            items = open_browser(search, i)
            print(items)
            filling_csv_file(name, items)
        except Exception as er:
            print(er)
            break

    print('Finished')


if __name__ == '__main__':
    main()
