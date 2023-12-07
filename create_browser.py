from selenium import webdriver
from selenium_stealth import stealth

def init_stealth(driver):
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start_maximized")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.headless = True
    driver = webdriver.Chrome(options=options)
    init_stealth(driver)
    return driver

