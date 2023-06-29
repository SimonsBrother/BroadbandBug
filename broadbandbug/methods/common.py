import broadbandbug.library.constants as consts
import broadbandbug.methods.speedtestcli as speedtestcli
import broadbandbug.methods.which_website as which_website

import speedtest


# Webdriver imports
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Configures a Chrome WebDriver
def makeChromeWebDriver(timeout=10):
    # Setup driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(timeout)
    return driver


# Configures a Chrome WebDriver
def makeEdgeWebDriver(timeout=10):
    # Setup driver
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.implicitly_wait(timeout)
    return driver


def determineMethodFunction(method_name, preferred_driver):
    # Get function related to method
    if method_name == consts.METHOD_SPEEDTESTCLI:  # speedtest cli method
        # Assign method function
        function = speedtestcli.performSpeedTest

        # Generate new speedtest object, and store it in tuple to be passed as parameters
        speedtest_obj = speedtest.Speedtest()
        speedtest_obj.get_best_server()
        params = (speedtest_obj,)

        return function, params

    elif method_name == consts.METHOD_BTWEBSITE:  # bt website method
        raise NotImplementedError

    elif method_name == consts.METHOD_WHICHWEBSITE:  # which website method
        if preferred_driver == consts.CHROME:
            driver = makeChromeWebDriver()
        else:
            driver = makeEdgeWebDriver()
        which_website.setupWebsite(driver)

        function = which_website.performSpeedTest
        params = (driver,)

        return function, params

    else:
        raise NameError("Invalid method name")
