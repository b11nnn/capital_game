import streamlit as st
import time

# ==========================================
# 1. Page Configuration & Custom CSS (밝은 한지 테마 & 먹색 글씨)
# ==========================================
st.set_page_config(page_title="캐피탈 조선", page_icon="🏯", layout="centered")

# Custom CSS for Joseon Theme (Light & Clear)
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');

html, body, [class*="stMarkdown"] {
    font-family: 'Noto Serif KR', serif;
    font-size: 1.05rem !important;
    color: #1c1c1c; /* 먹색 (깊은 검은색) */
}

/* Base background configuration (한지 느낌) */
.main {
    background-color: #fdfcf5; /* 밝은 크림색/한지색 */
}

.main-game-page-container {
    padding: 30px;
    background-color: #f5f0e1; /* 약간 더 짙은 한지색 */
    background-image: linear-gradient(0deg, transparent 24%, rgba(0, 0, 0, .03) 25%, rgba(0, 0, 0, .03) 26%, transparent 27%, transparent 74%, rgba(0, 0, 0, .03) 75%, rgba(0, 0, 0, .03) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 0, 0, .03) 25%, rgba(0, 0, 0, .03) 26%, transparent 27%, transparent 74%, rgba(0, 0, 0, .03) 75%, rgba(0, 0, 0, .03) 76%, transparent 77%, transparent);
    background-size: 50px 50px;
    border-radius: 15px;
    border: 2px solid #8c6c3e; /* 짙은 청동/금색 테두리 */
}

.main-game-title h1 {
    font-size: 3.0em !important;
    font-weight: bold !important;
    color: #8c6c3e !important; /* 짙은 청동색 */
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    margin-bottom: 15px !important;
}
.main-game-desc p {
    font-size: 1.4em !important;
    color: #333 !important; /* 짙은 회색 */
}
.main-subheader h2 {
    font-size: 2.2em !important;
    color: #1c1c1c !important; /* 먹색 */
    margin-top: 35px !important;
    border-bottom: 2px solid #8c6c3e;
    padding-bottom: 10px;
}

/* Metric Cards styled like Joseon scrolls */
.game-metric-card-styled {
    background-color: white; /* 순백색 종이 */
    padding: 25px;
    border-radius: 10px;
    box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 25px;
    border: 1px solid #ddd;
    color: #1c1c1c !important; /* 먹색 */
}
.game-metric-card-styled h3 {
    font-size: 1.4em;
    margin-top: 0;
    margin-bottom: 12px;
    color: #8c6c3e;
}
.game-metric-card-styled p {
    font-size: 2.5em;
    font-weight: bold;
    color: #1c1c1c; /* 먹색 */
    margin: 0;
}
.game-metric-card-styled .caption-styled {
    font-size: 1.2em;
    color: #555;
    margin-top: 12px;
    font-style: italic;
}

/* Lord Message Box (King's Command tone) */
.lord-msg-styled {
    font-size: 1.5em !important;
    font-weight: bold !important;
    padding: 25px;
    border-radius: 10px;
    margin-top: 25px;
    margin-bottom: 25px;
    border: 2px solid;
    color: #1c1c1c !important; /* 먹색 */
}
.stMarkdown .stCaption {
    font-size: 1.1rem !important;
    color: #555 !important; /* 짙은 회색 */
}

/* Result Message Styled boxes */
.result-msg-styled {
    font-size: 1.5em;
    font-weight: bold;
    padding: 25px;
    border-radius: 10px;
    margin-top: 25px;
    margin-bottom: 25px;
    color: #1c1c1c !important; /* 먹색 */
}

/* Deployment Area styling */
.asset-deploy-card-styled {
    background-color: white; /* 순백색 */
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}
.asset-deploy-card-styled label {
    font-size: 1.4em !important;
    color: #8c6c3e !important; /* 짙은 청동색 */
}

/* Result chat styling */
.stChat .chat-message-styled {
    font-size: 1.3em !important;
    padding: 25px;
    background-color: white;
    color: #1c1c1c;
    border-radius: 10px;
    border-left: 5px solid #8c6c3e;
    margin-bottom: 25px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}

