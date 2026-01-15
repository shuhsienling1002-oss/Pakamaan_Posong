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
# Layer 3.5: CSS 視覺優化
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
# Layer 1: 鄉鎮地理物理資料庫 (Geo-Physics DB)
# 定義每個鄉鎮相對於「花蓮市」的距離偏移量與戰略屬性
# ==========================================
TOWNSHIP_DB = {
    "花蓮縣": {
        "北花蓮 (花蓮市/新城/吉安)": {"time_offset": 0, "south_link_score": 0, "zone": "North"},
        "中花蓮 (壽豐/鳳林/光復)": {"time_offset": 0.5, "south_link_score": 20, "zone": "Mid"},
        "海線 (豐濱)": {"time_offset": 1.0, "south_link_score": 30, "zone": "Coast"},
        "南花蓮 (瑞穗/玉里/富里)": {"time_offset": 1.5, "south_link_score": 60, "zone": "South"} # 關鍵：玉里富里走南迴有競爭力
    },
    "台東縣": {
        "縱谷線 (池上/關山/鹿野)": {"time_offset": 2.5, "south_link_score": 80, "zone": "Rift"},
        "海線 (長濱/成功/東河)": {"time_offset": 3.0, "south_link_score": 70, "zone": "Coast_TT"},
        "台東市區 (台東市/卑南)": {"time_offset": 3.5, "south_link_score": 95, "zone": "City"}, # 南迴絕對優勢
        "南迴線 (太麻里/大武)": {"time_offset": 4.0, "south_link_score": 100, "zone": "South_Link"}
    }
}

