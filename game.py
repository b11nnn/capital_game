import streamlit as st
import time

# ==========================================
# 1. Page Configuration & Custom CSS 
# ==========================================
st.set_page_config(page_title="나만의 주식 제국", page_icon="🏰", layout="centered")

# Custom CSS
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;700&display=swap');

html, body, [class*="stMarkdown"] {
    font-family: 'Roboto Serif', serif;
    font-size: 1.05rem !important;
    color: #333;
}

.main-game-page-container {
    padding: 30px;
    background-color: #f7f7f7;
    background-image: linear-gradient(0deg, transparent 24%, rgba(200, 200, 200, .1) 25%, rgba(200, 200, 200, .1) 26%, transparent 27%, transparent 74%, rgba(200, 200, 200, .1) 75%, rgba(200, 200, 200, .1) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(200, 200, 200, .1) 25%, rgba(200, 200, 200, .1) 26%, transparent 27%, transparent 74%, rgba(200, 200, 200, .1) 75%, rgba(200, 200, 200, .1) 76%, transparent 77%, transparent);
    background-size: 50px 50px;
    border-radius: 15px;
}

.main-game-title h1 {
    font-size: 2.8em !important;
    font-weight: bold !important;
    color: #2c3e50 !important;
    margin-bottom: 10px !important;
}
.main-game-desc p {
    font-size: 1.3em !important;
    color: #555 !important;
}
.main-subheader h2 {
    font-size: 2.0em !important;
    color: #333 !important;
    margin-top: 30px !important;
}

.game-metric-card-styled {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 25px;
    border: 1px solid #ddd;
}
.game-metric-card-styled h3 {
    font-size: 1.3em;
    margin-top: 0;
    margin-bottom: 10px;
    color: #444;
}
.game-metric-card-styled p {
    font-size: 2.2em;
    font-weight: bold;
    color: #2c3e50;
    margin: 0;
}
.game-metric-card-styled .caption-styled {
    font-size: 1.1em;
    color: #666;
    margin-top: 10px;
}

.lord-msg-styled {
    font-size: 1.4em !important;
    font-weight: bold !important;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    margin-bottom: 20px;
}
.stMarkdown .stCaption {
    font-size: 1.0rem !important;
    color: #777 !important;
}

