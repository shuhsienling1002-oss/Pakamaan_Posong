import streamlit as st
import time

# ==========================================
# Layer 0: 頁面設定 (Mobile Config)
# ==========================================
st.set_page_config(
    page_title="三一協會過年返鄉攻略",
    page_icon="🧨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# Layer 3.5: CSS 視覺優化層 (App-like UI)
# ==========================================
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stButton > button {
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 100%;
    }
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 12px;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 初始化登入狀態
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1 & 2: 物理邏輯引擎 (The Core)
# 以「交通工具」為主體的邏輯設計
# ==========================================
class FPCRF_Strategy_Engine:
    def calculate_strategies(self, date_type, departure_hour, destination, selected_modes):
        strategies = []
        is_peak = (date_type == "春節連假首日/除夕")
        traffic_entropy = self._get_traffic_entropy(departure_hour) if is_peak else 20
        is_taitung = (destination == "台東") 

        # --- 定義所有可能的交通模組 ---
        
        # 1. 火車 (Train)
        if "火車" in selected_modes or "全部" in selected_modes:
            success_rate = 10 if is_peak else 60
            strategies.append({
                "mode": "🚄 火車直達 (EMU3000)",
                "type": "火車",
                "details": f"桃園 ➔ {destination} (直達)",
                "time_cost": "3.0hr" if not is_taitung else "4.5hr",
                "pain_index": 20,
                "success_rate": success_rate,
                "advice": "除夕搶票難度極高，建議多開視窗。若搶到騰雲座艙則是王者。",
                "tags": ["舒適", "極難訂"]
            })

            # 區間快 (Local Express)
            strategies.append({
                "mode": "🚆 區間快車 (始發站)",
                "type": "火車",
                "details": f"樹林/南港(始發) ➔ {destination}",
                "time_cost": "4.5hr" if not is_taitung else "7.0hr",
                "pain_index": 70 if not is_taitung else 90,
                "success_rate": 99,
                "advice": "不要在桃園等！務必回頭搭始發車才有位子。去台東會非常痛苦。",
                "tags": ["保證有車", "累"]
            })

        # 2. 混合/組合模式 (Mixed)
        if "混合模式" in selected_modes or "全部" in selected_modes:
            # 高鐵轉乘
            success_rate_hsr = 15 if is_peak else 65
            strategies.append({
                "mode": "🚅+🚄 高鐵轉乘戰術",
                "type": "混合模式",
                "details": "桃園HSR ➔ 台北車站 ➔ 東部幹線",
                "time_cost": "3.5hr",
                "pain_index": 30,
                "success_rate": success_rate_hsr,
                "advice": "用高鐵跳過國道塞車段，準時抵達台北轉乘，風險減半。",
                "tags": ["效率", "轉乘"]
            })

            # 鐵公路聯運
            strategies.append({
                "mode": "🚌+🚆 鐵公路聯運",
                "type": "混合模式",
                "details": "台北轉運站 ➔ 羅東 ➔ 火車",
                "time_cost": "4.5hr",
                "pain_index": 50,
                "success_rate": 85,
                "advice": "國5有大客車專用道。這是買不到火車票時的最佳中繼解。",
                "tags": ["高彈性"]
            })

            # 南迴 (台東限定)
            if is_taitung:
                strategies.append({
                    "mode": "🔄 高鐵南迴大迂迴",
                    "type": "混合模式",
                    "details": "桃園HSR ➔ 左營 ➔ 台東",
                    "time_cost": "5.0hr",
                    "pain_index": 25,
                    "success_rate": 75,
                    "advice": "台東人返鄉首選！完全避開蘇花改瓶頸，票源充裕。",
                    "tags": ["逆向思維", "神招"]
                })

        # 3. 開車 (Car)
        if "開車" in selected_modes or "全部" in selected_modes:
            base_time = 3.5 if not is_taitung else 6.0
            jam_factor = 1 + (traffic_entropy / 100) * 3
            strategies.append({
                "mode": "🚗 自行開車 (蘇花改)",
                "type": "開車",
                "details": f"{departure_hour}:00 出發",
                "time_cost": f"{base_time * jam_factor:.1f}hr",
                "pain_index": min(30 + traffic_entropy, 100),
                "success_rate": 100,
                "advice": self._get_driving_advice(departure_hour, is_peak),
                "tags": ["自主", "塞車地獄"]
            })

            # 包車 (Charter)
            strategies.append({
                "mode": "💸 包車/白牌 (鈔能力)",
                "type": "開車",
                "details": "到府接送 ➔ 花東",
                "time_cost": "同開車",
                "pain_index": 10,
                "success_rate": 90,
                "advice": "春節加價約1.5倍。你在車上睡覺，讓司機去承擔塞車的痛苦。",
                "tags": ["輕鬆", "貴"]
            })

        # 4. 飛機 (Plane)
        if "飛機" in selected_modes or "全部" in selected_modes:
            flight_success = 5 if is_peak else 40
            strategies.append({
                "mode": "✈️ 飛機空運 (候補)",
                "type": "飛機",
                "details": f"松山(TSA) ➔ {destination}",
                "time_cost": "2.5hr",
                "pain_index": 15,
                "success_rate": flight_success,
                "advice": "除非是設籍居民，否則現場候補是大賭局，不建議當主方案。",
                "tags": ["豪賭", "看天吃飯"]
            })

        return strategies

    def _get_traffic_entropy(self, hour):
        if 2 <= hour <= 4: return 5
        if 5 <= hour <= 6: return 30
        if 7 <= hour <= 19: return 95
        if 20 <= hour <= 23: return 40
        return 10

    def _get_driving_advice(self, hour, is_peak):
        if not is_peak: return "路況正常。"
        if 2 <= hour <= 4: return "🌟 完美物理窗口。全天唯一的倖存區間。"
        elif 7 <= hour <= 19: return "💀 絕對死局。建議改走台2線。"
        else: return "⚠️ 緩衝區。心理準備塞2小時以上。"

# ==========================================
# Layer 3: 手機版介面 (Mobile UI)
# ==========================================

def login_page():
    # 登入頁面排版
    st.container(height=50, border=False) 
    st.markdown("<h2 style='text-align: center;'>🔒 協會會員驗證</h2>", unsafe_allow_html=True)
    
    # [修正] 嚴格遵守文案要求
    st.info("會員請向三一協會索取密碼")
    
    password = st.text_input("密碼", type="password", label_visibility="collapsed", placeholder="請輸入密碼")
    
    if st.button("登入系統 (Login)", type="primary", use_container_width=True):
        if password == "1234":
            st.session_state['logged_in'] = True
            st.toast("✅ 驗證成功！")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("❌ 密碼錯誤")

def main_app():
    # App 頂部標題
    st.markdown("<h3 style='margin-bottom:0px; color:#E63946;'>🧨 三一協會過年返鄉攻略</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em; margin-top:5px;'>FP-CRF v6.6 | 交通工具戰略版</p>", unsafe_allow_html=True)
    
    # 設定區
    with st.expander("⚙️ 行程與選項設定 (點擊展開)", expanded=True):
        
        # [修正] 交通工具成為主要選項 (Multiselect)
        st.markdown("**1. 選擇您考慮的交通工具 (可複選):**")
        mode_options = ["全部", "火車", "開車", "混合模式", "飛機"]
        selected_modes = st.multiselect("交通工具", mode_options, default=["全部"], label_visibility="collapsed")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**2. 目的地:**")
            destination = st.selectbox("Dest", ["花蓮", "台東"], label_visibility="collapsed")
            st.markdown("**3. 日期:**")
            date_type = st.selectbox("Date", ["春節連假首日/除夕", "春節收假", "一般週末"], label_visibility="collapsed")
        with col2:
            st.markdown("**4. 出發時間:**")
            departure_hour = st.selectbox("Time", [f"{i:02d}:00" for i in range(24)], index=8, label_visibility="collapsed")
            st.markdown("**5. 排序依據:**")
            sort_focus = st.selectbox("Sort", ["成功率優先", "舒適度優先", "時間效率"], label_visibility="collapsed")
        
        if st.button("登出系統", help="退出"):
            st.session_state['logged_in'] = False
            st.rerun()

    # 主操作按鈕
    hour_int = int(departure_hour.split(":")[0])
    
    if st.button("🚀 開始計算最佳路徑", type="primary", use_container_width=True):
        
        # 處理 "全部" 選項邏輯
        modes_to_query = mode_options[1:] if "全部" in selected_modes else selected_modes
        if not modes_to_query: # 防止使用者什麼都沒選
            modes_to_query = mode_options[1:]

        # 呼叫邏輯引擎
        engine = FPCRF_Strategy_Engine()
        strategies = engine.calculate_strategies(date_type, hour_int, destination, modes_to_query)
        
        # 排序邏輯 (移到 UI 層處理，更靈活)
        if sort_focus == "成功率優先":
            strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        elif sort_focus == "舒適度優先":
            strategies.sort(key=lambda x: x['pain_index']) # 越低越好
        else:
            strategies.sort(key=lambda x: float(x['time_cost'].split('hr')[0]))

        st.markdown("---")
        st.markdown(f"**📊 分析報告 ({len(strategies)} 種方案)**")
        
        if not strategies:
            st.warning("⚠️ 沒有符合您選定交通工具的方案，請增加選項。")

        # 顯示卡片列表
        for i, s in enumerate(strategies):
            pain = s['pain_index']
            
            # 定義動態顏色
            bg_color = "#ffffff"
            icon = "🔹"
            
            if pain > 80:
                bg_color = "#FFF5F5" # 紅
                icon = "🔥"
            elif pain < 30:
                bg_color = "#F0FFF4" # 綠
                icon = "✨"
            elif i == 0:
                bg_color = "#F0F8FF" # 藍 (推薦)
                icon = "🏆"
                
            # 卡片本體
            with st.container(border=True):
                # 上半部：標題 (顯示交通工具類型)
                c1, c2 = st.columns([4, 1.5])
                with c1:
                    st.markdown(f"**{icon} {s['mode']}**")
                    st.caption(f"{s['type']} | {s['details']}")
                with c2:
                    st.markdown(f"<div style='text-align:right; font-weight:bold; color:#2A9D8F; font-size:1.1em;'>{s['success_rate']}%</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:right; font-size:0.7em; color:gray;'>成功率</div>", unsafe_allow_html=True)

                # 中間：詳細建議
                st.markdown(f"""
                <div style='background-color:{bg_color}; padding:10px; border-radius:8px; font-size:0.9em; margin: 8px 0;'>
                    💡 {s['advice']}
                </div>
                """, unsafe_allow_html=True)
                
                # 底部：數據與標籤
                c_bottom_1, c_bottom_2 = st.columns([1, 1])
                with c_bottom_1:
                     st.markdown(f"⏱️ **{s['time_cost']}**")
                with c_bottom_2:
                     st.markdown(f"😖 痛苦: **{s['pain_index']}**")
                
                # 標籤列
                tags_html = "".join([f"<span style='background:#eee; padding:2px 6px; border-radius:4px; font-size:0.75em; margin-right:4px;'>#{t}</span>" for t in s['tags']])
                st.markdown(f"<div style='margin-top:5px;'>{tags_html}</div>", unsafe_allow_html=True)

# ==========================================
# 程式入口
# ==========================================
if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
