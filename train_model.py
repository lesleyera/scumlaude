# train_model.py

import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
import joblib

print("모델 훈련을 시작합니다...")

# 데이터 로드
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target)

# 모델 훈련 (Random Forest 사용)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 훈련된 모델을 파일로 저장
joblib.dump(model, 'model.joblib')

print("모델 훈련 및 저장이 완료되었습니다: model.joblib")