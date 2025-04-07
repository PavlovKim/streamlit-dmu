# -*- coding:utf-8 -*-
import pandas as pd
from utils import load_data
import streamlit as st
from millify import prettify

def run_home():
    # 데이터 불러오기
    total_df = load_data()

    # Home 화면 상단 설명
    st.markdown("## 대시보드 개요")
    st.markdown("본 프로젝트는 서울시 부동산 실거래가를 알려주는 대시보드입니다.")
    st.markdown("↓↓↓ 여기에 원하는 내용을 추가할 수 있습니다. ↓↓↓")

    # 날짜 변환 및 데이터 필터링
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'], format="%Y-%m-%d")
    total_df['month'] = total_df['CTRT_DAY'].dt.month
    total_df = total_df.loc[total_df['BLDG_USG'] == '아파트', :]

    # 사용자 입력 (자치구 & 월 선택)
    cgg_nm = st.sidebar.selectbox("자치구", sorted(total_df['CGG_NM'].unique()))
    selected_month = st.sidebar.radio("확인하고 싶은 월을 선택하세요", ['2월', '3월'])

    month_dict = {'2월': 2, '3월': 3}

    # 선택한 자치구와 월에 대한 데이터 필터링
    filtered_month = total_df[total_df['month'] == month_dict[selected_month]]
    filtered_month = filtered_month[filtered_month['CGG_NM'] == cgg_nm]

    # 최소/최대 가격 계산
    min_price = filtered_month['THING_AMT'].min()
    max_price = filtered_month['THING_AMT'].max()

    # 최소/최대 가격 출력
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"{cgg_nm} 최소가격(만원)", value=prettify(min_price))
    with col2:
        st.metric(label=f"{cgg_nm} 최대가격(만원)", value=prettify(max_price))

    # 아파트 가격 상위 3 & 하위 3 테이블
    st.markdown("### 아파트 가격 상위 3")
    sorted_df = filtered_month[
        ["CGG_NM", "STDG_NM", "BLDG_USG", "ARCH_AREA", "THING_AMT"]
    ]
    st.dataframe(sorted_df.sort_values(by='THING_AMT', ascending=False)
                 .head(3).reset_index(drop=True))

    st.markdown("### 아파트 가격 하위 3")
    st.dataframe(sorted_df.sort_values(by='THING_AMT', ascending=True)
                 .head(3).reset_index(drop=True))

    # 출처 표시
    st.caption("출처: [서울시 부동산 실거래가 정보]"
               "(https://data.seoul.go.kr/datalist/OA-21275/S/1/datasetView.do)")





