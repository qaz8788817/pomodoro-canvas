import customtkinter as ctk
from tkinter import messagebox
import json
import os
import platform

# 系統字型判定
if platform.system() == "Windows":
    main_font_family = "Segoe UI"
elif platform.system() == "Darwin":
    main_font_family = "PingFang TC"
else:
    main_font_family = "Arial"

ctk.set_appearance_mode("light")

class PomodoroCanvasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 紫黃多巴胺配色
        self.bg_purple = "#C69FD5"      # 粉紫背景
        self.text_yellow = "#FDFDC9"    # 奶油黃字
        self.dark_purple = "#4A2E80"    # 深紫容器
        self.bar_bg = "#63439C"         # 進度條未填滿軌道
        self.pause_orange = "#FFB347"   # 暫停時的亮橘色字

        self.title("Prompt-Based Pomodoro Canvas ⏱️")
        self.geometry("820x500") # 預設大視窗比例
        self.resizable(False, False)
        self.configure(fg_color=self.bg_purple)
        
        # ✨ 初始狀態：不置頂（可以被其他程式蓋住，方便移動視窗）
        self.attributes("-topmost", False)

        self.db_file = "pomo_stats.json"
        self.data = self.load_data()

        # 馬卡龍統計條專屬顏色清單
        self.cat_colors = ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFDFBA", "#E8D7FF", "#FDFDC9"]

        # 計時器核心內部位元
        self.current_task = "Idle 💤"
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.timer_running = False
        self.timer_paused = False 
        self.timer_id = None 
        self.is_mini_mode = False 

        self.title_font = ctk.CTkFont(family=main_font_family, size=18, weight="bold")
        self.big_clock_font = ctk.CTkFont(family=main_font_family, size=48, weight="bold")
        self.body_font = ctk.CTkFont(family=main_font_family, size=13)
        self.cmd_font = ctk.CTkFont(family="Consolas" if platform.system() == "Windows" else "Courier", size=14)

        self.setup_ui()
        self.refresh_stats_ui()

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"stats": {}} 

    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def setup_ui(self):
        # 主雙欄配置外框
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=55) 
        self.main_frame.grid_columnconfigure(1, weight=45) 
        self.main_frame.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # ⏱️ 【左欄】：盲打控制與番茄鐘畫布
        # =====================================================================
        self.left_column = ctk.CTkFrame(self.main_frame, fg_color=self.dark_purple, corner_radius=12)
        self.left_column.grid(row=0, column=0, padx=(0, 10), sticky="nsew", pady=5)

        self.lbl_pomo_title = ctk.CTkLabel(self.left_column, text="⏱️ Pomodoro Canvas", font=self.title_font, text_color=self.text_yellow)
        self.lbl_pomo_title.pack(pady=(20, 5))
        
        self.lbl_task_status = ctk.CTkLabel(self.left_column, text=f"Current: {self.current_task}", font=self.body_font, text_color=self.text_yellow)
        self.lbl_task_status.pack()

        # 大時鐘數字（點擊可切換放大/縮小模式）
        self.lbl_clock = ctk.CTkLabel(self.left_column, text="00:00", font=self.big_clock_font, text_color=self.text_yellow, cursor="hand2")
        self.lbl_clock.pack(pady=15)
        self.lbl_clock.bind("<Button-1>", lambda e: self.toggle_view_mode())

        self.pomo_progress = ctk.CTkProgressBar(self.left_column, height=12, progress_color=self.text_yellow, fg_color=self.bar_bg)
        self.pomo_progress.pack(fill="x", padx=40, pady=5)
        self.pomo_progress.set(0)

        self.lbl_cmd_tips = ctk.CTkLabel(self.left_column, text="Commands: /todo [task] [min] | /p (pause) | /r (resume) | /reset", font=self.body_font, text_color=self.text_yellow)
        self.lbl_cmd_tips.pack(pady=(25, 2))
        
        # 盲打輸入框
        self.ent_cmd = ctk.CTkEntry(self.left_column, placeholder_text="Type command here...", font=self.cmd_font, fg_color="#FFFFFF", text_color="#000000", height=35)
        self.ent_cmd.pack(fill="x", padx=40, pady=(0, 20))
        self.ent_cmd.bind("<Return>", self.parse_command) 
        self.ent_cmd.focus() 

        # =====================================================================
        # 📊 【右欄】：大數據專注統計牆
        # =====================================================================
        self.right_column = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_column.grid(row=0, column=1, padx=(10, 0), sticky="nsew", pady=5)

        self.lbl_stats_title = ctk.CTkLabel(self.right_column, text="📊 Focus Statistics (Hours)", font=self.title_font, text_color=self.dark_purple)
        self.lbl_stats_title.pack(anchor="w", padx=5, pady=(5, 5))

        self.stats_panel = ctk.CTkScrollableFrame(self.right_column, fg_color=self.dark_purple, corner_radius=12)
        self.stats_panel.pack(fill="both", expand=True)
        self.stats_panel._scrollbar.configure(width=0)
        self.stats_panel._scrollbar.pack_forget()
