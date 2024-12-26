import psycopg2
from psycopg2 import sql

# 连接到 PostgreSQL 数据库
def conn_postgre():
    conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
    cur = conn.cursor()
    return cur,conn

def create_table(name, columns):
    cur, conn = conn_postgre()
    # Convert table name to sql.Identifier
    table_name = sql.Identifier(name)
    # Convert column names to sql.Identifier and format the columns
    column_definitions = sql.SQL(", ").join(
        sql.SQL("{} FLOAT4").format(sql.Identifier(col)) for col in columns
    )
    # Create the SQL query
    create_table_query = sql.SQL("""
        CREATE TABLE {} (
            {}
        )
    """).format(
        table_name,
        column_definitions
    )
    # Execute the query
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

def insert_data(name, df):
    cur,conn = conn_postgre() 
    table_name = sql.Identifier(name)
    columns = df.columns.tolist()
    column_placeholders = ", ".join([sql.Identifier(col).as_string(conn) for col in columns])
    value_placeholders = ", ".join(["%s"] * len(columns))
    insert_query = sql.SQL("""
        INSERT INTO {} ({})
        VALUES ({})
    """).format(table_name,
        sql.SQL(column_placeholders),
        sql.SQL(value_placeholders)
    )
    try:
        for i, row in df.iterrows():
            cur.execute(insert_query, tuple(row))
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def change_column_type_to_timestamp(table_name, column_name="date"):
    cur, conn = conn_postgre()
    try:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name}_temp TIMESTAMP;")
        cur.execute(f"""
            UPDATE {table_name}
            SET {column_name}_temp = '1970-01-01'::DATE + ({column_name} * INTERVAL '1 day');
        """)
        cur.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")
        cur.execute(f"ALTER TABLE {table_name} RENAME COLUMN {column_name}_temp TO {column_name};")
        cur.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({column_name});")
        
        conn.commit()
        print("Column type changed to timestamp and set as primary key successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()







