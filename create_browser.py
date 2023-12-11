from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchDriverException
import time


class ChromeDriver:
    def __enter__(self):
        print('Start creating browser:')
        self.driver = self.create_driver()
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        time.sleep(200)
        self.driver.quit()
        print('Finish parsing')

    @staticmethod
    def form_chrome_options():
        options = webdriver.ChromeOptions()
        options.add_argument("start_maximized")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        for agrument in [
            # '--no-sandbox',
            # '--disable-gpu',
            # '--headless',
            # '--disable-dev-shm-usage',
            # '--allow-running-insecure-content',
            # '--ignore-certificate-errors',
            # '--ignore-ssl-errors=yes',
            # '--disable-proxy-certificate-handler',
            # '--remote-debugging-port=8000'
        ]:
            options.add_argument(agrument)
        options.headless = True
        return options

    @staticmethod
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
    
    def create_driver(self):
        try:
            driver = webdriver.Chrome(
                options=self.form_chrome_options(),
                seleniumwire_options={}
            )
        except NoSuchDriverException:
            print("Can't open chrome. ChromeDriverManager is using")
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.form_chrome_options(),
                seleniumwire_options={}
            )
        self.init_stealth(driver)
        print('Browser created')
        return driver
