from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def wait_for(driver, func):
    WebDriverWait(driver, timeout=30).until(func)

def scroll_to(driver, element):
    ActionChains(driver).move_to_element(element).perform()
