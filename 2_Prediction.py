# pages/2_Prediction.py (상단 부분 수정)

import streamlit as st
import joblib
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import requests # 파일 다운로드를 위해 추가
import os # 파일 존재 여부 확인을 위해 추가

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="주택 가격 예측",
    page_icon="🤖",
    layout="wide"
)

# --- 모델 파일 불러오기 (다운로드 기능 추가) ---
@st.cache_resource # 모델처럼 큰 객체는 cache_data 대신 cache_resource 사용
def load_model():
    """
    모델 파일을 로드합니다. 파일이 없으면 구글 드라이브에서 다운로드합니다.
    """
    file_path = 'model.joblib'
    
    # 1. 파일이 이미 있는지 확인
    if not os.path.exists(file_path):
        st.info("모델 파일을 다운로드합니다... (최초 실행 시 몇 초 소요)")
        
        # 2. 다운로드 링크 (본인의 링크로 교체하세요!)
        url = 'https://drive.google.com/uc?export=download&id=1iLICa05xza_8FbmSGnWtmIzZO8_Yv9bz/' # <-- 여기에 본인 링크의 FILE_ID 입력
        
        # 3. 파일 다운로드
        with st.spinner('다운로드 중...'):
            r = requests.get(url, stream=True)
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
    
    # 4. 파일 로드
    try:
        model = joblib.load(file_path)
        return model
    except FileNotFoundError:
        st.error("모델 파일을 찾을 수 없습니다.")
        return None

model = load_model()

# --- 사이드바 ---
st.sidebar.header("변수 입력")

# 사용자가 입력할 변수 목록
feature_list = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
# 사용자가 입력한 값을 저장할 딕셔너리
user_inputs = {}

# 사이드바에서 각 변수에 대한 입력을 받습니다.
for feature in feature_list:
    user_inputs[feature] = st.sidebar.number_input(
        label=f'{feature} 값을 입력하세요',
        step=0.1,
        format="%.4f" # 소수점 네 자리까지 표시
    )

# --- 메인 화면 ---
st.title('🤖 주택 가격 예측')
st.markdown("---")

# 모델 파일이 성공적으로 로드되었을 경우에만 예측 기능을 보여줍니다.
if model is not None:
    # '예측 실행' 버튼
    if st.sidebar.button('예측 실행'):
        # 사용자 입력값을 데이터프레임으로 변환
        input_df = pd.DataFrame([user_inputs])
        
        # 모델 예측
        prediction = model.predict(input_df)
        
        # 예측 결과 표시
        st.subheader('예측 결과')
        predicted_price = prediction[0] * 100000  # 단위 변환
        st.metric(label="예상 주택 가격", value=f"${predicted_price:,.2f}")
        
        st.markdown("---")
        st.subheader('예측 위치 지도')

        # 지도 표시를 위한 위도, 경도 값 가져오기
        lat = user_inputs['Latitude']
        lon = user_inputs['Longitude']
        
        # 1. Folium을 이용해 지도 객체 생성
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # 2. 구글맵 타일 레이어 추가
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='Google',
            name='Google Maps'
        ).add_to(m)

        # 3. 지도 위에 마커(표시) 추가
        folium.Marker(
            [lat, lon],
            popup=f"예상 가격: ${predicted_price:,.2f}",
            tooltip="예측 위치"
        ).add_to(m)

        # 4. 지도에 레이어 컨트롤 추가
        folium.LayerControl().add_to(m)

        # 5. Folium 지도를 HTML로 변환하여 드래그 가능하게 만듦
        map_html = m._repr_html_()
        components.html(map_html, height=500)

    else:
        st.info("사이드바에 값을 입력하고 '예측 실행' 버튼을 눌러주세요.")