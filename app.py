import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# 1. 초기 설정 및 데이터 로드
st.set_page_config(page_title="공정 실시간 모니터링", layout="wide")
df_full = pd.read_csv('manufacturing_process_data.csv')

# 정상 데이터 기준 관리 한계선 설정 (UCL, LCL)
normal_mu = 10.02
normal_sigma = 0.80
ucl = normal_mu + 3 * normal_sigma
lcl = normal_mu - 3 * normal_sigma

st.title("🏭 실시간 제조 공정 관리 대시보드")

# 2. 대시보드 레이아웃 구성
col1, col2, col3 = st.columns(3)
kpi_rate = col1.empty()
kpi_count = col2.empty()
kpi_status = col3.empty()

chart_placeholder = st.empty()
alert_placeholder = st.container()

# 3. 실시간 루프 시작
if st.button('모니터링 시작'):
    display_df = pd.DataFrame()
    
    for i in range(len(df_full)):
        # 데이터가 하나씩 추가되는 시뮬레이션
        new_row = df_full.iloc[[i]]
        display_df = pd.concat([display_df, new_row]).iloc[-50:] # 최근 50개만 유지
        
        # 지표 계산
        current_val = new_row['Measurement'].values[0]
        total_defects = (display_df['Status_Label'] == 'Abnormal').sum()
        defect_rate = (total_defects / len(display_df)) * 100
        
        # 상단 지표 업데이트
        kpi_rate.metric("최근 불량률", f"{defect_rate:.1f}%")
        kpi_count.metric("현재 측정값", f"{current_val:.2f}")
        
        # 조기 경보 로직
        if current_val > ucl or current_val < lcl:
            kpi_status.error("⚠️ 이상 탐지")
            with alert_placeholder:
                st.warning(f"🚨 [Batch {new_row['Batch_ID'].values[0]}] 관리 한계 이탈 발생! 측정치: {current_val:.2f}")
        else:
            kpi_status.success("✅ 정상 작동 중")

        # 관리도 그래프 업데이트 (Plotly)
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=display_df['Measurement'], mode='lines+markers', name='측정치'))
        fig.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL")
        fig.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL")
        fig.add_hline(y=normal_mu, line_color="green", annotation_text="Target")
        
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        time.sleep(0.5) # 0.5초 간격으로 갱신
