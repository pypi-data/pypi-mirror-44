##  IEXWrapper
This is a simple wrapper to IEXTrading API (https://iextrading.com/developer/docs/)

# Installation
```
pip install IEXWrapper
```

 Some example
```
from IEXWrapper import IEXTrading
```
```
symbols = ['AAPL', 'MSFT']

```
or...
```
symbols = 'aapl,msft'
```
```
w = IEXTrading(symbols)
```

Then you can simply run
```
w.get_company_info()
w.get_key_stats()

```

Responses are in JSON

  Available methods

* availableStocks() - return a list of stocks supported by IEX
* get_stock_quote()
* get_news()
* get_book()
* get_chart(range)
* get_list_value(group) - return an array of quotes for the top 10 symbols in a specified list
* get_sector_performance()
* get_company_info()
* get_companies_by_sector() - still need URL encode
* get_companies_by_tag() - still need URL encode
* get_stock_dividend(range)
* get_earnings()
* get_custom_call(url) - allow you to make custom call, to IEX's not wrapped functionality
* get_financial_statement(period)
* get_key_stats()
* get_ohlc()
* get_previous()

All informations can be found [here](https://iextrading.com/developer/docs/)

```
availableRanges = ['5y','2y', '1y','ytd','6m', '3m', '1m', '1d', 'date', 'dynamic']
availableGroups = ['mostactive', 'gainers', 'losers', 'iexvolume', 'iexpercent', 'infocus']
availablePeriod = ['annual','quarter']
```


 Works are still in progress
