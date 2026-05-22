import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_ecommerce():
    df = pd.read_csv('data/ecommerce_sales_data.csv', index_col=0)
    df['City'] = df['City'].str.strip()

    # 카테고리 한글화 매핑
    category_map = {
        'Laptops and Computers': '노트북/컴퓨터',
        'Electronics': '전자제품',
        'Home Appliances': '가전제품',
        'Charging Cables': '충전 케이블',
        'Monitors': '모니터',
        'Phones and Accessories': '휴대폰/액세서리',
        'Audio Devices': '오디오 기기',
        'Batterie': '배터리',
        'Entertainment Devices': '엔터테인먼트 기기'
    }
    
    df['Product Category'] = df['Product Category'].replace(category_map)
    return df


df = load_ecommerce().copy()

st.set_page_config(layout="wide")

st.title("🛒 이커머스 매출 대시보드")

with st.sidebar:
    st.header("필터")
    if st.button("필터 초기화"):
        st.session_state['categories'] = df['Product Category'].unique().tolist()
        st.session_state['month_range'] = (1, 12)

    categories = st.multiselect(
        "카테고리",
        df['Product Category'].unique().tolist(),
        default=st.session_state.get('categories', df['Product Category'].unique().tolist()),
        key='categories'
    )

    st.divider()

    month_range = st.slider("월 범위", 1, 12, (1, 12), key='month_range')


filtered = df[
    df['Product Category'].isin(categories) &
    df['Month'].between(month_range[0], month_range[1])
]

col1, col2 = st.columns(2)
col1.metric("총 주문 수", f"{len(filtered):,}")
col2.metric("총 매출", f"${filtered['Sales'].sum():,.0f}")

font_config = dict(family="Malgun Gothic", size=14) # 탭별로 사용할 한글폰트 미리 지정


tab1, tab2, tab3 = st.tabs(["📊 카테고리별 성과", "📦 카테고리 종합 성과", "⏰ 시간별 트렌드"])

with tab1:
    st.subheader("카테고리별 총 매출")
    fig = px.bar(
    filtered.groupby('Product Category')['Sales'].sum().reset_index(),
    x='Product Category', y='Sales',
    title='카테고리별 총 매출',
    labels={'Product Category': '상품 카테고리', 'Sales': '판매액($)'}
    )
    st.plotly_chart(fig)


with tab2:
    st.subheader("카테고리별 판매량 및 판매액 종합 비교")
    st.caption("💡 각 상품 카테고리별로 총 판매수량(개수)과 총 판매액($)의 규모를 좌우로 나란히 비교합니다. 마우스를 올리면 상세 수치가 표시됩니다.")
    cat_perf = filtered.groupby('Product Category').agg({
        'Quantity Ordered': 'sum',
        'Sales': 'sum'
    }).reset_index().sort_values(by='Sales', ascending=False) # 매출액이 높은 순서로 보기 좋게 정렬
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_vol = px.bar(
            cat_perf, 
            x='Product Category', 
            y='Quantity Ordered', 
            text='Quantity Ordered',
            title="카테고리별 총 판매량 (개)", 
            labels={'Product Category': '상품 카테고리', 'Quantity Ordered': '판매량'}
        )
        fig_vol.update_traces(
            texttemplate='%{text:,}개', 
            textposition='outside',
            hovertemplate="카테고리: %{x}<br>총 판매량: %{y:,}개<extra></extra>"
        )
        fig_vol.update_layout(font=font_config)
        st.plotly_chart(fig_vol, use_container_width=True)
        
    with col_chart2:
        fig_rev = px.bar(
            cat_perf, 
            x='Product Category', 
            y='Sales', 
            text='Sales',
            title="카테고리별 총 판매액 ($)", 
            labels={'Product Category': '상품 카테고리', 'Sales': '판매액'}
        )
        fig_rev.update_traces(
            texttemplate='$%{text:,.0f}', 
            textposition='outside',
            hovertemplate="카테고리: %{x}<br>총 판매액: $%{y:,.0f}<extra></extra>"
        )
        fig_rev.update_layout(font=font_config)
        st.plotly_chart(fig_rev, use_container_width=True)

with tab3:
    st.subheader("시간대별 카테고리별 판매 트렌드 (히트맵)")
    st.caption("💡 0시부터 23시까지 각 시간대별로 어떤 카테고리의 상품이 집중적으로 주문되었는지 분석합니다.")
    
    time_pivot = filtered.pivot_table(index='Product Category', columns='Hour', values='Quantity Ordered', aggfunc='sum').fillna(0)
    
    fig_time = px.imshow(
        time_pivot,
        aspect="auto",
        color_continuous_scale='Blues',
        text_auto=',.0f',
        labels=dict(x="구매 시간 (시)", y="상품 카테고리", color="판매량(개)")
    )
    fig_time.update_xaxes(title_text="구매 시간대", tickmode='linear', tick0=0, dtick=1)
    fig_time.update_yaxes(title_text="상품 카테고리")
    fig_time.update_traces(hovertemplate="카테고리: %{y}<br>시간대: %{x}시<br>판매량: %{z:,}개<extra></extra>")
    fig_time.update_layout(font=font_config)
    st.plotly_chart(fig_time, use_container_width=True)

    # 💡 이커머스 데이터셋에 연동되도록 하단에 폼 추가
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