.result-msg-styled {
    font-size: 1.4em;
    font-weight: bold;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.asset-deploy-card-styled {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    border: 1px solid #eee;
    margin-bottom: 15px;
}
.asset-deploy-card-styled label {
    font-size: 1.2em !important;
    color: #444 !important;
}

.stChat .chat-message-styled {
    font-size: 1.2em !important;
    padding: 20px;
    background-color: #e9ecef;
    border-radius: 12px;
    margin-bottom: 20px;
}

.stMetric {
    font-size: 1.2rem !important;
}
.stNumberInput label {
    font-size: 1.2rem !important;
}
.stWarning {
    font-size: 1.1rem !important;
}
.stSelectbox label {
    font-size: 1.1rem !important;
}
.stButton button {
    font-size: 1.2rem !important;
    padding: 8px 16px !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Define Regime Data
REGIMES = {
    "기초 공사": {
        "emoji": "🏗️", 
        "title": "기초 공사 (Accumulation)",
        "lord_msg": "폭풍이 지나간 자리를 다지고 있어요. 이제 튼튼한 성을 쌓을 준비를 할 시간입니다!",
        "hint": "VIX: 하락 안정화 | 금리: 저금리 유지",
        "color": "#e2e6ea" 
    },
    "평화로운 번영": {
        "emoji": "☀️", 
        "title": "평화로운 번영 (Expansion)",
        "lord_msg": "세금이 쑥쑥 걷히고 백성들이 행복해요! 성을 높이 올리고 영토를 넓히기에 가장 좋은 날입니다.",
        "hint": "VIX: 매우 낮음 (평온) | 환율: 안정적",
        "color": "#e2e6ea" 
    },
    "전염병의 전조": {
        "emoji": "🐀", 
        "title": "전염병의 전조 (Warning)",
        "lord_msg": "성 안에서 흉흉한 소문이 들려요. 맑은 하늘인데 갑자기 쥐떼가 나타난 것처럼, 무언가 심상치 않네요.",
        "hint": "금리: 가파른 상승 | VIX: 서서히 꿈틀거림",
        "color": "#fff3cd" 
    },
    "옆 나라의 습격": {
        "emoji": "👾", 
        "title": "옆 나라의 습격 (Crisis)",
        "lord_msg": "성벽이 무너지고 있습니다! 공격보다는 생존입니다. 지금 당장 방어 타워(금/현금)를 세우세요!",
        "hint": "VIX: 폭발적 상승 (피크) | 환율: 급등 (압박)",
        "color": "#f8d7da" 
    },
    "재건의 시간": {
        "emoji": "🛠️", 
        "title": "재건의 시간 (Bottoming)",
        "lord_msg": "몬스터들이 물러갔습니다. 폐허 속에서 보물을 찾을 시간이에요. 더 크고 멋진 성을 계획해 볼까요?",
        "hint": "달러: 힘이 빠지기 시작 | VIX: 높은 곳에서 하락 시작",
        "color": "#d4edda" 
    }
}

st.markdown('<div class="main-game-page-container">', unsafe_allow_html=True)

# ==========================================
# 2. Main Title Area 
# ==========================================
st.markdown('<div class="main-game-title"><h1>🏰 나만의 주식 제국 🏰</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="main-game-desc"><p>HMM 예언자(AI)가 알려주는 지표를 읽고, 자산을 배치해 PPO 고문관과 대결하세요!</p></div>', unsafe_allow_html=True)

st.markdown('<hr style="border: 1px solid #ccc; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)

# ==========================================
# 3. Time Machine Selection Area 
# ==========================================
st.markdown('<div class="main-subheader"><h2>📜 타임머신</h2></div>', unsafe_allow_html=True)
stage_choice = st.selectbox(
    "과거의 중대한 사건으로 이동합니다.",
    ["[선택] 이동할 시대를 고르세요", "2020년 3월 (코로나 팬데믹)", "2021년 11월 (저금리 호황)", "2022년 9월 (금리 인상기)"]
)

# Indicator & Simulation Logic
if stage_choice == "2020년 3월 (코로나 팬데믹)":
    current_regime = "옆 나라의 습격"
    vix, rate, dollar, ex_rate = 65.0, "0.2%", 102.5, "1,280원"
    yields = {'stock': -45.0, 'bond': 5.0, 'gold': 15.0}
    ai_alloc = {'stock': 10, 'bond': 40, 'gold': 50}
elif stage_choice == "2021년 11월 (저금리 호황)":
    current_regime = "평화로운 번영"
    vix, rate, dollar, ex_rate = 15.2, "0.1%", 95.0, "1,180원"
    yields = {'stock': 25.0, 'bond': -2.0, 'gold': -5.0}
    ai_alloc = {'stock': 80, 'bond': 20, 'gold': 0}
elif stage_choice == "2022년 9월 (금리 인상기)":
    current_regime = "전염병의 전조"
    vix, rate, dollar, ex_rate = 28.5, "3.5%", 110.2, "1,420원"
    yields = {'stock': -15.0, 'bond': -10.0, 'gold': 8.0}
    ai_alloc = {'stock': 20, 'bond': 30, 'gold': 50}
else:
    st.info("시대를 선택하면 예언자의 보고서가 도착합니다.")
    st.stop()

# ==========================================
# 4. Market weather Indicators
# ==========================================
st.markdown('<div class="main-subheader"><h2>📡 예언자의 시장 지표 보고서</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    cap_vix = "🚨 사람들이 엄청나게 겁에 질려 있어요. 주식을 마구 팔고 도망가는 중이에요!" if vix > 30 else "✅ 평온합니다. 백성들이 시장에서 안심하고 장사를 하고 있어요."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>😱 공포지수 (VIX)</h3>
        <p>{vix}</p>
        <div class="caption-styled">{cap_vix}</div>
    </div>
    """, unsafe_allow_html=True)
    
    cap_rate = "🚨 시장에 돈이 마르고 있어요. 상인들이 돈 빌리기가 힘들어져서 활기가 없네요." if "3" in rate or "4" in rate else "✅ 금리가 낮아 돈이 흔합니다. 건물을 새로 올리기 좋은 시기입니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>💧 금리</h3>
        <p>{rate}</p>
        <div class="caption-styled">{cap_rate}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    cap_dollar = "🚨 중앙 제국의 힘이 너무 강해서, 우리 영지의 돈이 그쪽으로 다 빨려가고 있어요!" if dollar > 105 else "✅ 중앙 제국의 위세가 적당하여 우리 영지도 살 만합니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>👑 달러 인덱스</h3>
        <p>{dollar}</p>
        <div class="caption-styled">{cap_dollar}</div>
    </div>
    """, unsafe_allow_html=True)
    
    cap_ex_rate = "🚨 한국 경제가 강한 압박을 받고 있어요. 외국인 용병들이 우리 영지를 떠날 수도 있어요!" if ex_rate >= "1,300원" else "✅ 외부의 압박이 적어 국경이 안정적입니다."
    st.markdown(f"""
    <div class="game-metric-card-styled">
        <h3>🛡️ 환율</h3>
        <p>{ex_rate}</p>
        <div class="caption-styled">{cap_ex_rate}</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. HMM regime Result 
# ==========================================
st.markdown('<hr style="border: 1px solid #ccc; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)
regime_data = REGIMES[current_regime]

st.markdown(f"""
<div class="main-subheader"><h2>🔮 예언의 구슬: 현재는 『{regime_data['emoji']} {regime_data['title']}』 단계입니다.</h2></div>
<div class="lord-msg-styled" style="background-color: {regime_data['color']};">
    <p>영주님! {regime_data['lord_msg']}</p>
</div>
<div class="stMarkdown"><caption class="stCaption">💡 예언자의 힌트: {regime_data['hint']}</caption></div>
""", unsafe_allow_html=True)

# ==========================================
# 6. Troop Deployment Inputs
# ==========================================
st.markdown('<hr style="border: 1px solid #ccc; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)
st.markdown('<div class="main-subheader"><h2>⚔️ 병력 배치 (자산 배분)</h2></div>', unsafe_allow_html=True)
st.markdown('<div class="main-game-desc"><p>영주님, 예언을 바탕으로 100명의 병력을 어떻게 배치하시겠습니까? PPO 고문관도 배치를 마쳤습니다.</p></div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown('<div class="asset-deploy-card-styled">🏇 정규 기사단 (주식/SPY)</div>', unsafe_allow_html=True)
    stock_w = st.number_input("", min_value=0, max_value=100, value=50, key="stock_input")
with col_s2:
    st.markdown('<div class="asset-deploy-card-styled">🛡️ 수비 방패병 (채권/TLT)</div>', unsafe_allow_html=True)
    bond_w = st.number_input("", min_value=0, max_value=100, value=30, key="bond_input")
with col_s3:
    st.markdown('<div class="asset-deploy-card-styled">💰 지하 금고 (금/GLD)</div>', unsafe_allow_html=True)
    gold_w = st.number_input("", min_value=0, max_value=100, value=20, key="gold_input")

total_w = stock_w + bond_w + gold_w

st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
if total_w != 100:
    st.markdown(f"""
    <div class="stWarning">현재 총 병력이 {total_w}명입니다. 정확히 100명(100%)을 배치해 주세요!</div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if total_w == 100:
    start_battle = st.button("🚀 전투 시작! (결과 확인)")
    
    # ==========================================
    # 7. Results Section (Human vs PPO AI)
    # ==========================================
    if start_battle:
        with st.spinner("3개월의 시간이 흐르고 있습니다..."):
            time.sleep(2)

            # Calculate returns based on simulated yields
            user_return = (stock_w * yields['stock'] + bond_w * yields['bond'] + gold_w * yields['gold']) / 100
            ai_return = (ai_alloc['stock'] * yields['stock'] + ai_alloc['bond'] * yields['bond'] + ai_alloc['gold'] * yields['gold']) / 100

            st.markdown('<hr style="border: 1px solid #ccc; margin-top: 30px; margin-bottom: 30px;">', unsafe_allow_html=True)
            st.markdown('<div class="main-subheader"><h2>📊 전투 성적표: 영주 vs PPO 고문관</h2></div>', unsafe_allow_html=True)
            
            # Show Returns Side by Side
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("👤 영주님의 성과", f"{user_return:.1f}%")
                st.caption(f"주식 {stock_w}% / 채권 {bond_w}% / 금고 {gold_w}%")
            with col_res2:
                st.metric("🤖 PPO 고문관의 성과", f"{ai_return:.1f}%")
                st.caption(f"주식 {ai_alloc['stock']}% / 채권 {ai_alloc['bond']}% / 금고 {ai_alloc['gold']}%")

            # Determine Winner
            if user_return > ai_return:
                st.markdown(f"""
                <div class="result-msg-styled" style="background-color: #d4edda; color: #155724;">
                    🎉 영주님의 승리입니다! 기계보다 뛰어난 직관으로 영지를 번영시켰습니다!
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            elif user_return < ai_return:
                st.markdown(f"""
                <div class="result-msg-styled" style="background-color: #f8d7da; color: #721c24;">
                    💥 PPO 고문관의 승리입니다. AI의 냉철한 데이터 분석이 조금 더 정확했네요.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-msg-styled" style="background-color: #e2e6ea; color: #2c3e50;">
                    🤝 무승부입니다! 영주님과 PPO 고문관 모두 훌륭한 전략을 세웠습니다.
                </div>
                """, unsafe_allow_html=True)

            # AI chat feedback
            if current_regime == "옆 나라의 습격":
                ai_msg = "저는 PPO 알고리즘을 통해 수만 번의 과거 침공 데이터를 학습했습니다. 그 결과, 공포지수가 치솟을 때는 정규 기사단(주식)을 최소화하고 지하 금고(금)에 자산을 숨기는 것이 생존 확률을 가장 높인다는 것을 알아냈죠."
            elif current_regime == "평화로운 번영":
                ai_msg = "평화로운 시기에는 방어막을 거두고 최대한의 병력을 내보내 세금을 걷어야 합니다. 저는 이 국면에서 정규 기사단의 비중을 80%까지 끌어올리는 전략을 선택했습니다."
            else:
                ai_msg = "지표들이 엇갈릴 때는 어느 한쪽에 몰빵하기보다 위험을 분산하는 것이 중요합니다. 제 알고리즘은 극단적인 선택보다는 균형을 택했습니다."

            st.markdown('<h3>고문관의 조언</h3>', unsafe_allow_html=True)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f'<div class="chat-message-styled">PPO 고문관의 회고: {ai_msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
                