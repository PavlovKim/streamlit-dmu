# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from utils import load_data
from home import run_home
from eda.eda_home import run_eda
from ml.ml_home import run_ml
def main():
    st.set_page_config(page_title="빅데이터 분석 프로젝트", layout="wide")
    with st.sidebar:
        sidebar_selected = option_menu(
            "대시보드 메뉴", ["Home", "탐색적 자료 분석", "부동산 예측"],
            icons=['house', 'bar-chart', 'graph-up'],
            menu_icon="cast", default_index=0
        )

    total_df = load_data()
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'])

    if sidebar_selected == "Home":
        run_home()
    elif sidebar_selected == "탐색적 자료 분석":
        run_eda(total_df)
    elif sidebar_selected == "부동산 예측":
        run_ml(total_df)
    else:
        print("error")

if __name__ == '__main__':
    main()