import customtkinter as ctk
from tkinter import messagebox
import json
import os
import platform

# 系統字型判定
if platform.system() == "Windows":
    main_font_family = "Segoe UI"
elif platform.system() == "Darwin":
    main_font_family = "PingFang TC"
else:
    main_font_family = "Arial"

ctk.set_appearance_mode("light")

class PomodoroCanvasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 紫黃多巴胺配色
        self.bg_purple = "#C69FD5"      # 粉紫背景
        self.text_yellow = "#FDFDC9"    # 奶油黃字
        self.dark_purple = "#4A2E80"    # 深紫容器
        self.bar_bg = "#63439C"         # 進度條未填滿軌道
        self.pause_orange = "#FFB347"   # 暫停時的亮橘色字

        self.title("Prompt-Based Pomodoro Canvas ⏱️")
        self.geometry("820x500") # 預設大視窗比例
        self.resizable(False, False)
        self.configure(fg_color=self.bg_purple)
        
        # ✨ 初始狀態：不置頂（可以被其他程式蓋住，方便移動視窗）
        self.attributes("-topmost", False)

        self.db_file = "pomo_stats.json"
        self.data = self.load_data()

        # 馬卡龍統計條專屬顏色清單
        self.cat_colors = ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFDFBA", "#E8D7FF", "#FDFDC9"]

        # 計時器核心內部位元
        self.current_task = "Idle 💤"
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.timer_running = False
        self.timer_paused = False 
        self.timer_id = None 
        self.is_mini_mode = False 

        self.title_font = ctk.CTkFont(family=main_font_family, size=18, weight="bold")
        self.big_clock_font = ctk.CTkFont(family=main_font_family, size=48, weight="bold")
        self.body_font = ctk.CTkFont(family=main_font_family, size=13)
        self.cmd_font = ctk.CTkFont(family="Consolas" if platform.system() == "Windows" else "Courier", size=14)

        self.setup_ui()
        self.refresh_stats_ui()

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"stats": {}} 

    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def setup_ui(self):
        # 主雙欄配置外框
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=55) 
        self.main_frame.grid_columnconfigure(1, weight=45) 
        self.main_frame.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # ⏱️ 【左欄】：盲打控制與番茄鐘畫布
        # =====================================================================
        self.left_column = ctk.CTkFrame(self.main_frame, fg_color=self.dark_purple, corner_radius=12)
        self.left_column.grid(row=0, column=0, padx=(0, 10), sticky="nsew", pady=5)

        self.lbl_pomo_title = ctk.CTkLabel(self.left_column, text="⏱️ Pomodoro Canvas", font=self.title_font, text_color=self.text_yellow)
        self.lbl_pomo_title.pack(pady=(20, 5))
        
        self.lbl_task_status = ctk.CTkLabel(self.left_column, text=f"Current: {self.current_task}", font=self.body_font, text_color=self.text_yellow)
        self.lbl_task_status.pack()

        # 大時鐘數字（點擊可切換放大/縮小模式）
        self.lbl_clock = ctk.CTkLabel(self.left_column, text="00:00", font=self.big_clock_font, text_color=self.text_yellow, cursor="hand2")
        self.lbl_clock.pack(pady=15)
        self.lbl_clock.bind("<Button-1>", lambda e: self.toggle_view_mode())

        self.pomo_progress = ctk.CTkProgressBar(self.left_column, height=12, progress_color=self.text_yellow, fg_color=self.bar_bg)
        self.pomo_progress.pack(fill="x", padx=40, pady=5)
        self.pomo_progress.set(0)

        self.lbl_cmd_tips = ctk.CTkLabel(self.left_column, text="Commands: /todo [task] [min] | /p (pause) | /r (resume) | /reset", font=self.body_font, text_color=self.text_yellow)
        self.lbl_cmd_tips.pack(pady=(25, 2))
        
        # 盲打輸入框
        self.ent_cmd = ctk.CTkEntry(self.left_column, placeholder_text="Type command here...", font=self.cmd_font, fg_color="#FFFFFF", text_color="#000000", height=35)
        self.ent_cmd.pack(fill="x", padx=40, pady=(0, 20))
        self.ent_cmd.bind("<Return>", self.parse_command) 
        self.ent_cmd.focus() 

        # =====================================================================
        # 📊 【右欄】：大數據專注統計牆
        # =====================================================================
        self.right_column = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_column.grid(row=0, column=1, padx=(10, 0), sticky="nsew", pady=5)

        self.lbl_stats_title = ctk.CTkLabel(self.right_column, text="📊 Focus Statistics (Hours)", font=self.title_font, text_color=self.dark_purple)
        self.lbl_stats_title.pack(anchor="w", padx=5, pady=(5, 5))

        self.stats_panel = ctk.CTkScrollableFrame(self.right_column, fg_color=self.dark_purple, corner_radius=12)
        self.stats_panel.pack(fill="both", expand=True)
        self.stats_panel._scrollbar.configure(width=0)
        self.stats_panel._scrollbar.pack_forget()

    # --- 📐 視窗模式動態切換邏輯 ---
    def toggle_view_mode(self):
        """點擊時鐘時，在放大與迷你模式間切換"""
        if self.is_mini_mode:
            self.switch_to_large_mode()
        else:
            self.switch_to_mini_mode()

    def switch_to_mini_mode(self):
        """將視窗收縮成精緻的 220x80 懸浮時鐘"""
        if self.is_mini_mode: return
        self.is_mini_mode = True

        # 隱藏非必要元件
        self.right_column.grid_remove() 
        self.lbl_pomo_title.pack_forget()
        self.lbl_task_status.pack_forget()
        self.pomo_progress.pack_forget()
        self.lbl_cmd_tips.pack_forget()
        self.ent_cmd.pack_forget()

        self.main_frame.pack_configure(padx=0, pady=0)
        self.left_column.grid_configure(padx=0, pady=0)
        self.left_column.configure(corner_radius=0) 
        self.lbl_clock.pack_configure(pady=10)

        self.geometry("220x80")
        self.ent_cmd.focus() 

    def switch_to_large_mode(self):
        """彈回原本的大型儀表板畫面"""
        if not self.is_mini_mode: return
        self.is_mini_mode = False

        self.geometry("820x500")
        self.left_column.configure(corner_radius=12)
        self.main_frame.pack_configure(padx=20, pady=20)
        self.left_column.grid_configure(padx=(0, 10), pady=5)

        # 重新排版元件
        self.lbl_pomo_title.pack(pady=(20, 5))
        self.lbl_task_status.pack()
        
        self.lbl_clock.pack_forget()
        self.lbl_clock.pack(pady=15)
        
        self.pomo_progress.pack(fill="x", padx=40, pady=5)
        self.lbl_cmd_tips.pack(pady=(25, 2))
        self.ent_cmd.pack(fill="x", padx=40, pady=(0, 20))

        self.right_column.grid()
        self.ent_cmd.focus()

    # --- ⌨️ 盲打命令字串解析核心 ---
    def parse_command(self, event):
        raw_cmd = self.ent_cmd.get().strip()
        self.ent_cmd.delete(0, "end") 
        
        if not raw_cmd: return

        parts = raw_cmd.split()
        main_cmd = parts[0].lower()

        # ⏸️ 暫停指令
        if main_cmd == "/p" or main_cmd == "/pause":
            if self.timer_running and not self.timer_paused:
                self.timer_paused = True
                self.lbl_clock.configure(text_color=self.pause_orange)
                if self.is_mini_mode:
                    self.lbl_clock.configure(text="PAUSE") 
            return

        # ▶️ 繼續計時指令
        if main_cmd == "/r" or main_cmd == "/resume":
            if self.timer_running and self.timer_paused:
                self.timer_paused = False
                self.lbl_clock.configure(text_color=self.text_yellow) 
                self.update_timer_clock_display()
            return

        # 🔄 重設指令
        if main_cmd == "/reset":
            self.stop_timer_logic()
            self.timer_paused = False
            self.lbl_clock.configure(text_color=self.text_yellow)
            
            # ✨ 還原時解開置頂安全鎖
            self.attributes("-topmost", False)
            
            self.switch_to_large_mode() 
            self.current_task = "Idle 💤"
            self.lbl_task_status.configure(text=f"Current: {self.current_task}")
            self.lbl_clock.configure(text="00:00")
            self.pomo_progress.set(0)
            return

        # 清除所有統計歷史資料
        if main_cmd == "/clear":
            if messagebox.askyesno("Clear Stats", "Are you sure you want to wipe out all focus history data?", parent=self):
                self.data = {"stats": {}}
                self.save_data()
                self.refresh_stats_ui()
            return

        # 建立番茄鐘
        if main_cmd == "/todo":
            if len(parts) < 3:
                messagebox.showwarning("Syntax Error", "Usage: /todo [task_name] [minutes]", parent=self)
                return
            
            minutes_str = parts[-1]
            task_name = " ".join(parts[1:-1]) 

            try:
                minutes = int(minutes_str)
                if minutes <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Minutes must be a valid positive integer!", parent=self)
                return

            self.stop_timer_logic()
            self.timer_paused = False
            self.lbl_clock.configure(text_color=self.text_yellow)

            self.current_task = task_name
            self.total_seconds = minutes * 60
            self.remaining_seconds = self.total_seconds
            self.timer_running = True
            
            self.lbl_task_status.configure(text=f"Current: {self.current_task}")
            self.update_timer_clock_display()
            self.countdown_loop()

            # ✨ 關鍵魔法：開始計時的這一刻，才將視窗強制固定在螢幕最上層，並縮小！
            self.attributes("-topmost", True)
            self.switch_to_mini_mode()
            return

        messagebox.showwarning("Unknown Command", f"Command '{main_cmd}' not found.", parent=self)

    # --- ⏱️ 計時器後台驅動邏輯 ---
    def countdown_loop(self):
        if not self.timer_running: return

        if self.timer_paused:
            self.timer_id = self.after(1000, self.countdown_loop)
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_clock_display()
            self.timer_id = self.after(1000, self.countdown_loop)
        else:
            self.timer_running = False
            task_min = round(self.total_seconds / 60)
            self.data["stats"][self.current_task] = self.data["stats"].get(self.current_task, 0) + task_min
            self.save_data()

            # ✨ 時間到！自動解開置頂安全鎖
            self.attributes("-topmost", False)
            
            self.switch_to_large_mode()
            self.refresh_stats_ui()
            messagebox.showinfo("Time's Up! 🎯", f"Great job! You've focused on '{self.current_task}' for {task_min} mins!", parent=self)
            self.current_task = "Finished 🏆"
            self.lbl_task_status.configure(text=f"Current: {self.current_task}")
            self.pomo_progress.set(1.0)

    def stop_timer_logic(self):
        self.timer_running = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer_clock_display(self):
        if self.timer_paused: return 
        mins, secs = divmod(self.remaining_seconds, 60)
        self.lbl_clock.configure(text=f"{mins:02d}:{secs:02d}")
        ratio = (self.total_seconds - self.remaining_seconds) / self.total_seconds if self.total_seconds > 0 else 0
        self.pomo_progress.set(ratio)

    # --- 📊 統計圖表動態渲染邏輯 ---
    def refresh_stats_ui(self):
        for widget in self.stats_panel.winfo_children():
            widget.destroy()

        if not self.data["stats"]:
            ctk.CTkLabel(self.stats_panel, text="No focus data captured this month.", font=self.body_font, text_color="gray").pack(pady=40)
            return

        total_minutes = sum(self.data["stats"].values())

        for idx, (task, mins) in enumerate(self.data["stats"].items()):
            hours = mins / 60.0
            color = self.cat_colors[idx % len(self.cat_colors)]
            ratio = mins / total_minutes if total_minutes > 0 else 0

            row = ctk.CTkFrame(self.stats_panel, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=6)

            lbl_name = ctk.CTkLabel(row, text=task, font=self.body_font, text_color=self.text_yellow)
            lbl_name.pack(side="left")

            lbl_val = ctk.CTkLabel(row, text=f"{hours:.1f} hrs", font=self.body_font, text_color=self.text_yellow)
            lbl_val.pack(side="right")

            prog = ctk.CTkProgressBar(self.stats_panel, height=6, progress_color=color, fg_color=self.bar_bg)
            prog.pack(fill="x", padx=10, pady=(0, 8))
            prog.set(ratio)


