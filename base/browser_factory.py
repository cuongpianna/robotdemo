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
from pyvirtualdisplay import Display


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
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-setuid-sandbox')
        # chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument("--headless")
        # chrome_options.binary_location = "C:\\path\\to\\chrome.exe"
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-dev-shm-using')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--disable-extensions-file-access-check")
        chrome_options.add_argument('--disable-extensions-http-throttling')
        chrome_options.add_argument(
            '--disable-extensions --disable-extensions-file-access-check --disable-extensions-http-throttling')
        cwd = os.getcwd()
        # display = Display(visible=0, size=(800, 600))
        # display.start()
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            firefox_path = os.path.join(cwd, 'base', 'geckodriver')
            driver = webdriver.Firefox(executable_path=firefox_path)
        elif self.browser == "chrome":
            # Set chrome driver
            chrome_options.binary_location = "/usr/bin/google-chrome-stable"
            chrome_path = os.path.join(cwd, 'base', 'chromedriver')
            chrome_path = '/usr/local/bin/chromedriver'
            driver = webdriver.Chrome(chrome_path, options=chrome_options)
        else:
            driver = webdriver.Firefox()

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(3)
        # Maximize the window
        # Loading browser with App URL
        return driver
