

# Configures a chrome WebDriver
def makeWebDriver(timeout=10):
    # Setup driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(timeout)
    return driver


# Makes selenium use the bt website to get download and upload bandwidth speed.
def bt_speedtest(wd):
    # Speed test starts automatically, takes at least 10 seconds
    minimum_wait_time = 15
    wd.get('https://speedtest.btwholesale.com/details')
    sleep(minimum_wait_time)

    # Speed test returns values of ping, download speed and upload speed in classes named 'fontvalue'.
    # By default, these contain '--'.
    ping = download = upload = blank = '--'
    while ping == blank or download == blank or upload == blank:
        try:
            ping, download, upload = [element.text for element in wd.find_elements(By.CLASS_NAME, 'fontvalue')]

        except:
            picture_name = f"{datetime.now().strftime(TIME_FORMAT).replace('-', '_').replace(':', '_')}.png"
            picture_directory = Path(getPath()).joinpath(Path("errors"))

            try:  # Ensure directory exists
                os.mkdir(picture_directory)
            except FileExistsError:
                pass

            wd.save_screenshot(os.path.join(picture_directory, picture_name))
            raise

    return Results(download, upload)
