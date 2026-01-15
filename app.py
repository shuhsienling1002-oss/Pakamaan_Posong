import streamlit as st
import time

# ==========================================
# Layer 0: 頁面設定與 Session 狀態初始化
# ==========================================
st.set_page_config(
    page_title="FP-CRF 花東戰略指揮部",
    page_icon="🧬",
    layout="centered"
)

# 初始化 Session State (用來記住是否有登入)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1 & 2: 物理邏輯核心 (Physics Engine)
# 這裡包含所有運算邏輯，與介面無關
# ==========================================
class FPCRF_Strategy_Engine:
    def calculate_strategies(self, date_type, departure_hour, focus, destination):
        strategies = []
        
        # 參數校準
        is_peak = (date_type == "春節連假首日/除夕")
        traffic_entropy = self._get_traffic_entropy(departure_hour) if is_peak else 20
        is_taitung = (destination == "台東") 

        # --- 策略 1: 火車直達 (Standard) ---
        success_rate_train = 10 if is_peak else 60
        strategies.append({
            "mode": "🚄 火車直達 (EMU3000/普悠瑪)",
            "details": f"桃園 -> {destination}",
            "time_cost": "2.5 - 3.5 hr" if not is_taitung else "4.0 - 5.0 hr",
            "pain_index": 20,
            "success_rate": success_rate_train,
            "advice": "最優解，但若是除夕，搶票難度等同中樂透。",
            "tags": ["舒適", "極難訂"]
        })

        # --- 策略 2: 區間快暴力解 (Hardcore) ---
        strategies.append({
            "mode": "🚆 區間快車 (EMU900) 暴力接力",
            "details": f"桃園 -> 樹林(始發) -> {destination}",
            "time_cost": "4.0 hr" if not is_taitung else "6.5 hr",
            "pain_index": 65 if not is_taitung else 85,
            "success_rate": 99,
            "advice": "回到樹林/南港搶始發站座位。去花蓮可接受，去台東屁股會裂開 (Pain > 80)。",
            "tags": ["保證有車", "累"]
        })

        # --- 策略 3: 高鐵轉乘 (HSR Relay) ---
        strategies.append({
            "mode": "🚅+🚄 高鐵轉乘 (HSR Relay)",
            "details": f"桃園HSR -> 台北車站 -> 轉乘東部幹線",
            "time_cost": "3.0 hr" if not is_taitung else "4.5 hr",
            "pain_index": 30,
            "success_rate": success_rate_train + 5,
            "advice": "利用高鐵跳過桃園-台北的台鐵擁擠段。關鍵還是在搶台北出發的東部票。",
            "tags": ["效率", "轉乘"]
        })

        # --- 策略 4: 飛機空運 (Sky Vector) ---
        flight_success = 5 if is_peak else 40
        strategies.append({
            "mode": "✈️ 飛機空運 (Sky Vector)",
            "details": f"機捷 -> 松山機場(TSA) -> {destination}機場",
            "time_cost": "2.5 hr (含報到)",
            "pain_index": 15,
            "success_rate": flight_success,
            "advice": "立榮/華信春節加班機極少。除非你是「設籍居民」有保留位，否則現場候補是絕望的賭局。",
            "tags": ["豪賭", "看天吃飯"]
        })

        # --- 策略 5: 南迴大迂迴 (台東限定神招) ---
        if is_taitung:
            strategies.append({
                "mode": "🔄 高鐵南下 + 南迴北上 (大迂迴)",
                "details": "桃園HSR -> 左營 -> (新自強/租車) -> 台東",
                "time_cost": "4.5 - 5.5 hr",
                "pain_index": 25,
                "success_rate": 75,
                "advice": "✨ 台東返鄉首選！避開蘇花改瓶頸。左營到台東票比台北到台東好買太多了。",
                "tags": ["逆向思維", "高成功率"]
            })
        
        # --- 策略 6: 自行開車 (Driving) ---
        drive_time = (3.5 if not is_taitung else 6.0) * (1 + (traffic_entropy / 100) * 3)
        strategies.append({
            "mode": "🚗 自行開車 (蘇花路廊)",
            "details": f"出發時間 {departure_hour}:00",
            "time_cost": f"{drive_time:.1f} hr",
            "pain_index": min(30 + traffic_entropy, 100),
            "success_rate": 100,
            "advice": self._get_driving_advice(departure_hour, is_peak),
            "tags": ["自主性", "塞車地獄"]
        })

        # --- 策略 7: 鐵公路聯運 (Bus Hybrid) ---
        strategies.append({
            "mode": "🚌+🚆 鐵公路聯運 (Gap Seeker)",
            "details": "桃園 -> 台北轉運站 -> 客運至羅東 -> 火車",
            "time_cost": "4.5 hr",
            "pain_index": 50,
            "success_rate": 85,
            "advice": "利用國5大客車專用道優勢。適合買不到火車票的中繼手段。",
            "tags": ["高彈性"]
        })

        # --- 策略 8: 金錢換空間 (Money Solve) ---
        strategies.append({
            "mode": "💸 包車/白牌/共乘 (Money Solve)",
            "details": "到府接送 -> 花東",
            "time_cost": "同開車",
            "pain_index": 10,
            "success_rate": 90,
            "advice": "春節加價幅度約 1.5x - 2x。優點是你可以在車上睡覺，讓司機去承擔塞車的痛苦。",
            "tags": ["鈔能力", "輕鬆"]
        })

        # 根據用戶選擇進行排序
        if focus == "成功率 (只要回得去)":
            strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        elif focus == "低痛苦 (舒適度)":
            strategies.sort(key=lambda x: x['pain_index'])
        else:
            # 簡單解析時間字串進行排序
            strategies.sort(key=lambda x: float(x['time_cost'].split()[0].split('-')[0]))

        return strategies

    def _get_traffic_entropy(self, hour):
        # 塞車熵值模型 (Layer 1 Physics)
        if 2 <= hour <= 4: return 5
        if 5 <= hour <= 6: return 30
        if 7 <= hour <= 19: return 95
        if 20 <= hour <= 23: return 40
        return 10

    def _get_driving_advice(self, hour, is_peak):
        if not is_peak: return "路況正常。"
        if 2 <= hour <= 4: return "🌟 完美物理窗口。這是唯一的倖存區間。"
        elif 7 <= hour <= 19: return "💀 絕對死局。建議改走台2線或放棄開車。"
        else: return "⚠️ 緩衝區。要有塞 2 小時以上的心理準備。"

