import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Remote


def statistics(url, headers, options):
    with Remote(command_executor=os.environ["GRID_URL"], options=options) as driver:
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

