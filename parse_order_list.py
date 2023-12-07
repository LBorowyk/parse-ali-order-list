import pychrome
from selenium.webdriver.common.by import By
import time

from cookie_tools import auth
from create_browser import create_chrome_driver

print('Hello selenium')
url = "https://www.aliexpress.com/p/order/index.html"

print('create browser:')
driver = create_chrome_driver()

print('Start load url:')
driver.get(url)

print('start auth:')
auth(driver, 'session')

def output_start(**kwargs):
    print('start', kwargs)

dev_tools = pychrome.Browser(url="http://localhost:9090")
tab = dev_tools.list_tab()[0]
tab.start()

driver.get(url)

tab.call_method(
    "Network.emulateNetworkConditions", 
    offline=False,
    latency=100,
    downloadThroughput=93750,
    uploadThroughput=31250,
    connectionType="wifi"
)

tab.call_method("Network.enable", _timeout=20)
tab.set_listener("Network.requestWillBeSent", output_start)




# submit_button = driver.find_element(By.CLASS_NAME, "comet-btn-primary")
# if submit_button is not None:
#     submit_button.click()
#     print('submit_button click')




# print('Get requests:')
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

# time.sleep(2000)


driver.quit()
print('Finish parsing')