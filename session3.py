import streamlit as st
import pandas as pd

@st.cache_data
def load_titanic():
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
    return pd.read_csv(url)

df = load_titanic().copy()
ALL_PCLASS = [1, 2, 3]

if st.sidebar.button("필터 초기화"):
    st.session_state['pclass'] = ALL_PCLASS
    st.session_state['survived_only'] = False

with st.sidebar:
    pclass = st.multiselect(
        "객실 등급", ALL_PCLASS,
        default=st.session_state.get('pclass', ALL_PCLASS),
        key='pclass'
    )
    survived_only = st.checkbox(
        "생존자만",
        value=st.session_state.get('survived_only', False),
        key='survived_only'
    )

filtered = df[df['Pclass'].isin(pclass)]
if survived_only:
    filtered = filtered[filtered['Survived'] == 1]

st.write(f"선택된 승객: {len(filtered):,}명")
st.dataframe(filtered.head(20))