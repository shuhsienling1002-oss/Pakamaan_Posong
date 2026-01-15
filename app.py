import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random

# ==========================================
# Layer 0: 安全驗證與入口 (Security & Auth)
# ==========================================
class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        self.window = tk.Toplevel(master)
        self.window.title("🔒 FP-CRF 協會會員驗證")
        self.window.geometry("400x250")
        self.window.resizable(False, False)
        
        # 攔截關閉事件，強制登入或退出
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # UI 佈局
        style = ttk.Style()
        style.configure("Auth.TLabel", font=("Microsoft JhengHei", 12))
        
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="⚠️ 系統存取受限", font=("Microsoft JhengHei", 16, "bold"), foreground="red").pack(pady=10)
        ttk.Label(frame, text="會員請向協會索取密碼", style="Auth.TLabel").pack(pady=5)
        
        self.pwd_entry = ttk.Entry(frame, show="*", font=("Arial", 12))
        self.pwd_entry.pack(pady=15, fill=tk.X)
        self.pwd_entry.focus()
        
        # 綁定 Enter 鍵
        self.pwd_entry.bind('<Return>', lambda event: self.check_password())

        btn = ttk.Button(frame, text="驗證身份 (Verify)", command=self.check_password)
        btn.pack(pady=10, fill=tk.X)

    def check_password(self):
        pwd = self.pwd_entry.get()
        if pwd == "1234":
            messagebox.showinfo("Access Granted", "✅ 身份確認。歡迎進入 FP-CRF 戰略指揮部。")
            self.window.destroy()
            self.on_success() # 呼叫主程式顯示回調
        else:
            messagebox.showerror("Access Denied", "❌ 密碼錯誤。物理法則拒絕您的存取。")
            self.pwd_entry.delete(0, tk.END)

    def on_close(self):
        self.master.destroy()

