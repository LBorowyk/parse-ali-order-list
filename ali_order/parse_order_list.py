from tools.base_utils import extract_file_name_from_url
from tools.cookie_tools import auth
from tools.create_browser import ChromeDriver
from ali_order.order_parser import ParsedOrderDetails
from ali_order.read_orders_hrefs import get_orders_hrefs, wait_for, By
from tools.file_tools import save_image, download_image


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

        print('found ' + str(len(hrefs)) + ' hrefs for parsing')

        data = ""
        # hrefs = hrefs[0:5]
        # hrefs = hrefs[0:3]
        for order_detail_href in hrefs:
            driver.get(order_detail_href)
            wait_for(driver, lambda d: d.find_element(By.CLASS_NAME, "order-wrap"))
            item = ParsedOrderDetails(driver)
            # for detail in item.items:
            #     if detail.image_url:
            #         save_image(
            #             download_image(detail.image_url),
            #             extract_file_name_from_url(detail.image_url)
            #         )
            data = data + item.to_string() + "\n\n"

        with open('result.txt', 'w') as file:
            file.write(data)
            # print(item.to_string())
