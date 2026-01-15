import streamlit as st

# ==========================================
# Layer 0: 頁面基礎設定
# ==========================================
st.set_page_config(
    page_title="三一協會過年返鄉攻略", 
    page_icon="🧨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 優化 (手機版面與大按鈕)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
    .stButton > button {
        border-radius: 12px; height: 3.5em; font-weight: bold; width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stVerticalBlock"] > div {border-radius: 12px; margin-bottom: 10px;}
    .origin-badge {
        background-color: #E9ECEF; color: #1F2937; padding: 6px 12px;
        border-radius: 20px; font-weight: 900; font-size: 1.1em;
        display: inline-block; margin-bottom: 10px; border: 2px solid #DEE2E6;
    }
    .step-title {
        font-size: 1.2em; font-weight: bold; color: #E63946; margin-top: 10px; margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 登入初始化
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# ==========================================
# Layer 1: 核心資料庫 (地理/時段)
# ==========================================
TOWNSHIP_DB = {
    "花蓮縣": ["花蓮市/吉安", "壽豐/鳳林", "光復/瑞穗", "玉里/富里 (南花蓮)", "豐濱 (海線)"],
    "台東縣": ["池上/關山 (縱谷)", "台東市/卑南", "成功/長濱 (海線)", "太麻里/大武 (南迴)"]
}

# ==========================================
# Layer 2: 戰略邏輯引擎 (Scenario Engine)
# ==========================================
class StrategyEngine:
    
    def get_driving_advice(self, date_str, hour):
        """邏輯 1: 如果開車，怎麼開最快"""
        # [修正] 根據 2026 真實行事曆定義塞車日 (2/13-2/15)
        is_jam_day = "2/13" in date_str or "2/14" in date_str or "2/15" in date_str
        
        # God Mode 判斷 (凌晨 3-5 點)
        if 3 <= hour <= 5:
            return "🟢 **[God Mode]** 這是唯一的「物理倖存時段」。國5全線暢通，現在出發最快。", 1.0, "暢通"
        elif 6 <= hour <= 15 and is_jam_day:
            return "🔴 **[自殺行為]** 現在是停車場時段。建議等到晚上20:00後再出發，或改走台2線濱海公路。", 2.5, "塞爆"
        elif 16 <= hour <= 20 and is_jam_day:
            return "🟠 **[痛苦緩解]** 車流開始消化，但仍會塞。建議再忍2小時，22:00後出發。", 1.5, "車多"
        else:
            return "⚪ **[一般路況]** 車流正常，隨時可出發。", 1.1, "正常"

    def get_no_ticket_strategy(self, township):
        """邏輯 2: 沒訂到票的替代方案"""
        # 判斷是否為南花蓮/台東 (適合南迴)
        is_south = "玉里" in township or "台東" in township or "池上" in township
        
        plans = []
        # Plan A: 鐵公路聯運 (通用)
        plans.append({
            "title": "🚌 方案 A: 鐵公路聯運 (最穩)",
            "route": "桃園 ➔ 台北轉運站 ➔ 羅東轉運站 ➔ 區間車往花蓮",
            "desc": "國5客運有專用道，不塞車。到羅東後，火車班次非常多，保證有位子。",
            "tags": ["推薦"]
        })
        
        # Plan B: 始發站戰術 (北部限定)
        plans.append({
            "title": "🚆 方案 B: 樹林始發站 (保底)",
            "route": "桃園 ➔ 樹林車站 ➔ 轉搭區間快",
            "desc": "不要在桃園等車！回頭搭到樹林(始發站)，有位子坐的機率大增。EMU900區間快很新很快。",
            "tags": ["省錢"]
        })
        
        # Plan C: 南迴 (針對台東/南花蓮)
        if is_south:
            plans.append({
                "title": "🔄 方案 C: 高鐵南迴 (神招)",
                "route": "桃園高鐵 ➔ 左營 ➔ 台鐵往台東/玉里",
                "desc": "完全避開北部與蘇花路段。雖然繞一圈，但這時候往台東的票比往花蓮好買。",
                "tags": ["舒適"]
            })
            
        return plans

# ==========================================
# Layer 3: 使用者介面 (Wizard UI)
# ==========================================
def main_app():
    st.markdown("<h3 style='margin:0; color:#E63946;'>🧨 三一協會過年返鄉攻略</h3>", unsafe_allow_html=True)
    st.markdown("<div class='origin-badge'>📍 桃園全區出發</div>", unsafe_allow_html=True)
    
    # ----------------------------------------
    # Step 1: 你的條件是什麼？
    # ----------------------------------------
    st.markdown("<div class='step-title'>1. 請問您的目前狀況？</div>", unsafe_allow_html=True)
    user_status = st.radio(
        "Status",
        ["🚗 我有車，準備開車返鄉", 
         "🎫 沒搶到火車票 (求救!)", 
         "✅ 已經有票了 (查詢時刻)"],
        label_visibility="collapsed"
    )
    
    # ----------------------------------------
    # Step 2: 目的地與時間
    # ----------------------------------------
    st.markdown("---")
    st.markdown("<div class='step-title'>2. 目的地與時間</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        county = st.selectbox("縣市", ["花蓮縣", "台東縣"])
        township = st.selectbox("鄉鎮", TOWNSHIP_DB[county])
    with c2:
        # [修正] 2026 正確農曆日期對照
        date_str = st.selectbox("日期", [
            "2/13 (五) 假期前1天 (下班狂奔)",
            "2/14 (六) 連假第1天 (返鄉車潮)", # [修正] 這天不是初一
            "2/15 (日) 小年夜 (最後採買)",   # [修正] 這天是小年夜
            "2/16 (一) 除夕 (圍爐)",         # [修正] 這天是除夕
            "2/17 (二) 初一 (走春)"          # [修正] 這天才是初一
        ])
        
        # 根據不同情境顯示不同時間輸入方式
        if "開車" in user_status:
            hour = st.slider("預計出發 (24h)", 0, 23, 7)
        else:
            hour = 8 # 搭車預設早上，不影響邏輯
            
    # ----------------------------------------
    # Step 3: 診斷結果 (Diagnosis)
    # ----------------------------------------
    st.markdown("---")
    
    if st.button("🚀 分析最佳策略", type="primary"):
        engine = StrategyEngine()
        
        # === 情境 A: 開車 ===
        if "開車" in user_status:
            advice, jam_factor, status = engine.get_driving_advice(date_str, hour)
            base_time = 3.5 + (1.0 if "台東" in county else 0) + (0.5 if "南花蓮" in township else 0)
            real_time = base_time * jam_factor
            
            st.markdown(f"#### 🚘 開車戰略報告")
            st.info(f"**目的地:** {township} | **日期:** {date_str.split(' ')[0]}")
            
            with st.container(border=True):
                st.markdown(f"### 預估耗時: {real_time:.1f} 小時")
                st.markdown(advice)
                
                if status == "暢通":
                    st.success("✨ 完美決策！這個時間點出發是贏家。")
                elif status == "塞爆":
                    st.error("💀 強烈建議改期！或改在 **凌晨 03:00** 出發。")
                    st.markdown("**替代方案:** 走台61 + 台2線濱海，雖然遠但車會動。")

        # === 情境 B: 沒搶到票 (救命模式) ===
        elif "沒搶到" in user_status:
            st.markdown(f"#### 🆘 沒票救援計畫")
            st.warning(f"**目標:** 前往 {township} (桃園無直達火車/客運)")
            
            strategies = engine.get_no_ticket_strategy(township)
            
            for plan in strategies:
                with st.container(border=True):
                    st.markdown(f"**{plan['title']}**")
                    st.markdown(f"📍 路線: `{plan['route']}`")
                    st.markdown(f"💡 {plan['desc']}")

        # === 情境 C: 有票 (確認) ===
        else:
            st.markdown(f"#### ✅ 行程確認")
            st.success("恭喜有票！請確認以下接駁資訊：")
            st.markdown(f"- **出發地:** 桃園/中壢火車站")
            st.markdown(f"- **抵達地:** {township}")
            
            if "豐濱" in township:
                st.info("💡 抵達花蓮站後，請轉搭 **花蓮客運 1140/1145** 往海線。")
            elif "富里" in township or "玉里" in township:
                st.info("💡 建議搭到 **玉里站** 下車，班次較多，再轉計程車或公車。")
            elif "台東" in township:
                 st.info("💡 抵達台東站後，市區公車或普悠瑪客運很方便。")
            else:
                 st.info("💡 抵達車站後，站前計程車或租車是最快選擇。")

# 登入頁面
def login_page():
    st.container(height=50, border=False)
    st.markdown("<h2 style='text-align: center;'>🔒 協會會員驗證</h2>", unsafe_allow_html=True)
    st.info("會員請向三一協會索取密碼")
    pwd = st.text_input("密碼", type="password", label_visibility="collapsed")
    if st.button("登入", type="primary"):
        if pwd == "1234":
            st.session_state['logged_in'] = True
            st.rerun()
        else: st.error("密碼錯誤")

if __name__ == "__main__":
    if not st.session_state['logged_in']: login_page()
    else: main_app()
