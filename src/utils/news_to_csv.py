import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def parse_news_to_csv(symbol: str):
  with open(f'/home/user/data/sentiment/{symbol}.json', 'r') as sentiment_json:
    stories = json.load(sentiment_json)
  
  data = []

  for story in stories:
    data.extend([[story['date'], story['sentiment']]])

  df = pd.DataFrame(data, columns=["date", "sentiment"])

  df.to_csv(f'/home/user/data/sentiment-csv/{symbol}.csv', index=False)
