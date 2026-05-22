import streamlit as st
import pandas as pd

upload = st.file_uploader("CSV 파일 입력 : ", ["csv"])

if upload is not None:
    df = pd.read_csv(upload)
    st.dataframe(df.head())