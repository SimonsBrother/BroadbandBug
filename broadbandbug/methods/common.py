import broadbandbug.library.constants as consts
import broadbandbug.methods.speedtestcli as speedtestcli

import speedtest


# Webdriver imports
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def determineMethodFunction(method_name):
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
        # Assign method function
        function = speedtestcli.performSpeedTest

        # Generate new speedtest object, and store it in tuple to be passed as parameters
        speedtest_obj = speedtest.Speedtest()
        speedtest_obj.get_best_server()
        params = (speedtest_obj,)

        return function, params

    # todo support which

    else:
        raise NameError("Invalid method name")


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
