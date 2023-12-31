import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data_retrieval.stock_scraper import scrape
from data_processing.stock_parser import parser
from data_validate.stock_validator import validate
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type", "Accept"]
)

running_tasks = {}


@app.get("/stock/{ticker}")
async def fetch_stock_data(ticker: str):
    if ticker in running_tasks:
        running_tasks[ticker].cancel()
        del running_tasks[ticker]

    try:
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, lambda: scrape(ticker))
        running_tasks[ticker] = task
        result = await task
    except asyncio.CancelledError:
        raise HTTPException(status_code=400, detail="Request canceled due to a new request with the same ticker.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if ticker in running_tasks:
            del running_tasks[ticker]

    return parser(result, ticker)


@app.get("/validate/{ticker}")
def validate_stock(ticker: str):
    return validate(f"https://finance.yahoo.com/quote/{ticker}")


@app.get("/health")
def health():
    string = "OK"
    try:
        return string
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, port=1000, host='localhost')
