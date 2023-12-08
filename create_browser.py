from seleniumwire  import webdriver
from selenium_stealth import stealth
import time

class ChromeDriver:
    def __enter__(self):
        print('Start creating browser:')
        self.driver = self.create_driver()
        print('Browser created')
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        time.sleep(200)
        self.driver.quit()
        print('Finish parsing')

    def form_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start_maximized")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # options.add_argument("--remote-debugging-port=8000")
        options.headless = True
        return options

    def init_stealth(self, driver):
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
        )
    
    def create_driver(self):
        driver = webdriver.Chrome(options=self.form_chrome_options(), seleniumwire_options={})
        self.init_stealth(driver)
        return driver

