from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def main():

    # open google chrome browser and login in us.shein.com
    driver = webdriver.Chrome()
    driver.implicitly_wait(4)

    username = input('Username: ')
    password = input('Password: ')
    shein_login(driver, username, password)

    # Get order number
    order = input("Order No: ")
    shein_orders_url = 'https://us.shein.com/user/orders/detail/' + order

    driver.get(shein_orders_url)


    # Get urls of the items in x Shein order.
    items_urls = get_shein_items_urls(driver)

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


def shein_login(driver, username, password):
    """
    Go to shein login page, find text inputs and write user and pass using send_keys
    """
    go_to_url('https://us.shein.com/user/auth/login')

    # find user text input and send username
    user_input = driver.find_element(By.XPATH, '//div[@class="ksLow S-input S-input_suffix"]//*[contains(@aria-label,"Email Address:")]')
    user_input.send_keys(username)

    pass_input = driver.find_element(By.XPATH, '//div[@class="ksLow S-input S-input_suffix"]//*[contains(@aria-label,"Password:")]')
    pass_input.send_keys(password)


def get_shein_items_urls(driver):
    urls = []


    return urls


    


if __name__ == '__main__':
    main()



