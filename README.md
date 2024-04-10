# SmartInsights - chat with your enterprise data

This tool is designed to facilitate data exploration and visualization. It uses Streamlit for the web interface, pandas for data manipulation, Plotly for data visualization, and jaydebeapi for database connectivity.

Watch the video https://youtu.be/l1pLM7Ub3So

## Dependencies

- Streamlit
- pandas
- Plotly
- jaydebeapi
- pandasai

## Setup

1. Install the required Python packages.

```bash
pip install streamlit pandas plotly.express jaydebeapi pandasai
```

2. Set your PandasAI API key as an environment variable.

```bash
export PANDASAI_API_KEY="YOUR_API_KEY"
```

## Usage

Run the Streamlit app with the following command:

```bash
streamlit run main.py
```

The app provides an interface for connecting to a data lake, fetching table schemas, selecting tables and fields, and executing SQL queries. The results can be visualized using various plot types.

## Features

- File Upload: Upload a CSV, Parquet, XML, or JSON file to explore its data.
- Connect to DataLake: Connect to a data lake and fetch table schemas.
- Select Fields: Select fields from a table in the data lake.
- Execute: Execute a SQL query on the data lake.
- Request Authorization: Request authorization for certain operations.

## Upcoming features

- Added support to more data sources
- Support for data graphs 
- Improvised chat interface
  
## Note

Please replace `YOUR_API_KEY`, `YOUR_TENANT`, `your_username`, and `your_password` with your actual API key, tenant, username, and password, respectively.
```