# ==========================================
# Layer 1 & 2: 物理邏輯核心 (Physics Engine)
# ==========================================
class FPCRF_Strategy_Engine:
    def calculate_strategies(self, date_type, departure_hour, focus, destination):
        strategies = []
        is_peak = (date_type == "春節連假首日/除夕")
        traffic_entropy = self._get_traffic_entropy(departure_hour) if is_peak else 20
        
        # --- 基礎變量 ---
        is_taitung = (destination == "台東") # 台東的物理邏輯跟花蓮不同

        # 1. 火車直達 (Standard)
        success_rate_train = 10 if is_peak else 60
        strategies.append({
            "mode": "🚄 火車直達 (EMU3000/普悠瑪)",
            "details": f"桃園 -> {destination}",
            "time_cost": "2.5 - 3.5 hr" if not is_taitung else "4.0 - 5.0 hr",
            "pain_index": 20,
            "success_rate": success_rate_train,
            "advice": "最優解，但若是除夕，搶票難度等同中樂透。",
            "tags": ["舒適", "極難訂"]
        })

        # 2. 區間快暴力解 (Hardcore)
        strategies.append({
            "mode": "🚆 區間快車 (EMU900) 暴力接力",
            "details": f"桃園 -> 樹林(始發) -> {destination}",
            "time_cost": "4.0 hr" if not is_taitung else "6.5 hr",
            "pain_index": 65 if not is_taitung else 85, # 台東搭區間車會死人
            "success_rate": 99,
            "advice": "回到樹林/南港搶始發站座位。去花蓮可接受，去台東屁股會裂開 (Pain > 80)。",
            "tags": ["保證有車", "累"]
        })

        # 3. 高鐵轉乘戰術 (Speed Relay)
        strategies.append({
            "mode": "🚅+🚄 高鐵轉乘 (HSR Relay)",
            "details": f"桃園HSR -> 台北車站 -> 轉乘東部幹線",
            "time_cost": "3.0 hr" if not is_taitung else "4.5 hr",
            "pain_index": 30,
            "success_rate": success_rate_train + 5, # 稍微好一點因為省一段票
            "advice": "利用高鐵跳過桃園-台北的台鐵擁擠段。關鍵還是在搶台北出發的東部票。",
            "tags": ["效率", "轉乘"]
        })

        # 4. 飛機候補 (Sky Gamble) - 新增
        flight_success = 5 if is_peak else 40
        strategies.append({
            "mode": "✈️ 飛機空運 (Sky Vector)",
            "details": f"機捷 -> 松山機場(TSA) -> {destination}機場",
            "time_cost": "2.5 hr (含報到)",
            "pain_index": 15, # 最舒服
            "success_rate": flight_success,
            "advice": "立榮/華信春節加班機極少。除非你是「設籍居民」有保留位，否則現場候補是絕望的賭局。",
            "tags": ["豪賭", "看天吃飯"]
        })

        # 5. 南迴大迂迴 (The Encirclement) - 台東專用神招
        if is_taitung:
            strategies.append({
                "mode": "🔄 高鐵南下 + 南迴北上 (大迂迴)",
                "details": "桃園HSR -> 左營 -> (新自強/租車) -> 台東",
                "time_cost": "4.5 - 5.5 hr",
                "pain_index": 25, # 很舒服
                "success_rate": 75, # 票源分流
                "advice": "✨ 台東返鄉首選！避開蘇花改瓶頸。左營到台東票比台北到台東好買太多了。",
                "tags": ["逆向思維", "高成功率"]
            })
        
        # 6. 開車 (Su-Hua Corridor)
        drive_time = (3.5 if not is_taitung else 6.0) * (1 + (traffic_entropy / 100) * 3)
        strategies.append({
            "mode": "🚗 自行開車 (蘇花路廊)",
            "details": f"出發時間 {departure_hour}:00",
            "time_cost": f"{drive_time:.1f} hr",
            "pain_index": min(30 + traffic_entropy, 100),
            "success_rate": 100,
            "advice": self._get_driving_advice(departure_hour, is_peak),
            "tags": ["自主性", "塞車地獄"]
        })

        # 7. 鐵公路聯運 (Bus Strategy)
        strategies.append({
            "mode": "🚌+🚆 鐵公路聯運 (Gap Seeker)",
            "details": "桃園 -> 台北轉運站 -> 客運至羅東 -> 火車",
            "time_cost": "4.5 hr",
            "pain_index": 50,
            "success_rate": 85,
            "advice": "利用國5大客車專用道優勢。適合買不到火車票的中繼手段。",
            "tags": ["高彈性"]
        })

        # 8. 金錢換空間 (The Rich Way) - 新增
        strategies.append({
            "mode": "💸 包車/白牌/共乘 (Money Solve)",
            "details": "到府接送 -> 花東",
            "time_cost": "同開車",
            "pain_index": 10, # 你在睡覺
            "success_rate": 90, # 只要有錢
            "advice": "春節加價幅度約 1.5x - 2x。優點是你可以在車上睡覺，讓司機去承擔塞車的痛苦。",
            "tags": ["鈔能力", "輕鬆"]
        })

        # 排序邏輯
        if focus == "成功率 (只要回得去)":
            strategies.sort(key=lambda x: x['success_rate'], reverse=True)
        elif focus == "低痛苦 (舒適度)":
            strategies.sort(key=lambda x: x['pain_index'])
        else: # 效率
            # 簡單解析時間字串進行排序
            strategies.sort(key=lambda x: float(x['time_cost'].split()[0].split('-')[0]))

        return strategies

    def _get_traffic_entropy(self, hour):
        # 塞車模型
        if 2 <= hour <= 4: return 5
        if 5 <= hour <= 6: return 30
        if 7 <= hour <= 19: return 95
        if 20 <= hour <= 23: return 40
        return 10

    def _get_driving_advice(self, hour, is_peak):
        if not is_peak: return "路況正常。"
        if 2 <= hour <= 4:
            return "🌟 完美物理窗口。這是唯一的倖存區間。"
        elif 7 <= hour <= 19:
            return "💀 絕對死局。建議改走台2線或放棄開車。"
        else:
            return "⚠️ 緩衝區。要有塞 2 小時以上的心理準備。"

