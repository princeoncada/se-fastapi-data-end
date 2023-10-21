from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def financials(url, headers, options):
    with Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        driver.get(url)
        try:
            inner_dictionary = {}
            for header in headers:
                if header[0] == ">":
                    header = header[2:]
                    try:
                        btn = driver.find_element("xpath", f'//button[@aria-label="{header}"]')
                        print("clicked button for " + header)
                        btn.click()
                    except NoSuchElementException:
                        print(f"No button for {header}!")
                try:
                    span = driver.find_element("xpath", f'//span[contains(text(), "{header}")]')
                    grand_parent_div = span.find_element("xpath", "../..")
                    if header == "Breakdown":
                        grand_parent_div = span.find_element("xpath", "..")
                    siblings = grand_parent_div.find_elements("xpath", "./following-sibling::div")
                    inner_dictionary[header] = [sibling.text for sibling in siblings]
                except NoSuchElementException:
                    print(f"No {header} element!")
            return inner_dictionary
        except TimeoutException:
            return None
