import streamlit as st
from config import custom_icon_path, logo_url

#st.set_page_config(page_title="Niel - Explore the unexplored", page_icon=custom_icon_path, layout="wide", initial_sidebar_state="expanded")

#st.sidebar.image(logo_url)

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

tab_titles = ['General']
tab_titles_main = ['Data','Basic Plots', 'Statistical Plots', 'Chat']

tab_icons = {
    'General': '🌐',
    'EasyAPI': '🔗',
    'Object Store': '📦',
    'EasySQL': ':rocket:',
    'Infor': '🚀',
    'Data': '🔍',
    'Basic Plots': '📊',
    'Statistical Plots': '📈',
    'Scientific Plots': '🔬',
    'ML Visuals': '🤖',
    'Chat': ':speech_balloon:',
}

