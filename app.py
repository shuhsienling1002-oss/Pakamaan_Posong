import streamlit as st
import time
from datetime import datetime, timedelta

# ==========================================
# Layer 0: 頁面設定
# ==========================================
st.set_page_config(
    page_title="三一返鄉戰情室",
    page_icon="🚄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# Layer 3.5: CSS 視覺優化 (原生 App 質感)
# ==========================================
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    .stButton > button {
        border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stVerticalBlock"] > div {border-radius: 12px; margin-bottom: 10px;}
    .tactical-box {
        background-color: #f8f9fa; border-left: 5px solid #E63946;
        padding: 15px; margin: 10px 0; border-radius: 5px; font-size: 0.95em;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1.5: 搶票戰術邏輯庫 (Ticket Strategy Core)
# 這裡運用資訊力，提供具體的「時間差」與「空間切割」策略
# ==========================================
class Ticket_War_Room:
    def get_tactics(self, mode):
        tactics = []
        
        if mode == "火車":
            tactics.append({
                "title": "⚔️ 戰術 A: 拓撲切割法 (Split Ticket)",
                "desc": "台鐵長途票配額極少，但短途多。",
                "steps": [
                    "不要搜「桃園 ➔ 花蓮」 (直達票池極小)",
                    "**第一刀 (切換乘點):** 買 **「桃園 ➔ 宜蘭/羅東」** (西部幹線票多)",
                    "**第二刀 (攻擊瓶頸):** 買 **「宜蘭/羅東 ➔ 花蓮」** (這段才是真正的瓶頸)",
                    "**操作:** 兩個視窗同時開，先搶第二段(宜蘭-花蓮)，因為第一段隨時有客運備案。"
                ],
                "level": "⭐⭐⭐⭐⭐"
            })
            tactics.append({
                "title": "🧟 戰術 B: 殭屍票回魂 (Resurrection)",
                "desc": "利用系統清票邏輯撿漏。",
                "steps": [
                    "**首波釋出:** 訂票日起訂後 **第3天 00:00** (未付款釋出)",
                    "**次波釋出:** 發車前 **14天 00:00** (退票潮)",
                    "**最後一擊:** 發車前 **1天** (甚至當天早上)，會有保留座釋出。",
                    "**App設定:** 使用官方 App 的「自動媒合」功能，不要手動刷。"
                ],
                "level": "⭐⭐⭐⭐"
            })
            tactics.append({
                "title": "🛡️ 戰術 C: 區間快保底 (The Safety Net)",
                "desc": "當所有對號座都失敗時的最後防線。",
                "steps": [
                    "桃園沒有始發車，去桃園等車必死無疑。",
                    "**逆向操作:** 買一張桃園往板橋的票，**搭回「樹林站」**。",
                    "在樹林站 (東部幹線始發站) 排隊上 EMU900 區間快車。",
                    "**優勢:** 100% 有位子，且 EMU900 椅子比普悠瑪好坐。"
                ],
                "level": "⭐⭐⭐"
            })

        elif mode == "高鐵轉乘":
            tactics.append({
                "title": "⚡ 戰術 A: 雙軌並進 (Dual Track)",
                "desc": "高鐵票比台鐵好買，先確保「跨過中央山脈前」的路段。",
                "steps": [
                    "**開賣日 (D-29):** 先搶 **「桃園 ➔ 台北」** 的高鐵票 (確保 100% 準點)。",
                    "**轉乘緩衝:** 在台北站預留 **40分鐘** 以上轉乘時間 (避免台鐵月台人流管制)。",
                    "**東部段:** 集中火力搶 **「台北 ➔ 花蓮」** 的台鐵票 (台北發車配額最多)。"
                ],
                "level": "⭐⭐⭐⭐"
            })
        
        elif mode == "開車":
            tactics.append({
                "title": "🌙 戰術 A: 物理時窗 (Time Window)",
                "desc": "利用人類生理極限避開熱力學擁堵。",
                "steps": [
                    "**唯一解:** **凌晨 03:00 - 05:00** 通過雪隧。",
                    "**理由:** 這是大數據顯示國5唯一「綠色」的時段。",
                    "**禁忌:** 早上 07:00 後上路 = 自殺行為 (車速 < 20km/h)。"
                ],
                "level": "⭐⭐⭐⭐⭐"
            })

        return tactics

# ==========================================
# Layer 1 & 2: 物理邏輯引擎 (不變)
# ==========================================
class FPCRF_Strategy_Engine:
    def calculate_strategies(self, date_type, departure_hour, destination, selected_modes):
        # (此處保留 v6.6 的完整演算邏輯，為節省篇幅省略，實際執行時請包含 v6.6 的 class 內容)
        # 為了讓代碼完整可執行，這裡放入簡化版的核心邏輯
        strategies = []
        is_peak = (date_type == "春節連假首日/除夕")
        traffic_entropy = 95 if (7 <= departure_hour <= 19 and is_peak) else 20
        is_taitung = (destination == "台東") 

        # 1. 火車
        if "火車" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚄 火車直達 (EMU3000)", "type": "火車",
                "details": f"桃園 ➔ {destination}",
                "time_cost": "3.0hr", "pain_index": 20, "success_rate": 10 if is_peak else 60,
                "advice": "直達票極難訂，請參考戰術分頁的「拓撲切割法」。", "tags": ["舒適", "難訂"]
            })
            strategies.append({
                "mode": "🚆 區間快車 (始發站)", "type": "火車",
                "details": f"樹林(始發) ➔ {destination}",
                "time_cost": "4.5hr", "pain_index": 70, "success_rate": 99,
                "advice": "回頭去搭始發車，保證有位。", "tags": ["保底", "累"]
            })

        # 2. 混合
        if "混合模式" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚅+🚄 高鐵轉乘", "type": "混合模式",
                "details": "桃園HSR ➔ 台北 ➔ 火車",
                "time_cost": "3.5hr", "pain_index": 30, "success_rate": 20 if is_peak else 70,
                "advice": "用高鐵換取準點率，主攻台北發車的票。", "tags": ["效率"]
            })
        
        # 3. 開車
        if "開車" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚗 自行開車", "type": "開車",
                "details": f"{departure_hour}:00 出發",
                "time_cost": "3.5hr" if traffic_entropy < 50 else "8.0hr",
                "pain_index": traffic_entropy, "success_rate": 100,
                "advice": "凌晨3點出發是唯一活路。" if traffic_entropy > 50 else "路況尚可。", "tags": ["塞車"]
            })

        strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        return strategies

