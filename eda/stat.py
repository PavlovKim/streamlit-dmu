# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from scipy.stats import ttest_ind

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def twoMeans(total_df):
    total_df['month'] = total_df['CTRT_DAY'].dt.month

    # 아파트 데이터 필터링 (2월과 3월 데이터)
    apt_df = total_df[(total_df['BLDG_USG'] == '아파트') & (total_df['month'].isin([2, 3]))]

    st.markdown("### 집계 \n"
                "- 2월과 3월의 아파트 가격을 비교합니다.")

    # 평균, 표준편차, 샘플 수 집계
    ttest_df = round(apt_df.groupby('month')['THING_AMT'].agg(['mean', 'std', 'size']), 1)
    st.dataframe(ttest_df, use_container_width=True)

    st.markdown("### 서울시 통합 2월 vs 3월 차이 검정 \n"
                "- 2월과 3월의 아파트 평균 가격의 차이를 검정합니다. \n"
                "- 가설설정 \n"
                "  - 귀무가설(H₀): 2월과 3월의 아파트 평균 차이는 없다. \n"
                "  - 대립가설(H₁): 2월과 3월의 아파트 평균 차이는 있다.")

    # 2월과 3월 데이터 분리
    feb_df = apt_df[apt_df['month'] == 2]
    march_df = apt_df[apt_df['month'] == 3]

    # 독립 표본 t-검정 수행
    result = ttest_ind(feb_df['THING_AMT'], march_df['THING_AMT'], equal_var=False)

    # p-value 확인
    st.markdown(f"- 확인 결과 p-value 값이 **{result.pvalue:.5f}** 이므로")

    if result.pvalue > 0.05:
        st.markdown("- 귀무가설(H₀)을 채택하여, 2월과 3월의 아파트 평균 차이는 없다.")
    else:
        st.markdown("- 대립가설(H₁)을 채택하여, 2월과 3월의 아파트 평균 차이는 있다.")

    # 자치구 선택
    selected_cgg_nm = st.sidebar.selectbox("자치구명", sorted(total_df['CGG_NM'].unique()))

    st.markdown(f"### 서울시 {selected_cgg_nm} 2월 vs 3월 차이 검정 \n"
                "- 선택한 자치구의 2월과 3월 아파트 평균 차이를 검정합니다.")

    # 선택한 자치구 데이터 필터링
    cgg_df = apt_df[apt_df['CGG_NM'] == selected_cgg_nm]
    cgg_feb_df = cgg_df[cgg_df['month'] == 2]
    cgg_march_df = cgg_df[cgg_df['month'] == 3]

    # 자치구별 독립 표본 t-검정 수행
    cgg_result = ttest_ind(cgg_feb_df['THING_AMT'], cgg_march_df['THING_AMT'], equal_var=False)

    st.markdown(f"- 확인 결과 p-value 값이 **{cgg_result.pvalue:.5f}** 이므로")

    if cgg_result.pvalue > 0.05:
        st.markdown(f"- 귀무가설(H₀)을 채택하여, **{selected_cgg_nm}**의 2월과 3월 아파트 평균 차이는 없다.")
    else:
        st.markdown(f"- 대립가설(H₁)을 채택하여, **{selected_cgg_nm}**의 2월과 3월 아파트 평균 차이는 있다.")

    # 시각화
    st.markdown(f"### 서울시 **{selected_cgg_nm}** 2월 vs 3월 시각화", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 3))
    sns.pointplot(x='month', y='THING_AMT', data=cgg_df)
    sns.despine()
    st.pyplot(fig)

    # 집계된 데이터 출력
    st.dataframe(round(cgg_df.groupby('month')['THING_AMT'].agg(["mean", "std", "size"]), 1), use_container_width=True)

