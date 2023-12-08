from cookie_tools import auth
from create_browser import ChromeDriver
from order_parser import ParsedOrderDetails
from read_orders_hrefs import get_orders_hrefs, wait_for, By

print('Hello selenium')
url = "https://www.aliexpress.com/p/order/index.html"

with ChromeDriver() as driver:
    print('Start load url:')
    driver.get(url)

    print('start auth:')
    auth(driver, 'session')

    print('get orders hrefs:')
    hrefs = get_orders_hrefs(driver);

    for order_detail_href in hrefs[0:3]:
        driver.get(order_detail_href)
        wait_for(driver, lambda d: d.find_element(By.CLASS_NAME, "order-wrap"))
        item = ParsedOrderDetails(driver)
        print(item.to_string())