from selenium.webdriver.common.by import By
from base_utils import find, replace_mass
from webpage_utils import scroll_to

def extract_element_by_tag(items, tag):
    item = find(lambda item: item['tag'] == tag if tag is not None else item['tag'] is None, items)
    return item['value'] if item is not None else None

def get_text_excluding_children(element):
    child_texts = (c.text for c in element.find_elements(By.XPATH, ".//*"))
    return replace_mass(element.text, child_texts, '').strip()

def form_tag_value_items(items, tag_func, el_func = lambda el: get_text_excluding_children(el)):
    return list({"value": el_func(el), "tag": tag_func(el)} for el in items)

class ParsedOrderDetails:
    def __init__(self, driver):
        self.driver = driver
        self.parseStatus()
        self.parseContactInfo()
        self.parseOrderPrice()

    def to_string(self):
        return f'''
        status = {self.status}
        contact_name = {self.contact_name}
        contact_phone = {self.contact_phone}
        delivery_address = {self.delivery_address}
        order_detail_id = {self.order_detail_id}
        order_detail_date = {self.order_detail_date}
        order_detail_payment = {self.order_detail_payment}
        '''
    
    def parseStatus(self):
        self.status = self.driver.find_element(By.CLASS_NAME, "order-block-title").text

    def parseContactInfo(self):
        [contact_info, order_info] = self.driver.find_element(By.CLASS_NAME, "order-detail-info").find_elements(By.CLASS_NAME, "order-detail-info-content")       
        self.parseCustomerInfo(form_tag_value_items(contact_info.find_elements(By.TAG_NAME, 'div'), lambda el: el.get_attribute("data-pl")))
        self.parseOrderInfo(form_tag_value_items(order_info.find_elements(By.CLASS_NAME, 'info-row'), lambda el: el.find_element(By.TAG_NAME, 'span').get_attribute("data-pl")))
    
    def parseCustomerInfo(self, contact_info):
        (self.contact_name, self.contact_phone, self.delivery_address) = (extract_element_by_tag(contact_info, tag) for tag in ['contact_info', None, 'contact_info_address'])

    def parseOrderInfo(self, order_info):
        (self.order_detail_id, self.order_detail_date, self.order_detail_payment) = (extract_element_by_tag(order_info, tag) for tag in ['order_detail_gray_id', 'order_detail_gray_date', 'order_detail_gray_payment'])
    
    def show_all_price_components(self, order_price_block):
        scroll_to(order_price_block)
        

    def parseOrderPrice(self):
        order_price_block = self.driver.find_elements(By.CLASS_NAME, 'order-price')
        self.show_all_price_components(order_price_block)
        


