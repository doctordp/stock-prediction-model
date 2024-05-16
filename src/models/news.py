import json
import logging
from datetime import datetime
import time
import sys
import random
from GoogleNews import GoogleNews
from models.sentiment import SentimentAnalyzer

logger = logging.getLogger(__name__)

class NewsCollector:
  __START_YEAR = 2008
  __END_YEAR = 2024
  __NEWS_DIRECTORY = '/home/user/data'

  def __init__(self, sentiment_analyzer: SentimentAnalyzer) -> None:
    self.__SENTIMENT_ANALYZER = sentiment_analyzer

  async def get_news(self, symbol: str) -> None:
    news_results = []
    request_year = self.__START_YEAR

    while request_year <= self.__END_YEAR:
      news_from_year = await self.get_trends_by_semester(symbol, request_year)
      
      if request_year >= self.__END_YEAR - 1:
        news_from_year = self.parse_incomplete_dates(news_from_year, request_year)

      news_results.extend(news_from_year)
      request_year = request_year + 1

    for new in news_results:
      if 'datetime' in new:
        del new['datetime']
      
      sentiment_result = self.__SENTIMENT_ANALYZER.extract_sentiment(new['title'])
      new['sentiment'] = sentiment_result

      date_object = datetime.strptime(new['date'], "%b %d, %Y")
      # Format the date object as "DD/MM/YYYY"
      formatted_date = date_object.strftime("%d/%m/%Y")
      new['date'] = formatted_date

    with open(f'{self.__NEWS_DIRECTORY}/{symbol}.json', 'w') as news_file:
      json.dump(news_results, news_file)

  
  async def get_trends_by_semester(self, symbol, request_year):
    year_trends =  []
    start_of_year = '01/01'
    first_mid_of_year = '06/30'
    second_mid_of_year = '07/01'
    end_of_year = '12/31'

    for iteration in range(2) if request_year != 2024 else range(1):
      start_date=f"{start_of_year if iteration == 0 else second_mid_of_year}/{request_year}"
      end_date=f"{first_mid_of_year if iteration == 0 else end_of_year}/{request_year}" if request_year != 2024 else f"03/31/{request_year}"
      request_success = False
      tries = 0

      while not request_success and tries <= 50:
        try:
          logger.error(f'Getting {symbol} from {start_date} to {end_date}')
          pd_trends = await self.get_news_from_symbol(symbol, start_date, end_date)
          year_trends.extend(pd_trends)
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


  async def get_news_from_symbol(self, symbol: str, start_date, end_date) -> list:
    google_news = GoogleNews(lang='en', start=start_date,end=end_date)
    google_news.get_news(symbol)
    google_results = google_news.results(sort=True)

    return google_results
  
  def parse_incomplete_dates(self, news, year):
    for new in news:
      if 'date' in new and ',' not in new['date']:
        current_date = new['date']
        new['date'] = f'{current_date}, {year}'
    
    return news