from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def details(url, headers, options):
    with Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        driver.get(url)
        try:
            inner_dictionary = {
                "Price": None,
                "Ticker": None,
                "Name": None,
                "Address": None,
                "Sector(s)": None,
                "Industry": None,
                "Full Time Employees": None,
                "Description": None
            }

            for key, value in headers.items():
                try:
                    if key == "Address":
                        address_data = driver.find_element("xpath", value).text.split("\n")
                        index_two = address_data[1].split(" ")
                        inner_dictionary["Address"] = {
                            "Street": address_data[0],
                            "City": index_two[0][:-1],
                            "State": index_two[1],
                            "Zip": index_two[2],
                            "Country": address_data[2],
                            "Phone": address_data[3],
                            "Website": address_data[4]
                        }
                    elif key == "Sector":
                        sector_data = driver.find_element("xpath", value).text.split("\n")
                        for data in sector_data:
                            split_data = data.split(": ")
                            inner_dictionary[split_data[0]] = split_data[1]
                    else:
                        inner_dictionary[key] = driver.find_element("xpath", value).text
                except Exception as e:
                    print(f"{key} caused and error! Error: {e}")
        except TimeoutException:
            return None
        return inner_dictionary
