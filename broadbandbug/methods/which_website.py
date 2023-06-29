from datetime import datetime

from broadbandbug.library.classes import Result
from broadbandbug.library.constants import TIME_FORMAT, METHOD_WHICHWEBSITE

from selenium.webdriver.common.by import By


def setupWebsite(driver):
    """ Sets up the website for performSpeedTest by accepting cookies """
    driver.get("https://broadbandtest.which.co.uk")

    # Accept cookies
    accept_cookies_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    while not accept_cookies_btn.is_displayed():
        pass
    accept_cookies_btn.click()


def performSpeedTest(driver):  # todo test
    """ Uses a webdriver with a setup window for the Which? broadband speedtest website to get a result """
    driver.get("https://broadbandtest.which.co.uk")

    # Find start button
    start_btn = driver.find_element(By.NAME, "start")

    # Find the "Find a better broadband deal" button
    find_btn = driver.find_element(By.NAME, "find")

    # Wait for start button to appear and click it
    while not start_btn.is_displayed():
        pass
    start_btn.click()

    # Wait for website to complete speedtest, by waiting for the "Find a better broadband deal" button to appear
    while not find_btn.is_displayed():
        pass

    # Get the results from the speedtest
    values = driver.find_elements(By.NAME, "value")
    timestamp = datetime.now().strftime(TIME_FORMAT)

    return Result(values[1].text, values[2].text, timestamp, METHOD_WHICHWEBSITE)


if __name__ == "__main__":
    from broadbandbug.methods.common import makeChromeWebDriver

    wd = makeChromeWebDriver()
    setupWebsite(wd)
    while True:
        print(performSpeedTest(wd))
