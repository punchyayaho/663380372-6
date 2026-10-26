from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class DriverManager:
    def __init__(self, browser_type: str = "chrome", headless: bool = True):
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.driver = None

    def get_driver(self):
        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            try:
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                # Fallback: Selenium 4.6+ has a built-in Selenium Manager that finds the driver itself
                print(f"webdriver-manager failed ({e}). Falling back to Selenium Manager...")
                self.driver = webdriver.Chrome(options=options)

        elif self.browser_type == "firefox":
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")

            try:
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                print(f"webdriver-manager failed ({e}). Falling back to Selenium Manager...")
                self.driver = webdriver.Firefox(options=options)

        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

        self.driver.implicitly_wait(10)
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()
