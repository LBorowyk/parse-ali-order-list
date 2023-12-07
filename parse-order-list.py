import pychrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import pickle

cookie_file_name = 'session'

def dump_cookies(driver):
    pickle.dump(driver.get_cookies(), open(cookie_file_name, 'wb'))
    print('Cookies were saving')

def load_cookies(driver):
    for cookie in pickle.load(open(cookie_file_name, 'rb')):
        driver.add_cookie(cookie)
    print('Cookies were loading')
    driver.refresh()

def init_stealth(driver):
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start_maximized")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.headless = True
    driver = webdriver.Chrome(options=options)
    init_stealth(driver)
    return driver

print('Hello selenium')
driver = create_chrome_driver()

url = "https://www.aliexpress.com/p/order/index.html"
driver.get(url)





# submit_button = driver.find_element(By.CLASS_NAME, "comet-btn-primary")
# if submit_button is not None:
#     submit_button.click()
#     print('submit_button click')

input("Are you ready?")
print('Refresh page')
driver.get(url)

print('Get requests:')
# print(driver.requests)

# for request in driver.requests:
#     if request.response:
#         print(
#             request.url,
#             request.response.status_code, 
#             request.response.headers['Content-Type']
#         )

# print("I`m ready to parsing")

# items = driver.find_elements(By.CLASS_NAME, "order-item")
# print(items)

# for item in items: 
#     links = item.find_elements(By.TAG_NAME, "a")
#     print(links)

time.sleep(2000)
driver.quit()