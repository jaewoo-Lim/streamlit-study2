import streamlit as st

st.write("홈")

name = st.text_input("이름 입력하세요", key='user_name')

if st.session_state.get('user_name'):
    st.success(f"반갑습니다. {st.session_state['user_name']}님")