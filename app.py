import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="KGC Insight - Everytime Balance",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# KGC 브랜드 아이덴티티를 위한 커스텀 CSS 적용
st.markdown("""
    <style>
    @import url('https://docs.google.com/spreadsheets/d/148Xv8z4aPfOZaQgWV40jOSNFPfsBKbCC857J8-4tqkk/edit?usp=sharing');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }
    
    .main {
        background-color: #F8FAFC;
    }
    
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #E63946;
    }
    
    .report-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 사이드바 구성
with st.sidebar:
    st.title("🔴 KGC Insight")
    st.markdown("---")
    st.selectbox("메뉴 선택", ["대시보드 홈", "판매 분석", "고객 통찰", "캠페인 현황"])
    
    st.info("""
    **팀장 Note:**
    리뉴얼 초기 지표가 매우 고무적입니다. 특히 편의점 채널의 2030 유입은 브랜드 영타겟팅 전략이 유효함을 증명합니다.
    """)
    
    st.markdown("---")
    st.caption("마지막 업데이트: 2026.03.31 09:00")

# 메인 헤더
st.title("🚀 Weekly Performance")
st.subheader("에브리타임 밸런스 리뉴얼 | 2026.03.W4")

# KPI 4개 컬럼 배치
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="수도권 성장률", value="+15.0%", delta="주간 최고", delta_color="normal")
with col2:
    st.metric(label="2030 타겟 비중", value="45.0%", delta="전략 타겟 집중", delta_color="off")
with col3:
    st.metric(label="스포츠 키워드", value="+30.0%", delta="TPO 확장중", delta_color="normal")
with col4:
    st.metric(label="제품 만족도", value="4.2 / 5", delta="-0.3 (UX 이슈)", delta_color="inverse")

st.markdown("---")

# 차트 레이아웃 구성
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### 📍 지역별 채널 성과 분석")
    fig_region = go.Figure(data=[
        go.Bar(
            x=['수도권 (편의점)', '지방 (대형마트)'],
            y=[15, -2],
            marker_color=['#E63946', '#1D3557'],
            text=['+15%', '-2%'],
            textposition='auto',
        )
    ])
    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_region, use_container_width=True)

with chart_col2:
    st.markdown("### 👥 구매 고객층 세부 구성")
    labels = ['2030 사회초년생', '4050 중장년층', '기타']
    values = [45, 40, 15]
    fig_age = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=['#E63946', '#457B9D', '#CBD5E1'])])
    fig_age.update_layout(
        showlegend=True,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_age, use_container_width=True)

detail_col1, detail_col2 = st.columns([1, 2])

with detail_col1:
    st.markdown("### ✨ 리뉴얼 제품 속성 평가")
    categories = ['디자인', '맛(쓴맛완화)', '가격 합리성', '개봉 편의성', '휴대성']
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[4.8, 4.5, 3.2, 2.8, 4.7],
        theta=categories,
        fill='toself',
        line_color='#E63946'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=False,
        height=300,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.warning("약점: 가격 및 개봉 편의성 보완 필요")

with detail_col2:
    st.markdown("### 🏕️ 취식 상황(TPO) 연관어 분석")
    tpo_data = pd.DataFrame({
        '키워드': ['오피스', '테니스', '등산', '골프', '피크닉', '선물'],
        '언급량': [50, 90, 85, 55, 65, 45],
        '성장세': [10, 40, 35, 15, 20, 5],
        '컬러': ['#CBD5E1', '#E63946', '#E63946', '#457B9D', '#457B9D', '#94A3B8']
    })
    fig_bubble = px.scatter(
        tpo_data, x="언급량", y="성장세",
        size="언급량", color="키워드",
        hover_name="키워드", size_max=60,
        color_discrete_sequence=['#E63946', '#457B9D', '#1D3557', '#CBD5E1', '#94A3B8', '#F4A261']
    )
    fig_bubble.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bubble, use_container_width=True)

# 실행 과제 테이블
st.markdown("---")
st.markdown("### 📋 차주 전략 실행 과제 (Action Items)")
action_data = {
    "전략 카테고리": ["MARKETING", "SALES", "QC/UX"],
    "세부 과제": [
        "등산/테니스 크루 샘플링 지원",
        "지방 대형마트 프로모션 재설계",
        "패키지 개봉 프로세스 정밀 점검"
    ],
    "우선순위": ["P1 (매우높음)", "P1 (높음)", "P2 (보통)"],
    "담당": ["브랜드팀", "영업본부", "생산팀"],
    "기한": ["04.05", "04.07", "04.10"]
}
st.table(pd.DataFrame(action_data))

st.markdown(
    "<br><hr><center style='color: #94A3B8; font-size: 0.8rem;'>"
    "&copy; 2026 KGC Ginseng Corp. Brand Strategy Internal Use Only."
    "</center>", 
    unsafe_allow_html=True
)
