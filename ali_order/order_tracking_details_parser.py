from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from tools.base_parse_page import ParsePage
from tools.webpage_utils import wait_for


class ParseTrackingInfo(ParsePage):
    def __init__(self, driver, order_detail_id):
        super().__init__(driver)
        self.order_detail_id = order_detail_id
        self.parse_tracking_details()
        print('Tracking parsing complete.')

    @staticmethod
    def form_snapshot_url(order_id):
        return "https://www.aliexpress.com/snapshot/0.html?orderId=" + order_id

    @staticmethod
    def form_track_ali_url(order_id):
        return "https://track.aliexpress.com/logisticsdetail.htm?tradeId=" + order_id
    
    def load_tracking_page(self):
        self.driver.get(self.form_track_ali_url(self.order_detail_id))
        try:
            wait_for(self.driver, lambda d: d.find_element(By.CLASS_NAME, 'main-wrapper'))
            return True
        except TimeoutException:
            print("Can`t load traching page for ", self.order_detail_id)
            return False


    @staticmethod
    def parse_tracking_info(tracking_block, tracking_code_class='tracking-no'):
        def get_text(find_element_func):
            element = ParsePage.try_find(find_element_func)
            return element.text.strip() if element else None
        tracking_name_block = ParsePage.try_find(lambda: tracking_block.find_element(By.CLASS_NAME, 'tracking-name'))
        return {
            "tracking_name": get_text(lambda: tracking_name_block.find_element(By.CLASS_NAME, 'title')),
            "tracking_tag": get_text(lambda: tracking_name_block.find_element(By.CLASS_NAME, 'tag')),
            "tracking_code": get_text(lambda: tracking_block.find_element(
                By.CLASS_NAME, tracking_code_class
            ).find_element(By.TAG_NAME, 'span'))
        } if tracking_name_block else {}

    def parse_tracking_details(self):
        if not self.load_tracking_page():
            return
        tracking_block = self.try_find(lambda: self.driver.find_element(By.CLASS_NAME, 'tracking-detail'))
        if tracking_block:
            track_info = self.parse_tracking_info(tracking_block)
            (self.tracking_name, self.tracking_tag, self.tracking_code) = (track_info[tag] for tag in [
                'tracking_name', 'tracking_tag', 'tracking_code'
            ])
            self.other_track_codes = list(
                self.parse_tracking_info(other_tracking_block_n, 'tracking-no-de')
                for other_tracking_block_n in self.driver.find_elements(By.CLASS_NAME, 'tracking-detail-n')
            )
        else:
            print("Order " + self.order_detail_id + " has no tracking information")
            (self.tracking_name, self.tracking_tag, self.tracking_code, self.other_track_codes) = (None, None, None, [])
            