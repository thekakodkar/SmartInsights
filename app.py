import streamlit as st
import pandas as pd
import plotly.express as px
import jaydebeapi
import os
from pandasai import Agent
from pandasai import SmartDatalake

os.environ["PANDASAI_API_KEY"] = "$2a$10$Xi7K5OzC81codGQatnTXeed8zj0TWPmm3R2Wyp4WfVDdMwaOVN0h."
query_response = ""

def connect_to_datalake():
    # Set up the JDBC driver and connection
    jdbc_url = "jdbc:infordatalake://VRKUNNOSSAPITOOY_TST"
    username = "your_username"
    password = "your_password"
    driver_path = "jdbc/infor-compass-jdbc-2023.10/infor-compass-jdbc-2023.10.jar"

    try:
        conn = jaydebeapi.connect(
            "com.infor.idl.jdbc.Driver",
            jdbc_url,
            {"user": username, "password": password},
            driver_path,
        )
    except Exception as e:
        st.error(f"Connection Error")
    return conn

# Fetch table schema
def fetch_table_schema(conn):
    #conn = connect_to_datalake()
    #cursor = conn.cursor()
    query = "SELECT DISTINCT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='default'"
    obj_schema = pd.read_sql(query, conn)
    #conn.close()  # Close the connection
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


def execute_query(query):
    conn = connect_to_datalake()
    cursor = conn.cursor()
    # Execute your queries here
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    data = pd.DataFrame(results, columns=column_names)
    return data


# Define the layout
custom_icon_path = "images/icon4.png"
st.set_page_config(page_title="Niel - Explore the unexplored", page_icon=custom_icon_path, layout="wide", initial_sidebar_state="expanded")

logo_url = "images/logo4.png"
st.sidebar.image(logo_url)

