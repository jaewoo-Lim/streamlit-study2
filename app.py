import streamlit as st

# 페이지 정의
overview = st.Page("marketing_campaign.py", title="마케팅 분석", icon="📊")
detail   = st.Page("ecommerce_sales.py",   title="이커머스 분석", icon="🔍")

# 네비게이션 설정
pg = st.navigation([overview, detail])
pg.run()