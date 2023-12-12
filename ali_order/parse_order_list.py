from tools.cookie_tools import auth
from tools.create_browser import ChromeDriver
from ali_order.order_parser import ParsedOrderDetails
from ali_order.read_orders_hrefs import get_orders_hrefs, wait_for, By


def parse_order_list():
    print('Hello selenium')
    url = "https://www.aliexpress.com/p/order/index.html"

    with ChromeDriver() as driver:
        print('Start load url:')
        driver.get(url)

        print('start auth:')
        auth(driver, 'session')

        print('get orders hrefs:')
        hrefs = get_orders_hrefs(driver)
        # hrefs = hrefs[5:10]
        hrefs = hrefs[0:3]
        for order_detail_href in hrefs:
            driver.get(order_detail_href)
            wait_for(driver, lambda d: d.find_element(By.CLASS_NAME, "order-wrap"))
            item = ParsedOrderDetails(driver)
            print(item.to_string())
