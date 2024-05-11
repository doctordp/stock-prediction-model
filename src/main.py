import logging
from fastapi import FastAPI
from transformers import pipeline

import yfinance as yf
import asyncio
import pandas as pd
from datetime import datetime
import requests
from pytrends.request import TrendReq
from GoogleNews import GoogleNews
import json
import csv

import requests
from datetime import datetime




logger = logging.getLogger(__name__)

app = FastAPI(title='Yahoo Finance')
symbols = ["MSFT", "AAPL", "NVDA", "AMZN", "META", "AVGO", "TSLA", "COST", "GOOGL",
           "GOOG", "AMD", "NFLX", "ADBE", "PEP", "CSCO", "TMUS", "INTU", "INTC", "QCOM",
           "CMCSA", "AMAT", "AMGN", "TXN", "ISRG", "HON", "BKNG", "LRCX", "VRTX", "REGN",
           "SBUX", "ADP", "PANW", "MDLZ", "MU", "ADI", "KLAC", "GILD", "SNPS", "PDD",
           "ASML", "CDNS", "MELI", "CSX", "MAR", "CRWD", "ABNB", "PYPL", "ORLY", "CTAS",
           "NXPI", "WDAY", "MRVL", "PCAR", "MNST", "ROP", "LULU", "ADSK", "CEG", "FTNT",
           "CPRT", "ROST", "IDXX", "ODFL", "DASH", "MCHP", "PAYX", "DXCM", "AEP", "KHC",
           "CHTR", "GEHC", "FAST", "KDP", "DDOG", "CTSH", "AZN", "TTD", "EA", "MRNA", "EXC",
           "CSGP", "ZS", "VRSK", "ON", "CDW", "FANG", "BIIB", "TEAM", "DLTR", "XEL", "CCEP",
           "MDB", "BKR", "ANSS", "GFS", "SPLK", "TTWO", "ILMN", "WBD", "WBA", "SIRI"]

@app.on_event('startup')
async def get_data():
  pipeline = init_sentiment_processor()
  await get_news([symbols[0]], pipeline)


async def get_stock_data(symbols: list[str]):
  for symbol in symbols:
    yahoo_result = await get_symbol_stock_data(symbol)
    yahoo_result.reset_index(inplace = True)
    logger.info(yahoo_result.columns.values)
    yahoo_result['Date'] = yahoo_result['Date'].dt.strftime('%d-%m-%Y')
    logger.info(yahoo_result.values)
    yahoo_result.to_csv(f'/home/user/data/stocks/{symbol}.csv', sep=',', index=False, encoding='utf-8')

async def get_symbol_stock_data(symbol: str):
  msft = yf.Ticker(symbol)
  result = msft.history(period="max")
  return result

async def get_trends(symbols: list[str]):
  for symbol in symbols:
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([symbol], cat=0, timeframe=['2008-01-01 2024-03-01'], geo='', gprop='')
    trends = pytrends.interest_over_time()
    pd.DataFrame(trends).to_csv(f'/home/user/data/trends/{symbol}.csv', sep=',', encoding='utf-8')

async def get_news(symbols: list[str], pipeline):
  dates = {'start': '01/01/2024'}

  for symbol in symbols:
    news_results = []

    with open(f'/home/user/data/stocks/{symbols[0]}.csv', 'r') as file:
      csv_reader = csv.reader(file)
      csv_reader = list(csv_reader)
      dates['end'] = csv_reader[-1][0]

    request_year = int(dates['start'].split('/')[2])
    end_year = int(dates['end'].split('-')[2])

    news_results = []

    while int(request_year) <= end_year:
      news_results.extend(await get_news_from_symbol(symbols[0], int(request_year)))
      request_year = request_year + 1

    for new in news_results:
      if 'datetime' in new:
        del new['datetime']
      
        sentiment_result = pipeline(new['title'])[0]
        new['sentiment'] = sentiment_result['label']




    with open(f'/home/user/data/sentiment/{symbol}-2.json', 'w') as news_file:
      json.dump(news_results, news_file)
  
  return

  # Parse the date string
  date_object = datetime.strptime(google_results[0]['date'], "%b %d, %Y")

  # Format the date object as "DD/MM/YYYY"
  formatted_date = date_object.strftime("%d/%m/%Y")

  google_results[0]['date'] = formatted_date

  with open("data.json", "w") as json_file:
    json_file.write(json.dumps(google_results))



async def get_news_from_symbol(symbol: str, start_year: int) -> list:
  print(f'llego {start_year}')
  google_news = GoogleNews(lang='en', start=f'01/01/{start_year}',end=f'12/31/{start_year}')
  google_news.get_news(symbol)
  google_results = google_news.results(sort=True)

  return google_results

def init_sentiment_processor():
  __PIPELINE_NAME = 'sentiment-analysis'
  __PIPELINE_MODEL = 'sangrimlee/bert-base-multilingual-cased-nsmc'
  __MAX_TENSOR_SIZE = 51

  return pipeline(__PIPELINE_NAME, model=__PIPELINE_MODEL,
                                   tokenizer=__PIPELINE_MODEL,
                                   max_length=__MAX_TENSOR_SIZE, truncation=True)