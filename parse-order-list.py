import pychrome
from selenium import webdriver
# from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import pickle

print('Hello selenium')

options = webdriver.ChromeOptions()
options.add_argument("start_maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.headless = True
driver = webdriver.Chrome(options=options)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True
)

url = "https://www.aliexpress.com/p/order/index.html"
driver.get(url)

# time.sleep(30)

# pickle.dump(driver.get_cookies(), open('session', 'wb'))
# print('Cookies were saving')

for cookie in pickle.load(open('session', 'rb')):
    driver.add_cookie(cookie)
print('Cookies were loading')
driver.refresh()
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