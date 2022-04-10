from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request

def main():

    # open google chrome browser and login in us.shein.com
    driver = webdriver.Chrome()
    driver.implicitly_wait(4)
    driver.maximize_window()
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
    for sku, url in items_urls.items():
        go_to_url(driver, url)
        print(image_names)
        sleep(0.5)
        download_images(driver, image_names[sku])



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
    go_to_url(driver, 'https://us.shein.com/user/auth/login')


    username = input('Username: ')
    password = input('Password: ')

    # find user text input and send username
    user_input = driver.find_element(By.XPATH, '//div[@class="ksLow S-input S-input_suffix"]//*[contains(@aria-label,"Email Address:")]')
    user_input.send_keys(username)

    pass_input = driver.find_element(By.XPATH, '//div[@class="ksLow S-input S-input_suffix"]//*[contains(@aria-label,"Password:")]')
    pass_input.send_keys(password)

    # Press submit button
    driver.find_element(By.XPATH, '//div[@class="page-login__emailLoginItem"]//div[@class="login-btn"]//button').click()
    

    sleep(10)


def get_shein_items_urls(driver, img_names):
    urls = {}
    order_rows = driver.find_elements(By.XPATH, '//table[@class="c-order-detail-table"]//tbody//tr')

    for row in order_rows:
        # get sku of each row and compare with the data to see if image download is necessary
        sku = row.find_element(By.XPATH, './/td[3]').text

        if sku in img_names.keys():
            url = row.find_element(By.XPATH, './/td[1]//div//div[2]//div//span//p//a').get_attribute('href')
            print(url)
            urls[sku] = url
    return urls
 

def download_images(driver, image_name):
    # Clickear en imagen para agrandarla
    driver.find_element(By.XPATH, '//div[@class="swiper-slide product-intro__main-item cursor-zoom-in swiper-slide-active"]').click()
    sleep(2)
    images =  driver.find_elements(By.XPATH, '//div[@class="productimg-extend__thumbnails"]//ul//li')

    
    # Hover in each of the side images and screenshot the big image
    counter = 0
    for image in images:
        hover = ActionChains(driver).move_to_element(image)
        hover.perform()  
        sleep(0.4)
        # Get full image
        full_image_url = driver.find_element(By.XPATH, '//div[@class="productimg-extend__main-image"]//img').get_attribute("src")
        full_name = 'images\\' + image_name +' (' + str(counter) + ').png'
        urllib.request.urlretrieve(full_image_url, full_name)
        counter += 1



if __name__ == '__main__':
    main()



