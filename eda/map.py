# -*- coding:utf-8 -*-
import pandas as pd
import streamlit as st
import geopandas as gpd
import io
import json
import matplotlib.pyplot as plt
import plotly.express as px

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def mapMatplotlib(merge_df):
    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(15, 10))

    # 2월(변경된 값)
    merge_df[merge_df['month'] == 2].plot(ax=ax[0], column="mean", cmap="Pastel1", legend=False, alpha=0.9, edgecolor='gray')
    # 3월(변경된 값)
    merge_df[merge_df['month'] == 3].plot(ax=ax[1], column="mean", cmap="Pastel1", legend=False, alpha=0.9, edgecolor='gray')

    patch_col = ax[0].collections[0]
    cb = fig.colorbar(patch_col, ax=ax, shrink=0.5)

    # 2월 데이터 라벨링 (중복 방지)
    annotated_names = set()  # 이미 표기한 이름을 저장할 집합
    for i, row in merge_df[merge_df['month'] == 2].iterrows():
        if row['SIG_KOR_NM'] not in annotated_names:
            ax[0].annotate(row['SIG_KOR_NM'], xy=(row['lon'], row['lat']),
                           xytext=(-7, 2), textcoords="offset points", fontsize=8, color='black')
            annotated_names.add(row['SIG_KOR_NM'])  # 집합에 추가

    # 3월 데이터 라벨링 (중복 방지)
    annotated_names.clear()  # 새로운 월 데이터 표기를 위해 초기화
    for i, row in merge_df[merge_df['month'] == 3].iterrows():
        if row['SIG_KOR_NM'] not in annotated_names:
            ax[1].annotate(row['SIG_KOR_NM'], xy=(row['lon'], row['lat']),
                           xytext=(-7, 2), textcoords="offset points", fontsize=8, color='black')
            annotated_names.add(row['SIG_KOR_NM'])  # 집합에 추가

    ax[0].set_title('2025-2월 아파트 평균(만원)')
    ax[1].set_title('2025-3월 아파트 평균(만원)')
    ax[0].set_axis_off()
    ax[1].set_axis_off()

    st.pyplot(fig)

def showMap(total_df):
    st.markdown("### 병합 데이터 확인 \n- 컬럼명 확인")

    # 서울 행정구역 GeoJSON 파일 로드
    seoul_gpd = gpd.read_file("./data/seoul_sig.geojson")
    seoul_gpd = seoul_gpd.set_crs(epsg='5178', allow_override=True)
    seoul_gpd['center_point'] = seoul_gpd['geometry'].centroid
    seoul_gpd['geometry'] = seoul_gpd['geometry'].to_crs(epsg=4326)
    seoul_gpd['center_point'] = seoul_gpd['center_point'].to_crs(epsg=4326)
    seoul_gpd['lon'] = seoul_gpd['center_point'].map(lambda x: x.xy[0][0])
    seoul_gpd['lat'] = seoul_gpd['center_point'].map(lambda x: x.xy[1][0])
    seoul_gpd = seoul_gpd.rename(columns={"SIG_CD": "CGG_CD"})
    print(seoul_gpd.head())
    # 데이터 변환 및 컬럼명 변경
    total_df['month'] = total_df['CTRT_DAY'].dt.month
    total_df = total_df[(total_df['BLDG_USG'] == '아파트') & (total_df['month'].isin([2, 3]))]
    total_df = total_df[['CTRT_DAY', 'month', 'CGG_CD', 'CGG_NM', 'THING_AMT', 'BLDG_USG']].reset_index(drop=True)

    # 그룹화하여 요약 데이터 생성
    summary_df = total_df.groupby(['CGG_CD', 'month'])['THING_AMT'].agg(["mean", "std", "size"]).reset_index()
    summary_df['CGG_CD'] = summary_df['CGG_CD'].astype(str)

    # GeoDataFrame과 병합
    merge_df = seoul_gpd.merge(summary_df, on='CGG_CD')

    # 데이터 확인 출력
    buffer = io.StringIO()
    merge_df.info(buf=buffer)
    df_info = buffer.getvalue()
    st.text(df_info)

    st.markdown("### 일부 데이터만 확인")
    st.write(merge_df[['SIG_KOR_NM', 'geometry', 'mean']].head(3))
    st.markdown("<hr>", unsafe_allow_html=True)

    # 시각화 라이브러리 선택
    selected_lib = st.sidebar.radio("라이브러리 종류", ["Matplotlib", "Plotly"])

    if selected_lib == "Matplotlib":
        st.markdown("### Matplotlib 스타일")
        mapMatplotlib(merge_df)
    elif selected_lib == "Plotly":
        st.markdown("### Plotly 스타일")
        ## 직접 구현 해보기.
    else:
        pass



