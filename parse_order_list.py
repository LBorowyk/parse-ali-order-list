from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
# import pychrome

from cookie_tools import auth
from create_browser import create_chrome_driver

# from selenium.webdriver.support.expected_conditions import staleness_of

# def wait_for_page_load(driver, timeout=30):
#     old_page = driver.find_elements(By.CLASS_NAME, "order-wrap")
#     yield
#     WebDriverWait(driver, timeout).until(
#         staleness_of(old_page)
#     )

print('Hello selenium')
url = "https://www.aliexpress.com/p/order/index.html"

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
        return order_mode.find_element(By.TAG_NAME, "button") if order_mode is not None else None
    except NoSuchElementException:
        return None

def wait_for(driver, func):
    WebDriverWait(driver, timeout=30).until(func)

def get_order_detail_href(item):
    header = item.find_element(By.CLASS_NAME, "order-item-header-right")
    if header is not None:
        return header.find_element(By.TAG_NAME, "a").get_attribute('href')

print("Wait for order-content")
wait_for(driver, lambda d: d.find_element(By.CLASS_NAME, "order-content"))

print("I`m ready to parsing")

'''
current_items_len = len(get_order_items(driver))
order_more_button = get_order_more_button(driver)

while order_more_button is not None and current_items_len < 20:
    ActionChains(driver).move_to_element(order_more_button).perform()
    order_more_button.click()
    wait_for(driver, lambda d: len(get_order_items(d)) > current_items_len)
    current_items_len = len(get_order_items(driver))
    order_more_button = get_order_more_button(driver)
'''

items = get_order_items(driver)
print("items length = ", len(items))

hrefs = list(get_order_detail_href(item) for item in items)
# print(hrefs)

def get_text_excluding_children(driver, element):
    child_texts = '.*'.join(c.text for c in element.find_elements(By.XPATH, ".//*"))
    print(child_texts, element.text)
    return element.text

class ParsedOrderDetails:
    def __init__(self, driver):
        self.driver = driver
        self.parseStatus()
        self.parseContactInfo()

    def to_string(self):
        return f'''
        status = {self.status}
        contact_info = {self.contact_info}
        order_info = {self.order_info}
        '''
    
    def parseStatus(self):
        self.status = self.driver.find_element(By.CLASS_NAME, "order-block-title").text

    def parseContactInfo(self):
        [contact_info, order_info] = self.driver.find_element(By.CLASS_NAME, "order-detail-info").find_elements(By.CLASS_NAME, "order-detail-info-content")
        self.contact_info = list({"value": get_text_excluding_children(self.driver, el), "tag": el.get_attribute("data-pl")} for el in contact_info.find_elements(By.TAG_NAME, 'div'))
        self.order_info = list({"value": get_text_excluding_children(self.driver, el), "tag": el.find_element(By.TAG_NAME, 'span').get_attribute("data-pl")} for el in order_info.find_elements(By.CLASS_NAME, 'info-row'))

for order_detail_href in hrefs[0:3]:
    driver.get(order_detail_href)
    wait_for(driver, lambda d: d.find_element(By.CLASS_NAME, "order-wrap"))
    item = ParsedOrderDetails(driver)
    print(item.to_string())
    """
    

    orderid = driver.find_element(By.XPATH, "//span[@data-pl='order_detail_gray_id']").text
    print(f'''href={order_detail_href}
    orderid = {orderid}
    status = {status}
    contract_info = {contract_info}
    ''')   
    """

# time.sleep(200)

driver.quit()
print('Finish parsing')