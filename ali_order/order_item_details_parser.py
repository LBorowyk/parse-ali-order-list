from selenium.webdriver.common.by import By
from tools.base_parse_page import ParsePage
from tools.base_utils import to_float, to_int, extract_url_from_style


class OrderItemDetailsParser(ParsePage):
    def __init__(self, driver, element):
        super().__init__(driver)
        self.element = element
        self.title = self.parse_title()
        self.properties = self.parse_properties()
        (self.price, self.count) = self.parse_price_and_count()
        (self.image_url, self.item_url) = self.parse_item_image()
        self.tags = self.parse_tags()
        self.item_tracking_info = self.parse_item_tracking_info()
        print('Parse details')
        
    def to_string(self):
        return f'''
            title = {self.title}
            properties = {self.properties}
            item_tracking_info = {self.item_tracking_info}
            price = {self.price}
            count = {self.count}
            tags = {self.tags}
            item_tracking_info = {self.item_tracking_info}
            image_url = {self.image_url}
            item_url = {self.item_url}
        '''
    
    def parse_title(self):
        return self.element.find_element(
            By.CLASS_NAME, 'item-title'
        ).find_element(By.TAG_NAME, 'a').text.strip()
    
    def parse_properties(self):
        attr = self.try_find(lambda: self.element.find_element(By.CLASS_NAME, 'item-sku-attr'))
        return list(s.strip() for s in attr.text.split(',')) if attr else list()
    
    def parse_price_and_count(self):
        block = self.try_find(lambda: self.element.find_element(By.CLASS_NAME, 'item-price'))
        price_block = self.try_find(lambda: block.find_element(By.TAG_NAME, 'div'))
        count_block = self.try_find(lambda: block.find_element(By.CLASS_NAME, 'item-price-quantity'))
        return (
            to_float(price_block.text) if price_block else 0,
            to_int(count_block.text) if count_block else 0
        )
    
    def parse_tags(self):
        def parse_tag(tag_element):
            return tag_element.text.strip() if tag_element else None
        tags = self.try_find(lambda: self.element.find_element(By.CLASS_NAME, 'item-tags'))
        return list(
            parse_tag(tag_element) for tag_element in tags.find_elements(By.CLASS_NAME, 'order-item-tag')
        ) if tags else list()
        
    def parse_item_tracking_info(self):
        def read_tracking_info(track_block):
            track_info = track_block.find_element(By.CLASS_NAME, 'order-detail-item-track-eta-text').text
            (label, value) = list(s.strip() for s in track_info.split(':'))
            last_status_block = self.try_find(
                lambda: track_block.find_element(By.CLASS_NAME, 'order-detail-item-track-info-desc')
            )
            return {
                "label": label,
                "value": value,
                "last_track_status": (last_status_block.text if last_status_block else None)
            }
        tracking_block = self.try_find(lambda: self.element.find_element(By.CLASS_NAME, 'order-detail-item-track'))
        return read_tracking_info(tracking_block) if tracking_block else {}

    def parse_item_image(self):
        img_block = self.try_find(lambda: self.element.find_element(By.CLASS_NAME, 'order-detail-item-content-img'))
        return (
            extract_url_from_style(img_block.get_attribute('style')),
            img_block.get_attribute('href')
        ) if img_block else (None, None)
        