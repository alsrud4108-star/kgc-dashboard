import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="KGC 브랜드전략실 - 대시보드", layout="wide")

# --- [데이터 로드 섹션] ---
# 사용자님의 시트 ID와 각 탭의 gid 번호입니다.
SHEET_ID = "148Xv8z4aPfOZaQgWV40jOSNFPfsBKbCC857J8-4tqkk"

KPI_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
REGION_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1330935199"
AGE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=547463562"

@st.cache_data(ttl=60)  # 1분간 캐시 유지
def load_data(url):
    return pd.read_csv(url)

try:
    # 1. KPI 데이터 로드 (A7 셀의 요약 내용이 포함된 시트)
    df_kpi_raw = load_data(KPI_URL)
    
    # 2. 기타 차트 데이터 로드
    df_region = load_data(REGION_URL)
    df_age = load_data(AGE_URL)

    # 💡 [핵심 수정] A7 셀의 요약 내용 추출하기
    # 판다스에서 첫 행은 헤더로 처리되므로:
    # Row 2 = index 0, Row 3 = index 1 ... Row 7(A7) = index 5 입니다.
    # 열(column)은 첫 번째인 A열(index 0)을 선택합니다.
    ai_summary = df_kpi_raw.iloc[5, 0] if len(df_kpi_raw) >= 6 else "요약 데이터를 생성 중입니다..."

    # 3. KPI 카드용 데이터만 분리 (1행~4행까지의 데이터만 사용)
    df_kpi = df_kpi_raw.head(4)

except Exception as e:
    st.error(f"⚠️ 데이터를 불러올 수 없습니다. 시트 설정을 확인해주세요. ({e})")
    st.stop()
# -----------------------

# 2. 커스텀 CSS
st.markdown("""
    <style>
    .kpi-value { font-size: 28px; font-weight: bold; color: #A6192E; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더 영역
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("📈 에브리타임 밸런스 마케팅 대시보드")
    st.markdown("**2026년 3월 4주차 | 리뉴얼 제품 판매 현황 분석**")
with col_header2:
    st.write("") 
    st.info("👤 **팀장: 인선미** (Brand Strategy)")

st.markdown("---")

# 4. KPI 카드 영역 (상위 4개 지표만 표시)
kpi_cols = st.columns(len(df_kpi))
for i, col in enumerate(kpi_cols):
    d_color = "off" if i in [1, 3] else "normal"
    col.metric(
        label=df_kpi.iloc[i]['label'], 
        value=df_kpi.iloc[i]['value'], 
        delta=df_kpi.iloc[i]['delta'],
        delta_color=d_color
    )

st.markdown("<br>", unsafe_allow_html=True)

# 5. 차트 영역
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("지역별 판매 성장률 (%)")
    fig_region = px.bar(
        df_region, x="지역", y="성장률", text="성장률", 
        color="지역", color_discrete_sequence=['#A6192E', '#94a3b8']
    )
    fig_region.update_layout(showlegend=False, margin=dict(t=20, b=20, l=0, r=0))
    st.plotly_chart(fig_region, use_container_width=True)

with chart_col2:
    st.subheader("소비자 연령대 분포")
    fig_age = px.pie(
        df_age, values="비중", names="연령대", hole=0.5,
        color_discrete_sequence=['#A6192E', '#C5A059', '#cbd5e1']
    )
    fig_age.update_layout(margin=dict(t=20, b=20, l=0, r=0), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_age, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. 피드백 및 인사이트
bottom_col1, bottom_col2 = st.columns([2, 1])
with bottom_col1:
    st.subheader("💬 실시간 고객 VOC 분석")
    voc1, voc2 = st.columns(2)
    with voc1:
        st.success("**🟢 Positive**\n\n- 포장이 세련되어 선물용으로 최고입니다.\n- 기존 홍삼보다 쓴맛이 덜해서 먹기 편해요.")
    with voc2:
        st.error("**🔴 Improvement**\n\n- 리뉴얼 후 가격이 조금 오른 것 같아요.\n- **박스 개봉 시 가끔 뻑뻑함이 느껴집니다.**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 팀장 전략 제언 (Action Items)")
    st.info("""
    1. **아웃도어 마케팅:** 테니스/등산 커뮤니티 연계 '오운완' 캠페인 즉시 실행
    2. **채널 최적화:** 지방권 대형마트 '가족 건강 키트' 번들 기획 구성
    3. **품질 개선:** 패키지 개봉 편의성(Easy-off) 관련 생산 파트 피드백 전달
    """)

with bottom_col2:
    st.subheader("🔥 트렌드 키워드")
    st.markdown("`#사회초년생` `#테니스` `#오운완` `#선물추천` `#등산` `#에너지부스터`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📌 Today's Summary")
    # 💡 [결과 반영] 구글 시트 A7 셀의 AI 요약 내용을 표시합니다.
    st.info(ai_summary)
    st.caption("※ 구글 시트의 마케팅 데이터를 Gemini AI가 실시간 분석한 결과입니다.")