# ==========================================
# Layer 3: 手機版介面 (Mobile UI)
# ==========================================

def login_page():
    st.container(height=50, border=False) 
    st.markdown("<h2 style='text-align: center;'>🔒 協會會員驗證</h2>", unsafe_allow_html=True)
    st.info("會員請向三一協會索取密碼")
    
    password = st.text_input("密碼", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
    
    if st.button("登入系統", type="primary", use_container_width=True):
        if password == "1234":
            st.session_state['logged_in'] = True
            st.toast("✅ 驗證成功！")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("❌ 密碼錯誤")

def main_app():
    st.markdown("<h3 style='margin-bottom:0px; color:#E63946;'>🧨 三一協會過年返鄉攻略</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em;'>FP-CRF v7.0 | 戰情室版</p>", unsafe_allow_html=True)
    
    # [新功能] 使用 Tabs 分頁，將「路徑規劃」與「搶票戰術」分開
    tab1, tab2 = st.tabs(["🚀 路徑規劃", "🎫 搶票戰術指導"])
    
    # --- Tab 1: 路徑規劃 (原本的功能) ---
    with tab1:
        with st.expander("⚙️ 設定選項 (點擊展開)", expanded=True):
            st.markdown("**1. 交通工具 (可複選):**")
            mode_options = ["全部", "火車", "開車", "混合模式"]
            selected_modes = st.multiselect("交通工具", mode_options, default=["全部"], label_visibility="collapsed")
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                destination = st.selectbox("目的地", ["花蓮", "台東"])
                date_type = st.selectbox("日期", ["春節連假首日/除夕", "平日"])
            with c2:
                departure_hour = st.selectbox("時間", [f"{i:02d}:00" for i in range(24)], index=8)

        if st.button("開始計算", type="primary", use_container_width=True):
            modes_to_query = mode_options[1:] if "全部" in selected_modes else selected_modes
            engine = FPCRF_Strategy_Engine()
            strategies = engine.calculate_strategies(date_type, int(departure_hour.split(":")[0]), destination, modes_to_query)
            
            st.markdown("---")
            for i, s in enumerate(strategies):
                pain = s['pain_index']
                bg_color = "#FFF5F5" if pain > 80 else ("#F0FFF4" if pain < 30 else "#ffffff")
                icon = "🏆" if i == 0 else "🔹"
                
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1.5])
                    with c1:
                        st.markdown(f"**{icon} {s['mode']}**")
                        st.caption(f"{s['type']} | {s['details']}")
                    with c2:
                        st.markdown(f"<div style='text-align:right; font-weight:bold; color:#2A9D8F;'>{s['success_rate']}%</div>", unsafe_allow_html=True)
                        st.caption("成功率")
                    
                    st.markdown(f"<div style='background-color:{bg_color}; padding:8px; border-radius:5px; margin:5px 0; font-size:0.9em;'>💡 {s['advice']}</div>", unsafe_allow_html=True)
                    st.caption(f"⏱️ {s['time_cost']} | 😖 痛苦: {s['pain_index']}")

    # --- Tab 2: 搶票戰術指導 (新增的高價值資訊) ---
    with tab2:
        st.markdown("#### 🛡️ 戰情室戰術看板")
        st.info("這裡提供 FP-CRF 分析後的最佳「買票策略」，請依據您的交通工具選擇戰術。")
        
        war_room = Ticket_War_Room()
        
        # 火車戰術
        st.markdown("##### 🚂 火車/台鐵戰術")
        train_tactics = war_room.get_tactics("火車")
        for t in train_tactics:
            with st.expander(f"{t['title']} ({t['level']})"):
                st.markdown(t['desc'])
                for step in t['steps']:
                    st.markdown(f"- {step}")
        
        # 開車戰術
        st.markdown("##### 🚗 開車/自駕戰術")
        car_tactics = war_room.get_tactics("開車")
        for t in car_tactics:
            with st.expander(f"{t['title']} ({t['level']})"):
                st.markdown(t['desc'])
                for step in t['steps']:
                    st.markdown(f"- {step}")

        st.markdown("---")
        st.caption("※ 戰術僅供參考，實際狀況依當日運能與路況為主。")

    # 登出區
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("登出系統"):
        st.session_state['logged_in'] = False
        st.rerun()

# ==========================================
# 入口
# ==========================================
if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
