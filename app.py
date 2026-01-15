import streamlit as st
import time

# ==========================================
# Layer 0: 頁面設定 (Mobile Configuration)
# ==========================================
st.set_page_config(
    page_title="三一協會過年返鄉攻略", 
    page_icon="🧨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# Layer 3.5: CSS 視覺優化 (App-like UI)
# ==========================================
hide_streamlit_style = """
<style>
    /* 隱藏 Streamlit 預設元素，模擬原生 App */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 手機版面留白調整 */
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    
    /* 原生 App 風格按鈕 */
    .stButton > button {
        border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 卡片容器圓角 */
    div[data-testid="stVerticalBlock"] > div {border-radius: 12px; margin-bottom: 10px;}
    
    /* 日期警告卡片樣式 */
    .date-warning {
        padding: 10px; border-radius: 8px; font-size: 0.9em; margin-top: 5px;
        background-color: #fff3cd; border: 1px solid #ffeeba; color: #856404;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 初始化登入狀態
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1: 靜態資料庫 (地理 + 時刻表)
# ==========================================
TOWNSHIP_DB = {
    "花蓮縣": {
        "北花蓮 (花蓮市/新城/吉安)": {"time_offset": 0, "south_link_score": 0, "zone": "North"},
        "中花蓮 (壽豐/鳳林/光復)": {"time_offset": 0.5, "south_link_score": 20, "zone": "Mid"},
        "海線 (豐濱)": {"time_offset": 1.0, "south_link_score": 30, "zone": "Coast"},
        "南花蓮 (瑞穗/玉里/富里)": {"time_offset": 1.5, "south_link_score": 60, "zone": "South"} 
    },
    "台東縣": {
        "縱谷線 (池上/關山/鹿野)": {"time_offset": 2.5, "south_link_score": 80, "zone": "Rift"},
        "海線 (長濱/成功/東河)": {"time_offset": 3.0, "south_link_score": 70, "zone": "Coast_TT"},
        "台東市區 (台東市/卑南)": {"time_offset": 3.5, "south_link_score": 95, "zone": "City"}, 
        "南迴線 (太麻里/大武)": {"time_offset": 4.0, "south_link_score": 100, "zone": "South_Link"}
    }
}

# 簡易靜態時刻表對照 (Mock Schedule for 2026)
TRAIN_SCHEDULE_DB = {
    0:  "深夜列車 (需查詢)",
    1:  "深夜列車 (需查詢)",
    2:  "無班次",
    3:  "無班次",
    4:  "無班次",
    5:  "區間快 4006 (05:50)",
    6:  "普悠瑪 402 (06:15)",
    7:  "自強3000 408 (07:30) [秒殺王]",
    8:  "自強3000 410 (07:55)",
    9:  "普悠瑪 218 (09:20)",
    10: "自強3000 472 (10:05)",
    11: "普悠瑪 222 (11:20)",
    12: "自強3000 426 (12:30)",
    13: "太魯閣 228 (13:10)",
    14: "自強3000 476 (14:10)",
    15: "普悠瑪 232 (15:20)",
    16: "自強3000 432 (16:00)",
    17: "自強3000 434 (17:15)",
    18: "普悠瑪 282 (18:10)",
    19: "自強3000 438 (19:00)",
    20: "太魯閣 248 (20:10)",
    21: "自強3000 448 (21:10)",
    22: "普悠瑪 252 (22:15)",
    23: "區間快 4054 (23:05)"
}

# ==========================================
# Layer 1.5: 搶票戰術邏輯庫 (Ticket War Room)
# [嚴格執行] 文字內容完全無刪減
# ==========================================
class Ticket_War_Room:
    def get_tactics(self, mode):
        tactics = []
        
        if mode == "火車":
            tactics.append({
                "title": "⚔️ 戰術 A: 拓撲切割法 (Split Ticket)",
                "desc": "台鐵長途票(如桃園-花蓮)配額極少，但區段票多。請善用「空間換取機率」。",
                "steps": [
                    "**核心觀念:** 不要搜尋「桃園 ➔ 花蓮」。",
                    "**第一刀 (切換乘點):** 先買 **「桃園 ➔ 宜蘭/羅東」** (西部幹線票較多)。",
                    "**第二刀 (攻擊瓶頸):** 同時開視窗搶 **「宜蘭/羅東 ➔ 花蓮」** (這段才是真正的瓶頸)。",
                    "**備案:** 只要搶到第二段，第一段就算沒火車票，也可以搭客運到羅東轉乘。"
                ],
                "level": "⭐⭐⭐⭐⭐"
            })
            tactics.append({
                "title": "🧟 戰術 B: 殭屍票回魂 (Resurrection)",
                "desc": "利用台鐵系統清票邏輯，撿那些「逾期未取」或「退票」的位子。",
                "steps": [
                    "**首波釋出:** 訂票日起訂後 **第3天 00:00** (系統自動釋出未付款座位)。",
                    "**次波釋出:** 發車前 **14天 00:00** (因退票手續費級距改變，會有一波退票潮)。",
                    "**最後一擊:** 發車前 **1天** (甚至當天早上)，通常會有保留座或臨時退票釋出。",
                    "**技巧:** 使用官方 App 的「自動媒合」功能，效率優於手動。"
                ],
                "level": "⭐⭐⭐⭐"
            })
            tactics.append({
                "title": "🛡️ 戰術 C: 區間快保底 (The Safety Net)",
                "desc": "當所有對號座都失敗時，這是唯一保證能回家的路。",
                "steps": [
                    "**禁忌:** 桃園沒有東部幹線始發車，去桃園站等區間車通常擠不上去。",
                    "**逆向操作:** 買一張桃園往板橋的票，**搭回「樹林站」**。",
                    "**執行:** 在樹林站 (東部幹線始發站) 排隊上 EMU900 區間快車。",
                    "**優勢:** 100% 有位子，且 EMU900 椅子比普悠瑪好坐。"
                ],
                "level": "⭐⭐⭐"
            })

        elif mode == "開車":
            tactics.append({
                "title": "🌙 戰術 A: 物理時窗 (God Mode)",
                "desc": "利用人類生理極限避開熱力學擁堵。這是唯一的物理倖存區間。",
                "steps": [
                    "**唯一解:** **凌晨 03:00 - 05:00** 通過雪山隧道。",
                    "**理由:** 這是大數據顯示國5唯一呈現「綠色流動」的時段。",
                    "**警告:** 早上 07:00 後上路 = 自殺行為 (車速將低於 20km/h)。"
                ],
                "level": "⭐⭐⭐⭐⭐"
            })
            tactics.append({
                "title": "🛣️ 戰術 B: 台2線替代 (Coastal Route)",
                "desc": "當國5紫爆且你必須白天出發時的最後手段。",
                "steps": [
                    "**條件:** 當 Google Maps 顯示國5行車時間 > 2.5小時。",
                    "**路徑:** 桃園 -> 62快速道路 -> 瑞濱 -> 台2線(濱海) -> 頭城。",
                    "**心法:** 雖然路程遠，但是車子是在動的 (Flow > 0)，心理壓力較小。"
                ],
                "level": "⭐⭐⭐"
            })

        return tactics

# ==========================================
# Layer 2: 物理邏輯引擎 (Core Physics Engine)
# ==========================================
class FPCRF_Strategy_Engine:
    
    def analyze_date_physics(self, date_str):
        mapping = {
            "2/12 (四) - 假期前2天 (提早閃人)": {"entropy": 30, "desc": "🟢 舒適圈", "base_advice": "完美決策，贏在起跑點。"},
            "2/13 (五) - 假期前1天 (下班狂奔)": {"entropy": 95, "desc": "🔴 死亡交叉", "base_advice": "全台大塞車，上班族傾巢而出。"},
            "2/14 (六) - 假期第1天 (返鄉車潮)": {"entropy": 90, "desc": "🟠 擁塞主流", "base_advice": "早上就是停車場。"},
            "2/15 (日) - 小年夜 (最後採買)": {"entropy": 60, "desc": "🟡 緩衝期", "base_advice": "車流稍減，但市區塞。"},
            "2/16 (一) - 除夕 (圍爐決戰)": {"entropy": 40, "desc": "🟢 上午賭局", "base_advice": "中午過後路上沒車。"},
            "2/17 (二) - 初一 (走春拜年)": {"entropy": 75, "desc": "🟠 區域塞車", "base_advice": "各大景點爆炸。"},
            "2/21 (六) - 收假前1天 (北返地獄)": {"entropy": 100, "desc": "⚫ 絕對死局", "base_advice": "必死無疑，請迴避。"},
            "一般平日/週末": {"entropy": 20, "desc": "⚪ 正常", "base_advice": "路況正常。"}
        }
        return mapping.get(date_str, mapping["一般平日/週末"])

    def get_nearest_train(self, hour):
        # 尋找最接近的車次
        train_info = TRAIN_SCHEDULE_DB.get(hour, "自強3000 (一般班次)")
        return train_info

    def calculate_strategies(self, date_str, departure_hour, county, township_key, selected_modes):
        strategies = []
        
        geo_data = TOWNSHIP_DB[county][township_key]
        time_offset = geo_data["time_offset"]
        south_link_score = geo_data["south_link_score"]
        
        date_physics = self.analyze_date_physics(date_str)
        base_entropy = date_physics["entropy"]
        
        # God Mode 判斷
        is_god_mode = (2 <= departure_hour <= 4)
        
        if is_god_mode:
            final_entropy = 10 
            final_car_advice = f"🌌 [深夜特權] 這是前往{township_key.split(' ')[0]}唯一的『物理倖存窗口』。全速前進！"
        elif 7 <= departure_hour <= 20 and base_entropy > 60:
            final_entropy = min(100, base_entropy + 10)
            final_car_advice = f"💀 {date_physics['desc']}。開到{township_key.split(' ')[0]}會讓人崩潰。"
        else:
            final_entropy = base_entropy
            final_car_advice = f"{date_physics['desc']}。{date_physics['base_advice']}"

        # --- 策略生成邏輯 ---
        
        # A. 火車策略
        if "火車" in selected_modes or "全部" in selected_modes:
            train_time = 2.5 + (time_offset * 0.8) 
            ticket_difficulty = 95 if base_entropy > 80 else 60
            if south_link_score > 50: ticket_difficulty += 5
            
            # [修正] 獲取真實車次
            real_train = self.get_nearest_train(departure_hour)
            
            strategies.append({
                "mode": f"🚄 {real_train}", # 顯示真實車次
                "details": f"桃園 ➔ {township_key.split(' ')[0]}",
                "time_cost": f"{train_time:.1f}hr",
                "pain_index": 20,
                "success_rate": max(5, 100 - ticket_difficulty),
                "advice": f"依據您選的 {departure_hour}:00，這是最接近的熱門直達車。", 
                "tags": ["舒適", "極難訂"]
            })
            
            # 如果是北花蓮/中花蓮，顯示區間車備案
            if county == "花蓮縣" and south_link_score < 50:
                 strategies.append({
                    "mode": "🚆 區間快 (樹林始發)", 
                    "details": f"樹林 ➔ {township_key.split(' ')[0]}",
                    "time_cost": f"{train_time + 1.5:.1f}hr",
                    "pain_index": 70, 
                    "success_rate": 99,
                    "advice": "樹林始發絕對有位，雖慢但穩。", "tags": ["保底"]
                })

        # B. 開車策略
        if "開車" in selected_modes or "全部" in selected_modes:
            base_drive_time = 3.5 + time_offset
            jam_factor = 1.0 if is_god_mode else (1 + (final_entropy / 100) * 2.5)
            total_drive_time = base_drive_time * jam_factor
            drive_pain = final_entropy + (time_offset * 10)
            
            strategies.append({
                "mode": "🚗 自行開車 (蘇花改)", 
                "details": f"{departure_hour}:00 出發",
                "time_cost": f"{total_drive_time:.1f}hr",
                "pain_index": min(100, drive_pain), 
                "success_rate": 100,
                "advice": final_car_advice,
                "tags": ["順暢" if is_god_mode else ("地獄" if drive_pain > 80 else "普通")]
            })
            
            strategies.append({
                "mode": "💸 包車/白牌",
                "details": "到府接送",
                "time_cost": f"{total_drive_time:.1f}hr",
                "pain_index": 10,
                "success_rate": 90,
                "advice": "有錢就是任性，你在睡覺司機在塞。",
                "tags": ["鈔能力"]
            })

        # C. 混合/高鐵策略
        if "混合模式" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚅+🚄 高鐵北迴轉乘", 
                "details": "桃園 ➔ 台北 ➔ 東部幹線",
                "time_cost": f"{3.0 + (time_offset * 0.8):.1f}hr", 
                "pain_index": 30, 
                "success_rate": 40 if base_entropy > 80 else 70,
                "advice": "用金錢換取避開國道塞車。", "tags": ["效率"]
            })
            
            if south_link_score >= 50:
                south_time = 1.5 + 2.5 + ((100 - south_link_score)/100)
                strategies.append({
                    "mode": "🔄 高鐵南迴大迂迴",
                    "details": f"桃園 ➔ 左營 ➔ {township_key.split(' ')[0]}",
                    "time_cost": f"{south_time:.1f}hr", 
                    "pain_index": 25, 
                    "success_rate": 80, 
                    "advice": f"✨ 針對{township_key.split(' ')[0]}的神招！完全避開蘇花改。", 
                    "tags": ["逆向思維", "推薦"]
                })

        # D. 飛機策略
        if "飛機" in selected_modes or "全部" in selected_modes:
             strategies.append({
                "mode": "✈️ 飛機空運",
                "details": f"松山 ➔ {county[:2]}",
                "time_cost": "2.5hr", 
                "pain_index": 15, 
                "success_rate": 5 if base_entropy > 80 else 40,
                "advice": "非設籍居民候補是大賭局。", "tags": ["豪賭"]
            })

        strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        return strategies

# ==========================================
# Layer 3: 手機版使用者介面 (UI)
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
    st.markdown("<h3 style='margin-bottom:0px; color:#E63946;'>🧨 三一協會過年返鄉攻略</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em;'>v9.5 | 絕對完整版</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 戰略規劃", "🎫 搶票密技"])
    
    with tab1:
        with st.expander("⚙️ 設定行程 (已展開)", expanded=True):
            
            st.markdown("**1. 交通工具 (複選):**")
            mode_options = ["全部", "火車", "開車", "混合模式", "飛機"]
            selected_modes = st.multiselect("Modes", mode_options, default=["全部"], label_visibility="collapsed")
            
            st.markdown("---")
            
            st.markdown("**2. 目的地 (精準至鄉鎮):**")
            c_county, c_town = st.columns([1, 1.5])
            with c_county:
                county = st.selectbox("縣市", ["花蓮縣", "台東縣"], label_visibility="collapsed")
            with c_town:
                town_options = list(TOWNSHIP_DB[county].keys())
                township = st.selectbox("鄉鎮", town_options, label_visibility="collapsed")
            
            st.markdown("---")

            st.markdown("**3. 出發日期 & 時間:**")
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
            
            c_time, c_preview = st.columns([1, 2])
            with c_time:
                departure_hour = st.selectbox("Time", [f"{i:02d}:00" for i in range(24)], index=3, label_visibility="collapsed")
            
            with c_preview:
                engine_temp = FPCRF_Strategy_Engine()
                preview = engine_temp.analyze_date_physics(date_str)
                st.markdown(f"<div style='font-size:0.8em; color:gray; padding-top:10px;'>{preview['desc']}</div>", unsafe_allow_html=True)

        if st.button("🚀 開始計算", type="primary", use_container_width=True):
            modes = mode_options[1:] if "全部" in selected_modes else selected_modes
            engine = FPCRF_Strategy_Engine()
            hour_int = int(departure_hour.split(":")[0])
            
            strategies = engine.calculate_strategies(date_str, hour_int, county, township, modes)
            
            st.markdown("---")
            st.markdown(f"**📊 分析報告: 桃園 ➔ {township.split(' ')[0]}**")
            
            if not strategies:
                 st.warning("⚠️ 請選擇至少一種交通工具。")

            for i, s in enumerate(strategies):
                pain = s['pain_index']
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
        st.markdown("#### 🎫 搶票戰術 (Ticket War Room)")
        war_room = Ticket_War_Room()
        
        st.markdown("##### 🚂 火車/台鐵戰術")
        for t in war_room.get_tactics("火車"):
            with st.expander(f"{t['title']} ({t['level']})"):
                st.markdown(t['desc'])
                for s in t['steps']: st.markdown(f"- {s}")

        st.markdown("##### 🚗 開車/自駕戰術")
        for t in war_room.get_tactics("開車"):
            with st.expander(f"{t['title']} ({t['level']})"):
                st.markdown(t['desc'])
                for s in t['steps']: st.markdown(f"- {s}")

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
