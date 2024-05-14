from operator import itemgetter
from pytrends.request import TrendReq
import pandas as pd
import time
import random
import logging
import sys

logger = logging.getLogger(__name__)

class TrendsCollector:
  __START_YEAR = 2008
  __END_YEAR = 2024
  __TRENDS_DIRECTORY = '/home/user/data/trends'

  async def get_trends(self, symbol: str,):
    request_year = self.__START_YEAR
    total_trends = pd.DataFrame()

    while request_year <= self.__END_YEAR:
      year_trends = await self.get_trends_by_semester(symbol, request_year)
      total_trends = pd.concat([total_trends, pd.DataFrame(year_trends)])
      request_year += 1
    
    
    total_trends.to_csv(f'{self.__TRENDS_DIRECTORY}/{symbol}.csv', sep=',', encoding='utf-8')

  async def get_trends_by_year(self, symbol, request_year):
    start_date=f"{request_year}-01-01"
    end_date=f"{request_year}-12-31" if request_year != 2024 else f"{request_year}-03-31"
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([symbol], cat=0, timeframe=[f'{start_date} {end_date}'], geo='', gprop='')
    trends = pytrends.interest_over_time()
    return trends

  async def get_trends_by_semester(self, symbol, request_year):
    year_trends =  pd.DataFrame()
    start_of_year = '01-01'
    first_mid_of_year = '06-30'
    second_mid_of_year = '07-01'
    end_of_year = '12-31'

    for iteration in range(2) if request_year != 2024 else range(1):
      start_date=f"{request_year}-{start_of_year if iteration == 0 else second_mid_of_year}"
      end_date=f"{request_year}-{first_mid_of_year if iteration == 0 else end_of_year}" if request_year != 2024 else f"{request_year}-03-31"
      request_success = False
      tries = 0

      while not request_success and tries <= 50:
        try:
          logger.error(f'Getting {symbol} from {start_date} to {end_date}')
          pd_trends = await self.get_trends_by_symbol_and_time(symbol, start_date, end_date)
          year_trends = pd.concat([ year_trends, pd_trends])
          logger.error(f'Getting {symbol} from {start_date} to {end_date}: SUCCESS')
          request_success = True
        except Exception as e:
          logger.error(f'Getting {symbol} from {start_date} to {end_date}: ERROR')
          logger.error(e)
          time.sleep(random.randint(1, 9))
          tries += 1

      if tries >= 50:
        sys.exit('Exiting program')

    return year_trends
  
  async def get_trends_by_symbol_and_time(self, symbol, start_date, end_date):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([symbol], cat=0, timeframe=[f'{start_date} {end_date}'], geo='', gprop='')
    trends = pytrends.interest_over_time()
    pd_trends = pd.DataFrame(trends)

    return pd_trends