import streamlit as st

st.write("대시보드")

st.header(f"{st.session_state.get('user_name')}님의 대시보드")