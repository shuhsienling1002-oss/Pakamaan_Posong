import streamlit as st
import time

# ==========================================
# Layer 0: 頁面設定 (Mobile Config)
# ==========================================
st.set_page_config(
    page_title="三一返鄉",
    page_icon="🧨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# Layer 3.5: CSS 視覺強制層 (UI Injection)
# 這段代碼負責把「網頁」偽裝成「App」
# ==========================================
hide_streamlit_style = """
<style>
    /* 1. 隱藏 Streamlit 預設的上方白條與漢堡選單 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 2. 調整頂部邊距，讓內容往上滿版 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* 3. 強制按鈕變成圓角大按鈕 (類 iOS 風格) */
    .stButton > button {
        border-radius: 20px;
        height: 3em;
        font-weight: bold;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    
    /* 4. 卡片樣式優化 */
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 15px;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 初始化 Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1 & 2: 物理邏輯核心 (Physics Engine)
# ==========================================
class FPCRF_Strategy_Engine:
    def calculate_strategies(self, date_type, departure_hour, focus, destination):
        strategies = []
        is_peak = (date_type == "春節連假首日/除夕")
        traffic_entropy = self._get_traffic_entropy(departure_hour) if is_peak else 20
        is_taitung = (destination == "台東") 

        # 1. 火車
        success_rate_train = 10 if is_peak else 60
        strategies.append({
            "mode": "🚄 火車直達",
            "details": f"桃園 ➔ {destination}",
            "time_cost": "3.0hr" if not is_taitung else "4.5hr",
            "pain_index": 20,
            "success_rate": success_rate_train,
            "advice": "除夕搶票極難，建議多開視窗。",
            "tags": ["舒適", "難訂"]
        })

        # 2. 區間快
        strategies.append({
            "mode": "🚆 區間快 (始發站)",
            "details": f"樹林/南港(始發) ➔ {destination}",
            "time_cost": "4.5hr" if not is_taitung else "7.0hr",
            "pain_index": 70,
            "success_rate": 99,
            "advice": "不要在桃園等，回頭搭始發車。",
            "tags": ["保證有車", "累"]
        })

        # 3. 高鐵轉乘
        strategies.append({
            "mode": "🚅+🚄 高鐵轉乘",
            "details": "桃園HSR ➔ 台北 ➔ 東部幹線",
            "time_cost": "3.5hr",
            "pain_index": 30,
            "success_rate": success_rate_train + 5,
            "advice": "用高鐵跳過塞車段，準時抵達台北。",
            "tags": ["效率", "轉乘"]
        })

        # 4. 飛機
        strategies.append({
            "mode": "✈️ 飛機空運",
            "details": f"松山 ➔ {destination}",
            "time_cost": "2.5hr",
            "pain_index": 15,
            "success_rate": 5 if is_peak else 40,
            "advice": "除非有保留位，否則候補是大賭局。",
            "tags": ["豪賭"]
        })

        # 5. 南迴 (台東)
        if is_taitung:
            strategies.append({
                "mode": "🔄 高鐵南迴迂迴",
                "details": "桃園HSR ➔ 左營 ➔ 台東",
                "time_cost": "5.0hr",
                "pain_index": 25,
                "success_rate": 75,
                "advice": "台東人首選！避開蘇花改。",
                "tags": ["神招", "推薦"]
            })
        
        # 6. 開車
        base_time = 3.5 if not is_taitung else 6.0
        jam_factor = 1 + (traffic_entropy / 100) * 3
        strategies.append({
            "mode": "🚗 自行開車",
            "details": f"{departure_hour}:00 出發 (蘇花改)",
            "time_cost": f"{base_time * jam_factor:.1f}hr",
            "pain_index": min(30 + traffic_entropy, 100),
            "success_rate": 100,
            "advice": self._get_driving_advice(departure_hour, is_peak),
            "tags": ["自主", "塞車"]
        })

        # 7. 聯運
        strategies.append({
            "mode": "🚌+🚆 鐵公路聯運",
            "details": "台北轉運站 ➔ 羅東 ➔ 火車",
            "time_cost": "4.5hr",
            "pain_index": 50,
            "success_rate": 85,
            "advice": "國5客運有專用道。",
            "tags": ["彈性"]
        })

        # 8. 鈔能力
        strategies.append({
            "mode": "💸 包車/白牌",
            "details": "到府接送 ➔ 花東",
            "time_cost": "同開車",
            "pain_index": 10,
            "success_rate": 90,
            "advice": "加價約1.5倍。你在睡覺司機塞車。",
            "tags": ["輕鬆"]
        })

        # 排序
        if focus == "成功率":
            strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        elif focus == "舒適度":
            strategies.sort(key=lambda x: x['pain_index'])
        else:
            strategies.sort(key=lambda x: float(x['time_cost'].split('hr')[0]))
        return strategies

    def _get_traffic_entropy(self, hour):
        if 2 <= hour <= 4: return 5
        if 5 <= hour <= 6: return 30
        if 7 <= hour <= 19: return 95
        if 20 <= hour <= 23: return 40
        return 10

    def _get_driving_advice(self, hour, is_peak):
        if not is_peak: return "路況正常。"
        if 2 <= hour <= 4: return "🌟 完美物理窗口 (倖存區)。"
        elif 7 <= hour <= 19: return "💀 絕對死局，建議改道。"
        else: return "⚠️ 緩衝區，心理準備塞2hr。"

# ==========================================
# Layer 3: 手機版使用者介面 (Mobile UI)
# ==========================================

def login_page():
    # 使用空白容器推擠排版
    st.container(height=50, border=False) 
    
    st.markdown("<h2 style='text-align: center;'>🔒 會員驗證</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>FP-CRF 三一協會專用通道</p>", unsafe_allow_html=True)
    
    password = st.text_input("輸入密碼", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
    
    if st.button("登入系統 (Login)", type="primary", use_container_width=True):
        if password == "1234":
            st.session_state['logged_in'] = True
            st.toast("✅ 驗證成功！")
            time.sleep(0.5)
            st.rerun()
        else:
            st.toast("❌ 密碼錯誤")

def main_app():
    # 手機版頂部標題區
    st.markdown("<h3 style='margin-bottom:0px;'>🧨 2026 返鄉攻略</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em;'>三一協會專用 | FP-CRF v6.4</p>", unsafe_allow_html=True)
    
    # 設置區 (使用 Expander 收合，模擬手機下拉選單)
    with st.expander("⚙️ 行程設定 (點擊展開)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            destination = st.selectbox("目的地", ["花蓮", "台東"])
            date_type = st.selectbox("日期", ["除夕/首日", "收假", "平日"])
        with col2:
            departure_hour = st.selectbox("出發時間", [f"{i}:00" for i in range(24)], index=8)
            focus = st.selectbox("策略", ["成功率", "舒適度", "效率"])
        
        # 登出小按鈕
        if st.button("登出", help="退出系統"):
            st.session_state['logged_in'] = False
            st.rerun()

    # 主操作按鈕
    hour_int = int(departure_hour.split(":")[0])
    
    if st.button("🚀 開始計算最佳路徑", type="primary", use_container_width=True):
        
        engine = FPCRF_Strategy_Engine()
        strategies = engine.calculate_strategies(date_type, hour_int, focus, destination)
        
        st.markdown("---")
        st.markdown(f"**📊 分析結果 ({len(strategies)}種方案)**")
        
        for i, s in enumerate(strategies):
            pain = s['pain_index']
            
            # 視覺化顏色定義
            border_color = "#e0e0e0"
            bg_color = "#ffffff"
            icon = "🔹"
            
            if pain > 80:
                bg_color = "#fff0f0" # 淡紅
                icon = "🔥"
            elif pain < 30:
                bg_color = "#f0fff4" # 淡綠
                icon = "✨"
            elif i == 0:
                bg_color = "#f0f8ff" # 淡藍
                icon = "🏆"

            # 模擬手機卡片 (Card View)
            with st.container(border=True):
                # 上半部：標題與數據
                c1, c2 = st.columns([4, 2])
                with c1:
                    st.markdown(f"**{icon} {s['mode']}**")
                    st.caption(f"{s['details']}")
                with c2:
                    st.markdown(f"<div style='text-align:right; font-weight:bold; color:#555;'>{s['success_rate']}%</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:right; font-size:0.8em; color:gray;'>成功率</div>", unsafe_allow_html=True)

                # 下半部：建議與標籤
                st.markdown(f"<div style='background-color:{bg_color}; padding:8px; border-radius:5px; font-size:0.9em;'>💡 {s['advice']}</div>", unsafe_allow_html=True)
                
                # 底部數據列
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; margin-top:8px; font-size:0.8em; color:#666;'>
                    <span>⏳ {s['time_cost']}</span>
                    <span>😖 痛苦: {s['pain_index']}</span>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# 入口
# ==========================================
if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
