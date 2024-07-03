""" Stores general functions to assist with recorders. """
import broadbandbug.library.constants as consts
import broadbandbug.methods.speedtestcli as speedtestcli
import broadbandbug.methods.which_website as which_website

import speedtest
from selenium import webdriver

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Configures a Chrome WebDriver
def makeEdgeWebDriver(timeout=10):
    # Setup driver
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.implicitly_wait(timeout)
    return driver

# Converts from bits/s to megabits/s. TODO snake case
def convertToMbs(bps):
    return float(bps) / 1_000_000


def determineMethodFunction(method_name, preferred_driver):
    """ Returns function related to method and the arguments to pass to it; returns (None, Exception) if exception """

    try:
        # Speedtest CLI
        if method_name == consts.METHOD_SPEEDTESTCLI:
            # Assign method function
            function = speedtestcli.performSpeedTest

            # Generate new speedtest object, and store it in tuple to be passed as parameters
            speedtest_obj = speedtest.Speedtest()
            speedtest_obj.get_best_server()
            params = (speedtest_obj,)

            return function, params

        # BT Website
        elif method_name == consts.METHOD_BTWEBSITE:
            raise NotImplementedError

        # Which? Website
        elif method_name == consts.METHOD_WHICHWEBSITE:
            if preferred_driver == consts.CHROME:
                driver = makeChromeWebDriver()
            else:
                # todo test edge
                driver = makeEdgeWebDriver()
            which_website.setupWebsite(driver)

            function = which_website.performSpeedTest
            params = (driver,)

            return function, params

        # Invalid method given
        else:
            raise NameError("Invalid method name")

    except Exception as e:
        return None, e
