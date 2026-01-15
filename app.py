import streamlit as st
import time

# ==========================================
# Layer 0: 頁面基礎設定 (Page Configuration)
# 設定網頁標題、圖示與手機版面優化
# ==========================================
st.set_page_config(
    page_title="三一協會過年返鄉攻略",
    page_icon="🧨",
    layout="centered",                  # 手機版建議置中，閱讀體驗較佳
    initial_sidebar_state="collapsed"   # 預設收起側邊欄，讓手機畫面更乾淨
)

# 初始化 Session State (用來記憶使用者是否已登入)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==========================================
# Layer 1 & 2: 物理邏輯運算核心 (Physics Engine)
# 包含所有交通方式的計算邏輯、痛苦指數與成功率推演
# ==========================================
class FPCRF_Strategy_Engine:
    """
    FP-CRF v6.3 策略計算引擎
    負責計算痛苦指數 (Pain Index) 與 成功率 (Survival Rate)
    """
    
    def calculate_strategies(self, date_type, departure_hour, focus, destination):
        strategies = []
        
        # --- 參數校準 (Calibration) ---
        # 判斷是否為尖峰時刻 (除夕/初一)
        is_peak = (date_type == "春節連假首日/除夕")
        
        # 獲取該時段的交通熵值 (Traffic Entropy)
        traffic_entropy = self._get_traffic_entropy(departure_hour) if is_peak else 20
        
        # 判斷目的地 (台東的物理距離與策略不同)
        is_taitung = (destination == "台東") 

        # ----------------------------------------
        # 策略 1: 火車直達 (Standard Train)
        # ----------------------------------------
        success_rate_train = 10 if is_peak else 60
        strategies.append({
            "mode": "🚄 火車直達 (EMU3000)",
            "details": f"桃園 ➔ {destination}",
            "time_cost": "2.5-3.5hr" if not is_taitung else "4.0-5.0hr",
            "pain_index": 20,  # 舒適度高
            "success_rate": success_rate_train,
            "advice": "除夕搶票難度極高，建議多開視窗。若搶到騰雲座艙則是王者。",
            "tags": ["舒適", "極難訂"]
        })

        # ----------------------------------------
        # 策略 2: 區間快暴力解 (Local Express)
        # ----------------------------------------
        strategies.append({
            "mode": "🚆 區間快車 (始發站戰術)",
            "details": f"桃園 ➔ 樹林/南港(始發) ➔ {destination}",
            "time_cost": "4.0hr" if not is_taitung else "6.5hr",
            "pain_index": 65 if not is_taitung else 85, # 台東搭區間車非常痛苦
            "success_rate": 99, # 只要擠得上去
            "advice": "千萬不要在桃園等車！務必回頭去搭始發車，才有位子坐。",
            "tags": ["保證有車", "累"]
        })

        # ----------------------------------------
        # 策略 3: 高鐵轉乘 (HSR Relay)
        # ----------------------------------------
        strategies.append({
            "mode": "🚅+🚄 高鐵轉乘戰術",
            "details": f"桃園HSR ➔ 台北車站 ➔ 東部幹線",
            "time_cost": "3.0hr" if not is_taitung else "4.5hr",
            "pain_index": 30,
            "success_rate": success_rate_train + 5, # 避開一段風險
            "advice": "用高鐵跳過國道塞車段，準時抵達台北轉乘，風險減半。",
            "tags": ["效率", "轉乘"]
        })

        # ----------------------------------------
        # 策略 4: 飛機空運 (Air Vector)
        # ----------------------------------------
        flight_success = 5 if is_peak else 40
        strategies.append({
            "mode": "✈️ 飛機空運 (候補)",
            "details": f"松山(TSA) ➔ {destination}",
            "time_cost": "2.5hr",
            "pain_index": 15,
            "success_rate": flight_success,
            "advice": "除非是設籍居民，否則現場候補是大賭局，不建議作為主要方案。",
            "tags": ["豪賭", "看天吃飯"]
        })

        # ----------------------------------------
        # 策略 5: 南迴大迂迴 (Encirclement)
        # *僅限台東*
        # ----------------------------------------
        if is_taitung:
            strategies.append({
                "mode": "🔄 高鐵南迴大迂迴",
                "details": "桃園HSR ➔ 左營 ➔ 台東",
                "time_cost": "4.5-5.5hr",
                "pain_index": 25, # 雖然久但很舒服
                "success_rate": 75,
                "advice": "台東人返鄉首選！完全避開蘇花改瓶頸，票源充裕。",
                "tags": ["逆向思維", "神招"]
            })
        
        # ----------------------------------------
        # 策略 6: 自行開車 (Driving)
        # ----------------------------------------
        base_time = 3.5 if not is_taitung else 6.0
        jam_factor = 1 + (traffic_entropy / 100) * 3 # 塞車係數
        drive_time = base_time * jam_factor
        
        strategies.append({
            "mode": "🚗 自行開車 (蘇花改)",
            "details": f"出發時間 {departure_hour}:00",
            "time_cost": f"{drive_time:.1f}hr",
            "pain_index": min(30 + traffic_entropy, 100),
            "success_rate": 100,
            "advice": self._get_driving_advice(departure_hour, is_peak),
            "tags": ["自主", "塞車地獄"]
        })

        # ----------------------------------------
        # 策略 7: 鐵公路聯運 (Bus Hybrid)
        # ----------------------------------------
        strategies.append({
            "mode": "🚌+🚆 鐵公路聯運",
            "details": "台北轉運站 ➔ 羅東 ➔ 火車",
            "time_cost": "4.5hr",
            "pain_index": 50,
            "success_rate": 85,
            "advice": "國5有大客車專用道。這是買不到直達火車票時的最佳中繼解。",
            "tags": ["高彈性"]
        })

        # ----------------------------------------
        # 策略 8: 鈔能力 (Money Solve)
        # ----------------------------------------
        strategies.append({
            "mode": "💸 包車/白牌 (鈔能力)",
            "details": "到府接送 ➔ 花東",
            "time_cost": "同開車",
            "pain_index": 10, # 睡覺就好
            "success_rate": 90,
            "advice": "春節加價約1.5倍。你在車上睡覺，讓司機去承擔塞車的痛苦。",
            "tags": ["輕鬆", "貴"]
        })

        # --- 排序邏輯 ---
        if focus == "成功率 (只要回得去)":
            strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        elif focus == "低痛苦 (舒適度)":
            strategies.sort(key=lambda x: x['pain_index'])
        else:
            strategies.sort(key=lambda x: float(x['time_cost'].split('hr')[0].split('-')[0]))

        return strategies

    def _get_traffic_entropy(self, hour):
        """依據春節數據庫模擬塞車熵值"""
        if 2 <= hour <= 4: return 5   # 暢通 (God Mode)
        if 5 <= hour <= 6: return 30  # 升溫
        if 7 <= hour <= 19: return 95 # 塞爆 (Red Zone)
        if 20 <= hour <= 23: return 40 # 緩解
        return 10 # 深夜

    def _get_driving_advice(self, hour, is_peak):
        """生成駕駛建議文字"""
        if not is_peak: return "路況正常。"
        if 2 <= hour <= 4: return "🌟 完美物理窗口。全天唯一的倖存區間。"
        elif 7 <= hour <= 19: return "💀 絕對死局。建議改走台2線。"
        else: return "⚠️ 緩衝區。心理準備塞2小時以上。"

