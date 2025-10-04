# app.py (홈페이지)

import streamlit as st

st.set_page_config(
    page_title="캘리포니아 주택 가격 예측",
    page_icon="🏠",
    layout="wide"
)

st.title('🏠 캘리포니아 주택 가격 예측 대시보드')
st.markdown("---")

st.header('프로젝트 소개')
st.write("""
이 대시보드는 캘리포니아 주택 가격 데이터를 사용하여 만든 Streamlit 기반의 웹 애플리케이션입니다.
데이터 분석(EDA)과 머신러닝 모델을 통한 가격 예측 기능을 제공합니다.

**주요 기능:**
- **EDA 대시보드:** 데이터의 분포와 변수 간의 관계를 시각적으로 탐색합니다.
- **가격 예측:** 사용자가 직접 입력한 변수를 바탕으로 주택 가격을 예측합니다.

**사용한 기술 스택:**
- Python, Streamlit, Pandas, Scikit-learn, Seaborn/Matplotlib
""")

st.markdown("---")
st.info("사이드바 메뉴를 통해 다른 페이지로 이동할 수 있습니다.")
