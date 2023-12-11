from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


def wait_for(driver, func, timeout=30):
    WebDriverWait(driver, timeout=timeout).until(func)


def scroll_to(driver, element):
    ActionChains(driver).move_to_element(element).perform()
