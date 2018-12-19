from datetime import date
from nsepy import get_history
from nsepy import get_index_pe_history
#Stock history
sbin = get_history(symbol='SBIN',
                    start=date(2015,1,1), 
                    end=date(2016,12,31))
sbin[[ 'VWAP', 'Turnover']].plot(secondary_y='Turnover')

"""	Index price history
	symbol can take these values (These indexes have derivatives as well)
	"NIFTY" or "NIFTY 50",
	"BANKNIFTY" or "NIFTY BANK",
	"NIFTYINFRA" or "NIFTY INFRA",
    	"NIFTYIT" or "NIFTY IT",
    	"NIFTYMID50" or "NIFTY MIDCAP 50",
    	"NIFTYPSE" or "NIFTY PSE"
	In addition to these there are many indices
	For full list refer- http://www.nseindia.com/products/content/equities/indices/historical_index_data.htm
"""
nifty = get_history(symbol="NIFTY", 
                    start=date(2015,1,1), 
                    end=date(2015,1,10),
					index=True)
nifty[['Close', 'Turnover']].plot(secondary_y='Turnover')

#Futures and Options historical data
nifty_fut = get_history(symbol="NIFTY", 
			start=date(2015,1,1), 
			end=date(2015,1,10),
			index=True,
			futures=True, expiry_date=date(2015,1,29))
						
stock_opt = get_history(symbol="SBIN",
			start=date(2015,1,1), 
			end=date(2015,1,10),
			option_type="CE",
			strike_price=300,
			expiry_date=date(2015,1,29))

#Index P/E ratio history
nifty_pe = get_index_pe_history(symbol="NIFTY",
				start=date(2015,1,1), 
				end=date(2015,1,10))
