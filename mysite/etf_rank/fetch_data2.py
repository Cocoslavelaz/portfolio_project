from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql
import pandas as pd
from .conn_postgre import conn_postgre

cur,conn = conn_postgre()
today = datetime.today().strftime('%Y-%m-%d')
date_365_days_ago = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

def fetch_market(code="2330", start=date_365_days_ago, end=today):
    query = sql.SQL('''
        SELECT {date_column}, {close_column}
        FROM close
        WHERE {date_column} BETWEEN %s AND %s
    ''').format(
        date_column=sql.Identifier('date'),
        close_column=sql.Identifier(code + "_close")
    )
    # 执行查询
    cur.execute(query, (start, end))
    result = cur.fetchall()
    close = pd.DataFrame(result, columns=["date", "close"])

    query = sql.SQL('''
        SELECT {date_column}, {close_column}
        FROM open
        WHERE {date_column} BETWEEN %s AND %s
    ''').format(
        date_column=sql.Identifier('date'),
        close_column=sql.Identifier(code + "_open")
    )
    cur.execute(query, (start, end))
    result = cur.fetchall()
    open = pd.DataFrame(result, columns=["date", "open"])

    query = sql.SQL('''
        SELECT {date_column}, {close_column}
        FROM high
        WHERE {date_column} BETWEEN %s AND %s
    ''').format(
        date_column=sql.Identifier('date'),
        close_column=sql.Identifier(code + "_high")
    )
    cur.execute(query, (start, end))
    result = cur.fetchall()
    high = pd.DataFrame(result, columns=["date", "high"])

    query = sql.SQL('''
        SELECT {date_column}, {close_column}
        FROM low
        WHERE {date_column} BETWEEN %s AND %s
    ''').format(
        date_column=sql.Identifier('date'),
        close_column=sql.Identifier(code + "_low")
    )
    cur.execute(query, (start, end))
    result = cur.fetchall()
    low = pd.DataFrame(result, columns=["date", "low"])

    query = sql.SQL('''
        SELECT {date_column}, {close_column}
        FROM volume
        WHERE {date_column} BETWEEN %s AND %s
    ''').format(
        date_column=sql.Identifier('date'),
        close_column=sql.Identifier(code + "_volume")
    )
    cur.execute(query, (start, end))
    result = cur.fetchall()
    volume = pd.DataFrame(result, columns=["date", "volume"])
    merged_df = close.merge(open, on='date', how='left')\
                    .merge(high, on='date', how='left')\
                    .merge(low, on='date', how='left')\
                    .merge(volume, on='date', how='left')
    return merged_df


def fetch_closes(code_list=["2330"], start="2018-01-02", end=today):
    # Ensure 'code_list' is not empty
    if not code_list:
        raise ValueError("code_list cannot be empty")
    # Establish database connection
    cur, conn = conn_postgre()
    try:
        # Build the SQL query
        query = sql.SQL('''
            SELECT {date_column}, {columns}
            FROM close
            WHERE {date_column} BETWEEN %s AND %s
        ''').format(
            date_column=sql.Identifier('date'),
            columns=sql.SQL(', ').join([sql.Identifier(code + '_close') for code in code_list])
        )
        # Execute the query
        cur.execute(query, (start, end))
        result = cur.fetchall()
        # Get column names
        columns = ["date"] + [code + "_close" for code in code_list]
        # Convert result to DataFrame
        df = pd.DataFrame(result, columns=columns)
        # Commit the transaction
        conn.commit()
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"An error occurred: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    return df