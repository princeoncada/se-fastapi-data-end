import json
from time import perf_counter
import pandas as pd
from data_processing.stock_formulas import (calculate_ratios, convert_percentage_to_decimal,
                                            convert_to_float, stock_score)
from data_retrieval.stock_scraper import scrape


def parser(stock_data, ticker):
    stock_data["details"]["Ticker"] = ticker

    # Convert the data into Pandas DataFrames
    income_statement_df = pd.DataFrame(stock_data["financials"]["income_statement"])
    balance_sheet_df = pd.DataFrame(stock_data["financials"]["balance_sheet"])
    cash_flow_df = pd.DataFrame(stock_data["financials"]["cash_flow"])
    statistics_dict = stock_data["statistics"]

    # Convert numeric columns to float (excluding "Breakdown" columns)
    cols_to_convert = income_statement_df.columns.difference(["Breakdown"])
    income_statement_df[cols_to_convert] = income_statement_df[cols_to_convert].map(convert_to_float)
    cols_to_convert = balance_sheet_df.columns.difference(["Breakdown"])
    balance_sheet_df[cols_to_convert] = balance_sheet_df[cols_to_convert].map(convert_to_float)
    cols_to_convert = cash_flow_df.columns.difference(["Breakdown"])
    cash_flow_df[cols_to_convert] = cash_flow_df[cols_to_convert].map(convert_to_float)

    # Calculate Ratios
    statistics_dict = calculate_ratios(income_statement_df, cash_flow_df, statistics_dict)

    # Convert percentages to decimals
    for key in statistics_dict:
        statistics_dict[key] = convert_percentage_to_decimal(statistics_dict[key])

    # Convert all other values to floats
    for key in statistics_dict:
        statistics_dict[key] = convert_to_float(statistics_dict[key])

    score_data = stock_score(statistics_dict)

    statistics_dict["Quarterly Revenue Growth"] = (statistics_dict["Quarterly Revenue Growth"] / 4) / 0.05
    statistics_dict["Quarterly Earnings Growth"] = (statistics_dict["Quarterly Earnings Growth"] / 4) / 0.05

    # Create a dictionary with lists instead of DataFrames
    combined_data = {
        "details": stock_data["details"],
        "score": score_data,
        "financials": {
            "income_statement": income_statement_df.to_dict(orient='list'),
            "balance_sheet": balance_sheet_df.to_dict(orient='list'),
            "cash_flow": cash_flow_df.to_dict(orient='list'),
        },
        "statistics": statistics_dict
    }

    return combined_data


if __name__ == "__main__":
    start = perf_counter()
    print(json.dumps(parser(scrape("PLTR"), "PLTR"), indent=4))
    end = perf_counter()
    print(f"Time elapsed: {end - start}")
