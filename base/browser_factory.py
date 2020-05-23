"""
@package base
WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations
Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverFactory:

    def __init__(self, browser):
        """
        Inits WebDriverFactory class
        Returns:
            None
        """
        self.browser = browser

    """
        Set chrome driver and iexplorer environment based on OS
        chromedriver = "C:/.../chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)
        PREFERRED: Set the path on the machine where browser will be executed
    """

    def get_web_driver_instance(self):
        """
       Get WebDriver Instance based on the browser configuration
        Returns:
            'WebDriver Instance'
        """

        chrome_options = Options()
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--disable-extensions-file-access-check")
        chrome_options.add_argument('--disable-extensions-http-throttling')
        chrome_options.add_argument(
            '--disable-extensions --disable-extensions-file-access-check --disable-extensions-http-throttling')
        cwd = os.getcwd()
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            firefox_path = os.path.join(cwd, 'base', 'geckodriver.exe')
            driver = webdriver.Firefox(executable_path=firefox_path)
        elif self.browser == "chrome":
            # Set chrome driver
            chrome_path = os.path.join(cwd, 'base', 'chromedriver')
            driver = webdriver.Chrome(chrome_path, options=chrome_options)
        else:
            driver = webdriver.Firefox()

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(3)
        # Maximize the window
        # Loading browser with App URL
        return driver
