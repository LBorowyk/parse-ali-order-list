from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from tools.webpage_utils import wait_for, scroll_to


def get_order_items(driver):
    return driver.find_elements(By.CLASS_NAME, "order-item")


def get_order_more_button(driver):
    try:
        order_mode = driver.find_element(By.CLASS_NAME, "order-more")
        return order_mode.find_element(By.TAG_NAME, "button") if order_mode is not None else None
    except NoSuchElementException:
        return None


def get_order_detail_href(item):
    header = item.find_element(By.CLASS_NAME, "order-item-header-right")
    return header.find_element(By.TAG_NAME, "a").get_attribute('href') if header is not None else None


def load_full_order_list(driver):
    print("Wait for order-content")
    wait_for(driver, lambda d: d.find_element(By.CLASS_NAME, "order-content"), 100)
    # driver.minimize_window()

    def calc_order_items_len(d):
        return len(get_order_items(d))

    current_items_len = calc_order_items_len(driver)
    order_more_button = get_order_more_button(driver)

    while order_more_button is not None:
        scroll_to(driver, order_more_button)
        order_more_button.click()
        wait_for(driver, lambda d: calc_order_items_len(d) > current_items_len)
        current_items_len = calc_order_items_len(driver)
        order_more_button = get_order_more_button(driver)

    print("I`m ready to parsing")


def get_orders_hrefs(driver):
    load_full_order_list(driver)
    return list(get_order_detail_href(item) for item in get_order_items(driver))
