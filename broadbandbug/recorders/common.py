""" Stores general functions to assist with recorders. """
from selenium import webdriver

"""from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


# Configures a Chrome WebDriver
def make_edge_web_driver(timeout=10):
    # Setup driver
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.implicitly_wait(timeout)
    return driver"""


# Converts from bits/s to megabits/s.
def convert_to_mbs(bps):
    return float(bps) / 1_000_000


"""# Which? Website
elif method_name == consts.METHOD_WHICHWEBSITE:
    if preferred_driver == consts.CHROME:
        driver = makeChromeWebDriver()
    else:
        # todo test edge
        driver = makeEdgeWebDriver()
    which_website.setupWebsite(driver)

    function = which_website.performSpeedTest
    params = (driver,)

    return function, params"""