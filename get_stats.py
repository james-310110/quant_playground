import pysnowball as ball
import tushare as ts
import sys
import csv
import numpy as np
import pandas as pd


def get_ticker_list(input_path, format):
    print("Acquiring ticker list")
    tickers = []
    portfolio_file = open(input_path,"r")
    for line in portfolio_file:
        ticker = line.strip().split('\n')[0]
        if format == "ball":
            ticker = ticker[-2:] + ticker[:6]
        tickers.append(ticker)
    return tickers

def get_company_stats(tickers):
    print("Acquiring stock data")
    num_tickers = len(tickers)
    stats = np.zeros((num_tickers,9))
    for i in range(num_tickers):
        main = ball.main_indicator(tickers[i])
        alr = main['data']['items'][0]['asset_liab_ratio']
        annual_income = ball.income(symbol=tickers[i],is_annals=1,count=3)
        tr_2018 = annual_income['data']['list'][0]['total_revenue'][0]
        tr_2017 = annual_income['data']['list'][1]['total_revenue'][0]
        tr_2016 = annual_income['data']['list'][2]['total_revenue'][0]
        np_2018 = annual_income['data']['list'][0]['net_profit'][0]
        np_2017 = annual_income['data']['list'][1]['net_profit'][0]
        np_2016 = annual_income['data']['list'][2]['net_profit'][0]
        quarter_income = ball.income(symbol=tickers[i],is_annals=0,count=1)
        tr_2019q1 = quarter_income['data']['list'][0]['total_revenue'][0]
        np_2019q1 = quarter_income['data']['list'][0]['net_profit'][0]
        row = np.array([alr,tr_2019q1,tr_2018,tr_2017,tr_2016,np_2019q1,np_2018,np_2017,np_2016])
        stats[i] = row
    return stats

def filter_blacklist(tickers):
    print("Filtering blacklisted companies ")
    blacklist_tickers = get_ticker_list("blacklist.csv")
    num_blacklisted_companies = 0
    for ticker in tickers:
        for blacklisted_ticker in blacklist_tickers:
            if ticker == blacklisted_ticker:
                num_blacklisted_companies += 1
                if ticker in tickers:
                    tickers.remove(ticker)
    print("Successfully filtered "+str(num_blacklisted_companies)+" blacklisted companies")
    return tickers

def output_stats_table(stats,output_path):
    df = pd.DataFrame(stats)
    df.to_excel(output_path,index=False)
    print('Script completed')


def find_pledge_ratio_pro(tickers):
    print("Finding pledge ratios")
    num_tickers = len(tickers)
    p_ratios = []
    pro = ts.pro_api('7e56c92dd88e3aa14d6558ae0eb80f3e14b023d03c1c59d8b836a214')
    for i in range(50,num_tickers):
        df = pro.pledge_stat(ts_code=tickers[i])
        if not df.empty:
            p_ratio = df.iloc[0]['pledge_ratio']
        else:
            p_ratio = 'N/A'
        p_ratios.append(p_ratio)
    return p_ratios
        

def find_no1_pledge_ratio(tickers):
    print("Finding the pledge ratio of the No.1 shareholder")
    num_tickers = len(tickers)
    p_ratios = []
    # acquire your own token at https://tushare.pro/user/token
    pro = ts.pro_api('7e56c92dd88e3aa14d6558ae0eb80f3e14b023d03c1c59d8b836a214')
    for i in range(50,num_tickers):
        df = pro.top10_holders(ts_code=tickers[i])
        if not df.empty:
            holder_name = df.iloc[0]['holder_name']
            df = pro.query('pledge_detail',ts_code=tickers[i])
            df = df[df.holder_name==holder_name]
            if not df.empty:
                if df.iloc[0]['holding_amount'] is not None and df.iloc[0]['pledged_amount'] is not None:
                    p_ratio = df.iloc[0]['pledged_amount'] / df.iloc[0]['holding_amount']
                else:
                    p_ratio = 'N/A'
                print(holder_name,"has",p_ratio,"pledging")
                p_ratios.append(p_ratio)
            else:
                p_ratios.append(0)
                print("all pledged amounts released for", tickers[i])
        else:
            p_ratios.append('N/A')
            print(tickers[i])
    return p_ratios


class InvalidInputException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if sys.argv[1] != "stats" and sys.argv[1] != "p_ratio_all" and sys.argv[1] != "p_ratio_no1":
    raise InvalidInputException("Option not found")
option = sys.argv[1]
input_path = "/inputs/stocks.csv"
output_path = "/outputs/stats.xlsx"
### set token for pysnowball, acquire your own through https://blog.crackcreed.com/diy-xue-qiu-app-shu-ju-api/
ball.set_token('xq_a_token=6317a2c02c6b467a70acdfe43169ea7c95f72bb6')
    
if option == "stats":
    tickers = get_ticker_list(input_path,'ball')
    tickers = filter_blacklist(tickers,'ball')
    stats = get_company_stats(tickers)
    output_stats_table(stats,output_path)

if option == "p_ratio_all":
    tickers = get_ticker_list(input_path,'ts')
    tickers = filter_blacklist(tickers,'ts')
    ### find pledge ratios of overall shareholders
    stats = find_pledge_ratio_pro(tickers)
    output_stats_table(stats,output_path)

if option == "p_ratio_no1":
    tickers = get_ticker_list(input_path,'ts')
    tickers = filter_blacklist(tickers,'ts')
    ### find pledge ratios of no.1 shareholders
    stats = find_no1_pledge_ratio(tickers)
    stats = find_pledge_ratio_pro(tickers)
    output_stats_table(stats,output_path)