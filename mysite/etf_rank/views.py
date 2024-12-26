from django.shortcuts import render
from .conn_postgre import conn_postgre
import pandas as pd
import numpy as np

def index(request):
    """
    渲染 ETF 排行榜
    """
    df_last_six = get_last_30_rows()
    sorted_etf_returns = calculate_sorted_30_day_avg_return(df_last_six)
    etf_list = [
        {"name": k, "avg_return": round(v * 100, 2)}
        for k, v in list(sorted_etf_returns.items())[:20]
    ]
    return render(request, './etf_rank/index.html', {'etf_list': etf_list})

def get_last_30_rows():
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM all_etf_close
    ORDER BY date DESC
    LIMIT 30;
    """
    df = pd.read_sql(query, conn)
    df = df.sort_values(by="date").reset_index(drop=True)
    conn.close()
    return df

def calculate_sorted_30_day_avg_return(df):
    df = df.dropna(axis=1, how="all")
    prohibited_list = ["00632R"]
    daily_returns = df.set_index("date").pct_change()
    thirty_day_avg_returns = daily_returns.tail(30).mean()
    sorted_avg_returns = thirty_day_avg_returns.sort_values(ascending=False)
    sorted_avg_returns.index = sorted_avg_returns.index.str.replace("_close", "")
    sorted_avg_returns = sorted_avg_returns[~sorted_avg_returns.index.isin(prohibited_list)]
    return sorted_avg_returns.to_dict()







