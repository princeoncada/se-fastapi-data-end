def guide(ticker):
    objects = {
        "income_statement": {
            "url": f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}",
            "headers": [
                "Breakdown", "> Total Revenue", "Operating Revenue",
                "Cost of Revenue", "> Operating Expense", "Other Operating Expenses",
                "Research & Development", "Operating Income",
                "> Net Income Common Stockholders", "Net Income", "Total Expenses",
                "Interest Income", "Interest Expense", "Net Interest Income",
                "EBIT", "EBITDA"
            ]
        },
        "balance_sheet": {
            "url": f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}",
            "headers": [
                "Breakdown", "> Total Assets", "> Current Assets",
                "> Cash, Cash Equivalents & Short Term Investments",
                "Cash And Cash Equivalents", "Other Short Term Investments",
                "> Receivables", "Accounts receivable", "Other Receivables",
                "> Total Liabilities Net Minority Interest", "> Current Liabilities",
                "> Payables And Accrued Expenses", "> Payables", "Accounts Payable",
                "Dividends Payable", "Other Payable",
                "> Total Equity Gross Minority Interest", "> Stockholders' Equity",
                "Total Capitalization",
            ]
        },
        "cash_flow": {
            "url": f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}",
            "headers": [
                "Breakdown", "> Operating Cash Flow", "> Investing Cash Flow",
                "> Financing Cash Flow", "Free Cash Flow"
            ]
        },
        "statistics": {
            "url": f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}",
            "headers": [
                "Trailing P/E", "Price/Sales", "Price/Book", "Enterprise Value/EBITDA",
                "Return on Equity", "Quarterly Revenue Growth", "Quarterly Earnings Growth",
                "Total Debt/Equity", "Forward Annual Dividend Yield", "Trailing Annual Dividend Yield",
                "Payout Ratio"
            ]
        },
        "details": {
            "url": f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}",
            "headers": {
                "Price": f'//fin-streamer[@data-field="regularMarketPrice" and @data-symbol="{ticker}"]',
                "Name": f'//div[@data-test="asset-profile"]/div/h3',
                "Address": f'//div[@data-test="asset-profile"]/div/h3/following-sibling::div/p[1]',
                "Sector": f'//div[@data-test="asset-profile"]/div/h3/following-sibling::div/p[2]',
                "Description": f'//span[contains(text(), "Description")]/../following-sibling::p'
            }
        }
    }
    return objects
