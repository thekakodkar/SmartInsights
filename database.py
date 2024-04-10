import jaydebeapi
import pandas as pd
from config import jdbc_url, driver, username, password, driver_path

def connect_to_datalake(tenant):
    conn = jaydebeapi.connect(
        driver,
        url + tenant,
        {"user": username, "password": password},
        driver_path,
    )
    print(jdbc_url +tenant)
    return conn



# Fetch table schema
def fetch_table_schema(conn):
    query = "SELECT DISTINCT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='default'"
    obj_schema = pd.read_sql(query, conn)
    return obj_schema

# Fetch tables for the selected schema
def fetch_tables(selected_schema):
    conn = connect_to_datalake()
    cursor = conn.cursor()
    query = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='{selected_schema}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()  # Close the connection
    obj_table = pd.DataFrame(results, columns=["TABLE_NAME"])
    return obj_table

# Fetch fields for the selected table
def fetch_fields(selected_table):
    conn = connect_to_datalake()
    cursor = conn.cursor()
    query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{selected_table}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()  # Close the connection
    obj_fields = pd.DataFrame(results, columns=["COLUMN_NAME"])
    return obj_fields

# Fetch data for the selected fields
def fetch_data(selected_table, selected_fields):
    conn = connect_to_datalake()
    cursor = conn.cursor()
    fields_str = ", ".join(selected_fields)
    query = f"SELECT {fields_str} FROM {selected_table}"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()  # Close the connection
    data = pd.DataFrame(results)
    return data

def gen_query(selected_table, selected_fields):
    conn = connect_to_datalake()
    cursor = conn.cursor()
    fields_str = ", ".join(selected_fields)
    query = f"SELECT {fields_str} FROM {selected_table}"
    conn.close()  # Close the connection
    return query

def execute_query(query,tenant):
    conn = connect_to_datalake(tenant)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(results, columns=column_names)
    return data
