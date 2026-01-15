import streamlit as st
import pandas as pd

# ==========================================
# Layer 0: 頁面基礎設定
# ==========================================
st.set_page_config(
    page_title="三一協會過年返鄉攻略", 
    page_icon="🧨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 優化 (針對字體大小進行特化調整)
st.markdown("""
<style>
    /* 隱藏預設元素 */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    
    /* 容器調整 */
    .block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
    
    /* === 1. 分頁標籤 (Tabs) 字體放大 === */
    button[data-baseweb="tab"] div p {
        font-size: 1.3rem !important; /* 加大 Tab 字體 */
        font-weight: 700 !important;
    }
    
    /* === 2. 按鈕 (Button) 字體放大 === */
    .stButton > button {
        border-radius: 12px; 
        height: 3.8em; 
        font-weight: bold; 
        font-size: 1.3rem !important; /* 加大按鈕字體 */
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* === 3. 輸入框與提示框 (Input & Alert) 字體放大 === */
    .stTextInput input {
        font-size: 1.2rem !important;
    }
    div[data-baseweb="notification"] div {
        font-size: 1.1rem !important; /* 加大藍色提示框文字 */
        font-weight: 600;
    }
    
    /* === 4. 標題與其他元素 === */
    h2 {
        font-size: 2.2rem !important; /* 加大 H2 標題 */
    }
    
    /* 資訊卡片風格 */
    .info-card {
        background-color: #F8F9FA;
        border-left: 5px solid #E63946;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-size: 1.1rem; /* 卡片內文也稍微加大 */
    }

    /* 標籤徽章 */
    .origin-badge {
        background-color: #E9ECEF; color: #1F2937; padding: 4px 12px;
        border-radius: 16px; font-weight: 900; font-size: 0.9em;
        display: inline-block; margin-bottom: 5px; border: 1px solid #CED4DA;
    }
</style>
""", unsafe_allow_html=True)

# 登入狀態管理
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# ==========================================
# Layer 1: 核心資料庫 (物理限制與數據)
# ==========================================
TOWNSHIP_DB = {
    "花蓮縣": ["花蓮市/吉安", "壽豐/鳳林", "光復/瑞穗", "玉里/富里 (南花蓮)", "豐濱 (海線)"],
    "台東縣": ["池上/關山 (縱谷)", "台東市/卑南", "成功/長濱 (海線)", "太麻里/大武 (南迴)"]
}

# 2026 模擬時刻表 (針對熱門時段優化顯示)
TRAIN_DATA = [
    {"類型": "區間快", "車次": "4006", "桃園開": "05:50", "花蓮到": "08:25", "特徵": "早鳥保底"},
    {"類型": "普悠瑪", "車次": "402",   "桃園開": "06:15", "花蓮到": "08:20", "特徵": "熱門"},
    {"類型": "自強3000", "車次": "408", "桃園開": "07:30", "花蓮到": "09:35", "特徵": "👑 秒殺王"},
    {"類型": "自強3000", "車次": "426", "桃園開": "12:30", "花蓮到": "14:35", "特徵": "午餐車"},
    {"類型": "自強3000", "車次": "434", "桃園開": "17:15", "花蓮到": "19:25", "特徵": "下班首選"},
    {"類型": "普悠瑪", "車次": "282",   "桃園開": "18:10", "花蓮到": "20:15", "特徵": "晚餐車"},
    {"類型": "太魯閣", "車次": "248",   "桃園開": "20:10", "花蓮到": "22:20", "特徵": "末班快車"},
]

# ==========================================
# Layer 2: 戰略邏輯引擎 (含高承載與安全閥)
# ==========================================
class StrategyEngine:
    
    def get_driving_advice(self, date_str, hour):
        """邏輯 1: 開車策略 (加入高承載管制判定)"""
        # 假設 2026 春節高承載為 2/14-15 的 05:00-12:00
        is_hov_time = ("2/14" in date_str or "2/15" in date_str) and (5 <= hour < 12)
        is_jam_day = "2/13" in date_str or "2/14" in date_str or "2/15" in date_str
        
        advice = {}
        
        # 1. 高承載檢查 (物理硬限制)
        if is_hov_time:
            advice['hov_warning'] = "⛔ **觸發高承載管制 (05-12)**：車上未滿 3 人將無法上國道5號！"
        else:
            advice['hov_warning'] = None

        # 2. 路況判定
        if 3 <= hour <= 5:
            advice['status'] = "🟢 God Mode (神之領域)"
            advice['desc'] = "這是唯一的「物理倖存時段」。全線暢通，現在出發你是贏家。"
            advice['jam_factor'] = 1.0
        elif 6 <= hour <= 15 and is_jam_day:
            advice['status'] = "🔴 Suicide Run (停車場模式)"
            advice['desc'] = "國5現在是大型停車場。建議等到晚上 22:00 後再出發，或改走台2線濱海(雖遠但會動)。"
            advice['jam_factor'] = 2.8
        elif 16 <= hour <= 21 and is_jam_day:
            advice['status'] = "🟠 Struggle (痛苦緩解中)"
            advice['desc'] = "車流開始緩慢移動，但仍需排隊進雪隧。建議先吃晚餐，忍到 22:00 後。"
            advice['jam_factor'] = 1.8
        else:
            advice['status'] = "⚪ Normal (一般路況)"
            advice['desc'] = "車流正常，注意車距即可。"
            advice['jam_factor'] = 1.1
            
        return advice

    def get_transfer_strategy(self, township, hour, county):
        """邏輯 2: 沒票救援 (含轉乘風險計算)"""
        # 羅東轉運站末班車死線
        deadlines = {"花蓮縣": 22, "台東縣": 19} 
        deadline = deadlines.get(county, 21)
        
        # 估算抵達羅東的時間 (出發+3.5hr)
        arrival_luodong = hour + 3.5
        is_safe = arrival_luodong < deadline
        
        plans = []
        
        # 方案 A: 鐵公路聯運
        if is_safe:
            plans.append({
                "title": "🚌 方案 A: 鐵公路聯運 (推薦)",
                "icon": "✅",
                "desc": "國道客運(統聯/首都)走大客車專用道，**保證不塞車**。到羅東後，區間車像捷運一樣多。",
                "route": "桃園 ➔ 台北/板橋轉運站 ➔ 羅東 ➔ 區間車",
                "risk": "低"
            })
        else:
            plans.append({
                "title": "⛔ 方案 A (已失效)",
                "icon": "❌",
                "desc": f"太晚了！你到羅東時已經沒有往{county}的火車了。",
                "route": "此路不通",
                "risk": "極高"
            })

        # 方案 B: 樹林始發
        plans.append({
            "title": "🚆 方案 B: 逆向操作 (樹林始發)",
            "icon": "🛡️",
            "desc": "不要在桃園等！買票**逆向搭回樹林站** (東部幹線起點)，直接上車搶自由座/站票。",
            "route": "桃園 ➔ 樹林 (始發站) ➔ 花蓮/台東",
            "risk": "中 (需排隊)"
        })

        # 方案 C: 高鐵南迴 (針對台東/南花蓮)
        if "台東" in county or "玉里" in township:
            plans.append({
                "title": "🚄 方案 C: 金錢換時間 (高鐵南迴)",
                "icon": "🔄",
                "desc": "完全避開蘇花路廊。雖然繞半個台灣，但**確定性最高**，且南迴票比北迴好買。",
                "route": "桃園高鐵 ➔ 左營 ➔ 台鐵南迴線",
                "risk": "低 (傷荷包)"
            })
            
        return plans

# ==========================================
# Layer 3: 使用者介面 (Wizard UI)
# ==========================================
def main_app():
    # Header 區域
    st.markdown("<h2 style='text-align:center; color:#E63946;'>🧨 三一協會過年返鄉攻略</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6C757D;'>會員專屬 AI 決策輔助系統 v2.0</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 全局設定 (置頂)
    with st.container():
        c1, c2, c3 = st.columns([1.2, 1, 1])
        with c1:
            county = st.selectbox("📍 回哪裡？", ["花蓮縣", "台東縣"])
        with c2:
            township = st.selectbox("🏠 鄉鎮", TOWNSHIP_DB[county])
        with c3:
            date_str = st.selectbox("📅 日期", [
                "2/13 (五) 假前一天", "2/14 (六) 連假首日", 
                "2/15 (日) 小年夜", "2/16 (一) 除夕"
            ])

    # 核心功能分流 (Tabs)
    tab1, tab2, tab3 = st.tabs(["🚗 我要開車", "🎫 我沒搶到票", "✅ 我有票/查時刻"])

    engine = StrategyEngine()

    # === Tab 1: 開車決策 ===
    with tab1:
        st.write("#### 🕒 預計幾點從桃園出發？")
        hour = st.slider("拖曳選擇出發時間 (24h制)", 0, 23, 7, key="drive_slider")
        
        if st.button("🚀 分析路況", key="btn_drive", type="primary"):
            report = engine.get_driving_advice(date_str, hour)
            
            # 結果呈現
            st.markdown(f"### {report['status']}")
            
            # 進度條模擬擁塞度
            jam_val = min(100, int((report['jam_factor'] - 1) * 50))
            if jam_val < 0: jam_val = 0
            st.progress(jam_val / 100, text=f"擁塞指數: {jam_val}%")
            
            # 內容卡片
            st.markdown(f"""
            <div class="info-card">
                <b>💡 策略建議：</b><br>
                {report['desc']}
            </div>
            """, unsafe_allow_html=True)
            
            # 高承載警示
            if report['hov_warning']:
                st.error(report['hov_warning'])
                
            # 估算時間
            base_time = 3.5 + (1.0 if "台東" in county else 0)
            real_time = base_time * report['jam_factor']
            st.caption(f"🏁 預估抵達 {township} 耗時: 約 {real_time:.1f} 小時")

    # === Tab 2: 沒票救援 ===
    with tab2:
        st.write("#### 🕒 預計最快何時能出發？")
        hour_no_ticket = st.selectbox("選擇出發時間", range(6, 24), index=12, key="nt_time")
        
        if st.button("🚑 尋找替代方案", key="btn_no_ticket", type="primary"):
            strategies = engine.get_transfer_strategy(township, hour_no_ticket, county)
            
            st.write("### 📋 您的最佳撤退路徑")
            for plan in strategies:
                with st.expander(f"{plan['icon']} {plan['title']}", expanded=("推薦" in plan['title'])):
                    st.markdown(f"**路線：** `{plan['route']}`")
                    st.info(plan['desc'])
                    if plan['risk'] == "極高":
                        st.warning("⚠️ 此路徑風險極高，請勿嘗試")

    # === Tab 3: 時刻表查詢 ===
    with tab3:
        st.write("#### 🚄 參考車次 (桃園出發)")
        st.caption("僅列出熱門直達車次，完整資訊請以台鐵官網為準。")
        
        # 數據處理：Highlight 重點
        df = pd.DataFrame(TRAIN_DATA)
        st.dataframe(
            df, 
            hide_index=True,
            use_container_width=True,
            column_config={
                "特徵": st.column_config.TextColumn("特徵", help="班次特性"),
            }
        )
        
        st.markdown("---")
        st.markdown(f"**🚌 抵達 {township} 後轉乘：**")
        if "玉里" in township or "富里" in township:
             st.success("💡 建議搭到 **玉里站**，站前租車或轉乘最方便。")
        elif "豐濱" in township:
             st.success("💡 需在花蓮站轉搭 **1140/1145 客運** (海線)。")
        else:
             st.success("💡 車站前計程車充足，或請家人騎車來載。")
             
        st.link_button("🔗 前往台鐵訂票系統", "https://www.railway.gov.tw/")

# ==========================================
# Layer 0: 原始登入頁面 (Original)
# ==========================================
def login_page():
    st.container(height=50, border=False)
    # 這裡的標題也會受到 CSS 影響而變大
    st.markdown("<h2 style='text-align: center;'>🔒 會員驗證</h2>", unsafe_allow_html=True)
    st.info("請輸入協會通行碼 (1234)")
    pwd = st.text_input("密碼", type="password", label_visibility="collapsed")
    if st.button("登入系統", type="primary"):
        if pwd == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else: st.error("密碼錯誤")

if __name__ == "__main__":
    if not st.session_state['logged_in']: login_page()
    else: main_app()
