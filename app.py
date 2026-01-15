import streamlit as st
import time

# ==========================================
# Layer 0: 頁面設定
# ==========================================
st.set_page_config(
    page_title="三一返鄉戰情室",
    page_icon="🧨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# Layer 3.5: CSS 視覺優化 (App-like UI)
# ==========================================
hide_streamlit_style = """
<style>
    /* 隱藏網頁元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 手機版面調整 */
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    
    /* 按鈕樣式 */
    .stButton > button {
        border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 卡片與容器 */
    div[data-testid="stVerticalBlock"] > div {border-radius: 12px; margin-bottom: 10px;}
    
    /* 日期警告卡片 */
    .date-warning {
        padding: 10px; border-radius: 8px; font-size: 0.9em; margin-top: 5px;
        background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1.5: 搶票戰術邏輯庫 (Ticket Strategy Core)
# [完整回歸]：提供詳細的戰術步驟與星級評等
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
            tactics.append({
                "title": "🛣️ 戰術 B: 台2線替代 (Coastal Route)",
                "desc": "當國5紫爆時的最後手段。",
                "steps": [
                    "**條件:** 當 Google Maps 顯示國5行車時間 > 2.5小時。",
                    "**路徑:** 桃園 -> 62快速道路 -> 瑞濱 -> 台2線 -> 頭城。",
                    "**優點:** 雖然遠，但是車子是在動的 (Flow > 0)。"
                ],
                "level": "⭐⭐⭐"
            })

        return tactics

# ==========================================
# Layer 1 & 2: 物理邏輯引擎 (Core Logic)
# [完整保留]：包含 v8.1 的 God Mode 修復邏輯
# ==========================================
class FPCRF_Strategy_Engine:
    
    def analyze_date_physics(self, date_str):
        # 基礎日期屬性
        mapping = {
            "2/12 (四) - 假期前2天 (提早閃人)": 
                {"entropy": 30, "desc": "🟢 舒適圈", "base_advice": "完美決策，贏在起跑點。"},
            "2/13 (五) - 假期前1天 (下班狂奔)": 
                {"entropy": 95, "desc": "🔴 死亡交叉", "base_advice": "全台灣上班族都在這晚衝出來，國5保證紫爆。"},
            "2/14 (六) - 假期第1天 (返鄉車潮)": 
                {"entropy": 90, "desc": "🟠 擁塞主流", "base_advice": "標準塞車日，早上就是停車場。"},
            "2/15 (日) - 小年夜 (最後採買)": 
                {"entropy": 60, "desc": "🟡 緩衝期", "base_advice": "車流稍減，但市場周邊塞。"},
            "2/16 (一) - 除夕 (圍爐決戰)": 
                {"entropy": 40, "desc": "🟢 上午賭局", "base_advice": "中午過後路上沒車。"},
            "2/17 (二) - 初一 (走春拜年)": 
                {"entropy": 75, "desc": "🟠 區域塞車", "base_advice": "景點會爆炸。"},
            "2/21 (六) - 收假前1天 (北返地獄)": 
                {"entropy": 100, "desc": "⚫ 絕對死局", "base_advice": "北上必定回堵到崇德。"},
            "一般平日/週末": 
                {"entropy": 20, "desc": "⚪ 正常", "base_advice": "路況正常。"}
        }
        return mapping.get(date_str, mapping["一般平日/週末"])

    def calculate_strategies(self, date_str, departure_hour, destination, selected_modes):
        strategies = []
        is_taitung = (destination == "台東")
        
        # 1. 取得「日期」的原始物理屬性
        date_physics = self.analyze_date_physics(date_str)
        base_entropy = date_physics["entropy"]
        
        # 2. [邏輯修復] 根據「時間 (Hour)」進行權重覆蓋 (Override)
        is_god_mode = (2 <= departure_hour <= 4)
        
        if is_god_mode:
            # God Mode: 強制綠燈
            final_entropy = 10 
            final_car_advice = "🌌 [深夜特權] 雖然今天是塞車日，但這個時間點出發是唯一的『物理倖存窗口』。全速前進吧！"
        elif 7 <= departure_hour <= 20 and base_entropy > 60:
            # 尖峰時刻 + 塞車日 = 地獄
            final_entropy = min(100, base_entropy + 10)
            final_car_advice = f"💀 {date_physics['desc']}。{date_physics['base_advice']}在這個時間出發是自殺行為。"
        else:
            # 普通狀況
            final_entropy = base_entropy
            final_car_advice = f"{date_physics['desc']}。{date_physics['base_advice']}"

        # --- 策略生成 ---
        
        # A. 火車策略
        if "火車" in selected_modes or "全部" in selected_modes:
            ticket_difficulty = 95 if base_entropy > 80 else 60
            strategies.append({
                "mode": "🚄 火車直達 (EMU3000)", 
                "details": f"桃園 ➔ {destination}",
                "time_cost": "3.0hr" if not is_taitung else "4.5hr",
                "pain_index": 20,
                "success_rate": 100 - ticket_difficulty,
                "advice": f"這天搶票難度: {ticket_difficulty}%。請參考戰術分頁的切票法。", 
                "tags": ["舒適", "難訂"]
            })
            strategies.append({
                "mode": "🚆 區間快 (樹林始發)", 
                "details": f"樹林 ➔ {destination}",
                "time_cost": "4.5hr", "pain_index": 70, "success_rate": 99,
                "advice": "只要願意站/擠，這天保證回得去。", "tags": ["保底"]
            })

        # B. 開車策略
        if "開車" in selected_modes or "全部" in selected_modes:
            base_time = 3.5 if not is_taitung else 6.0
            # God Mode 不加成時間
            jam_factor = 1.0 if is_god_mode else (1 + (final_entropy / 100) * 2.5)
            
            strategies.append({
                "mode": "🚗 自行開車", 
                "details": f"{departure_hour}:00 出發",
                "time_cost": f"{base_time * jam_factor:.1f}hr",
                "pain_index": final_entropy, # 修正後的數值
                "success_rate": 100,
                "advice": final_car_advice,
                "tags": ["順暢" if is_god_mode else ("塞車風險" if final_entropy > 50 else "普通")]
            })
            
            strategies.append({
                "mode": "💸 包車/白牌",
                "details": "到府接送",
                "time_cost": "同開車",
                "pain_index": 10,
                "success_rate": 90,
                "advice": "有錢就是任性，你在睡覺司機在塞。",
                "tags": ["鈔能力"]
            })

        # C. 混合策略
        if "混合模式" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚅+🚄 高鐵轉乘", 
                "details": "桃園 ➔ 台北 ➔ 花東",
                "time_cost": "3.5hr", "pain_index": 30, 
                "success_rate": 40 if base_entropy > 80 else 70,
                "advice": "用金錢換取避開國道塞車。", "tags": ["效率"]
            })
            
            if is_taitung:
                strategies.append({
                    "mode": "🔄 高鐵南迴大迂迴",
                    "details": "左營 ➔ 台東",
                    "time_cost": "5.0hr", "pain_index": 25, "success_rate": 75,
                    "advice": "台東人神招，完全避開蘇花改。", "tags": ["神招"]
                })

        # D. 飛機策略
        if "飛機" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "✈️ 飛機空運",
                "details": "松山 ➔ 花東",
                "time_cost": "2.5hr", "pain_index": 15, "success_rate": 5 if base_entropy > 80 else 40,
                "advice": "候補是大賭局，非設籍居民勿試。", "tags": ["豪賭"]
            })

        strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        return strategies, date_physics

# ==========================================
# Layer 3: 手機版介面
# ==========================================

def login_page():
    st.container(height=50, border=False) 
    st.markdown("<h2 style='text-align: center;'>🔒 協會會員驗證</h2>", unsafe_allow_html=True)
    st.info("會員請向三一協會索取密碼")
    password = st.text_input("密碼", type="password", label_visibility="collapsed", placeholder="輸入密碼")
    if st.button("登入", type="primary", use_container_width=True):
        if password == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤")

def main_app():
    st.markdown("<h3 style='margin-bottom:0px; color:#E63946;'>🧨 三一返鄉戰情室</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em;'>v8.2 | 完全戰略版</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 戰略規劃", "🎫 搶票密技"])
    
    with tab1:
        with st.expander("⚙️ 設定行程 (已展開)", expanded=True):
            
            st.markdown("**1. 交通工具 (複選):**")
            mode_options = ["全部", "火車", "開車", "混合模式", "飛機"]
            selected_modes = st.multiselect("Modes", mode_options, default=["全部"], label_visibility="collapsed")
            
            st.markdown("---")
            
            st.markdown("**2. 出發日期 (2026 春節):**")
            date_options = [
                "2/12 (四) - 假期前2天 (提早閃人)",
                "2/13 (五) - 假期前1天 (下班狂奔)",
                "2/14 (六) - 假期第1天 (返鄉車潮)",
                "2/15 (日) - 小年夜 (最後採買)",
                "2/16 (一) - 除夕 (圍爐決戰)",
                "2/17 (二) - 初一 (走春拜年)",
                "2/21 (六) - 收假前1天 (北返地獄)",
                "一般平日/週末"
            ]
            date_str = st.selectbox("Date", date_options, index=1, label_visibility="collapsed")
            
            # 日期預覽
            engine_preview = FPCRF_Strategy_Engine()
            preview = engine_preview.analyze_date_physics(date_str)
            st.markdown(f"<div class='date-warning'><b>📊 日期體質:</b> {preview['desc']}</div>", unsafe_allow_html=True)

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**3. 目的地:**")
                destination = st.selectbox("Dest", ["花蓮", "台東"], label_visibility="collapsed")
            with c2:
                st.markdown("**4. 出發時間:**")
                # 預設 03:00 體驗 God Mode
                departure_hour = st.selectbox("Time", [f"{i:02d}:00" for i in range(24)], index=3, label_visibility="collapsed")

        if st.button("🚀 開始計算", type="primary", use_container_width=True):
            modes = mode_options[1:] if "全部" in selected_modes else selected_modes
            engine = FPCRF_Strategy_Engine()
            hour_int = int(departure_hour.split(":")[0])
            strategies, physics = engine.calculate_strategies(date_str, hour_int, destination, modes)
            
            st.markdown("---")
            st.markdown(f"**📊 分析報告 ({date_str})**")
            
            if not strategies:
                st.warning("⚠️ 請選擇至少一種交通工具。")
            
            for i, s in enumerate(strategies):
                pain = s['pain_index']
                
                # 顏色邏輯 (含 God Mode 修正)
                bg = "#FFF5F5" if pain > 80 else ("#F0FFF4" if pain < 30 else "#ffffff")
                
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1.5])
                    with c1:
                        st.markdown(f"**{s['mode']}**")
                        st.caption(f"{s['details']}")
                    with c2:
                        st.markdown(f"<div style='text-align:right; font-weight:bold; color:#2A9D8F;'>{s['success_rate']}%</div>", unsafe_allow_html=True)
                        st.caption("機率")
                    
                    st.markdown(f"<div style='background-color:{bg}; padding:8px; border-radius:5px; margin:5px 0; font-size:0.9em;'>💡 {s['advice']}</div>", unsafe_allow_html=True)
                    st.caption(f"⏱️ {s['time_cost']} | 😖 痛苦: {s['pain_index']}")

    with tab2:
        st.markdown("#### 🎫 搶票戰術看板")
        st.info("台鐵/高鐵 2026 春節配票邏輯分析")
        
        # 實例化戰術庫並顯示
        war_room = Ticket_War_Room()
        
        st.markdown("##### 🚂 火車戰術")
        train_tactics = war_room.get_tactics("火車")
        for t in train_tactics:
            with st.expander(f"{t['title']} ({t['level']})"):
                st.markdown(t['desc'])
                for step in t['steps']:
                    st.markdown(f"- {step}")
        
        st.markdown("##### 🚗 開車戰術")
        car_tactics = war_room.get_tactics("開車")
        for t in car_tactics:
            with st.expander(f"{t['title']} ({t['level']})"):
                st.markdown(t['desc'])
                for step in t['steps']:
                    st.markdown(f"- {step}")

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