/* Streamlit specific elements overrides */
.stMetric {
    font-size: 1.3rem !important;
}
.stMetric div[data-testid="stMetricValue"] {
    color: #1c1c1c !important; /* 먹색 */
}
.stNumberInput label {
    font-size: 1.3rem !important;
}
.stWarning {
    font-size: 1.2rem !important;
    background-color: #fff3cd; /* 경고 노랑 */
    color: #856404;
}
.stSelectbox label {
    font-size: 1.2rem !important;
}
.stButton button {
    font-size: 1.3rem !important;
    background-color: #8c6c3e !important; /* 짙은 청동색 */
    color: white !important; /* 버튼 글씨는 흰색 */
    font-weight: bold !important;
    border: none !important;
    padding: 10px 24px !important;
}
.stButton button:hover {
    background-color: #a6814c !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Define Regime Data (Joseon Theme Verbatim from Table)
REGIMES = {
    "개국 초창": {
        "emoji": "🏗️", 
        "title": "개국 초창 (開國 草創)",
        "lord_msg": "전란의 불길이 걷히고 가라앉은 대지를 다지고 있습니다. 이제 무너진 성벽을 다시 쌓고 영토를 다질 시간입니다.",
        "hint": "VIX: 하락 안정화 | 금리: 저금리 유지",
        "color": "#e2e6ea" # neutral grey-white
    },
    "태평성대": {
        "emoji": "☀️", 
        "title": "태평성대 (太平聖代)",
        "lord_msg": "백성들이 평안하며 시전엔 활기가 넘칩니다! 전하의 친위대를 움직여 영토를 넓히기에 가장 좋은 시기입니다.",
        "hint": "VIX: 매우 낮음 (평온) | 환율: 안정적",
        "color": "#e2e6ea" # neutral
    },
    "조정의 분열": {
        "emoji": "🐀", 
        "title": "조정의 분열 (朝廷의 分裂)",
        "lord_msg": "성 안에서 흉흉한 소문이 들려요. 맑은 하늘인데 갑자기 쥐떼가 나타난 것처럼, 무언가 심상치 않네요.",
        "hint": "금리: 가파른 상승 | VIX: 서서히 꿈틀거림",
        "color": "#fff3cd" # warning yellow
    },
    "전란의 위기": {
        "emoji": "⚔️", 
        "title": "전란의 위기 (戰亂의 危機)",
        "lord_msg": "결국 겨울이 왔습니다! 오랑캐들이 국경을 넘고 있습니다! 무리한 공격(주식)을 멈추고 영지의 자산을 지하 금고로 대피시키십시오!",
        "hint": "VIX: 폭발적 상승 (피크) | 환율: 급등 (압박)",
        "color": "#f8d7da" # error red
    },
    "전후 중흥": {
        "emoji": "⚒️", 
        "title": "전후 중흥 (戰後 中興)",
        "lord_msg": "폭풍이 휩쓸고 간 폐허 속에서 주인 없는 보물들이 발견됩니다. 가장 용감한 영주만이 이 기회를 잡을 것입니다.",
        "hint": "달러: 힘이 빠지기 시작 | VIX: 높은 곳에서 하락 시작",
        "color": "#d4edda" # success green
    }
}

st.markdown('<div class="main-game-page-container">', unsafe_allow_html=True)

# ==========================================
# 2. Main Title Area (Styled for Capital Joseon)
# ==========================================
st.markdown('<div class="main-game-title"><h1>🏯 주식 조선: 왕의 선택</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="main-game-desc"><p>HMM 도승지(AI)가 살핀 국면을 읽고, 전하의 전략으로 좌의정 AI와 수익 대결을 펼치세요!</p></div>', unsafe_allow_html=True)

st.markdown('<hr style="border: 1px solid #8c6c3e; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)

# ==========================================
# 3. Time Machine Selection Area (Historical Records)
# ==========================================
st.markdown('<div class="main-subheader"><h2>📜 역사의 기록</h2></div>', unsafe_allow_html=True)
stage_choice = st.selectbox(
    "조선의 운명을 결정했던 과거의 기록으로 이동합니다.",
    ["[선택] 이동할 연도를 고르세요", "2020년 3월 (역병의 창궐)", "2021년 11월 (풍요의 시대)", "2022년 9월 (세금 인상기)"]
)

# Indicator & Simulation Logic (Keep previous logic, only naming changed)
if stage_choice == "2020년 3월 (역병의 창궐)":
    current_regime = "전란의 위기"
    vix, rate, dollar, ex_rate = 65.0, "0.2%", 102.5, "1,280원"
    yields = {'stock': -45.0, 'bond': 5.0, 'gold': 15.0}
    ai_alloc = {'stock': 10, 'bond': 40, 'gold': 50}
elif stage_choice == "2021년 11월 (풍요의 시대)":
    current_regime = "태평성대"
    vix, rate, dollar, ex_rate = 15.2, "0.1%", 95.0, "1,180원"
    yields = {'stock': 25.0, 'bond': -2.0, 'gold': -5.0}
    ai_alloc = {'stock': 80, 'bond': 20, 'gold': 0}
elif stage_choice == "2022년 9월 (세금 인상기)":
    current_regime = "조정의 분열"
    vix, rate, dollar, ex_rate = 28.5, "3.5%", 110.2, "1,420원"
    yields = {'stock': -15.0, 'bond': -10.0, 'gold': 8.0}
    ai_alloc = {'stock': 20, 'bond': 30, 'gold': 50}
else:
    st.info("시대를 선택하시면 도승지가 정세 보고서를 올립니다.")
    st.stop()

# ==========================================
# 4. Market weather Indicators (Joseon Scrolls)
# ==========================================
st.markdown('<div class="main-subheader"><h2>📡 도승지의 정세 보고서</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    cap_vix = "🚨 민심이 극도로 흉흉합니다! 백성들이 시장을 떠나 피난을 가고 있습니다." if vix > 30 else "✅ 평온합니다. 백성들이 도성 안에서 안심하고 생업에 종사하고 있습니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>😱 민심의 동요 (VIX)</h3>
        <p>{vix}</p>
        <div class="caption-styled">{cap_vix}</div>
    </div>
    """, unsafe_allow_html=True)
    
    cap_rate = "🚨 조정의 세금 부담이 가중되고 있습니다. 상인들이 빚을 내기 힘들어져 영지의 활기가 사라졌습니다." if "3" in rate or "4" in rate else "✅ 세금 부담이 낮아 돈이 흔합니다. 새로운 전각을 올리기 좋은 시기입니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>💧 세금 부담 (금리)</h3>
        <p>{rate}</p>
        <div class="caption-styled">{cap_rate}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    cap_dollar = "🚨 대국의 힘이 너무 강하여, 우리 영지의 돈과 인재들이 그쪽으로 다 빨려가고 있습니다!" if dollar > 105 else "✅ 대국의 위세가 적당하여 우리 조선도 독자적인 힘을 기를 만합니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>👑 대국의 위세 (달러)</h3>
        <p>{dollar}</p>
        <div class="caption-styled">{cap_dollar}</div>
    </div>
    """, unsafe_allow_html=True)
    
    cap_ex_rate = "🚨 국경 지대의 긴장이 극에 달했습니다. 외국 용병들이 우리 영지를 떠날 수도 있습니다!" if ex_rate >= "1,300원" else "✅ 외부의 압박이 적어 국경이 안정적입니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>🛡️ 국경 긴장도 (환율)</h3>
        <p>{ex_rate}</p>
        <div class="caption-styled">{cap_ex_rate}</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. HMM regime Result (Joseon-style Message Box)
# ==========================================
st.markdown('<hr style="border: 1px solid #8c6c3e; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)
regime_data = REGIMES[current_regime]

# 컬러별 메시지 박스 테두리 색상 조정
border_color = regime_data['color'] if regime_data['color'] != '#e2e6ea' else '#8c6c3e'
if regime_data['color'] == '#f8d7da': # error red
     border_color = '#721c24'
elif regime_data['color'] == '#fff3cd': # warning yellow
     border_color = '#856404'
elif regime_data['color'] == '#d4edda': # success green
     border_color = '#155724'

st.markdown(f"""
<div class="main-subheader"><h2>🔮 정세 판독: 현재는 『{regime_data['emoji']} {regime_data['title']}』 국면입니다.</h2></div>
<div class="lord-msg-styled" style="background-color: {regime_data['color']}; border-color: {border_color};">
    <p>전하! {regime_data['lord_msg']}</p>
</div>
<div class="stMarkdown"><caption class="stCaption">💡 도승지의 조언: {regime_data['hint']}</caption></div>
""", unsafe_allow_html=True)

# ==========================================
# 6. Troop Deployment Inputs (Joseon Military)
# ==========================================
st.markdown('<hr style="border: 1px solid #8c6c3e; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)
st.markdown('<div class="main-subheader"><h2>⚔️ 군사 및 자원 배치 (자산 배분)</h2></div>', unsafe_allow_html=True)
st.markdown('<div class="main-game-desc"><p>주상 전하, 보고를 바탕으로 조선의 자원(100%)을 어떻게 분배하시겠습니까? 좌의정 AI도 배치를 마쳤습니다.</p></div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown('<div class="asset-deploy-card-styled">🏇 친위 기병대 (주식/SPY)</div>', unsafe_allow_html=True)
    stock_w = st.number_input("", min_value=0, max_value=100, value=50, key="stock_input", help="가장 공격적이지만 전란 시 피해를 입기 쉽습니다.")
with col_s2:
    st.markdown('<div class="asset-deploy-card-styled">🛡️ 수비 포졸 (채권/TLT)</div>', unsafe_allow_html=True)
    bond_w = st.number_input("", min_value=0, max_value=100, value=30, key="bond_input", help="적당한 수비력을 제공합니다.")
with col_s3:
    st.markdown('<div class="asset-deploy-card-styled">💰 지하 금고 (금/GLD)</div>', unsafe_allow_html=True)
    gold_w = st.number_input("", min_value=0, max_value=100, value=20, key="gold_input", help="위기 시 가장 안전한 비상 군자금입니다.")

total_w = stock_w + bond_w + gold_w

st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
if total_w != 100:
    st.markdown(f"""
    <div class="stWarning">현재 총 자원 배분이 {total_w}%입니다. 정확히 100%로 맞춰 주십시오!</div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if total_w == 100:
    start_battle = st.button("🚀 결정 완료! (결과 확인)")
    
    # ==========================================
    # 7. Results Section (Joseon vs 좌의정 AI)
    # ==========================================
    if start_battle:
        with st.spinner("3개월의 시간이 흐르고 있습니다..."):
            time.sleep(2)

            # Calculate returns based on simulated yields
            user_return = (stock_w * yields['stock'] + bond_w * yields['bond'] + gold_w * yields['gold']) / 100
            ai_return = (ai_alloc['stock'] * yields['stock'] + ai_alloc['bond'] * yields['bond'] + ai_alloc['gold'] * yields['gold']) / 100

            st.markdown('<hr style="border: 1px solid #8c6c3e; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)
            st.markdown('<div class="main-subheader"><h2>📊 전세 보고서: 주상 전하 vs 좌의정 AI</h2></div>', unsafe_allow_html=True)
            
            # Show Returns Side by Side (Joseon style Metrics)
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("👤 주상 전하의 성과", f"{user_return:.1f}%")
                st.caption(f"기병대 {stock_w}% / 수비병 {bond_w}% / 금고 {gold_w}%")
            with col_res2:
                st.metric("🤖 좌의정 AI의 성과", f"{ai_return:.1f}%")
                st.caption(f"기병대 {ai_alloc['stock']}% / 수비병 {ai_alloc['bond']}% / 금고 {ai_alloc['gold']}%")

            # Determine Winner (Joseon DRAMA feedback)
            if user_return > ai_return:
                st.markdown(f"""
                <div class="result-msg-styled" style="background-color: #d4edda; color: #155724;">
                    🎉 성군이시여! 주상 전하의 승리입니다. 전하의 혜안으로 조선의 국고가 풍족해졌습니다!
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            elif user_return < ai_return:
                st.markdown(f"""
                <div class="result-msg-styled" style="background-color: #f8d7da; color: #721c24;">
                    💥 좌의정 AI의 승리입니다. 전하, 다음에는 조금 더 신중한 결단을 내리셔야 하옵니다.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-msg-styled" style="background-color: #e2e6ea; color: #2c3e50;">
                    🤝 비겼습니다! 좌의정 AI도 전하의 깊은 뜻을 따라 무난한 전략을 세웠습니다.
                </div>
                """, unsafe_allow_html=True)

            # AI chat feedback (Joseon Advisor Persona)
            if current_regime == "전란의 위기":
                ai_msg = "저는 PPO 알고리즘을 통해 수만 번의 과거 침공 데이터를 학습했습니다. 그 결과, 민심이 극도로 흉흉할 때는 친위 기병대(주식)를 최소화하고 지하 금고(금)에 비상 군자금을 비축하는 것이 생존 확률을 가장 높인다는 것을 알아냈죠."
            elif current_regime == "태평성대":
                ai_msg = "태평성대에는 방어막을 거두고 최대한의 병력을 내보내 세금을 걷어야 합니다. 저는 이 국면에서 친위 기병대의 비중을 80%까지 끌어올리는 공격적인 전략을 선택했습니다."
            else:
                ai_msg = "조정의 정세가 불안할 때는 어느 한쪽에 전력을 집중하기보다 위험을 분산하는 것이 중요합니다. 제 알고리즘은 극단적인 선택보다는 균형을 택했습니다."

            st.markdown('<h3>좌의정 AI의 회고</h3>', unsafe_allow_html=True)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f'<div class="chat-message-styled">좌의정 AI: {ai_msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Close main container div