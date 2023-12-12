from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from tools.base_utils import find, replace_mass


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
        
    @staticmethod
    def try_find(find_func):
        try:
            return find_func()
        except NoSuchElementException:
            return None
