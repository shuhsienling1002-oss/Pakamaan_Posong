import streamlit as st
import time

# ==========================================
# Layer 0: 頁面設定
# ==========================================
st.set_page_config(
    page_title="三一協會過年返鄉攻略", 
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
    .origin-badge {
        background-color: #E9ECEF; color: #1F2937; padding: 8px 16px;
        border-radius: 20px; font-weight: 900; font-size: 1.2em;
        display: inline-block; margin-bottom: 15px; border: 2px solid #DEE2E6;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1: 鄉鎮資料庫 (含公車接駁資訊)
# [新增] bus_route, transfer_station
# ==========================================
TOWNSHIP_DB = {
    "花蓮縣": {
        "北花蓮 (花蓮市/新城/吉安)": {"time_offset": 0, "south_link_score": 0, "bus_info": "市區公車/計程車", "transfer": "花蓮站"},
        "中花蓮 (壽豐/鳳林/光復)": {"time_offset": 0.5, "south_link_score": 20, "bus_info": "台灣好行 303", "transfer": "花蓮站/光復站"},
        "海線 (豐濱/石梯坪)": {"time_offset": 1.5, "south_link_score": 30, "bus_info": "花蓮客運 1140/1145", "transfer": "花蓮站"},
        "南花蓮 (瑞穗/玉里/富里)": {"time_offset": 1.5, "south_link_score": 60, "bus_info": "統聯客運 1137", "transfer": "玉里站"} 
    },
    "台東縣": {
        "縱谷線 (池上/關山/鹿野)": {"time_offset": 2.5, "south_link_score": 80, "bus_info": "鼎東客運 8161/8163", "transfer": "池上/關山站"},
        "海線 (長濱/成功/東河)": {"time_offset": 3.0, "south_link_score": 70, "bus_info": "鼎東客運 8101/8102 (海線)", "transfer": "玉里站/台東站"},
        "台東市區 (台東市/卑南)": {"time_offset": 3.5, "south_link_score": 95, "bus_info": "市區公車/普悠瑪客運", "transfer": "台東站"}, 
        "南迴線 (太麻里/大武)": {"time_offset": 4.0, "south_link_score": 100, "bus_info": "國光/鼎東 8132", "transfer": "金崙/太麻里站"}
    }
}

TRAIN_SCHEDULE_DB = {
    6:  "普悠瑪 402 (06:15)", 7:  "自強3000 408 (07:30)", 8:  "自強3000 410 (07:55)",
    9:  "普悠瑪 218 (09:20)", 10: "自強3000 472 (10:05)", 11: "普悠瑪 222 (11:20)",
    12: "自強3000 426 (12:30)", 13: "太魯閣 228 (13:10)", 14: "自強3000 476 (14:10)",
    15: "普悠瑪 232 (15:20)", 16: "自強3000 432 (16:00)", 17: "自強3000 434 (17:15)",
    18: "普悠瑪 282 (18:10)", 19: "自強3000 438 (19:00)", 20: "太魯閣 248 (20:10)"
}

# ==========================================
# Layer 1.5: 搶票戰術庫 (含公車攻略)
# ==========================================
class Ticket_War_Room:
    def get_tactics(self, mode):
        tactics = []
        if mode == "火車":
            tactics.append({
                "title": "⚔️ 戰術 A: 拓撲切割法", "desc": "長途票少，請分段買。",
                "steps": ["第一段: 桃園➔羅東", "第二段: 羅東➔花蓮"]
            })
        elif mode == "公車/客運":
            tactics.append({
                "title": "🚌 戰術 A: 鐵公路聯運 (必殺技)",
                "desc": "買不到火車票時的最強備案。",
                "steps": [
                    "**第一段:** 搭客運 (葛瑪蘭/首都) 從台北到羅東 (走國5大客車專用道，不塞車)。",
                    "**第二段:** 從羅東搭區間車到花蓮 (班次極多)。",
                    "**優點:** 羅東轉運站就在火車站後站，走路 2 分鐘，無縫接軌。"
                ]
            })
            tactics.append({
                "title": "📱 戰術 B: iBus App 查班次",
                "desc": "花東公車班次少，錯過等1小時。",
                "steps": ["下載「iBus_公路客運」App", "輸入路線代碼 (如 1140, 8101) 掌握動態。"]
            })
        elif mode == "開車":
            tactics.append({
                "title": "🌙 戰術 A: 物理時窗 (God Mode)", "desc": "凌晨 03:00-05:00 是唯一解。",
                "steps": ["早上7點後出發 = 自殺行為"]
            })
        return tactics

# ==========================================
# Layer 2: 物理邏輯引擎 (Core Physics Engine)
# ==========================================
class FPCRF_Strategy_Engine:
    
    def analyze_date_physics(self, date_str):
        mapping = {
            "2/12 (四) - 假期前2天": {"entropy": 30, "desc": "🟢 舒適圈", "base_advice": "完美決策。"},
            "2/13 (五) - 假期前1天": {"entropy": 95, "desc": "🔴 死亡交叉", "base_advice": "全台大塞車。"},
            "2/14 (六) - 假期第1天": {"entropy": 90, "desc": "🟠 擁塞主流", "base_advice": "早上是停車場。"},
            "2/15 (日) - 小年夜": {"entropy": 60, "desc": "🟡 緩衝期", "base_advice": "車流稍減。"},
            "2/16 (一) - 除夕": {"entropy": 40, "desc": "🟢 上午賭局", "base_advice": "中午沒車。"},
            "2/17 (二) - 初一": {"entropy": 75, "desc": "🟠 區域塞車", "base_advice": "景點爆炸。"},
            "一般平日/週末": {"entropy": 20, "desc": "⚪ 正常", "base_advice": "路況正常。"}
        }
        return mapping.get(date_str, mapping["一般平日/週末"])

    def get_nearest_train(self, hour):
        return TRAIN_SCHEDULE_DB.get(hour, "自強3000 (一般班次)")

    def calculate_strategies(self, date_str, departure_hour, county, township_key, selected_modes):
        strategies = []
        
        geo_data = TOWNSHIP_DB[county][township_key]
        time_offset = geo_data["time_offset"]
        south_link_score = geo_data["south_link_score"]
        bus_info = geo_data.get("bus_info", "無")
        transfer_st = geo_data.get("transfer", "花蓮站")
        
        date_physics = self.analyze_date_physics(date_str)
        base_entropy = date_physics["entropy"]
        
        is_god_mode = (2 <= departure_hour <= 4)
        
        if is_god_mode:
            final_entropy = 10 
            final_car_advice = f"🌌 [深夜特權] 前往{township_key.split(' ')[0]}的唯一『物理倖存窗口』。"
        elif 7 <= departure_hour <= 20 and base_entropy > 60:
            final_entropy = min(100, base_entropy + 10)
            final_car_advice = f"💀 {date_physics['desc']}。開車會崩潰。"
        else:
            final_entropy = base_entropy
            final_car_advice = f"{date_physics['desc']}。{date_physics['base_advice']}"

        # --- 策略生成 ---
        
        # A. 火車 + 公車接駁 (Train + Bus)
        if "火車" in selected_modes or "全部" in selected_modes:
            train_time = 2.5 + (time_offset * 0.8) 
            ticket_difficulty = 95 if base_entropy > 80 else 60
            
            real_train = self.get_nearest_train(departure_hour)
            
            strategies.append({
                "mode": f"🚄 火車轉公車 ({real_train})", 
                "details": f"桃園 ➔ {transfer_st} ➔ 轉搭 {bus_info}",
                "time_cost": f"{train_time + 1.0:.1f}hr (含轉乘)", # 加轉乘時間
                "pain_index": 40, # 轉乘有痛苦
                "success_rate": max(5, 100 - ticket_difficulty),
                "advice": f"抵達{transfer_st}後，請轉搭 **{bus_info}** 前往{township_key.split(' ')[0]}。注意公車班次。", 
                "tags": ["接駁攻略", "無縫"]
            })

        # B. 公車/客運 (Bus Only / Hybrid)
        if "公車/客運" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚌 鐵公路聯運 (客運+火車)",
                "details": "桃園➔台北轉運站➔羅東➔花蓮",
                "time_cost": "4.5hr",
                "pain_index": 50,
                "success_rate": 85,
                "advice": "全程買不到票的救星。國5客運有專用道，比開車快。",
                "tags": ["必殺技", "彈性"]
            })

        # C. 開車 (Car)
        if "開車" in selected_modes or "全部" in selected_modes:
            base_drive_time = 3.5 + time_offset
            jam_factor = 1.0 if is_god_mode else (1 + (final_entropy / 100) * 2.5)
            total_drive_time = base_drive_time * jam_factor
            drive_pain = final_entropy + (time_offset * 10)
            
            strategies.append({
                "mode": "🚗 自行開車 (蘇花改)", 
                "details": f"桃園 ➔ {township_key.split(' ')[0]}",
                "time_cost": f"{total_drive_time:.1f}hr",
                "pain_index": min(100, drive_pain), 
                "success_rate": 100,
                "advice": final_car_advice,
                "tags": ["順暢" if is_god_mode else "塞車"]
            })

        # D. 混合/南迴
        if "混合模式" in selected_modes or "全部" in selected_modes:
            if south_link_score >= 50:
                south_time = 1.5 + 2.5 + ((100 - south_link_score)/100)
                strategies.append({
                    "mode": "🔄 高鐵南迴 + 公車",
                    "details": f"桃園 ➔ 左營 ➔ {township_key.split(' ')[0]}",
                    "time_cost": f"{south_time:.1f}hr", 
                    "pain_index": 25, 
                    "success_rate": 80, 
                    "advice": f"避開蘇花改，到當地再租車或搭 {bus_info}。", 
                    "tags": ["神招"]
                })

        strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        return strategies

