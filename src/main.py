import logging
from fastapi import FastAPI


from models.news import SentimentAnalyzer
from models.trends import TrendsCollector
from models.news import NewsCollector
from models.stock import StockCollector
from models.unify import Unifier

from utils.news_to_csv import parse_news_to_csv

sentiment_analyzer = SentimentAnalyzer()
trends_collector = TrendsCollector()
news_collector = NewsCollector(sentiment_analyzer)
stock_collector = StockCollector()
unifier = Unifier()

logger = logging.getLogger(__name__)

app = FastAPI(title='Yahoo Finance')
symbols = [
           "MSFT", "AAPL", "NVDA", "AMZN", "META", "AVGO", "TSLA", "COST", "GOOGL",
           "GOOG", "AMD", "NFLX", "ADBE", "PEP", "CSCO", "TMUS", "INTU", "INTC", "QCOM",
           "CMCSA", "AMAT", "AMGN", "TXN", "ISRG", "HON", "BKNG", "LRCX", "VRTX", "REGN",
           "SBUX", "ADP", "PANW", "MDLZ", "MU", "ADI", "KLAC", "GILD", "SNPS", "PDD",
           "ASML", "CDNS", "MELI", "CSX", "MAR", "CRWD", "ABNB", "PYPL", "ORLY", "CTAS",
           "NXPI", "WDAY", "MRVL", "PCAR", "MNST", "ROP", "LULU", "ADSK", "CEG", "FTNT",
           "CPRT", "ROST", 
           "IDXX", "ODFL", "DASH", "MCHP", "PAYX", "DXCM", "AEP", "KHC",
           "CHTR", "GEHC", "FAST", "KDP", "DDOG", "CTSH", 
           "AZN", "TTD", "EA", "MRNA", "EXC",
           "CSGP", "ZS", "VRSK", "ON", "CDW", "FANG", "BIIB", 
           "TEAM", "DLTR", "XEL", "CCEP",
           "MDB", "BKR", "ANSS", "GFS", "SPLK", "TTWO", "ILMN", "WBD", "WBA", "SIRI"]

@app.on_event('startup')
async def get_data():
  print('guay')

async def get_trends(symbols: list[str]):
  for symbol in symbols:
    await trends_collector.get_trends(symbol)

async def get_news(symbols: list[str]):
  for symbol in [symbols[0]]:
    await news_collector.get_news(symbol)
