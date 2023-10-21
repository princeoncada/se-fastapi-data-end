from selenium.common import TimeoutException
from selenium.webdriver import Chrome


def statistics(url, headers, options):
    with Chrome(options=options) as driver:
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

