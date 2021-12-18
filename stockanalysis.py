import requests
import json
import FinanceDatabase as fd
import pandas as pd
from pandas import json_normalize 


headers = {''}

# ### 야후 파이낸스 유료 API 불러오기 함수 ###
def get_quote(symbol, modules):
    url = f'https://yfapi.net/v11/finance/quoteSummary/{symbol}'
    querystring = {"symbols": symbol, "modules": modules}
    response = requests.request("GET", url, headers=headers, params=querystring)
    dict_response = json.loads(response.text)
    return dict_response["quoteSummary"]["result"][0][modules]


#1. symbol list 저장
stocks = fd.select_equities(country='United States', industry='Resorts & Casinos' )
symbol_lists = list(stocks.keys())


#2. ncav_list 생성 및 dataframe으로 형식 지정 
ncav_list =[]
#Create a DataFrame object
df = pd.DataFrame(ncav_list, columns = ['regularMarketPrice', 'totalCurrentAssets', 'totalLiab', 'sharesOutstanding', 'ncav', 'ncavs'])

#3. yahooapi에서 data 불러와서 ncav 관련 data 저장

for i in symbol_lists:
    try:
        regularMarketPrice = get_quote(i, "price")["regularMarketPrice"]["raw"]
        totalCurrentAssets = get_quote(i, "balanceSheetHistoryQuarterly")["balanceSheetStatements"][0]["totalCurrentAssets"]["raw"]
        totalLiab = get_quote(i, "balanceSheetHistoryQuarterly")["balanceSheetStatements"][0]["totalLiab"]["raw"]
        sharesOutstanding = get_quote(i, "defaultKeyStatistics")["sharesOutstanding"]["raw"]
        ncav = totalCurrentAssets - totalLiab
        ncavs = ncav / sharesOutstanding
        df.loc[i] = [regularMarketPrice, totalCurrentAssets, totalLiab, sharesOutstanding, ncav, ncavs]
    except:
        pass

df.to_excel("data.xlsx")
