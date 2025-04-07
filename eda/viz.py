import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


def meanChart(total_df, CGG_NM):
    st.markdown("## 가구별 평균 가격 추세")
    filtered_df = total_df[total_df['CGG_NM'] == CGG_NM]
    filtered_df = filtered_df[filtered_df['CTRT_DAY'].between("2025-02-01", "2025-03-31")]

    result = filtered_df.groupby(['CTRT_DAY', 'BLDG_USG'])['THING_AMT'].mean().reset_index()

    fig = make_subplots(rows=2, cols=2,
                        shared_xaxes=True,
                        subplot_titles=['아파트', '단독다가구', '오피스텔', '연립다세대'],
                        horizontal_spacing=0.15)

    house_types = ['아파트', '단독다가구', '오피스텔', '연립다세대']
    row_col = [(1, 1), (1, 2), (2, 1), (2, 2)]

    for i, house_type in enumerate(house_types):
        df = result[result['BLDG_USG'] == house_type]
        fig.add_trace(px.line(df, x='CTRT_DAY', y='THING_AMT').data[0],
                      row=row_col[i][0], col=row_col[i][1])

    st.plotly_chart(fig)

def barChart(total_df):
    st.markdown("### 지역별 평균 가격 막대 그래프")

    # 월 선택 & 가구 유형 선택
    month_selected = st.selectbox("월을 선택하세요", [2, 3])
    house_selected = st.selectbox("가구 유형을 선택하세요", total_df['BLDG_USG'].unique())

    # 데이터 전처리
    total_df['month'] = pd.to_datetime(total_df['CTRT_DAY']).dt.month
    result = total_df[(total_df['month'] == month_selected) & (total_df['BLDG_USG'] == house_selected)]

    # 평균 가격 계산
    bar_df = result.groupby('CGG_NM')['THING_AMT'].mean().reset_index()
    df_sorted = bar_df.sort_values('THING_AMT', ascending=False)

    # 막대 그래프 생성
    fig = px.bar(df_sorted, x='CGG_NM', y='THING_AMT')

    # 레이아웃 설정
    fig.update_yaxes(
        tickformat=".0f",
        title_text="물건 가격 (만원)",
        range=[0, df_sorted['THING_AMT'].max()]
    )
    fig.update_layout(
        title="Bar Chart - Ascending Order",
        xaxis_title="지역구명",
        yaxis_title="평균 가격 (만원)"
    )

    st.plotly_chart(fig)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 지역별 거래 건수 막대 그래프")

    # 거래 건수 집계
    cnt_df = (result.groupby(['CGG_NM', 'BLDG_USG'])['THING_AMT'].
              count().reset_index().rename(columns={'THING_AMT': '거래건수'}))
    cnt_df = cnt_df.sort_values('거래건수', ascending=False)

    # 막대 그래프 생성
    fig = px.bar(cnt_df, x='CGG_NM', y='거래건수')

    fig.update_layout(
        title="Bar Chart - Ascending Order",
        xaxis_title="지역구명",
        yaxis_title="거래 건수"
    )

    st.plotly_chart(fig)
    
def cntChart(total_df, cgg_nm):
    st.markdown("## 가구별 거래 건수 추세")

    # 선택된 자치구명에 맞춰 데이터 필터링
    filtered_df = total_df[total_df['CGG_NM'] == cgg_nm]
    filtered_df = filtered_df[filtered_df['CTRT_DAY'].between("2025-02-01", "2025-03-31")]

    # 거래 건수 집계
    result = (
        filtered_df.groupby(['CTRT_DAY', 'BLDG_USG'])['THING_AMT']
        .count()
        .reset_index()
        .rename(columns={'THING_AMT': '거래건수'})
    )

    # 주택 유형별 데이터 분리 및 서브플롯 설정
    house_types = ['아파트', '단독다가구', '오피스텔', '연립다세대']
    row_col = [(1, 1), (1, 2), (2, 1), (2, 2)]

    fig = make_subplots(
        rows=2, cols=2, shared_xaxes=True,
        subplot_titles=house_types,
        horizontal_spacing=0.15
    )

    # for 문을 사용하여 주택 유형별 그래프 추가
    for i, house_type in enumerate(house_types):
        df = result[result['BLDG_USG'] == house_type]
        if not df.empty:  # 데이터가 있는 경우만 추가
            trace = px.line(df, x='CTRT_DAY', y='거래건수', markers=True).data[0]
            fig.add_trace(trace, row=row_col[i][0], col=row_col[i][1])

    # Y축 설정
    fig.update_yaxes(
        tickformat=".0f",
        title_text="거래 건수",
        range=[0, result['거래건수'].max()]
    )

    # 레이아웃 업데이트
    fig.update_layout(
        title="가구별 거래 건수 추세 그래프",
        width=800, height=600,
        showlegend=False,
        template='plotly_white'
    )

    # 그래프 출력
    st.plotly_chart(fig)

def showViz(total_df):
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'], format="%Y-%m-%d")

    # 자치구 선택
    ssg_nm = st.sidebar.selectbox("자치구명", sorted(total_df['CGG_NM'].unique()))

    # 차트 메뉴 선택
    selected = st.sidebar.radio("차트 메뉴", ['가구당 평균 가격 추세', '가구당 거래 건수', '지역별 평균 가격 막대 그래프'])

    if selected == "가구당 평균 가격 추세":
        meanChart(total_df, ssg_nm)
    elif selected == "가구당 거래 건수":
        cntChart(total_df, ssg_nm)
    elif selected == "지역별 평균 가격 막대 그래프":
        barChart(total_df)
    else:
        st.warning("Error")
        



