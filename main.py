from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def main():

    # open google chrome browser and login in us.shein.com
    driver = webdriver.Chrome()
    driver.implicitly_wait(4)
    shein_login(driver)

    # Get order number and go to the link
    order = input("Order No: ")
    shein_orders_url = 'https://us.shein.com/user/orders/detail/' + order
    driver.get(shein_orders_url)


    # Get urls of the items in x Shein order. Convert the data in a dictionery sku:name from the dataframe
    data =  pd.read_csv('image_names.csv', sep=';')
    data = data.to_dict('list')
    image_names = dict(zip(data['sku'], data['name']))
    items_urls = get_shein_items_urls(driver, image_names)

    # Go to each of the urls and download all the full images as webp.
    for item_url in items_urls:
        go_to_url(driver, item_url)


def go_to_url(driver, url):
    while True:
        try:
            driver.get(url)
            break
        except:
            continue


def shein_login(driver):
    """
    Go to shein login page, find text inputs and write user and pass using send_keys
    """
    go_to_url('https://us.shein.com/user/auth/login')


    username = input('Username: ')
    password = input('Password: ')

    # find user text input and send username
    user_input = driver.find_element(By.XPATH, '//div[@class="ksLow S-input S-input_suffix"]//*[contains(@aria-label,"Email Address:")]')
    user_input.send_keys(username)

    pass_input = driver.find_element(By.XPATH, '//div[@class="ksLow S-input S-input_suffix"]//*[contains(@aria-label,"Password:")]')
    pass_input.send_keys(password)


def get_shein_items_urls(driver, img_names):
    urls = []
    order_rows = driver.find_elements(By.XPATH, '//table[@class="c-order-detail-table"]//tbody//tr')


    return urls
 


if __name__ == '__main__':
    main()