# ==========================================
# Layer 3: 使用者介面 (UI)
# ==========================================
class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.withdraw() # 先隱藏主視窗，等待登入
        
        # 啟動登入流程
        LoginWindow(self.root, self.show_main_app)
        
    def show_main_app(self):
        self.root.deiconify() # 顯示主視窗
        self.engine = FPCRF_Strategy_Engine()
        self.root.title("FP-CRF v6.1 (Platinum) 花東返鄉戰略指揮部")
        self.root.geometry("680x800")
        
        self._setup_styles()
        self._build_header()
        self._build_inputs()
        self._build_output()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Microsoft JhengHei", 11))
        style.configure("TButton", font=("Microsoft JhengHei", 12, "bold"))
        style.configure("Header.TLabel", font=("Microsoft JhengHei", 14, "bold"), foreground="navy")

    def _build_header(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.X)
        ttk.Label(frame, text="🧬 FP-CRF v6.1 完美花東戰略系統", style="Header.TLabel").pack()
        ttk.Label(frame, text="會員專屬版 | 含高鐵轉乘、空運、南迴迂迴算法").pack()

    def _build_inputs(self):
        input_frame = ttk.LabelFrame(self.root, text="Layer 0: 參數輸入", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # 目的地
        ttk.Label(input_frame, text="目的地:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar(value="花蓮")
        dest_cb = ttk.Combobox(input_frame, textvariable=self.dest_var, state="readonly", width=10)
        dest_cb['values'] = ("花蓮", "台東")
        dest_cb.grid(row=0, column=1, sticky=tk.W)

        # 日期
        ttk.Label(input_frame, text="時段:").grid(row=0, column=2, sticky=tk.W, padx=10)
        self.date_var = tk.StringVar(value="春節連假首日/除夕")
        date_cb = ttk.Combobox(input_frame, textvariable=self.date_var, state="readonly", width=18)
        date_cb['values'] = ("一般週末", "春節連假首日/除夕", "春節收假")
        date_cb.grid(row=0, column=3, sticky=tk.W)

        # 時間軸
        ttk.Label(input_frame, text="出發時間 (0-23):").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.hour_var = tk.IntVar(value=8)
        hour_scale = ttk.Scale(input_frame, from_=0, to=23, variable=self.hour_var, orient=tk.HORIZONTAL, length=200)
        hour_scale.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        self.hour_label = ttk.Label(input_frame, text="08:00")
        self.hour_label.grid(row=1, column=3, sticky=tk.W)
        hour_scale.configure(command=lambda x: self.hour_label.configure(text=f"{int(float(x)):02d}:00"))

        # 策略重心
        ttk.Label(input_frame, text="核心需求:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.focus_var = tk.StringVar(value="成功率 (只要回得去)")
        focus_cb = ttk.Combobox(input_frame, textvariable=self.focus_var, state="readonly", width=25)
        focus_cb['values'] = ("成功率 (只要回得去)", "低痛苦 (舒適度)", "速度 (極致效率)")
        focus_cb.grid(row=2, column=1, columnspan=3, sticky=tk.W)

        # 按鈕
        btn = ttk.Button(input_frame, text="開始運算 (Execute Simulation)", command=self.run_simulation)
        btn.grid(row=3, column=0, columnspan=4, pady=15, sticky="ew")

    def _build_output(self):
        output_frame = ttk.LabelFrame(self.root, text="Layer 1 & 2: 戰略輸出", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_area = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), height=20)
        self.result_area.pack(fill=tk.BOTH, expand=True)
        
        # 標籤樣式
        self.result_area.tag_config("best", foreground="purple", background="#EEE", font=("Consolas", 11, "bold"))
        self.result_area.tag_config("warn", foreground="red", font=("Consolas", 10, "bold"))
        self.result_area.tag_config("safe", foreground="green", font=("Consolas", 10, "bold"))
        self.result_area.tag_config("title", font=("Microsoft JhengHei", 12, "bold"))

    def run_simulation(self):
        date_type = self.date_var.get()
        hour = self.hour_var.get()
        focus = self.focus_var.get()
        dest = self.dest_var.get()

        strategies = self.engine.calculate_strategies(date_type, hour, focus, dest)
        
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, f"=== 戰略報告: 桃園 ➔ {dest} ===\n", "title")
        self.result_area.insert(tk.END, f"情境: {date_type} | 出發: {hour:02d}:00\n")
        self.result_area.insert(tk.END, f"導向: {focus}\n\n")

        for i, s in enumerate(strategies):
            rank_str = f"方案 {i+1}: {s['mode']}"
            
            # 依據排名給予顏色
            if i == 0:
                self.result_area.insert(tk.END, rank_str + " (系統推薦)\n", "best")
            else:
                self.result_area.insert(tk.END, rank_str + "\n", "title")
            
            self.result_area.insert(tk.END, f"   📍 路徑: {s['details']}\n")
            self.result_area.insert(tk.END, f"   ⏱️ 耗時: {s['time_cost']}\n")
            
            # 視覺化條
            pain_bar = "█" * (s['pain_index'] // 5)
            self.result_area.insert(tk.END, f"   🔥 痛苦: {s['pain_index']} {pain_bar}\n", "warn" if s['pain_index']>60 else "safe")
            self.result_area.insert(tk.END, f"   🎯 機率: {s['success_rate']}%\n")
            self.result_area.insert(tk.END, f"   💡 建議: {s['advice']}\n")
            self.result_area.insert(tk.END, f"   🏷️ 標籤: {', '.join(s['tags'])}\n")
            self.result_area.insert(tk.END, "-"*50 + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()
