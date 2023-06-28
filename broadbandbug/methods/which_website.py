from datetime import datetime

from broadbandbug.library.classes import Result
from broadbandbug.library.constants import TIME_FORMAT, METHOD_WHICHWEBSITE

from selenium.webdriver.common.by import By


def performSpeedTest(driver):  # todo test
    """ Uses a webdriver to open a window, open the Which? broadband speedtest website, and gets a result """
    driver.get("https://broadbandtest.which.co.uk")

    # Accept cookies
    accept_cookies_btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_cookies_btn.click()

    # Get start button, and click it
    start_btn = driver.find_element(By.NAME, "start")
    start_btn.click()

    # Wait for website to complete speedtest
    find_btn = driver.find_element(By.NAME, "find")
    while not find_btn.is_displayed():
        pass

    # Get the results from the speedtest
    values = driver.find_elements(By.NAME, "value")
    timestamp = datetime.now().strftime(TIME_FORMAT)

    # Delete cookies, so the cookie agreement button reappears (could be optimised)
    wd.delete_all_cookies()

    return Result(values[1].text, values[2].text, timestamp, METHOD_WHICHWEBSITE)


if __name__ == "__main__":
    from broadbandbug.methods.common import makeChromeWebDriver

    wd = makeChromeWebDriver()
    while True:
        print(performSpeedTest(wd))
