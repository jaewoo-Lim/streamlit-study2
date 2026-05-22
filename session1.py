import streamlit as st

# 좋아요 버튼 기능 구현

if 'liked' not in st.session_state:
    st.session_state['liked'] = False

label = "❤️ 좋아요 취소" if st.session_state['liked'] else "🤍 좋아요"
if st.button(label):
    st.session_state['liked'] = not st.session_state['liked']

if st.session_state['liked']:
    st.success("좋아요를 눌렀습니다!")









# ---

# count = 0

# if st.button("클릭"):
#     count += 1

# st.write("클릭횟수 : ", count)

# 1. 초기화 가드(조건문을 통한 가드) : 세션 초기값 세팅
if 'count' not in st.session_state:     
    st.session_state['count'] = 0

# count = 0으로 초기화하기
col1, col2 = st.columns([3, 1])
with col1:
    # 2. 쓰기 : 버튼이 클릭되었을 경우 세션상태값 업데이트
    if st.button("클릭"):
        st.session_state['count'] += 1

with col2:
    if st.button("초기화"):
        st.session_state['count'] = 0

# 3. 읽어서 보여주기
st.write("클릭 횟수 : ", st.session_state['count'])
