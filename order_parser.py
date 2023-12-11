from selenium.webdriver.common.by import By
from base_utils import find, replace_mass
from webpage_utils import scroll_to, wait_for
from selenium.common.exceptions import NoSuchElementException


def form_track_ali_url(order_id):
    return "https://track.aliexpress.com/logisticsdetail.htm?tradeId=" + order_id


def extract_element_by_tag(items, tag):
    element = find(lambda item: item['tag'] == tag if tag is not None else item['tag'] is None, items)
    return element['value'] if element is not None else None


def get_text_excluding_children(element):
    child_texts = (c.text for c in element.find_elements(By.XPATH, ".//*"))
    return replace_mass(element.text, child_texts, '').strip()


def form_tag_value_items(items, tag_func, el_func=lambda el: get_text_excluding_children(el)):
    return list({"value": el_func(el), "tag": tag_func(el)} for el in items)


class ParsePage:
    def __init__(self, driver):
        self.driver = driver


class ParseTrackInfo(ParsePage):
    def __init__(self, driver, order_detail_id):
        super().__init__(driver)
        self.order_detail_id = order_detail_id
        self.parse_tracking_details()
        print('Tracking parsing complete.')

    def load_tracking_page(self):
        self.driver.get(form_track_ali_url(self.order_detail_id))
        wait_for(self.driver, lambda d: d.find_element(By.CLASS_NAME, 'main-wrapper'))

    @staticmethod
    def parse_tracking_info(tracking_block, tracking_code_class='tracking-no'):
        tracking_name_block = tracking_block.find_element(By.CLASS_NAME, 'tracking-name')
        return {
            "tracking_name": tracking_name_block.find_element(By.CLASS_NAME, 'title').text.strip(),
            "tracking_tag": tracking_name_block.find_element(By.CLASS_NAME, 'tag').text.strip(),
            "tracking_code": tracking_block.find_element(
                By.CLASS_NAME, tracking_code_class
            ).find_element(By.TAG_NAME, 'span').text.strip()
        }

    def parse_tracking_details(self):
        self.load_tracking_page()
        try:
            tracking_block = self.driver.find_element(By.CLASS_NAME, 'tracking-detail')
            if tracking_block:
                track_info = self.parse_tracking_info(tracking_block)
                (self.tracking_name, self.tracking_tag, self.tracking_code) = (track_info[tag] for tag in [
                    'tracking_name', 'tracking_tag', 'tracking_code'
                ])
                self.other_track_codes = list(
                    self.parse_tracking_info(other_tracking_block_n, 'tracking-no-de')
                    for other_tracking_block_n in self.driver.find_elements(By.CLASS_NAME, 'tracking-detail-n')
                )
        except NoSuchElementException:
            print("Order " + self.order_detail_id + " has no tracking information")
            (self.tracking_name, self.tracking_tag, self.tracking_code, self.other_track_codes) = (None, None, None, [])


class ParsedOrderDetails(ParsePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.status = self.parse_status()
        self.parse_contact_info()
        self.price = self.parse_order_price()
        (self.store, self.store_href) = self.parse_store()
        print("Parse tracking info:")
        self.tracking = ParseTrackInfo(self.driver, self.order_detail_id)

    def to_string(self):
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