# ==========================================
# Layer 3: Streamlit 使用者介面 (UI)
# 這裡負責顯示畫面，包含登入頁與主程式
# ==========================================

def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True) # 排版留白
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔒 協會會員驗證")
        st.markdown("### ⚠️ 系統存取受限")
        st.info("會員請向協會索取密碼")
        
        password = st.text_input("請輸入密碼", type="password")
        
        if st.button("驗證身份 (Verify)", type="primary"):
            if password == "1234":
                st.session_state['logged_in'] = True
                st.success("✅ 身份確認。正在進入 FP-CRF 指揮部...")
                time.sleep(1)
                st.rerun() # 重新整理頁面以進入主程式
            else:
                st.error("❌ 密碼錯誤。物理法則拒絕您的存取。")

def main_app():
    # 側邊欄設定
    with st.sidebar:
        st.header("Layer 0: 參數校準")
        
        destination = st.selectbox("目的地", ["花蓮", "台東"])
        date_type = st.selectbox("時段類型", ["春節連假首日/除夕", "春節收假", "一般週末"])
        
        departure_hour = st.slider("預計出發時間 (0-23時)", 0, 23, 8)
        st.write(f"🕒 設定時間: {departure_hour:02d}:00")
        
        focus = st.selectbox("核心需求", ["成功率 (只要回得去)", "低痛苦 (舒適度)", "速度 (極致效率)"])
        
        st.divider()
        if st.button("登出系統"):
            st.session_state['logged_in'] = False
            st.rerun()

    # 主畫面
    st.title("🧬 FP-CRF v6.1 (Cloud)")
    st.markdown(f"**花東返鄉戰略指揮部 | 物理推演系統**")
    st.caption("v6.1 Platinum Edition - Contains HSR, Air, Charter, and Encirclement modules.")
    
    # 執行運算按鈕
    run_btn = st.button("🚀 執行物理推演 (Execute Simulation)", type="primary", use_container_width=True)

    if run_btn:
        with st.spinner('正在計算路徑熵值與物理極限...'):
            time.sleep(0.5) # 模擬運算感
            engine = FPCRF_Strategy_Engine()
            strategies = engine.calculate_strategies(date_type, departure_hour, focus, destination)
            
            st.subheader(f"📊 戰略報告: 桃園 ➔ {destination}")
            st.caption(f"情境: {date_type} | 出發: {departure_hour:02d}:00 | 導向: {focus}")
            st.divider()

            for i, s in enumerate(strategies):
                # 視覺化邏輯：根據痛苦指數給予不同顏色的框框
                pain = s['pain_index']
                if pain > 80:
                    container = st.error # 紅色 (高痛苦)
                elif pain < 30:
                    container = st.success # 綠色 (舒適)
                else:
                    container = st.warning # 黃色 (普通)
                
                with container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### 方案 {i+1}: {s['mode']}")
                        if i == 0:
                            st.caption("🏆 系統推薦最佳解 (The Best Physics Path)")
                        st.markdown(f"**📍 路徑:** {s['details']}")
                        st.markdown(f"**💡 建議:** {s['advice']}")
                        # 顯示標籤
                        tags_html = " ".join([f"`{tag}`" for tag in s['tags']])
                        st.markdown(f"🏷️ {tags_html}")
                    
                    with col2:
                        st.metric("成功率", f"{s['success_rate']}%")
                        st.metric("痛苦指數", f"{s['pain_index']}")
                        st.caption(f"⏱️ {s['time_cost']}")

# ==========================================
# 程式進入點 (Main Entry Point)
# ==========================================
if not st.session_state['logged_in']:
    login_page()
else:
    main_app()