if __name__ == "__main__":
    app = PomodoroCanvasApp()
    app.mainloop()
    # --- 📐 視窗模式動態切換邏輯 ---
    def toggle_view_mode(self):
        """點擊時鐘時，在放大與迷你模式間切換"""
        if self.is_mini_mode:
            self.switch_to_large_mode()
        else:
            self.switch_to_mini_mode()

    def switch_to_mini_mode(self):
        """將視窗收縮成精緻的 220x80 懸浮時鐘"""
        if self.is_mini_mode: return
        self.is_mini_mode = True

        # 隱藏非必要元件
        self.right_column.grid_remove() 
        self.lbl_pomo_title.pack_forget()
        self.lbl_task_status.pack_forget()
        self.pomo_progress.pack_forget()
        self.lbl_cmd_tips.pack_forget()
        self.ent_cmd.pack_forget()

        self.main_frame.pack_configure(padx=0, pady=0)
        self.left_column.grid_configure(padx=0, pady=0)
        self.left_column.configure(corner_radius=0) 
        self.lbl_clock.pack_configure(pady=10)

        self.geometry("220x80")
        self.ent_cmd.focus() 

    def switch_to_large_mode(self):
        """彈回原本的大型儀表板畫面"""
        if not self.is_mini_mode: return
        self.is_mini_mode = False

        self.geometry("820x500")
        self.left_column.configure(corner_radius=12)
        self.main_frame.pack_configure(padx=20, pady=20)
        self.left_column.grid_configure(padx=(0, 10), pady=5)

        # 重新排版元件
        self.lbl_pomo_title.pack(pady=(20, 5))
        self.lbl_task_status.pack()
        
        self.lbl_clock.pack_forget()
        self.lbl_clock.pack(pady=15)
        
        self.pomo_progress.pack(fill="x", padx=40, pady=5)
        self.lbl_cmd_tips.pack(pady=(25, 2))
        self.ent_cmd.pack(fill="x", padx=40, pady=(0, 20))

        self.right_column.grid()
        self.ent_cmd.focus()

    # --- ⌨️ 盲打命令字串解析核心 ---
    def parse_command(self, event):
        raw_cmd = self.ent_cmd.get().strip()
        self.ent_cmd.delete(0, "end") 
        
        if not raw_cmd: return

        parts = raw_cmd.split()
        main_cmd = parts[0].lower()

        # ⏸️ 暫停指令
        if main_cmd == "/p" or main_cmd == "/pause":
            if self.timer_running and not self.timer_paused:
                self.timer_paused = True
                self.lbl_clock.configure(text_color=self.pause_orange)
                if self.is_mini_mode:
                    self.lbl_clock.configure(text="PAUSE") 
            return

        # ▶️ 繼續計時指令
        if main_cmd == "/r" or main_cmd == "/resume":
            if self.timer_running and self.timer_paused:
                self.timer_paused = False
                self.lbl_clock.configure(text_color=self.text_yellow) 
                self.update_timer_clock_display()
            return

        # 🔄 重設指令
        if main_cmd == "/reset":
            self.stop_timer_logic()
            self.timer_paused = False
            self.lbl_clock.configure(text_color=self.text_yellow)
            
            # ✨ 還原時解開置頂安全鎖
            self.attributes("-topmost", False)
            
            self.switch_to_large_mode() 
            self.current_task = "Idle 💤"
            self.lbl_task_status.configure(text=f"Current: {self.current_task}")
            self.lbl_clock.configure(text="00:00")
            self.pomo_progress.set(0)
            return

        # 清除所有統計歷史資料
        if main_cmd == "/clear":
            if messagebox.askyesno("Clear Stats", "Are you sure you want to wipe out all focus history data?", parent=self):
                self.data = {"stats": {}}
                self.save_data()
                self.refresh_stats_ui()
            return

        # 建立番茄鐘
        if main_cmd == "/todo":
            if len(parts) < 3:
                messagebox.showwarning("Syntax Error", "Usage: /todo [task_name] [minutes]", parent=self)
                return
            
            minutes_str = parts[-1]
            task_name = " ".join(parts[1:-1]) 

            try:
                minutes = int(minutes_str)
                if minutes <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Minutes must be a valid positive integer!", parent=self)
                return

            self.stop_timer_logic()
            self.timer_paused = False
            self.lbl_clock.configure(text_color=self.text_yellow)

            self.current_task = task_name
            self.total_seconds = minutes * 60
            self.remaining_seconds = self.total_seconds
            self.timer_running = True
            
            self.lbl_task_status.configure(text=f"Current: {self.current_task}")
            self.update_timer_clock_display()
            self.countdown_loop()

            # ✨ 關鍵魔法：開始計時的這一刻，才將視窗強制固定在螢幕最上層，並縮小！
            self.attributes("-topmost", True)
            self.switch_to_mini_mode()
            return

        messagebox.showwarning("Unknown Command", f"Command '{main_cmd}' not found.", parent=self)

    # --- ⏱️ 計時器後台驅動邏輯 ---
    def countdown_loop(self):
        if not self.timer_running: return

        if self.timer_paused:
            self.timer_id = self.after(1000, self.countdown_loop)
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_clock_display()
            self.timer_id = self.after(1000, self.countdown_loop)
        else:
            self.timer_running = False
            task_min = round(self.total_seconds / 60)
            self.data["stats"][self.current_task] = self.data["stats"].get(self.current_task, 0) + task_min
            self.save_data()

            # ✨ 時間到！自動解開置頂安全鎖
            self.attributes("-topmost", False)
            
            self.switch_to_large_mode()
            self.refresh_stats_ui()
            messagebox.showinfo("Time's Up! 🎯", f"Great job! You've focused on '{self.current_task}' for {task_min} mins!", parent=self)
            self.current_task = "Finished 🏆"
            self.lbl_task_status.configure(text=f"Current: {self.current_task}")
            self.pomo_progress.set(1.0)

    def stop_timer_logic(self):
        self.timer_running = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer_clock_display(self):
        if self.timer_paused: return 
        mins, secs = divmod(self.remaining_seconds, 60)
        self.lbl_clock.configure(text=f"{mins:02d}:{secs:02d}")
        ratio = (self.total_seconds - self.remaining_seconds) / self.total_seconds if self.total_seconds > 0 else 0
        self.pomo_progress.set(ratio)

    # --- 📊 統計圖表動態渲染邏輯 ---
    def refresh_stats_ui(self):
        for widget in self.stats_panel.winfo_children():
            widget.destroy()

        if not self.data["stats"]:
            ctk.CTkLabel(self.stats_panel, text="No focus data captured this month.", font=self.body_font, text_color="gray").pack(pady=40)
            return

        total_minutes = sum(self.data["stats"].values())

        for idx, (task, mins) in enumerate(self.data["stats"].items()):
            hours = mins / 60.0
            color = self.cat_colors[idx % len(self.cat_colors)]
            ratio = mins / total_minutes if total_minutes > 0 else 0

            row = ctk.CTkFrame(self.stats_panel, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=6)

            lbl_name = ctk.CTkLabel(row, text=task, font=self.body_font, text_color=self.text_yellow)
            lbl_name.pack(side="left")

            lbl_val = ctk.CTkLabel(row, text=f"{hours:.1f} hrs", font=self.body_font, text_color=self.text_yellow)
            lbl_val.pack(side="right")

            prog = ctk.CTkProgressBar(self.stats_panel, height=6, progress_color=color, fg_color=self.bar_bg)
            prog.pack(fill="x", padx=10, pady=(0, 8))
            prog.set(ratio)


if __name__ == "__main__":
    app = PomodoroCanvasApp()
    app.mainloop()