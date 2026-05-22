import streamlit as st

# 위젯의 매개변수로 key를 지정할 경우
# session_state의 key로 자동 저장한다.
# 초기화 가드 대신 최초 실행시 value값을 초기값으로 사용한다.
# 데이터 변경시 -> rerun -> 마지막 session state값으로 불러온다.
age_range = st.slider("나이 범위", 0, 80, (0, 80), key='age_range')

st.write("현재 선택값 : ", st.session_state['age_range'])