def showStat(total_df):
    total_df['CTRT_DAY'] = pd.to_datetime(total_df['CTRT_DAY'], format="%Y-%m-%d")

    selected = st.sidebar.selectbox("분석 메뉴", ['두 집단간 차이 검정', '상관분석', '회귀분석'])

    if selected == '두 집단간 차이 검정':
        st.markdown("### 두 집단간 차이 검정 이론 설명 \n"
                    "- t-검정은 두 개의 독립적인 데이터 샘플의 평균 간에 유의미한 차이가 있는지 확인하는 데 사용할 수 있는 통계 테스트입니다. \n")

        st.markdown("t-통계량은 다음과 같이 계산됩니다.")
        st.latex(r"t = \frac{{\bar{X}_1 - \bar{X}_2}}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}")
        st.markdown("- $\\bar{X}$ : 표본의 평균을 나타냅니다. \n"
                    "- LaTeX expressions을 사용하여 수식을 표시할 수 있습니다. \n"
                    "- 나머지를 추가해보세요 .. ")
        twoMeans(total_df)


    elif selected == "상관분석":

        st.markdown("### 상관분석 이론 설명 \n"

                    "- 피어슨 상관계수 ... \n"

                    "- 스피어만 상관계수 ... \n"

                    "- 참고 자료 등을 통해 다양하게 꾸며봅니다 ... ")
        corrRelation(total_df)

    elif selected == "회귀분석":

        st.markdown("### 회귀분석 이론 설명 \n"

                    "- 회귀식의 가정 \n"

                    "- 회귀식의 가설 \n"

                    "- 추가 설명 ... ")

        regRession(total_df)


def corrRelation(total_df):
    total_df['month'] = total_df['CTRT_DAY'].dt.month

    # 아파트 데이터 필터링 (2월과 3월 데이터)
    apt_df = total_df[(total_df['BLDG_USG'] == '아파트')
                      & (total_df['month'].isin([2, 3]))]

    st.markdown("### 상관관계 분석을 위한 데이터 확인 \n"
                "- 건물면적과 물건금액의 상관관계를 확인합니다. \n"
                "- 먼저 추출된 데이터를 확인합니다.")

    # 필요한 컬럼 선택
    corr_df = apt_df[['CTRT_DAY', 'THING_AMT',
                      'ARCH_AREA', 'CGG_NM', 'month']].reset_index(drop=True)
    st.dataframe(corr_df.head())

    st.markdown("### 상관관계 분석 시각화 \n"
                "- 상관관계 데이터 시각화를 진행합니다.")

    # 산점도 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='ARCH_AREA', y='THING_AMT', data=corr_df, ax=ax)
    st.pyplot(fig)

    st.markdown("### 상관관계 계수 및 검정 \n"
                "- 계수를 확인합니다.")

    # 상관계수 계산
    corr_coef = pg.corr(corr_df['ARCH_AREA'], corr_df['THING_AMT']).round(3)
    st.dataframe(corr_coef, use_container_width=True)

    st.markdown(f"- 상관계수는 **{corr_coef['r'].values[0]}**이며, 건물면적이 증가할 "
                "때마다 물건금액도 같이 증가하는 경향성을 확인할 수 있습니다. \n"
                "- 각 자치구별로 상관관계를 시각화하고 상관계수를 비교해봅니다.")

    # 자치구 및 월 선택
    selected_cgg_nm = st.sidebar.selectbox("자치구명", sorted(corr_df['CGG_NM'].unique()))
    selected_month = st.sidebar.selectbox("월", sorted(corr_df['month'].unique()))

    st.markdown(f"### 서울시 {selected_cgg_nm} {selected_month}월 아파트 가격 ~ 건물면적 상관관계 분석 \n"
                "- 각 자치구 및 월별 시각화와 상관계수를 확인합니다.")

    # 선택한 자치구 및 월 필터링
    cgg_df = corr_df[(corr_df['CGG_NM'] == selected_cgg_nm) & (corr_df['month'] == selected_month)]

    # 자치구별 상관계수 계산
    cgg_corr_coef = pg.corr(cgg_df['ARCH_AREA'], cgg_df['THING_AMT'])
    st.dataframe(cgg_corr_coef, use_container_width=True)

    # 자치구별 상관관계 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='ARCH_AREA', y='THING_AMT', data=cgg_df, ax=ax)
    ax.text(0.95, 0.05, f'Pearson Correlation: {cgg_corr_coef["r"].values[0]:.2f}',
            transform=ax.transAxes, ha='right', fontsize=12)
    ax.set_title(f'{selected_cgg_nm} 피어슨 상관계수')
    st.pyplot(fig)

    st.markdown("### 거래건수 및 아파트 가격 상관관계")

    # 날짜별 평균 가격 및 거래건수 계산
    mean_size = cgg_df.groupby('CTRT_DAY')['THING_AMT'].agg(["mean", "size"]).reset_index()

    # 거래건수와 평균 가격의 상관계수 계산
    corr_coef_df = pg.corr(mean_size['size'], mean_size['mean'])
    st.dataframe(corr_coef_df, use_container_width=True)

    # 거래건수와 평균 가격의 산점도 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='size', y='mean', data=mean_size, ax=ax)
    ax.text(0.95, 0.05, f'Pearson Correlation: {corr_coef_df["r"].values[0]:.2f}',
            transform=ax.transAxes, ha='right', fontsize=12)
    ax.set_title(f'{selected_cgg_nm} 상관관계')
    ax.set_xlabel("거래건수")
    ax.set_ylabel("아파트 평균 가격")
    st.pyplot(fig)


