from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
# import pychrome

from cookie_tools import auth
from create_browser import create_chrome_driver

from selenium.webdriver.support.expected_conditions import staleness_of

def wait_for_page_load(driver, timeout=30):
    old_page = driver.find_elements(By.CLASS_NAME, "order-wrap")
    yield
    WebDriverWait(driver, timeout).until(
        staleness_of(old_page)
    )

print('Hello selenium')
url = "https://www.aliexpress.com/p/order/index.html"
# url = "https://fox.com"

print('create browser:')
driver = create_chrome_driver()

print('Start load url:')
driver.get(url)

print('start auth:')
auth(driver, 'session')

def get_order_items(driver):
    return driver.find_elements(By.CLASS_NAME, "order-item")

def get_order_more_button(driver):
    try:
        order_mode = driver.find_element(By.CLASS_NAME, "order-more")
        print(order_mode, order_mode is not None)
        return order_mode.find_element(By.TAG_NAME, "button") if order_mode is not None else None
    except NoSuchElementException:
        return None

print("Wait for order-content")
WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.CLASS_NAME,"order-content"))

print("I`m ready to parsing")

current_items_len = len(get_order_items(driver))
order_more_button = get_order_more_button(driver)

while order_more_button is not None:
    ActionChains(driver).move_to_element(order_more_button).perform()
    order_more_button.click()
    WebDriverWait(driver, timeout=30).until(lambda d: len(get_order_items(driver)) > current_items_len)
    current_items_len = len(get_order_items(driver))
    order_more_button = get_order_more_button(driver)

items = get_order_items(driver)
print("items length = ", len(items))

# for item in items: 
#     links = item.find_elements(By.TAG_NAME, "a")
#     # print(links)

time.sleep(200)

driver.quit()
print('Finish parsing')