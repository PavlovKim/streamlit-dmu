# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import json
from prophet.serialize import model_from_json
from prophet.plot import plot_plotly

# CSV 변환 함수
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# 리포트 메인 함수
def reportMain(total_df):
    st.markdown("### 자치구별 아파트 예측 리포트")

    # 자치구 선택
    sgg_nm = st.sidebar.selectbox("자치구 선택", sorted(total_df['CGG_NM'].unique()))

    # 예측 기간 선택
    periods = int(st.sidebar.number_input("향후 예측 기간을 지정하세요 (1~30일)"
                                          , min_value=1, max_value=30, step=1))

    # 모델 불러오기
    with open(f'ml/models/{sgg_nm}_model.json', 'r', encoding='utf-8') as fin:
        model = model_from_json(json.load(fin))

    # 예측 수행
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # CSV 다운로드 버튼
    csv = convert_df(forecast)
    st.sidebar.download_button(
        label="예측 결과 다운로드 (CSV)",
        data=csv,
        file_name=f"{sgg_nm}_아파트_평균값_예측_{periods}일간.csv",
        mime="text/csv"
    )

    # Plotly 시각화
    fig = plot_plotly(model, forecast)
    fig.update_layout(
        title=dict(
            text=f"{sgg_nm} 아파트 평균값 예측 ({periods}일간)",
            font=dict(size=20),
            x=0.5
        ),
        xaxis_title="날짜",
        yaxis_title="아파트 평균값 (만원)",
        autosize=False,
        width=800,
        height=600
    )
    fig.update_yaxes(tickformat=',')  # 천 단위 구분 쉼표

    # 그래프 출력
    st.plotly_chart(fig)





