import streamlit as st

# Columns

col1,col2 = st.columns(2)

with col1:
    col1.header("Column 1")
    col1.text("This is some text in column 1.")

with col2:
    col2.header("Column 2")
    col2.text("This is some text in column 2.")

# Tabs

tab1, tab2 = st.tabs(["Overview", "Details"])
with tab1:
    st.write("This is Overview")
with tab2:
    st.write("This is Details")

# Multiple Pages

# app.py
# pages/
#    page1.py
#    page2.py