#Hide Deploy button
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    .sidebar-content {
        display: flex;
        align-items: center;
        margin-right: 10px;
    }
    .logo {
        margin-right: 10px;
    }    
    </style>
    """, unsafe_allow_html=True
)


# Create tabs for sidebar
tab_titles = ['General', 'EasySQL', 'AdvSQL', 'EasyAPI']

# Create a dictionary to map tab titles to their corresponding icons
tab_icons = {
    'General': '🌐',
    'EasyAPI': '🔗',
    'Object Store': '📦',
    'EasySQL': ':rocket:',
    'AdvSQL': ':rocket:'# Use the Infor logo here (replace with the actual logo)
}
tabs = st.sidebar.tabs([f"{tab_icons[title]} {title}" for title in tab_titles])

tab_titles_main = ['Data','Basic Plots', 'Statistical Plots','Chat for Visuals']
# Create a dictionary to map tab titles to their corresponding icons
tab_icons = {
    'Data': '🔍',
    'Basic Plots': '📊',
    'Statistical Plots': '📈',
    'Scientific Plots': '🔬',
    'ML Visuals': '🤖',
    'Chat for Visuals': ':speech_balloon:',
}

# Create the tabs with icons
tabs_main = st.tabs([f"{tab_icons[title]} {title}" for title in tab_titles_main])

# Placeholder for data
df = None

# General sidebar tab
with tabs[0]:
    uploaded_file = st.file_uploader(" ", type=["csv", "parquet", "xml", "json"])
    show_data = st.checkbox('Show data')
with tabs[1]:
    # Add Font Awesome CSS (you can replace this with your preferred icon library)
    connect_checkbox = st.checkbox("Connect to DataLake")
    if connect_checkbox:
        obj_table = fetch_tables('default')
        selected_table = st.selectbox("Select a table:", obj_table['TABLE_NAME'], key="selected_table")

        if selected_table:
            # Fetch fields for the selected table
            obj_fields = fetch_fields(selected_table)

            select_fields = st.checkbox("Select Fields")
            if select_fields:
                selected_fields = st.multiselect("Select fields:", obj_fields['COLUMN_NAME'], key="selected_fields")
                if selected_fields :
                    # Fetch data for the selected fields
                        query_df = gen_query(selected_table, selected_fields)
                        query_def = st.text_input('Query',query_df)
                        if st.button("Execute"):
                            query_response = execute_query(query_def)
                        else:
                            st.write("Query generation failed")
                            #  st.dataframe(data)
            else:
                st.warning("Please select at least one field and a company")
        else:
            st.warning("Please select a table.")

with tabs[2]:
    query_adef = st.text_area('Query',
'''SELECT bpid
FROM   ln_tccom100
WHERE  bptx_ref_compnr = 430 
MINUS 
SELECT bpid
FROM   ln_tccom100
WHERE  bptx_ref_compnr = 420'''
)
    if st.button("Execute Query"):
        query_response = execute_query(query_adef)
    #else:
    #   st.write("Query generation failed")
with tabs[3]:
    st.text('Request Authorization')

# Row 1: Model Selection and Data Upload
with tabs_main[0]:
    with (st.expander("📁 File", expanded=True)):
        # Create resizable columns
        col1, col2 = st.columns([1, 1])  # Adjust column widths here
        # Column 1: Model Selection and Data Upload
        with col1:
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)  # Adjust based on file type
                    st.success("Data loaded successfully.")
                    st.write("Enter prompts below (separated by semicolon). Type 'bye' to exit:")
                    prompts = st.text_input("Prompt", "Which country have the maximum sales")
                except Exception as e:
                    st.error(f"Error loading data: {str(e)}")
            else:
                st.info("Upload a data file to display its content.")
        with col2:
            # Dynamic selection of X and Y columns
            try:
                if prompts:
                    if st.button("respond"):
                        # print(dfe)
                        try:
                            lake = SmartDatalake(df)
                            response = lake.chat(prompts)
                            st.write(response)
                            #st.write(lake.last_code_executed)
                        except Exception as e:
                            st.error(f"Error loading data: {str(e)}")
                if df is not None:
                    x_column = st.selectbox("Select X Column", df.columns)
                    y_columns = st.multiselect("Select Y Columns", df.columns)
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
        # Create a checkbox in the sidebar
        if show_data:
            try:
                st.dataframe(df.head())  # Display first few rows of the DataFrame
            except Exception as e:
                st.error(f"Upload the file to explore the data")

    with (st.expander(":rocket: InforOS", expanded=True)):
        try:
            st.dataframe(query_response)
        except Exception as e:
            print(f"Error: {str(e)}")

with tabs_main[1]:
    # Row 2: Line Chart Visualization
    with st.expander("📊 Basic Plots ", expanded=True):
        col3, col4 = st.columns([1, 1])  # Adjust column widths here
        if df is not None and y_columns is not None:
            # Create visualizations
            with col3:
                try:
                    fig = px.line(df, x=x_column, y=y_columns)
                    fig.update_layout(autosize=False, width=500, height=500)
                    st.plotly_chart(fig)
                    fig = px.bar(df, x=x_column, y=y_columns)
                    fig.update_layout(autosize=False, width=500, height=500)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"AError:  {str(e)}")
            with col4:
                try:
                    for y_column in y_columns:
                        fig = px.pie(df, names=x_column, values=y_column)  # Pie chart only supports one Y column
                        fig.update_layout(autosize=False, width=500, height=500)
                        st.plotly_chart(fig)

                    fig = px.scatter(df, x=x_column, y=y_columns)
                    fig.update_layout(autosize=False, width=500, height=500)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"BError:  {str(e)}")
with tabs_main[2]:
    # Row 2: Statistical Charts
    with st.expander("📈 Statistical Plots ", expanded=True):
            col5, col6 = st.columns([1, 1])  # Adjust column widths here
            if df is not None and y_columns is not None:
                # Create visualizations
                with col5:
                    try:
                        # elif visualization == "Histogram":
                        for y_column in y_columns:
                            fig = px.histogram(df, x=y_column)
                            fig.update_layout(autosize=False, width=500, height=500)
                            st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"CError:  {str(e)}")

                with col6:
                    try:
                        #   elif visualization == "Box Plot":
                        for y_column in y_columns:
                            fig = px.box(df, y=y_column)
                            fig.update_layout(autosize=False, width=500, height=500)
                            st.plotly_chart(fig)
                    except Exception as e:
                        st.error(f"DError:  {str(e)}")

#with tabs_main[3]:
    #st.write("Enter prompts below (separated by semicolon). Type 'bye' to exit:")

    #prompts = st.text_input("Prompt","Which country have the maximum sales")
    #dfe = pd.DataFrame.from_dict(df)
    #st.write(dfe)
    #lake = Agent(dfe)
    #st.write(dfe)
   # while True:
    #    if prompts.lower() == 'bye':
     #       break
    #if prompts:
     #   if st.button("respond"):
      #      #print(dfe)
       #     try:
        #        lake = SmartDatalake(df)
         #       response = lake.chat(prompts)
          #      st.write(response)
           #     st.write(lake.last_code_executed)
           # except Exception as e:
            #    st.error(f"Error loading data: {str(e)}")

"""
Copyright © 2024 Niel - Explore the unexplored

"""