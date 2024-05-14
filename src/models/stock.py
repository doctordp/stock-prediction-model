import yfinance as yf

class StockCollector:
  __STOCKS_DIRECTORY = '/home/user/data/stocks'

  async def get_stock_data(self, symbol: str) -> None:
    yahoo_result = await self.get_symbol_stock_data(symbol)
    yahoo_result.reset_index(inplace = True)
    yahoo_result['Date'] = yahoo_result['Date'].dt.strftime('%d-%m-%Y')
    yahoo_result.to_csv(f'{self.__STOCKS_DIRECTORY}/{symbol}.csv', sep=',', index=False, encoding='utf-8')

  async def get_symbol_stock_data(self, symbol: str):
    msft = yf.Ticker(symbol)
    result = msft.history(period="max")
    return result