def regRession(total_df):
    total_df['month'] = total_df['CTRT_DAY'].dt.month

    # 아파트 데이터 필터링 (2월과 3월 데이터)
    apt_df = total_df[(total_df['BLDG_USG'] == '아파트') & (total_df['month'].isin([2, 3]))]

    # 필요한 컬럼 선택
    corr_df = apt_df[['CTRT_DAY', 'THING_AMT',
                      'ARCH_AREA', 'CGG_NM', 'month']].reset_index(drop=True)

    # 자치구 및 월 선택
    selected_cgg_nm = st.sidebar.selectbox("자치구명", sorted(corr_df['CGG_NM'].unique()))
    selected_month = st.sidebar.selectbox("월", sorted(corr_df['month'].unique()))

    # 선택한 자치구 및 월 필터링
    reg_df = corr_df[(corr_df['CGG_NM'] == selected_cgg_nm)
                     & (corr_df['month'] == selected_month)]

    st.markdown("### 데이터 확인")
    st.dataframe(reg_df, use_container_width=True)

    # 회귀 분석
    st.markdown("### 건물면적과 아파트 가격 회귀분석 \n"
                "- 통계의 가정들이 맞는지 확인해보겠습니다. \n"
                "#### 정규성 검정 \n"
                "- 먼저 시각적으로 확인하고, 잔차의 정규성을 검정합니다.")

    # 회귀분석 수행
    model = pg.linear_regression(reg_df['ARCH_AREA'], reg_df['THING_AMT'])

    # 잔차 추출
    residuals = model.residuals_
    residuals = pd.DataFrame(residuals, columns=['Residuals'])

    # 잔차 히스토그램
    fig = px.histogram(residuals, x='Residuals')
    st.plotly_chart(fig)

    # 정규성 검정
    sw = pg.normality(residuals, method="shapiro")
    st.dataframe(sw, use_container_width=True)

    st.markdown("- 자치구에 따라 통계적으로 유의한 경우도 있고 그렇지 않은 경우도 있습니다. \n"
                "- 만약 p-value가 0.05보다 매우 작다면, "
                "잔차의 정규성이 위배되었으므로 일반적인 회귀 해석이 어렵습니다. \n"
                "- 이 경우, 극단적인 이상치를 제거하는 과정이 필요할 수 있습니다.")

    # 회귀 모델 결과 확인
    st.markdown("#### 회귀모형 확인 \n"
                "- 결정계수 $R^2$와 p-value를 확인합니다.")

    st.dataframe(model.round(2), use_container_width=True)

    intercept, slope = model['coef'].values[0], model['coef'].values[1]
    st.write("상수(Intercept):", intercept, "기울기(Slope):", slope)

    # 회귀선 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.linspace(0, reg_df['ARCH_AREA'].max())
    sns.scatterplot(data=reg_df, x='ARCH_AREA', y='THING_AMT', ax=ax)
    ax.set_title("The best-fitting regression line")
    ax.set_xlabel("건물면적")
    ax.set_ylabel("아파트 거래가격 (만원)")
    ax.plot(x, slope * x + intercept)

    # 회귀식 출력
    if intercept < 0:
        equation_line = (f'$Y = {slope:.1f}X {intercept:.1f}, '
                         f'R^2 = {np.round(model["adj_r2"].values[0], 3)}$')
    else:
        equation_line = (f'$Y = {slope:.1f}X + {intercept:.1f}, '
                         f'R^2 = {np.round(model["adj_r2"].values[0], 3)}$')

    ax.text(0.95, 0.05, equation_line, transform=ax.transAxes, ha='right', fontsize=12)
    st.pyplot(fig)