# ==========================================
# Layer 3: 手機版使用者介面 (Mobile UI)
# ==========================================

def login_page():
    """顯示登入畫面"""
    st.markdown("<br><br>", unsafe_allow_html=True) # 手機版面留白
    
    st.title("🔒 三一協會會員驗證")
    st.info("請輸入協會索取的密碼")
    
    # 密碼輸入框
    password = st.text_input("密碼", type="password")
    
    # 全寬按鈕 (方便手指點擊)
    if st.button("登入系統", type="primary", use_container_width=True):
        if password == "1234":
            st.session_state['logged_in'] = True
            st.success("✅ 驗證成功！")
            time.sleep(0.5)
            st.rerun() # 重新整理頁面
        else:
            st.error("❌ 密碼錯誤，請重試。")

def main_app():
    """主應用程式畫面"""
    # 標題區
    st.title("🧨 三一協會過年返鄉攻略")
    st.caption("FP-CRF v6.3 | 2026 春節戰略版")
    st.markdown("---")
    
    # --- 側邊欄設定 (手機版會收合在漢堡選單內) ---
    with st.sidebar:
        st.header("⚙️ 參數設定")
        
        destination = st.selectbox("目的地", ["花蓮", "台東"])
        date_type = st.selectbox("日期類型", ["春節連假首日/除夕", "春節收假", "一般週末"])
        departure_hour = st.slider("預計出發時間 (24h)", 0, 23, 8)
        
        st.write(f"🕒 目前設定: {departure_hour:02d}:00 出發")
        
        focus = st.selectbox("您的優先考量", ["成功率 (只要回得去)", "低痛苦 (舒適度)", "速度 (極致效率)"])
        
        st.markdown("---")
        # 登出按鈕
        if st.button("登出系統", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- 主操作區 ---
    if st.button("🚀 開始計算攻略", type="primary", use_container_width=True):
        
        # 呼叫邏輯引擎
        engine = FPCRF_Strategy_Engine()
        strategies = engine.calculate_strategies(date_type, departure_hour, focus, destination)
        
        # 顯示結果標題
        st.markdown("### 📊 攻略報告")
        st.caption(f"路線: 桃園 ➔ {destination} | 時間: {departure_hour:02d}:00")
        
        # --- 迭代顯示每一個策略卡片 ---
        for i, s in enumerate(strategies):
            pain = s['pain_index']
            
            # [Fix]: 使用 st.container(border=True) 替代舊版 st.error()，解決 TypeError
            with st.container(border=True):
                
                # 1. 策略名稱
                st.markdown(f"**{i+1}. {s['mode']}**")
                
                # 2. 狀態燈號 (使用 columns 排列)
                col_state, col_info = st.columns([1.5, 3.5])
                
                with col_state:
                    if pain > 80:
                        st.error("🔥 痛苦")
                    elif pain < 30:
                        st.success("✨ 舒適")
                    else:
                        st.warning("⚠️ 普通")
                
                with col_info:
                    if i == 0:
                        st.caption("🏆 協會推薦最佳路徑")
                    else:
                        st.caption(f"存活率: {s['success_rate']}%")

                # 3. 詳細資訊
                st.markdown(f"📍 {s['details']}")
                st.markdown(f"_{s['advice']}_")
                
                # 4. 數據指標
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.metric("機率", f"{s['success_rate']}%")
                c2.metric("痛苦", f"{s['pain_index']}")
                c3.metric("耗時", s['time_cost'].split('hr')[0])
                
                # 5. 標籤
                tags_str = " ".join([f"`#{t}`" for t in s['tags']])
                st.markdown(tags_str)

    else:
        # 尚未點擊按鈕時的引導畫面
        st.info("👆 請點擊上方按鈕開始分析")
        st.markdown("""
        **🔎 使用說明：**
        1. 點擊左上角 **>** 圖示開啟選單。
        2. 調整您的目的地與出發時間。
        3. 點擊 **「開始計算」**。
        4. 系統將依據 FP-CRF 物理模型為您排序。
        """)

# ==========================================
# 程式入口點 (Entry Point)
# ==========================================
if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()
