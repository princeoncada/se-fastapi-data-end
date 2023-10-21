import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def statistics(url, headers, options):
    service = Service(ChromeDriverManager().install())
    with Chrome(service=service, options=options) as driver:
        driver.get(url)
        try:
            inner_dictionary = {}
            for header in headers:
                xpath = f'//td/span[contains(text(), "{header}")]/../following-sibling::td'
                data = driver.find_element("xpath", xpath)
                inner_dictionary[header] = data.text
            return inner_dictionary
        except TimeoutException:
            return None

