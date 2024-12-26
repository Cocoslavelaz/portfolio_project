import pandas as pd 
import yfinance as yf
from psycopg2 import sql
from .conn_postgre import conn_postgre
from .get_stock import get_close
from datetime import date

def format_code(code):
    if isinstance(code, str) and code.isdigit():
        code_int = int(code)
        if code_int < 100:
            return f"{code_int:04d}"  # 将其格式化为四位数
    return code
    
stock_code = pd.read_csv("stock_code.csv")
code_list = stock_code["0"].astype(str).tolist()
code_list = [format_code(code) for code in code_list]
code_list = [code + "_close" for code in code_list]
today = date.today()

def get_all_close(start="2018-01-02", end=today):
    code_list_tw = [code.replace("_close", "") + ".Tw" for code in code_list]
    df = pd.DataFrame()
    count = 0
    index = 0
    for code in code_list_tw:
        stock_data = get_close(code, start=start, end=end).reset_index()
        stock_data.fillna(0, inplace=True)  # 填充缺失值
        date = stock_data["Date"]
        close = stock_data["Adj Close"]
        if count == 0:
            df["date"] = date
        df[code_list_tw[index]] = close
        count += 1
        index += 1
    columns = ["date"] + [col.replace(".Tw", "_close") for col in code_list_tw]
    df.columns = columns
    return df

def get_all_open(start="2018-01-02", end=today):
    code_list_tw = [code.replace("_close", "") + ".Tw" for code in code_list]
    df = pd.DataFrame()
    count = 0
    index = 0
    for code in code_list_tw:
        stock_data = get_close(code, start=start, end=end).reset_index()
        stock_data.fillna(0, inplace=True)  # 填充缺失值
        date = stock_data["Date"]
        Open = stock_data["Open"]
        if count == 0:
            df["date"] = date
        df[code_list_tw[index]] = Open
        count += 1
        index += 1
    columns = ["date"] + [col.replace(".Tw", "_open") for col in code_list_tw]
    df.columns = columns
    return df

def get_all_high(start="2018-01-02", end=today):
    code_list_tw = [code.replace("_close", "") + ".Tw" for code in code_list]
    df = pd.DataFrame()
    count = 0
    index = 0
    for code in code_list_tw:
        stock_data = get_close(code, start=start, end=end).reset_index()
        stock_data.fillna(0, inplace=True)  # 填充缺失值
        date = stock_data["Date"]
        high = stock_data["High"]
        if count == 0:
            df["date"] = date
        df[code_list_tw[index]] = high
        count += 1
        index += 1
    columns = ["date"] + [col.replace(".Tw", "_high") for col in code_list_tw]
    df.columns = columns
    return df

def get_all_volume(start="2018-01-02", end=today):
    code_list_tw = [code.replace("_close", "") + ".Tw" for code in code_list]
    df = pd.DataFrame()
    count = 0
    index = 0
    for code in code_list_tw:
        stock_data = get_close(code, start=start, end=end).reset_index()
        stock_data.fillna(0, inplace=True)  # 填充缺失值
        date = stock_data["Date"]
        volume = stock_data["Volume"]
        if count == 0:
            df["date"] = date
        df[code_list_tw[index]] = volume
        count += 1
        index += 1
    columns = ["date"] + [col.replace(".Tw", "_volume") for col in code_list_tw]
    df.columns = columns
    return df

def get_all_low(start="2018-01-02", end=today):
    code_list_tw = [code.replace("_close", "") + ".Tw" for code in code_list]
    df = pd.DataFrame()
    count = 0
    index = 0
    for code in code_list_tw:
        stock_data = get_close(code, start=start, end=end).reset_index()
        stock_data.fillna(0, inplace=True)  # 填充缺失值
        date = stock_data["Date"]
        low = stock_data["Low"]
        if count == 0:
            df["date"] = date
        df[code_list_tw[index]] = low
        count += 1
        index += 1
    columns = ["date"] + [col.replace(".Tw", "_low") for col in code_list_tw]
    df.columns = columns
    return df

