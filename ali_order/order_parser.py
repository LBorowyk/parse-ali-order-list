from selenium.webdriver.common.by import By
from ali_order.order_item_details_parser import OrderItemDetailsParser
from ali_order.order_tracking_details_parser import ParseTrackingInfo
from tools.webpage_utils import scroll_to, wait_for
from tools.base_parse_page import ParsePage, form_tag_value_items, extract_element_by_tag


class ParsedOrderDetails(ParsePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.status = self.parse_status()
        self.parse_contact_info()
        self.price = self.parse_order_price()
        (self.store, self.store_href) = self.parse_store()
        print("Parse items:")
        self.items = self.parse_items()
        print("Parse tracking info:")
        self.tracking = ParseTrackingInfo(self.driver, self.order_detail_id)

    def to_string(self):
        items_str = '\n'.join(item.to_string() for item in self.items)

        return f'''
        status = {self.status}
        contact_name = {self.contact_name}
        contact_phone = {self.contact_phone}
        delivery_address = {self.delivery_address}
        order_detail_id = {self.order_detail_id}
        order_detail_date = {self.order_detail_date}
        order_detail_payment = {self.order_detail_payment},
        price = {self.price},
        store = {self.store}
        store_href = {self.store_href}
        tracking = {{
            tracking_name = {self.tracking.tracking_name},
            tracking_tag = {self.tracking.tracking_tag},
            tracking_code = {self.tracking.tracking_code},
            other_track_codes = {self.tracking.other_track_codes}
        }}
        items = {{{items_str}}}
        '''
    
    def parse_status(self):
        return self.driver.find_element(By.CLASS_NAME, "order-block-title").text

    def parse_contact_info(self):
        [contact_info, order_info] = self.driver.find_element(
            By.CLASS_NAME, "order-detail-info"
        ).find_elements(By.CLASS_NAME, "order-detail-info-content")
        self.parse_customer_info(
            form_tag_value_items(
                contact_info.find_elements(By.TAG_NAME, 'div'), lambda el: el.get_attribute("data-pl")
            )
        )
        self.parse_order_info(
            form_tag_value_items(
                order_info.find_elements(By.CLASS_NAME, 'info-row'),
                lambda el: el.find_element(By.TAG_NAME, 'span').get_attribute("data-pl")
            )
        )
    
    def parse_customer_info(self, contact_info):
        (self.contact_name, self.contact_phone, self.delivery_address) = (
            extract_element_by_tag(contact_info, tag) for tag in ['contact_info', None, 'contact_info_address']
        )

    def parse_order_info(self, order_info):
        (self.order_detail_id, self.order_detail_date, self.order_detail_payment) = (
            extract_element_by_tag(order_info, tag) for tag in [
                'order_detail_gray_id', 'order_detail_gray_date', 'order_detail_gray_payment'
            ]
        )
    
    def show_all_price_components(self, order_price_block):
        scroll_to(self.driver, order_price_block)
        return self

    def toggle_price(self, order_price_block):
        toggle_price_details_button = order_price_block.find_element(By.CLASS_NAME, 'comet-icon-arrowdown')
        toggle_price_details_button.click()
        wait_for(self.driver, lambda d: d.find_element(By.CLASS_NAME, "comet-icon-arrowup"))
        return self

    def parse_prices(self):
        def form_price_item(order_price_item):
            children = form_tag_value_items(
                order_price_item.find_elements(By.XPATH, './/*'),
                lambda el: el.get_attribute("data-pl"),
                lambda el: el.text.strip()
            )
            return {
                "title": extract_element_by_tag(children, 'order_price_item_title'),
                "value": extract_element_by_tag(children, 'order_price_item_value')
            }

        print('Parse prices:')
        return list(
            form_price_item(order_price_item) for order_price_item in self.driver.find_element(
                By.CLASS_NAME, 'order-price'
            ).find_elements(By.CLASS_NAME, 'order-price-item')
        )

    def parse_order_price(self):
        order_price_block = self.driver.find_element(By.CLASS_NAME, 'order-price')
        return self.show_all_price_components(order_price_block).toggle_price(order_price_block).parse_prices()

    def parse_store(self):
        store_item = self.driver.find_element(By.CLASS_NAME, 'store-name')
        return (
            store_item.text.strip(),
            store_item.find_element(By.XPATH, '..').get_attribute('href')
        )
    
    def parse_items(self):
        return list(
            OrderItemDetailsParser(self.driver, element) for element in self.driver.find_elements(
                By.CLASS_NAME, 'order-detail-item-content-wrap'
            )
        )
