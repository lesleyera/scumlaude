# -----------------------------------------------------------
# 스트림릿 대시보드 1-3차시 통합 코드 (+ Regplot 참고)
# -----------------------------------------------------------

# --- 1차시: 기본 설정과 데이터 로딩 ---

# 1. 필요한 라이브러리들을 불러옵니다.
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

# 2. 페이지의 기본 설정을 지정합니다.
st.set_page_config(
    page_title="캘리포니아 주택 가격 분석",
    page_icon="🏠",
    layout="wide"
)

# 3. 데이터 로딩 함수에 캐시 데코레이터를 추가하여 속도를 향상시킵니다.
@st.cache_data
def load_data():
    """캘리포니아 주택 가격 데이터셋을 로드하고 데이터프레임으로 변환합니다."""
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['target'] = housing.target
    return df

# 함수를 호출하여 데이터를 df 변수에 저장합니다.
df = load_data()

# --- 3차시: 인터랙티브 위젯 (사이드바) ---
# (사이드바는 보통 코드 상단에 배치하여 전체 페이지에 영향을 주도록 합니다.)

st.sidebar.header('⚙️ 차트 옵션')

# X축 선택에 사용할 컬럼 리스트를 준비합니다.
feature_list = df.columns.drop('target')
# Y축 선택에 사용할 컬럼 리스트를 준비합니다.
all_features_list = df.columns

# 사이드바에 X축과 Y축 선택을 위한 selectbox를 만듭니다.
selected_x = st.sidebar.selectbox('X축으로 사용할 변수를 선택하세요.', feature_list)
selected_y = st.sidebar.selectbox('Y축으로 사용할 변수를 선택하세요.', all_features_list, index=list(all_features_list).index('target'))


# --- 메인 화면 구성 ---

# 페이지의 전체 제목을 설정합니다.
st.title('🏠 캘리포니아 주택 가격 데이터 분석')
st.markdown("---")

# --- 2차시: 정적(Static) 시각화와 레이아웃 ---

# 1. 원본 데이터 및 통계 정보를 테이블로 표시합니다.
st.subheader('1. 데이터 확인')
st.dataframe(df.head())

st.subheader('2. 데이터 통계')
st.dataframe(df.describe())
st.markdown("---")


# 2. 정적 차트들을 레이아웃에 맞춰 배치합니다.
st.subheader('3. 정적 데이터 시각화')

# st.columns를 이용해 화면을 두 개의 컬럼으로 나눕니다.
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 주택 가격 분포 (히스토그램)")
    fig, ax = plt.subplots()
    sns.histplot(df['target'], kde=True, ax=ax)
    st.pyplot(fig)

with col2:
    st.markdown("#### 중간 소득과 주택 가격 관계 (산점도)")
    fig, ax = plt.subplots()
    sns.scatterplot(x='MedInc', y='target', data=df, ax=ax, alpha=0.5)
    st.pyplot(fig)

# --- [참고] 추세선이 있는 산점도 (regplot) ---
st.subheader('[참고] 추세선이 있는 산점도 (regplot)')
st.markdown("`scatterplot` 대신 `regplot`을 사용하면 데이터의 경향을 나타내는 추세선을 함께 그릴 수 있습니다.")

fig, ax = plt.subplots()
sns.regplot(x='MedInc', y='target', data=df, ax=ax,
            scatter_kws={'alpha': 0.3}, # 점들의 투명도 조절
            line_kws={'color': 'red'})   # 추세선 색상 지정
st.pyplot(fig)


# 3. 상관관계 히트맵을 표시합니다.
st.markdown("---")
st.subheader('4. 특성(Feature) 간 상관관계 (히트맵)')

# df.corr()를 이용해 상관관계 행렬을 만듭니다.
corr_matrix = df.corr()

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)


# --- 3차시: 인터랙티브 위젯 (메인 화면) ---

st.markdown("---")
st.subheader('5. 동적 산점도 (Interactive Scatter Plot)')

# 사이드바에서 선택된 변수들을 이용해 산점도를 그립니다.
fig, ax = plt.subplots()
sns.scatterplot(x=selected_x, y=selected_y, data=df, ax=ax, alpha=0.5)
ax.set_title(f'{selected_x} vs. {selected_y}')
ax.set_xlabel(selected_x)
ax.set_ylabel(selected_y)
st.pyplot(fig)