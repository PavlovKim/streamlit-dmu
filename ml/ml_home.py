# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from ml.houseType import predictType
from ml.sgg_nm import predictDistrict
from ml.report import reportMain

def home():
    st.markdown("### 머신러닝 예측 개요")
    st.markdown("""
    - 주거 형태별 예측 그래프 추세  
    - 자치구역별 예측 그래프 추세  
    - 사용된 알고리즘: **Facebook Prophet**
    - [Prophet 공식 문서](https://facebook.github.io/prophet/docs/quick_start.html)
    """)

def run_ml(total_df):
    # 날짜 데이터 변환
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'], format="%Y-%m-%d")

    st.markdown("## 머신러닝 예측 페이지")
    st.markdown("예측 결과를 아래의 탭에서 확인할 수 있습니다.")

    # 상단 메뉴 (가로형)
    selected = option_menu(
        menu_title=None,
        options=["Home", "주거형태별", "자치구역별", "보고서"],
        icons=["house", "bar-chart", "map", "file-earmark-text"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#fafafa"
            },
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "color": "green"
            },
            "nav-link-selected": {
                "background-color": "#eee"
            }
        }
    )

    # 각 메뉴에 따른 실행
    if selected == 'Home':
        home()
    elif selected == '주거형태별':
        predictType(total_df)
    elif selected == '자치구역별':
        predictDistrict(total_df)
    elif selected == '보고서':
        reportMain(total_df)
    else:
        st.warning("올바르지 않은 메뉴입니다.")




