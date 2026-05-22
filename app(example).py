import streamlit as st

overview = st.Page("session1.py", title="요약",     icon="📊")
detail   = st.Page("session2.py",   title="상세 분석", icon="🔍")
setting  = st.Page("session3.py", title="설정")
                   
pg = st.navigation({"분석": [overview, detail],"설정":[setting]})

pg.run()