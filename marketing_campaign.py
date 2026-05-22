import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드 및 전처리
@st.cache_data
def load_marketing():
    df = pd.read_csv('data/marketing_campaign_dataset.csv')
    df['Acquisition_Cost'] = df['Acquisition_Cost'].str.replace('[$,]', '', regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])

    campaign_map = {
        'Search': '검색', 'Email': '이메일', 'Social Media': '소셜 미디어',
        'Display': '디스플레이 광고', 'Influencer': '인플루언서'
    }
    location_map = {
        'New York': '뉴욕', 'Chicago': '시카고', 'Miami': '마이애미',
        'Los Angeles': '로스앤젤레스', 'Houston': '휴스턴'
    }
    df['Campaign_Type'] = df['Campaign_Type'].replace(campaign_map)
    df['Location'] = df['Location'].replace(location_map)
    return df

df = load_marketing().copy()

st.set_page_config(layout="wide")
st.title("📣 마케팅 캠페인 대시보드")

# 사이드바 필터
with st.sidebar:
    st.header("필터")
    if st.button("필터 초기화"):
        st.session_state.clear()
        st.rerun()
    campaign_types = st.multiselect("캠페인 유형", df['Campaign_Type'].unique().tolist(), default=df['Campaign_Type'].unique().tolist())
    location = st.selectbox("지역", ["전체"] + sorted(df['Location'].unique().tolist()))

filtered = df[df['Campaign_Type'].isin(campaign_types)]
if location != "전체":
    filtered = filtered[filtered['Location'] == location]

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 캠페인 성과", "💰 비용 분석", "📍 지역 성과"])
font_config = dict(family="Malgun Gothic, AppleGothic, NanumGothic")

# 공통 범위 계산 함수 -> 수치들의 차이가 미비해서 시각적으로 차이를 보기위해 사용
def get_range(data, col):
    mn, mx = data[col].min(), data[col].max()  # 해당 컬럼의 최소값과 최대값을 구함
    p = (mx - mn) * 0.5 if mx != mn else 0.1   # 범위 차이의 50%를 여유 공간(padding)으로 설정, 값이 같으면 0.1 부여
    return [mn - p, mx + p]                    # Y축의 시작점과 끝점을 [최소-여유, 최대+여유]로 반환

with tab1:
    st.subheader("캠페인 유형별 평균 ROI") 
    st.caption("💡 그래프에 마우스를 올리면 각 캠페인 유형의 상세 평균 ROI 수치를 확인할 수 있습니다.")
    group_data = filtered.groupby('Campaign_Type')['ROI'].mean().reset_index() # 캠페인별 평균 ROI 계산 및 데이터프레임화
    fig1 = px.bar(group_data, x='Campaign_Type', y='ROI', text='ROI') # ROI를 막대 그래프로 생성, 막대 위에 수치 표시
    fig1.update_yaxes(range=get_range(group_data, 'ROI')) # Y축 범위를 위에서 정의한 함수(get_range)로 좁혀 차이를 확대
    fig1.update_traces(texttemplate='%{text:.4f}', textposition='outside') # 막대 위 텍스트를 소수점 4자리로 고정하고 밖에 배치
    fig1.update_layout(xaxis_title="카테고리 유형", yaxis_title="ROI(투자 수익률)", font=font_config)
    st.plotly_chart(fig1, use_container_width=True) 

with tab2:
    st.subheader("채널별 ROI 성과")
    st.caption("💡 각 채널 막대 위에 마우스를 올리면 상세 ROI 데이터를 확인할 수 있습니다.")
    group_channel = filtered.groupby('Channel_Used')['ROI'].mean().reset_index()
    fig2 = px.bar(group_channel, x='Channel_Used', y='ROI', color='ROI', text='ROI') # ROI 값에 따라 막대 색상이 변하도록 설정
    fig2.update_yaxes(range=get_range(group_channel, 'ROI'))
    fig2.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    fig2.update_layout(xaxis_title="마케팅 채널", yaxis_title="평균 ROI(투자 수익률)", font=font_config)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("지역 및 캠페인 유형별 ROI 히트맵")
    st.caption("💡 히트맵의 각 영역에 마우스를 올리면 상세 수치가 표시됩니다.")
    pivot = filtered.pivot_table(index='Location', columns='Campaign_Type', values='ROI', aggfunc='mean')
    fig3 = px.imshow(pivot, aspect="auto", color_continuous_scale='Blues', text_auto='.2f', # 히트맵 생성, 파란색 그라데이션을 줘 직관적 표시, 그래프안에 수치표현
                     labels=dict(x="캠페인 유형", y="지역", color="평균 ROI(투자 수익률)"))
    fig3.update_xaxes(title_text="캠페인 유형")
    fig3.update_yaxes(title_text="지역")
    fig3.update_traces(hovertemplate="지역: %{y}<br>유형: %{x}<br>평균 ROI: %{z:.4f}<extra></extra>")
    fig3.update_layout(font=font_config)
    st.plotly_chart(fig3, use_container_width=True)

    # 💡 마케팅 데이터셋에 연동되도록 하단에 폼 추가
with st.form("search_form"):
    keyword   = st.text_input("키워드 검색")
    submitted = st.form_submit_button("검색")

if submitted and keyword:
    mask    = df.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)
    filtered_search = df[mask]
    st.write(f"'{keyword}' 검색 결과: {len(filtered_search):,}행")
    st.dataframe(filtered_search.head(20))

st.divider()
uploaded = st.file_uploader("내 데이터 업로드 (CSV)", type=["csv"])
if uploaded is not None:
    user_df = pd.read_csv(uploaded)
    st.success(f"{uploaded.name} ({len(user_df):,}행)")
    st.dataframe(user_df.describe())