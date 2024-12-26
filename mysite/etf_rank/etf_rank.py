import pandas as pd
from conn_postgre import conn_postgre

def get_last_six_rows():
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    # 查詢資料表的最後六筆資料
    query = """
    SELECT * FROM all_etf_close
    ORDER BY date DESC
    LIMIT 6;
    """
    df = pd.read_sql(query, conn)
    # 依日期排序，確保從過去到最近日期的順序
    df = df.sort_values(by="date").reset_index(drop=True)
    # 關閉資料庫連線
    conn.close()
    return df

def calculate_sorted_five_day_avg_return(df):
    # 計算每日報酬率
    daily_returns = df.set_index("date").pct_change().dropna()  # 計算日報酬率
    # 計算每支 ETF 的五日平均日報酬率
    five_day_avg_returns = daily_returns.tail(5).mean()  # 計算近五日平均
    # 依平均日報酬率大小排序，並返回欄位名稱
    sorted_avg_returns = five_day_avg_returns.sort_values(ascending=False)
    return sorted_avg_returns.index.tolist()

def get_five_day_avg_return():
    """
    從資料庫中查詢 ETF 平均五日報酬率，按降序排序
    """
    df = get_last_six_rows()
    calculate_sorted_five_day_avg_return(df)
    # 使用 ORM 查詢 ETF 資料庫，計算平均五日報酬率
    df_last_six = get_last_six_rows()
    sorted_etf_columns = calculate_sorted_five_day_avg_return(df_last_six)
    return sorted[10:]


df_last_six = get_last_six_rows()
sorted_etf_columns = calculate_sorted_five_day_avg_return(df_last_six)

