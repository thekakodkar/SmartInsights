import streamlit as st
from config import custom_icon_path, logo_url

st.set_page_config(page_title="Niel - Explore the unexplored", page_icon=custom_icon_path, layout="wide", initial_sidebar_state="expanded")

from ui import tab_titles,tab_titles_main, tab_icons, custom_icon_path
from database import fetch_tables, fetch_fields, gen_query, execute_query
import pandas as pd
import plotly.express as px
from pandasai import SmartDatalake
from pandasai import Agent

st.sidebar.image(logo_url)

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


# Create the Sidebar tabs with icons
tabs_side = st.sidebar.tabs([f"{tab_icons[title]} {title}" for title in tab_titles])

# Create the tabs with icons
tabs_main = st.tabs([f"{tab_icons[title]} {title}" for title in tab_titles_main])

# Placeholder for data
df = None
query_response = None
response = None

# General sidebar tab
with tabs_side[0]:
    with (st.expander("📁 Files", expanded=False)):
        uploaded_file = st.file_uploader(" ", type=["csv", "parquet", "xml", "json"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)  # Adjust based on file type
        show_data = st.radio(
            "Show data",
            ["None","Head", "Full"],
            )

    #Infor Expander
    with (st.expander(":rocket: ERP/CRM", expanded=False)):
        tenant = st.text_input("Tenant","TENANT_NAME", type="password")
        query_adef = st.text_area('Query',
        '''SELECT *
        FROM   ln_tccom100
        WHERE  bptx_ref_compnr = 430 
        '''
        )
        if st.button("Execute Query"):
            try:
                query_response = execute_query(query_adef,tenant)
                df = query_response
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

with tabs_main[0]:
    if show_data == 'Head' and df is not None:
        st.dataframe(df.head())  # Display first few rows of the DataFrame
    elif show_data == 'Full' and df is not None:
        st.dataframe(df)  # Display first few rows of the DataFrame
    if query_response is not None:
        st.dataframe(query_response) #Display Infor data

with tabs_main[1]:
#Row 2: Line Chart Visualization
    try:
        if df is not None:
            x_column = st.selectbox("Select X Column", df.columns)
            y_columns = st.multiselect("Select Y Columns", df.columns)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
    with st.expander("📊 Basic Plots ", expanded=True):
        col3, col4 = st.columns([1, 1])  # Adjust column widths here
        if query_response is None:
            st.write(df)
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

with tabs_main[3]:
    prompts = st.text_input("Prompt", "Which country have the maximum sales")
    if prompts:
        if st.button("respond"):
            # print(dfe)
            try:
                lake = SmartDatalake(df)
                response = lake.chat(prompts)
                st.write(response)
                # st.write(lake.last_code_executed)
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")