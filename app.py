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
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    .stButton > button {
        border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stVerticalBlock"] > div {border-radius: 12px; margin-bottom: 10px;}
    
    /* 日期選擇器的視覺強化 */
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
# Layer 1 & 2: 物理邏輯引擎 (Core Logic)
# 針對 2026 春節日期的「熵值」詳細定義
# ==========================================
class FPCRF_Strategy_Engine:
    
    def analyze_date_physics(self, date_str):
        """
        解析日期的物理屬性
        回傳: (熵值, 描述, 建議)
        """
        # 2026 春節：2/14(六)開始放假，2/16(一)除夕
        
        mapping = {
            "2/12 (四) - 假期前2天 (提早閃人)": 
                {"entropy": 30, "desc": "🟢 舒適圈", "advice": "完美決策。雖然要多請2天假，但你贏了全台灣 90% 的人。"},
            
            "2/13 (五) - 假期前1天 (下班狂奔)": 
                {"entropy": 95, "desc": "🔴 死亡交叉", "advice": "極度危險。全台灣的上班族都在這天晚上衝出來，國5保證紫爆。"},
            
            "2/14 (六) - 假期第1天 (返鄉車潮)": 
                {"entropy": 90, "desc": "🟠 擁塞主流", "advice": "標準塞車日。早上 6:00-14:00 是蘇花改的停車場時段。"},
            
            "2/15 (日) - 小年夜 (最後採買)": 
                {"entropy": 60, "desc": "🟡 緩衝期", "advice": "車流稍減，但各大市場周邊會卡死。"},
            
            "2/16 (一) - 除夕 (圍爐決戰)": 
                {"entropy": 40, "desc": "🟢 上午賭局", "advice": "特殊物理窗口：中午 12:00 後路上幾乎沒車(都在吃飯)，是隱藏版神時段。"},
            
            "2/17 (二) - 初一 (走春拜年)": 
                {"entropy": 75, "desc": "🟠 區域塞車", "advice": "長途尚可，但市區與景點會爆炸。"},
            
            "2/21 (六) - 收假前1天 (北返地獄)": 
                {"entropy": 100, "desc": "⚫ 絕對死局", "advice": "蘇花改北上必定回堵到崇德。除了凌晨出發，沒有活路。"},
             
            "一般平日/週末": 
                {"entropy": 20, "desc": "⚪ 正常", "advice": "路況正常，隨意安排。"}
        }
        return mapping.get(date_str, mapping["一般平日/週末"])

    def calculate_strategies(self, date_str, departure_hour, destination, selected_modes):
        strategies = []
        is_taitung = (destination == "台東")
        
        # 取得日期物理屬性
        date_physics = self.analyze_date_physics(date_str)
        traffic_entropy = date_physics["entropy"]
        
        # 根據出發時間微調 (凌晨有加成)
        if 2 <= departure_hour <= 4:
            traffic_entropy = max(10, traffic_entropy - 50) # God Mode
            time_advice = " (凌晨加成: 路況暢通)"
        elif 7 <= departure_hour <= 19 and traffic_entropy > 60:
            traffic_entropy += 10 # 尖峰懲罰
            time_advice = " (尖峰懲罰: 雪上加霜)"
        else:
            time_advice = ""

        # --- 策略生成 ---
        
        # 1. 火車
        if "火車" in selected_modes or "全部" in selected_modes:
            # 越接近假期前1天，搶票越難
            ticket_difficulty = 95 if "2/13" in date_str or "2/16" in date_str else 60
            strategies.append({
                "mode": "🚄 火車直達 (EMU3000)", "type": "火車",
                "details": f"桃園 ➔ {destination}",
                "time_cost": "3.0hr" if not is_taitung else "4.5hr",
                "pain_index": 20,
                "success_rate": 100 - ticket_difficulty,
                "advice": f"此日期搶票難度: {ticket_difficulty}%。建議使用「拓撲切割法」。", 
                "tags": ["舒適", "難訂"]
            })
            strategies.append({
                "mode": "🚆 區間快 (樹林始發)", "type": "火車",
                "details": f"樹林 ➔ {destination}",
                "time_cost": "4.5hr", "pain_index": 70, "success_rate": 99,
                "advice": "只要願意站/擠，這天保證回得去。", "tags": ["保底"]
            })

        # 2. 開車
        if "開車" in selected_modes or "全部" in selected_modes:
            base_time = 3.5 if not is_taitung else 6.0
            jam_factor = 1 + (traffic_entropy / 100) * 2.5
            strategies.append({
                "mode": "🚗 自行開車", "type": "開車",
                "details": f"{departure_hour}:00 出發",
                "time_cost": f"{base_time * jam_factor:.1f}hr",
                "pain_index": min(traffic_entropy, 100),
                "success_rate": 100,
                "advice": f"{date_physics['desc']}。{date_physics['advice']}{time_advice}",
                "tags": ["塞車風險" if traffic_entropy > 50 else "順暢"]
            })

        # 3. 混合
        if "混合模式" in selected_modes or "全部" in selected_modes:
            strategies.append({
                "mode": "🚅+🚄 高鐵轉乘", "type": "混合",
                "details": "桃園 ➔ 台北 ➔ 花東",
                "time_cost": "3.5hr", "pain_index": 30, "success_rate": 40 if traffic_entropy > 80 else 70,
                "advice": "用金錢換取避開國道塞車。", "tags": ["效率"]
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
    st.markdown("<p style='color:gray; font-size:0.9em;'>v8.0 | 2026 春節日期戰略版</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 戰略規劃", "🎫 搶票密技"])
    
    with tab1:
        with st.expander("⚙️ 設定行程 (已展開)", expanded=True):
            
            # 1. 交通工具
            st.markdown("**1. 交通工具 (複選):**")
            mode_options = ["全部", "火車", "開車", "混合模式"]
            selected_modes = st.multiselect("Modes", mode_options, default=["全部"], label_visibility="collapsed")
            
            st.markdown("---")
            
            # 2. 日期戰略 (核心修改)
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
            date_str = st.selectbox("Date", date_options, index=2, label_visibility="collapsed")
            
            # 即時顯示日期評價
            engine_preview = FPCRF_Strategy_Engine()
            preview = engine_preview.analyze_date_physics(date_str)
            st.markdown(f"<div class='date-warning'><b>📊 日期分析:</b> {preview['desc']}<br>💬 {preview['advice']}</div>", unsafe_allow_html=True)

            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**3. 目的地:**")
                destination = st.selectbox("Dest", ["花蓮", "台東"], label_visibility="collapsed")
            with c2:
                st.markdown("**4. 出發時間:**")
                departure_hour = st.selectbox("Time", [f"{i:02d}:00" for i in range(24)], index=8, label_visibility="collapsed")

        if st.button("🚀 開始計算", type="primary", use_container_width=True):
            modes = mode_options[1:] if "全部" in selected_modes else selected_modes
            engine = FPCRF_Strategy_Engine()
            hour_int = int(departure_hour.split(":")[0])
            strategies, physics = engine.calculate_strategies(date_str, hour_int, destination, modes)
            
            st.markdown("---")
            st.markdown(f"**📊 分析報告 ({date_str})**")
            
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
        st.markdown("#### 🎫 搶票戰術看板")
        st.info("台鐵/高鐵 2026 春節配票邏輯分析")
        
        st.markdown("##### ⚔️ 戰術 A: 拓撲切割 (Split Ticket)")
        st.markdown("""
        - **原理:** 台鐵長途票(桃園-花蓮)配額少，短途票多。
        - **操作:** 1. 先買 **「桃園 ➔ 羅東」**
            2. 再買 **「羅東 ➔ 花蓮」**
        - **備註:** 羅東是關鍵節點，就算第二段沒買到，從羅東站回花蓮也比從桃園站輕鬆太多。
        """)
        
        st.markdown("##### 🧟 戰術 B: 殭屍票回魂")
        st.markdown("""
        - **第一波撿漏:** 訂票日後 **第3天 00:00** (未付款釋出)。
        - **第二波撿漏:** 發車前 **14天** (退票手續費級距改變前)。
        - **最後一擊:** 發車當日早上，通常會有保留位釋出。
        """)

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
