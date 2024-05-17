import json
import csv
from numpy import NaN
import pandas as pd
import logging

from regex import F

logger = logging.getLogger(__name__)

class Unifier:
  __SENTIMENT_DIRECTORY='/home/user/data/sentiment-csv'
  __STOCKS_DIRECTORY='/home/user/data/stocks'
  __TRENDS_DIRECTORY='/home/user/data/trends'
  __UNIFIED_DATA_DIRECTORY='/home/user/data/unified'

  def unify_by_symbol(self, symbol):    
    with open(f'{self.__STOCKS_DIRECTORY}/{symbol}.csv', 'r') as stocks_file:
      df_stock = pd.read_csv(stocks_file, header=0)

    with open(f'{self.__TRENDS_DIRECTORY}/{symbol}.csv', 'r') as trends_file:
      df_trends = pd.read_csv(trends_file, header=0)

    with open(f'{self.__SENTIMENT_DIRECTORY}/{symbol}.csv', 'r') as sentiment_file:
      df_sentiment = pd.read_csv(sentiment_file, header=0)
    
    df_stock.drop(columns=['Dividends', 'Stock Splits'], inplace=True)
    df_trends.drop(columns=['isPartial'], inplace=True)

    df_stock['Date'] = pd.to_datetime(df_stock['Date'], format='%d-%m-%Y')
    df_trends['date'] = pd.to_datetime(df_trends['date'], format='%Y-%m-%d')
    df_sentiment['date'] = pd.to_datetime(df_sentiment['date'], format='%d/%m/%Y')

    df_stock.sort_values('Date', inplace=True)
    df_trends.sort_values('date', inplace=True)
    df_sentiment.sort_values('date', inplace=True)
    
    df_trends.rename(columns={'date': 'Date'}, inplace=True)
    df_trends.rename(columns={symbol: 'Trends'}, inplace=True)

    df_sentiment.rename(columns={'date': 'Date'}, inplace=True)
    df_sentiment.rename(columns={'sentiment': 'Sentiment'}, inplace=True)
    
    df_sentiment = self.clear_duplicated_sentiment_dates(df_sentiment)

    merged_df = pd.merge(df_stock, df_trends, on='Date', how='left')
    merged_df = pd.merge(merged_df, df_sentiment, on='Date', how='left')
    merged_df.dropna(subset=['Trends'], inplace=True)
    

    merged_df['Sentiment'] = merged_df['Sentiment'].fillna(method='ffill').fillna('neutral')
    merged_df.insert(0, 'Symbol', symbol)

    merged_df.to_csv(f'{self.__UNIFIED_DATA_DIRECTORY}/{symbol}.csv', index=False)



    
  def clear_duplicated_sentiment_dates(self, df_sentiment):
    grouped = df_sentiment.groupby('Date')['Sentiment']

    for date, group in grouped:
      if len(group.unique()) > 1:
          if 'negative' in group.values and 'positive' in group.values:
              number_of_positives = (group == 'positive').sum()
              number_of_negatives = (group == 'negative').sum()
              if number_of_positives == number_of_negatives:
                  df_sentiment = df_sentiment[df_sentiment['Date'] != date]
                  new_row = pd.DataFrame({'Date': [date], 'Sentiment': ['neutral']})
                  df_sentiment = pd.concat([df_sentiment, new_row], ignore_index=True)
              elif number_of_positives > number_of_negatives:
                df_sentiment = df_sentiment[df_sentiment['Date'] != date]
                new_row = pd.DataFrame({'Date': [date], 'Sentiment': ['positive']})
                df_sentiment = pd.concat([df_sentiment, new_row], ignore_index=True)
              else:
                df_sentiment = df_sentiment[df_sentiment['Date'] != date]
                new_row = pd.DataFrame({'Date': [date], 'Sentiment': ['negative']})
                df_sentiment = pd.concat([df_sentiment, new_row], ignore_index=True)
      else:
        df_sentiment = df_sentiment[df_sentiment['Date'] != date]
        new_row = pd.DataFrame({'Date': [date], 'Sentiment': [group.values[0]]})
        df_sentiment = pd.concat([df_sentiment, new_row], ignore_index=True)

    return df_sentiment