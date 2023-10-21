import json
from time import perf_counter
from selenium.webdriver import ChromeOptions
from concurrent.futures import ThreadPoolExecutor, as_completed

from data_retrieval.stock_guide import guide
from data_retrieval.stock_financials import financials
from data_retrieval.stock_statistics import statistics
from data_retrieval.stock_details import details


def assign(url, key, headers):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    if key in ["income_statement", "balance_sheet", "cash_flow"]:
        return financials(url, headers, options)
    elif key == "statistics":
        return statistics(url, headers, options)
    elif key == "details":
        return details(url, headers, options)


def scrape(ticker):
    objects = guide(ticker)

    result_dict = {
        "details": {},
        "statistics": {},
        "financials": {},
    }

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(assign, value["url"], key, value["headers"])
                   for key, value in objects.items()]
        for future in as_completed(futures):
            if 'Price' in future.result():
                result_dict["details"] = future.result()
            if 'Trailing P/E' in future.result():
                result_dict["statistics"] = future.result()
            if 'Total Revenue' in future.result():
                result_dict["financials"]["income_statement"] = future.result()
            if 'Total Assets' in future.result():
                result_dict["financials"]["balance_sheet"] = future.result()
            if 'Operating Cash Flow' in future.result():
                result_dict["financials"]["cash_flow"] = future.result()

    return result_dict


if __name__ == "__main__":
    start = perf_counter()
    print(json.dumps(scrape("PLTR"), indent=4))
    end = perf_counter()
    print(f"Time elapsed: {end - start}")