# ==========================================
# Layer 3: 手機版 UI
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
    if password and password != "1234": st.error("❌ 密碼錯誤")

def main_app():
    st.markdown("<h3 style='margin-bottom:0px; color:#E63946;'>🧨 三一協會過年返鄉攻略</h3>", unsafe_allow_html=True)
    st.markdown("<div class='origin-badge'>📍 桃園出發</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em;'>v9.7 | 公車接駁版</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 戰略規劃", "🎫 搶票/公車密技"])
    
    with tab1:
        with st.expander("⚙️ 設定行程 (已展開)", expanded=True):
            
            # [修正] 加入公車選項
            st.markdown("**1. 交通工具 (複選):**")
            mode_options = ["全部", "火車", "公車/客運", "開車", "混合模式"]
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
            date_options = ["2/12 (四) - 假期前2天", "2/13 (五) - 假期前1天", "2/14 (六) - 假期第1天", "2/16 (一) - 除夕", "一般平日/週末"]
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
            
            if not strategies: st.warning("⚠️ 請選擇至少一種交通工具。")
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
        st.markdown("#### 🎫 搶票與公車戰術")
        war_room = Ticket_War_Room()
        
        st.markdown("##### 🚌 公車/客運戰術")
        for t in war_room.get_tactics("公車/客運"):
            with st.expander(t['title']):
                st.markdown(t['desc'])
                for s in t['steps']: st.markdown(f"- {s}")
        
        st.markdown("##### 🚂 火車戰術")
        for t in war_room.get_tactics("火車"):
            with st.expander(t['title']):
                st.markdown(t['desc'])
                for s in t['steps']: st.markdown(f"- {s}")

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
