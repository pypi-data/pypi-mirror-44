'''
This project wants to be a wrapper to use https://iextrading.com/ API in a simple way
IEX Docs: https://iextrading.com/developer/docs


The IEX API only supports GET requests at this time.

Parameter values must be comma-delimited when requesting multiple.
(i.e. ?symbols=SNAP,fb is correct.)
Casing does not matter when passing values to a parameter.
(i.e. Both ?symbols=fb and ?symbols=FB will work.)
Be sure to url-encode the values you pass to your parameter.
(i.e. ?symbols=AIG+ encoded is ?symbols=AIG%2b.)
Filter results
All HTTP request endpoints support a filter parameter to return a subset of data. Pass a comma-delimited list of field names to filter. Field names are case-sensitive and are found in the Reference section of each endpoint.

Example: ?filter=symbol,volume,lastSalePrice will return only the three fields specified.

TODO (wrap):
- Earnings Today
- IPO Calendar
- IEX Regulation SHO Threshold Securities List
- IEX Short Interest List
- Largest Trades
- Volume by Venue
- IEX Dividends, Corporate Actions, Next Day Ex Date
- TOPS
- Effective Spread
'''

import requests
import urllib

endpoint = "https://api.iextrading.com/1.0"

#availableRanges docs: https://iextrading.com/developer/docs/#chart
availableRanges = ['5y','2y', '1y','ytd','6m', '3m', '1m', '1d', 'date', 'dynamic']

#docs: https://iextrading.com/developer/docs/#list
availableGroups = ['mostactive', 'gainers', 'losers', 'iexvolume', 'iexpercent', 'infocus']


class IEXTrading():
    #constructor
    def __init__(self, ticker=''):
        self.ticker = ticker.lower() if isinstance(ticker, str) else [t.lower() for t in ticker]
        self._cache = {}
        if len(self.ticker) > 100:
            raise ValueError('IEX Trading API supports up to 100 stocks in a single call')

    #This method format lists in url format (ex. ['AAPL', 'MSFT'] --> 'AAPL,MSFT')
    def format_list(self, obj):
        if isinstance(obj, str) and obj != '':
            return obj
        elif isinstance(obj, list):
            return str(','.join(obj))
        else:
            raise ValueError('ticker missing')

    #Get the list of all available stocks in IEX
    def availablesStocks(self):
        #More info on this API: https://iextrading.com/developer/docs/#symbols
        return self.make_request('/ref-data/symbols')

    #Make and handle the HTTP request
    def make_request(self, requestUrl):
        resp = requests.get(endpoint + requestUrl)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise ConnectionError('IEX Trading API response code was: '+str(resp.status_code)+' URL: '+endpoint+requestUrl)

    #Get stocks quote
    def get_stock_quote(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=quote'
        return self.make_request(urlCall)

    #Get news for stock
    def get_news(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=news'
        return self.make_request(urlCall)

    #Get book for stock
    def get_book(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=book'
        return self.make_request(urlCall)

    #Get chart for stock
    def get_chart(self, range):
        if range in availableRanges:
            urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=chart&range='+range
            return self.make_request(urlCall)
        else:
            raise ValueError('\'range\' parameter value not supported. Supported values are: '+str(availableRanges))

    #Returns an array of quotes for the top 10 symbols in a specified list.
    def get_list_value(self, group):
        if group in availableGroups:
            urlCall = '/stock/market/'+group
            return self.make_request(urlCall)
        else:
            raise ValueError('\'group\' not supported. Available values are: '+str(availableGroups))

    #Return an array of sector performance. docs: https://iextrading.com/developer/docs/#relevant
    def get_sector_performance(self):
        return self.make_request('/stock/market/sector-performance')

    #company info. docs: https://iextrading.com/developer/docs/#company
    def get_company_info(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=company'
        return self.make_request(urlCall)

    #Note: need url encode
    def get_companies_by_sector(self, sectorName):
        urlCall = '/stock/market/collection/sector?collectionName='+urllib.parse.quote_plus(sectorName)
        return self.make_request(urlCall)

    #Note: need url encode
    def get_companies_by_tag(self, tagName):
        urlCall = '/stock/market/collection/tag?collectionName='+urllib.parse.quote_plus(tagName)
        return self.make_request(urlCall)

    #https://iextrading.com/developer/docs/#dividends
    def get_stock_dividend(self, range):
        if isinstance(self.ticker, str):
            if range in availableRanges:
                urlCall = '/stock/'+self.format_list(self.ticker)+'/dividends/'+range
            else:
                raise ValueError('Unsupported \'range\'')
        else:
            raise ValueError('\'get_stock_dividend\' function dosen\'t support multiple stocks')

    #https://iextrading.com/developer/docs/#earnings
    def get_earnings(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=earnings'
        return self.make_request(urlCall)

    #Get custom call using IEX Trading API
    def get_custom_call(self, end):
        #Send only the last part of the URL
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&'+end
        return self.make_request(urlCall)

    def get_financial_statement(self, period):
        if period.lower() in ['annual', 'quarter']:
            urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=financials&period='+period
            return self.make_request(urlCall)
        else:
            raise ValueError('\'period\' not supported. It can be only annual or quarter')

    #https://iextrading.com/developer/docs/#key-stats
    def get_key_stats(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=stats'
        return self.make_request(urlCall)

    def get_ohlc(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=ohlc'
        return self.make_request(urlCall)

    def get_previous(self):
        urlCall = '/stock/market/batch?symbols='+self.format_list(self.ticker)+'&types=previous'
        return self.make_request(urlCall)
