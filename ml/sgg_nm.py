# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import json
from prophet.serialize import model_from_json

plt.rcParams['font.family'] = "Malgun Gothic"

# 모델 불러오기 함수
@st.cache_resource
def load_models(sgg_nms):
    models = []
    for sgg_nm in sgg_nms:
        with open(f'ml/models/{sgg_nm}_model.json', 'r') as fin:
            model = model_from_json(json.load(fin))  # Load model
            models.append(model)
    return models


# Streamlit 시각화 함수
def predictDistrict(total_df):
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'], format="%Y-%m-%d")

    # 아파트만 필터링
    total_df = total_df[total_df['BLDG_USG'] == '아파트']

    # 자치구 리스트 생성
    sgg_nms = sorted(list(total_df['CGG_NM'].unique()))

    # 예측 기간 입력
    periods = int(st.number_input("향후 예측 기간을 지정하세요 (1~30일)"
                                  , min_value=1, max_value=30, step=1))

    # 모델 불러오기
    models = load_models(sgg_nms)

    # 5x5 서브플롯 생성
    fig, ax = plt.subplots(figsize=(20, 12), sharex=True, sharey=False, ncols=5, nrows=5)

    for i in range(len(sgg_nms)):
        future = models[i].make_future_dataframe(periods=periods)
        forecast = models[i].predict(future)

        row, col = divmod(i, 5)
        models[i].plot(forecast, uncertainty=True, ax=ax[row, col])
        ax[row, col].set_title(f"{sgg_nms[i]} 평균가격 예측 ({periods}일)")
        ax[row, col].set_xlabel("날짜")
        ax[row, col].set_ylabel("평균가격 (만원)")
        for tick in ax[row, col].get_xticklabels():
            tick.set_rotation(30)

    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    st.pyplot(fig)
