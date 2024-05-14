from transformers import pipeline

class SentimentAnalyzer:
  __PIPELINE_NAME = 'sentiment-analysis'
  __PIPELINE_MODEL = 'sangrimlee/bert-base-multilingual-cased-nsmc'
  __MAX_TENSOR_SIZE = 51

  def __init__(self) -> None:
    self.__pipeline = pipeline(self.__PIPELINE_NAME, model=self.__PIPELINE_MODEL,
                                tokenizer=self.__PIPELINE_MODEL,
                                max_length=self.__MAX_TENSOR_SIZE, truncation=True)
  
  def extract_sentiment(self, content: str) -> str:
    sentiment = self.__pipeline(content)[0]['label']

    return str(sentiment)