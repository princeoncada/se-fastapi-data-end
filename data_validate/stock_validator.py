import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Remote


def validate(url):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    with Remote(command_executor=os.environ["GRID_URL"], options=options) as driver:
        driver.get(url)
        try:
            statistics = len(driver.find_elements("xpath", "//span[contains(text(), 'Statistics')]")) == 1
            financials = len(driver.find_elements("xpath", "//span[contains(text(), 'Financials')]")) == 1
            profile = len(driver.find_elements("xpath", "//span[contains(text(), 'Profile')]")) == 1

            return all([statistics, financials, profile])
        except TimeoutException:
            return None