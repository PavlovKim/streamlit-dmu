# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from prophet import Prophet
import os
import matplotlib.font_manager as fm

def predictType(total_df):
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'], format="%Y-%m-%d")

    # 주거형태 목록
    types = list(total_df['BLDG_USG'].unique())

    # 사용자 입력: 예측 기간
    periods = int(st.number_input("향후 예측 기간을 지정하세요 (1~30일)"
                                  , min_value=1, max_value=30, step=1))

    font_dirs = [os.getcwd() + '/Nanum_Gothic']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)

    font_names = sorted(set([f.name for f in fm.fontManager.ttflist]))
    selected_font = st.selectbox("폰트 선택", font_names)
    plt.rc('font', family=selected_font)

    # 그래프 그리기
    fig = predict_plot(total_df, types, periods)

    st.pyplot(fig)
    st.markdown("<hr>", unsafe_allow_html=True)

def predict_plot(total_df, types, periods):
    fig, ax = plt.subplots(figsize=(10, 6), sharex=True, ncols=2, nrows=2)

    for i in range(len(types)):
        model = Prophet()

        # 해당 주거 유형 필터링
        df_filtered = total_df[total_df['BLDG_USG'] == types[i]][['CTRT_DAY', 'THING_AMT']]
        df_grouped = df_filtered.groupby('CTRT_DAY')['THING_AMT'].mean().reset_index()
        df_grouped = df_grouped.rename(columns={"CTRT_DAY": "ds", "THING_AMT": "y"})

        model.fit(df_grouped)

        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        # 좌표 계산
        row = i // 2
        col = i % 2

        model.plot(forecast, uncertainty=True, ax=ax[row, col])
        ax[row, col].set_title(f"서울시 {types[i]} 평균가격 예측 ({periods}일)")
        ax[row, col].set_xlabel("날짜")
        ax[row, col].set_ylabel("평균가격 (만원)")
        for tick in ax[row, col].get_xticklabels():
            tick.set_rotation(30)

    plt.tight_layout()
    return fig