# ==========================================
# Layer 2: 物理邏輯引擎
# ==========================================
class FPCRF_Strategy_Engine:
    
    def analyze_date_physics(self, date_str):
        # 基礎日期屬性
        mapping = {
            "2/12 (四) - 假期前2天 (提早閃人)": {"entropy": 30, "desc": "🟢 舒適圈", "base_advice": "完美決策。"},
            "2/13 (五) - 假期前1天 (下班狂奔)": {"entropy": 95, "desc": "🔴 死亡交叉", "base_advice": "全台大塞車。"},
            "2/14 (六) - 假期第1天 (返鄉車潮)": {"entropy": 90, "desc": "🟠 擁塞主流", "base_advice": "早上是停車場。"},
            "2/15 (日) - 小年夜": {"entropy": 60, "desc": "🟡 緩衝期", "base_advice": "車流稍減。"},
            "2/16 (一) - 除夕 (圍爐決戰)": {"entropy": 40, "desc": "🟢 上午賭局", "base_advice": "中午沒車。"},
            "2/17 (二) - 初一": {"entropy": 75, "desc": "🟠 區域塞車", "base_advice": "景點爆炸。"},
            "2/21 (六) - 收假前1天": {"entropy": 100, "desc": "⚫ 絕對死局", "base_advice": "必死無疑。"},
            "一般平日/週末": {"entropy": 20, "desc": "⚪ 正常", "base_advice": "路況正常。"}
        }
        return mapping.get(date_str, mapping["一般平日/週末"])

    def calculate_strategies(self, date_str, departure_hour, county, township_key, selected_modes):
        strategies = []
        
        # 1. 讀取地理參數
        geo_data = TOWNSHIP_DB[county][township_key]
        time_offset = geo_data["time_offset"] # 距離花蓮市的額外車程
        south_link_score = geo_data["south_link_score"] # 南迴適配度 (0-100)
        
        # 2. 讀取日期物理
        date_physics = self.analyze_date_physics(date_str)
        base_entropy = date_physics["entropy"]
        
        # 3. God Mode 判斷
        is_god_mode = (2 <= departure_hour <= 4)
        
        if is_god_mode:
            final_entropy = 10 
            final_car_advice = "🌌 [深夜特權] 這是前往該鄉鎮唯一的『物理倖存窗口』。全速前進！"
        elif 7 <= departure_hour <= 20 and base_entropy > 60:
            final_entropy = min(100, base_entropy + 10)
            final_car_advice = f"💀 {date_physics['desc']}。開到{township_key.split(' ')[0]}會讓人崩潰。"
        else:
            final_entropy = base_entropy
            final_car_advice = f"{date_physics['desc']}。"

        # --- 策略生成 ---
        
        # A. 火車策略 (Train)
        if "火車" in selected_modes or "全部" in selected_modes:
            # 計算該鄉鎮的火車耗時 (花蓮市基準 2.5hr + 偏移)
            # 火車比開車快，偏移量打 0.8 折
            train_time = 2.5 + (time_offset * 0.8)
            
            # 搶票難度：南花蓮/台東 比 北花蓮更難買 (因為班次少)
            ticket_difficulty = 95 if base_entropy > 80 else 60
            if south_link_score > 50: ticket_difficulty += 5 # 台東票更難
            
            strategies.append({
                "mode": "🚄 火車直達 (EMU3000)", 
                "details": f"桃園 ➔ {township_key.split(' ')[0]}",
                "time_cost": f"{train_time:.1f}hr",
                "pain_index": 20,
                "success_rate": max(5, 100 - ticket_difficulty),
                "advice": f"直達{township_key.split(' ')[0]}的票極少，建議分段買到羅東/花蓮。", 
                "tags": ["舒適", "極難訂"]
            })
            
            # 區間車只建議到北花蓮，去台東搭區間車會死人
            if county == "花蓮縣" and south_link_score < 50:
                 strategies.append({
                    "mode": "🚆 區間快 (樹林始發)", 
                    "details": f"樹林 ➔ {township_key.split(' ')[0]}",
                    "time_cost": f"{train_time + 1.5:.1f}hr",
                    "pain_index": 70, 
                    "success_rate": 99,
                    "advice": "樹林始發有位子，雖然慢但保證到。", "tags": ["保底"]
                })

        # B. 開車策略 (Car)
        if "開車" in selected_modes or "全部" in selected_modes:
            # 蘇花改基準 3.5hr + 鄉鎮偏移
            base_drive_time = 3.5 + time_offset
            jam_factor = 1.0 if is_god_mode else (1 + (final_entropy / 100) * 2.5)
            total_drive_time = base_drive_time * jam_factor
            
            # 如果去台東，開車痛苦指數隨距離增加
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

        # C. 混合/高鐵南迴策略 (South Link)
        if "混合模式" in selected_modes or "全部" in selected_modes:
            # 高鐵轉乘 (北迴)
            strategies.append({
                "mode": "🚅+🚄 高鐵北迴轉乘", 
                "details": "桃園 ➔ 台北 ➔ 東部幹線",
                "time_cost": f"{3.0 + (time_offset * 0.8):.1f}hr", 
                "pain_index": 30, 
                "success_rate": 40 if base_entropy > 80 else 70,
                "advice": "避開雪隧塞車。", "tags": ["效率"]
            })
            
            # **關鍵邏輯：南迴大迂迴**
            # 只有當目的地是「南花蓮」或「台東」時，才顯示此選項
            if south_link_score >= 50:
                # 桃園->左營(1.5h) + 左營->台東/玉里(2.5-3.5h)
                south_time = 1.5 + 2.5 + ((100 - south_link_score)/100) # 估算
                
                strategies.append({
                    "mode": "🔄 高鐵南迴大迂迴",
                    "details": f"桃園 ➔ 左營 ➔ {township_key.split(' ')[0]}",
                    "time_cost": f"{south_time:.1f}hr", 
                    "pain_index": 25, 
                    "success_rate": 80, # 南迴票比北迴好買
                    "advice": f"✨ 針對{township_key.split(' ')[0]}的神招！完全避開蘇花改，票源充足。", 
                    "tags": ["逆向思維", "推薦"]
                })

        strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        return strategies

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
    st.markdown("<p style='color:gray; font-size:0.9em;'>v9.0 | 鄉鎮精準版</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 戰略規劃", "🎫 搶票密技"])
    
    with tab1:
        with st.expander("⚙️ 設定行程 (已展開)", expanded=True):
            
            st.markdown("**1. 交通工具:**")
            mode_options = ["全部", "火車", "開車", "混合模式"]
            selected_modes = st.multiselect("Modes", mode_options, default=["全部"], label_visibility="collapsed")
            
            st.markdown("---")
            
            # --- 鄉鎮選擇邏輯 ---
            st.markdown("**2. 目的地 (精準至鄉鎮):**")
            c_county, c_town = st.columns([1, 1.5])
            with c_county:
                county = st.selectbox("縣市", ["花蓮縣", "台東縣"], label_visibility="collapsed")
            with c_town:
                # 根據縣市動態載入鄉鎮選單
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
            
            # 時間與預覽
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
        
        st.markdown("##### 🚂 火車戰術")
        for t in war_room.get_tactics("火車"):
            with st.expander(f"{t['title']}"):
                st.markdown(t['desc'])
                for s in t['steps']: st.markdown(f"- {s}")

        st.markdown("##### 🚗 開車戰術")
        for t in war_room.get_tactics("開車"):
            with st.expander(f"{t['title']}"):
                st.markdown(t['desc'])
                for s in t['steps']: st.markdown(f"- {s}")

# 補回被省略的 War Room class
class Ticket_War_Room:
    def get_tactics(self, mode):
        tactics = []
        if mode == "火車":
            tactics.append({
                "title": "⚔️ 戰術 A: 拓撲切割法",
                "desc": "台鐵長途票極少，請分段買。",
                "steps": ["第一段：桃園➔宜蘭/羅東", "第二段：宜蘭/羅東➔花蓮/台東"]
            })
            tactics.append({
                "title": "🧟 戰術 B: 殭屍票回魂",
                "desc": "利用系統清票邏輯撿漏。",
                "steps": ["訂票後第3天 00:00 (未付款釋出)", "發車前14天 (退票潮)"]
            })
        elif mode == "開車":
            tactics.append({
                "title": "🌙 戰術 A: 物理時窗",
                "desc": "凌晨 03:00-05:00 是唯一解。",
                "steps": ["早上7點後出發 = 自殺行為"]
            })
        return tactics

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
