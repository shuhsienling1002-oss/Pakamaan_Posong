import streamlit as st
import pandas as pd

# --- 🛑 Layer 0: System Config (標題：台灣全島溫泉地圖) ---
st.set_page_config(
    page_title="台灣全島溫泉地圖 Pro", 
    page_icon="♨️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 📱 Mobile CSS (針對溫泉主題優化視覺) ---
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: "PingFang TC", "Microsoft JhengHei", sans-serif; }
    
    /* 卡片設計 - 溫泉暖色系 */
    .mobile-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #ffccbc; /* 淺橘色邊框 */
        box-shadow: 0 4px 12px rgba(255, 87, 34, 0.08);
        position: relative;
    }
    
    .recommend-badge {
        position: absolute; top: 0; right: 0;
        background-color: #FF5722; color: white; /* 深橘色 */
        padding: 6px 16px; border-radius: 0 16px 0 16px;
        font-weight: bold; font-size: 0.85rem;
    }
    
    .free-badge {
        position: absolute; top: 0; left: 0;
        background-color: #4CAF50; color: white; /* 綠色代表免費 */
        padding: 4px 12px; border-radius: 16px 0 16px 0;
        font-weight: bold; font-size: 0.8rem;
        z-index: 10;
    }

    .card-title { font-size: 1.4rem; font-weight: 800; color: #37474f; margin-bottom: 4px; }
    
    .nav-btn {
        display: block; width: 100%; text-align: center;
        background: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%); /* 溫泉橘漸層 */
        color: white !important; padding: 12px; border-radius: 12px;
        text-decoration: none; font-weight: bold; margin-top: 15px;
    }
    
    .tag { background-color: #eceff1; color: #455a64; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; margin-right: 5px; }
    
    /* 泉質與功效區塊 */
    .spring-info-box {
        background-color: #E3F2FD; /* 淡藍色水質感 */
        border-left: 5px solid #2196F3;
        padding: 10px 15px;
        margin-top: 10px;
        border-radius: 4px;
        color: #0D47A1;
        font-size: 0.95rem;
    }
    
    .price-tag {
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    
    .price-0 { color: #2E7D32; background: #C8E6C9; } /* 免費 */
    .price-1 { color: #0277BD; background: #B3E5FC; } /* 百元 */
    .price-2 { color: #F57C00; background: #FFE0B2; } /* 千元 */
    .price-3 { color: #C2185B; background: #F8BBD0; } /* 奢華 */

    .stDataFrame { font-size: 1.1rem; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 🛑 Layer 1: The Massive Database (全國溫泉資料庫) ---
# price_level: 0=免費, 1=百元(大眾), 2=千元(湯屋), 3=奢華
# difficulty: 1=開車即達, 3=需步行, 5=野溪健行, 10=高難度溯溪
data = [
    # --- 北部 ---
    {
        "name": "北投溫泉 (地熱谷)", "region": "北部", "type": "青磺泉/白磺泉", 
        "ph": "PH 1-2 (強酸)", "benefit": "舒緩肌肉、皮膚病",
        "desc": "捷運可達，全台最方便的溫泉區，濃郁硫磺味。", 
        "price_level": 1, "price_desc": "💲 百元~千元皆有",
        "difficulty": 1, "diff_desc": "🟢 捷運直達", 
        "tags": ["捷運可達", "博物館", "日式風情"], "lat": 25.13, "lon": 121.50
    },
    {
        "name": "陽明山冷水坑", "region": "北部", "type": "弱酸性硫磺泉", 
        "ph": "PH 6", "benefit": "足湯、促進循環",
        "desc": "國家公園內的免費公共足湯與男/女裸湯。", 
        "price_level": 0, "price_desc": "🆓 完全免費",
        "difficulty": 2, "diff_desc": "🟢 需搭公車", 
        "tags": ["免費", "足湯", "需自備毛巾"], "lat": 25.16, "lon": 121.56
    },
    {
        "name": "烏來溫泉", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7-8 (弱鹼)", "benefit": "美人湯、滋潤皮膚",
        "desc": "無色無味，泡完皮膚滑嫩，適合不喜歡硫磺味的人。", 
        "price_level": 2, "price_desc": "💲💲 景觀湯屋",
        "difficulty": 2, "diff_desc": "🟢 開車/客運", 
        "tags": ["美人湯", "老街美食", "台車"], "lat": 24.86, "lon": 121.55
    },
    {
        "name": "新竹秀巒野溪溫泉", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7", "benefit": "野趣、賞楓",
        "desc": "位於尖石鄉深山，需辦理入山證，秋季賞楓絕美。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 4, "diff_desc": "🟡 需步行下切", 
        "tags": ["野溪", "賞楓", "需辦入山證"], "lat": 24.62, "lon": 121.28
    },
     {
        "name": "宜蘭礁溪溫泉公園", "region": "北部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7.5", "benefit": "平原溫泉、交通便",
        "desc": "森林風呂裸湯非常有日本味，外圍有免費足湯。", 
        "price_level": 1, "price_desc": "💲 百元 (裸湯)",
        "difficulty": 1, "diff_desc": "🟢 火車可達", 
        "tags": ["高CP值", "免費足湯", "平地"], "lat": 24.83, "lon": 121.77
    },

    # --- 中部 ---
    {
        "name": "苗栗泰安溫泉", "region": "中部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "美人湯、紓壓",
        "desc": "群山環繞，水質優良，知名電視劇《敗犬女王》取景地。", 
        "price_level": 3, "price_desc": "💲💲💲 頂級度假",
        "difficulty": 2, "diff_desc": "🟢 山路好走", 
        "tags": ["度假村", "環境清幽", "蜜月"], "lat": 24.47, "lon": 120.97
    },
    {
        "name": "台中谷關溫泉", "region": "中部", "type": "碳酸泉", 
        "ph": "PH 7.6", "benefit": "關節炎、腸胃",
        "desc": "中橫公路指標景點，明治天皇曾來過，有歷史感。", 
        "price_level": 2, "price_desc": "💲💲 飯店林立",
        "difficulty": 2, "diff_desc": "🟢 公車可達", 
        "tags": ["歷史悠久", "鱘龍魚餐", "健行"], "lat": 24.20, "lon": 121.00
    },
    {
        "name": "南投雲品/日月潭", "region": "中部", "type": "碳酸氫鈉泉", 
        "ph": "PH 8.6", "benefit": "極致放鬆、湖景",
        "desc": "日月潭第一泉，價格極高，但在房內看湖泡湯無價。", 
        "price_level": 3, "price_desc": "💲💲💲 奢華頂級",
        "difficulty": 1, "diff_desc": "🟢 全齡友善", 
        "tags": ["湖景", "五星級", "親子"], "lat": 23.87, "lon": 120.92
    },
    
    # --- 南部 ---
    {
        "name": "台南關子嶺溫泉", "region": "南部", "type": "泥漿溫泉 (稀有)", 
        "ph": "PH 8", "benefit": "去角質、風濕",
        "desc": "世界三大泥漿溫泉之一，黑色泉水，泡完皮膚極滑。", 
        "price_level": 2, "price_desc": "💲💲 特色湯屋",
        "difficulty": 2, "diff_desc": "🟢 開車/公車", 
        "tags": ["世界稀有", "泥漿", "甕缸雞"], "lat": 23.33, "lon": 120.50
    },
    {
        "name": "屏東四重溪溫泉", "region": "南部", "type": "鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "促進循環",
        "desc": "國境之南，日治時期四大名湯之一，有免費公共足湯。", 
        "price_level": 1, "price_desc": "🆓 足湯/💲 百元",
        "difficulty": 2, "diff_desc": "🟢 車程較遠", 
        "tags": ["免費足湯", "日本親王", "落山風"], "lat": 22.09, "lon": 120.74
    },
    {
        "name": "高雄寶來溫泉", "region": "南部", "type": "碳酸氫鈉泉", 
        "ph": "PH 7.2", "benefit": "軟化角質",
        "desc": "六龜山區，經歷風災後重生，賞梅花兼泡湯。", 
        "price_level": 2, "price_desc": "💲💲 露營/湯屋",
        "difficulty": 3, "diff_desc": "🟡 山路蜿蜒", 
        "tags": ["露營", "賞花", "泛舟"], "lat": 23.11, "lon": 120.70
    },

    # --- 東部 ---
    {
        "name": "台東栗松溫泉", "region": "東部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 7", "benefit": "視覺震撼、冒險",
        "desc": "【全台最美野溪溫泉】岩壁翠綠如翡翠，枯水期限定(11-4月)。", 
        "price_level": 0, "price_desc": "🆓 野溪免費",
        "difficulty": 8, "diff_desc": "🔴 需拉繩攀岩", 
        "tags": ["最美野溪", "體力活", "枯水期限定"], "lat": 23.19, "lon": 121.03
    },
    {
        "name": "花蓮瑞穗溫泉", "region": "東部", "type": "氯化物碳酸鹽泉", 
        "ph": "PH 6-7", "benefit": "傳說生男湯",
        "desc": "全台唯一的「黃金湯」，泉水富含鐵質，遇空氣變黃色。", 
        "price_level": 2, "price_desc": "💲💲 莊園/民宿",
        "difficulty": 2, "diff_desc": "🟢 火車+租車", 
        "tags": ["黃金湯", "生男湯", "平原"], "lat": 23.49, "lon": 121.35
    },
    {
        "name": "台東知本溫泉", "region": "東部", "type": "碳酸氫鈉泉", 
        "ph": "PH 8.4", "benefit": "美白、消除疲勞",
        "desc": "東部規模最大溫泉區，飯店設施完善，適合全家。", 
        "price_level": 2, "price_desc": "💲💲 飯店林立",
        "difficulty": 1, "diff_desc": "🟢 機場/火車", 
        "tags": ["煮溫泉蛋", "森林遊樂區", "老牌"], "lat": 22.69, "lon": 121.00
    },
     {
        "name": "宜蘭鳩之澤溫泉", "region": "東部", "type": "弱鹼性碳酸泉", 
        "ph": "PH 8", "benefit": "舒暢筋骨",
        "desc": "位於太平山下，超大石頭湯屋，著名的淡藍色乳白泉水。", 
        "price_level": 1, "price_desc": "💲 百元 (大眾池)",
        "difficulty": 3, "diff_desc": "🟡 山路(易起霧)", 
        "tags": ["煮玉米", "藍色溫泉", "國家公園"], "lat": 24.53, "lon": 121.50
    }
]

# --- 🛑 Layer 2: Main Interface (Tabs) ---
st.title("♨️ 台灣全島溫泉地圖 Pro")
st.caption("全國收錄 | 價格分級 | 泉質解析 | 野溪秘境")

# 建立分頁
tab1, tab2, tab3 = st.tabs(["📋 溫泉總覽", "🕵️ 智能篩選", "⚠️ 泡湯小知識"])

# --- TAB 1: Menu View (大清單模式) ---
with tab1:
    st.markdown("### 📋 全台 15 處精選溫泉區")
    
    # 轉換為 DataFrame 供展示
    df_view = pd.DataFrame(data)
    df_display = df_view[['region', 'name', 'price_desc', 'type', 'diff_desc']].copy()
    df_display.columns = ['地區', '名稱', '價格等級', '泉質', '難度']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=500 
    )

# --- TAB 2: Planner View (智能篩選) ---
with tab2:
    with st.expander("⚙️ 設定您的泡湯需求 (點擊收合)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            selected_region = st.selectbox("📍 選擇地區", ["全部顯示", "北部", "中部", "南部", "東部"], index=0)
        with c2:
            # 價格過濾器
            budget_options = ["全部", "🆓 免費 (野溪/足湯)", "💲 百元 (大眾/平價)", "💲💲 千元 (湯屋/住宿)", "💲💲💲 奢華 (度假村)"]
            selected_budget = st.selectbox("💰 預算範圍", budget_options)

        # 難度/類型過濾
        pref_type = st.radio("🛀 偏好類型", ["不拘", "輕鬆抵達 (飯店/湯屋)", "野外冒險 (野溪溫泉)"], horizontal=True)

    # Logic Engine
    def filter_springs(spot, u_region, u_budget, u_type):
        # 1. 地區篩選
        if u_region != "全部顯示" and spot['region'] != u_region:
            return False
            
        # 2. 預算篩選
        # price_level: 0=免費, 1=百元, 2=千元, 3=奢華
        if "免費" in u_budget and spot['price_level'] != 0: return False
        if "百元" in u_budget and spot['price_level'] != 1: return False
        if "千元" in u_budget and spot['price_level'] != 2: return False
        if "奢華" in u_budget and spot['price_level'] != 3: return False
        
        # 3. 類型/難度篩選
        # 野溪通常 difficulty >= 4
        if u_type == "輕鬆抵達 (飯店/湯屋)" and spot['difficulty'] >= 4: return False
        if u_type == "野外冒險 (野溪溫泉)" and spot['difficulty'] < 4: return False
        
        return True

    results = []
    for spot in data:
        if filter_springs(spot, selected_region, selected_budget, pref_type):
            results.append(spot)
            
    # 野溪排後面，奢華排前面 (或是依照使用者需求排序，這裡預設依價格排序)
    results.sort(key=lambda x: x['price_level'], reverse=True)

    # Output Rendering
    if not results:
        st.warning("⚠️ 找不到符合條件的溫泉。建議：\n1. 切換「預算」範圍\n2. 放寬「地區」限制")
    else:
        st.markdown(f"### ✨ 推薦 {len(results)} 個最佳溫泉")
        
        for spot in results:
            # 樣式定義
            border_color = "#ffccbc"
            badge_html = ""
            
            # 免費標籤
            if spot['price_level'] == 0:
                badge_html = '<div class="free-badge">🆓 FREE</div>'
                border_color = "#C8E6C9" # 綠色邊框
            elif spot['price_level'] == 3:
                badge_html = '<div class="recommend-badge">👑 奢華精選</div>'
                border_color = "#F8BBD0" # 粉色邊框

            # 價格顏色 Class
            p_class = f"price-{spot['price_level']}"
            
            tags_html = "".join([f'<span class="tag">{t}</span>' for t in spot['tags']])
            gmap = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
            
            html_str = ""
            html_str += f'<div class="mobile-card" style="border: 2px solid {border_color};">'
            html_str += f'{badge_html}'
            html_str += f'<div class="card-title">{spot["name"]} <span class="price-tag {p_class}">{spot["price_desc"]}</span></div>'
            html_str += f'<div class="card-meta" style="margin-bottom:8px;">'
            html_str += f'<span style="color:#555;">📍 {spot["region"]}</span> | '
            html_str += f'<span style="font-weight:bold; color:#E65100;">🚶 {spot["diff_desc"]}</span>'
            html_str += f'</div>'
            
            html_str += f'<div style="color:#455a64; margin-bottom:10px;">{spot["desc"]}</div>'
            
            # --- ✨ 專業泉質區塊 ---
            html_str += f'<div class="spring-info-box">'
            html_str += f'<b>🧪 泉質：</b>{spot["type"]} ({spot["ph"]})<br>'
            html_str += f'<b>💪 功效：</b>{spot["benefit"]}'
            html_str += f'</div>'
            
            html_str += f'<div style="margin-top:10px;">{tags_html}</div>'
            html_str += f'<a href="{gmap}" target="_blank" class="nav-btn">📍 Google Maps 導航</a>'
            html_str += f'</div>'

            st.markdown(html_str, unsafe_allow_html=True)

# --- TAB 3: Knowledge (專業知識) ---
with tab3:
    st.markdown("""
    ### ⚠️ 溫泉達人須知
    
    #### 1. 泉質速查
    * **硫磺泉 (北投/陽明山)**：有臭蛋味，軟化皮膚角質，止癢解毒。**皮膚敏感者慎入**。
    * **碳酸氫鈉泉 (烏來/礁溪/知本)**：俗稱「美人湯」，無色無味，泡完皮膚滑嫩。
    * **泥漿溫泉 (關子嶺)**：灰黑色，含礦物質，去角質效果極強。
    * **碳酸泉 (谷關/四重溪)**：氣泡泉，促進血液循環，對心臟負擔較小。

    #### 2. 野溪溫泉安全守則 (重要！)
    * **季節限定**：許多野溪溫泉（如栗松）僅在**枯水期（11月-4月）**適合前往。
    * **溪水暴漲**：山區午後雷陣雨可能導致溪水瞬間暴漲，見烏雲請立即撤退。
    * **無痕山林**：野溪多無垃圾桶，請務必**帶走所有垃圾**。
    
    #### 3. 泡湯禁忌
    * 飲酒後、過度疲勞、空腹或剛吃飽請勿泡湯。
    * 每次浸泡不超過 15 分鐘，起身要慢，以免姿態性低血壓暈倒。
    """)