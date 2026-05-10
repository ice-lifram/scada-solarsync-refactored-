# ui.py - Main User Interface for Solar Mo Lang

# =========================
# IMPORTS
# =========================
import logging
import datetime
import tkinter as tk
from tkinter import font as tkfont
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import engine 

# =========================
# FONTS AND THEMES
# =========================
def get_universal_font():
    try:
        root = tk.Tk(); root.withdraw()
        available = tkfont.families(); root.destroy()
        if "Segoe UI" in available: return "Segoe UI"
        if "Ubuntu" in available: return "Ubuntu"
        return "Arial"
    except: return "sans-serif"

FONT_NAME = get_universal_font()

THEME = {
    "bg_main": "#0f172a",        # Slate 900
    "bg_sidebar": "#020617",     # Slate 950 (Deepest)
    "card": "#1e293b",           # Slate 800
    "primary": "#38bdf8",        # Sky Blue
    "text_main": "#f8fafc",      # Slate 50
    "text_sub": "#94a3b8",       # Slate 400
    "accent": "#f59e0b",         # Amber
    "border": "#334155",         # Slate 700
    "danger": "#ef4444",         # Red
    "success": "#22c55e",        # Green
    "node_bg": "#1e293b",        # For Fault Line nodes
}

# =========================
# CORE USER INTERFACE
# =========================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark") # Forced Dark Mode
        self.title("Solar Mo Lang")
        self.geometry("1200x900")
        # --- ADD THIS LINE HERE ---
        self.active_toasts = [] 
        # --------------------------
        self.model = engine.DataModel(maxlen=500)
        self._running = True
        self.xp = 1904 
        self.level = 20
        self.current_user = None
        self.user_role = "System Administrator"
        self.current_view = "Dashboard"
        
        # New Quest State
        self.active_quests = [
            {"id": 1, "title": "Peak Harvester", "desc": "Reach > 400W output for 10 mins", "progress": 0.6},
            {"id": 2, "title": "Grid Independence", "desc": "Keep Battery > 80% for 2 hours", "progress": 0.2},
            {"id": 3, "title": "Safety First", "desc": "Run thermal diagnostics", "progress": 1.0}
        ]

        self.creds = {"admin": "1234", "operator": "solar123"}
        self._build_login()

    def _build_login(self):
        self.login_frame = ctk.CTkFrame(self, fg_color=THEME["bg_main"])
        self.login_frame.pack(fill="both", expand=True)
        
        inner = ctk.CTkFrame(self.login_frame, fg_color=THEME["card"], corner_radius=15, width=450, height=500, border_width=1, border_color=THEME["border"])
        inner.place(relx=0.5, rely=0.5, anchor="center")
        inner.pack_propagate(False)
        
        ctk.CTkLabel(inner, text="☀️ Solar Mo Lang", font=(FONT_NAME, 32, "bold"), text_color=THEME["primary"]).pack(pady=(50, 10))
        ctk.CTkLabel(inner, text="Secure SML Login", font=(FONT_NAME, 14), text_color=THEME["text_sub"]).pack(pady=(0, 30))

        self.u_ent = ctk.CTkEntry(inner, placeholder_text="Username", width=300, height=45, fg_color=THEME["bg_main"], border_color=THEME["border"]); self.u_ent.pack(pady=10)
        self.p_ent = ctk.CTkEntry(inner, placeholder_text="Password", show="*", width=300, height=45, fg_color=THEME["bg_main"], border_color=THEME["border"]); self.p_ent.pack(pady=10)
        
        self.login_err = ctk.CTkLabel(inner, text="", text_color=THEME["danger"])
        self.login_err.pack(pady=5)
        
        ctk.CTkButton(inner, text="Authorize System Access", command=self._check_login, 
                      fg_color=THEME["primary"], hover_color="#0284c7", text_color="#000000", width=300, height=45).pack(pady=20)

    def _check_login(self):
        u, p = self.u_ent.get().lower(), self.p_ent.get()
        if u in self.creds and p == self.creds[u]:
            self.current_user = u.capitalize()
            self.login_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.login_frame.destroy()
            self._init_main_ui()
        else:
            self.login_err.configure(text="Invalid credentials.")

    def _init_main_ui(self):
        self._running = True
        self.configure(fg_color=THEME["bg_main"])
        
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=THEME["bg_sidebar"], corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="☀️ SolarSync", font=("Segoe UI", 22, "bold"), text_color=THEME["primary"]).pack(pady=40, padx=25, anchor="w")
        
        self.nav_btns = {}
        nav_items = [("Dashboard", "📊"), ("Fault Line", "⚡"), ("Tips & Recs", "💡"), ("Rewards", "🏆")]
        
        for item, icon in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=f"{icon}  {item}", anchor="w", fg_color="transparent", 
                                text_color=THEME["text_sub"], hover_color=THEME["card"], height=45,
                                command=lambda x=item: self.switch_view(x))
            btn.pack(fill="x", padx=15, pady=5)
            self.nav_btns[item] = btn

        user_panel = ctk.CTkFrame(self.sidebar, fg_color=THEME["card"], corner_radius=12)
        user_panel.pack(side="bottom", fill="x", padx=15, pady=30)
        ctk.CTkLabel(user_panel, text=self.current_user, font=("Segoe UI", 14, "bold")).pack(pady=(15, 0))
        ctk.CTkButton(user_panel, text="Sign Out", text_color=THEME["danger"], fg_color="transparent", command=self.destroy).pack(pady=10)

        self.view_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.view_container.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        self.switch_view("Dashboard")
        self._update_loop()

    def switch_view(self, view_name):
        self.current_view = view_name
        for name, btn in self.nav_btns.items():
            is_active = (name == view_name)
            btn.configure(fg_color=THEME["card"] if is_active else "transparent", text_color=THEME["text_main"] if is_active else THEME["text_sub"])
        
        for child in self.view_container.winfo_children(): child.destroy()
        
        header = ctk.CTkFrame(self.view_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        ctk.CTkLabel(header, text=view_name, font=("Segoe UI", 32, "bold"), text_color=THEME["text_main"]).pack(side="left")
        
        if view_name == "Dashboard": self._draw_dashboard()
        elif view_name == "Fault Line": self._draw_fault_line()
        elif view_name == "Tips & Recs": self._draw_tips()
        elif view_name == "Rewards": self._draw_rewards()

    def _draw_dashboard(self):
        # Alert Box
        self.alert_box = ctk.CTkFrame(self.view_container, fg_color="#451a03", border_width=1, border_color=THEME["accent"])
        self.alert_lbl = ctk.CTkLabel(self.alert_box, text="", text_color=THEME["accent"], font=("Segoe UI", 14, "bold"))
        self.alert_lbl.pack(pady=15)
        self.alert_box.pack_forget()

        grid = ctk.CTkFrame(self.view_container, fg_color="transparent")
        grid.pack(fill="x", pady=10); grid.columnconfigure((0,1,2,3), weight=1)
        
        self.cards = {}
        specs = [("Battery Level", "batt"), ("Solar Output", "solar"), ("Efficiency", "eff"), ("Temperature", "temp")]
        
        for i, (title, key) in enumerate(specs):
            card = ctk.CTkFrame(grid, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            ctk.CTkLabel(card, text=title, text_color=THEME["text_sub"], font=("Segoe UI", 12)).pack(pady=(20,0))
            v_lbl = ctk.CTkLabel(card, text="--", font=("Segoe UI", 28, "bold"), text_color=THEME["primary"])
            v_lbl.pack(pady=(0, 20))
            self.cards[key] = v_lbl

        # Live Chart
        chart_card = ctk.CTkFrame(self.view_container, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
        chart_card.pack(fill="both", expand=True, pady=25)
        self.fig, self.ax = plt.subplots(figsize=(10, 4), facecolor=THEME["card"])
        self.ax.set_facecolor(THEME["card"])
        self.canvas = FigureCanvasTkAgg(self.fig, chart_card)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        self.ax.set_title(
            "Battery Telemetry",
            color=THEME["text_main"],
            fontsize=14,
            fontweight="bold"
        )

        self.ax.set_xlabel(
            "Time",
            color=THEME["text_sub"],
            fontsize=10
        )

        self.ax.set_ylabel(
            "Battery %",
            color=THEME["text_sub"],
            fontsize=10
        )
    def _trigger_toast(self, message, level="danger"):
        # Safety check for the list we just added
        if not hasattr(self, 'active_toasts'): self.active_toasts = []
        
        # Prevent duplicate toasts
        for t in self.active_toasts:
            if t['msg'] == message: return

        color = THEME["danger"] if level == "danger" else THEME["accent"]
        
        # Create toast on 'self' but call lift() to put it above the scrollable frame
        toast = ctk.CTkFrame(self, fg_color=color, corner_radius=10, border_width=2, border_color="#ffffff")
        
        # Place it top-right
        toast.place(relx=0.97, rely=0.05, anchor="ne")
        
        # CRITICAL: This pulls the toast to the very front of the UI
        toast.lift() 
        
        ctk.CTkLabel(toast, text=f"⚠️ {message}", text_color="white", 
                     font=(FONT_NAME, 13, "bold"), padx=20, pady=15).pack()
        
        toast_data = {'widget': toast, 'msg': message}
        self.active_toasts.append(toast_data)
        
        self.after(5000, lambda: self._remove_toast(toast_data))
    
    def _remove_toast(self, toast_data):
        if toast_data in self.active_toasts:
            toast_data['widget'].destroy()
            self.active_toasts.remove(toast_data)

    def _draw_fault_line(self):
        # Container
        flow_container = ctk.CTkFrame(self.view_container, fg_color=THEME["bg_sidebar"], 
                                     height=550, corner_radius=15, border_width=1, border_color=THEME["border"])
        flow_container.pack(fill="x", pady=20, padx=10)
        
        # IMPORTANT: Force the UI to process the 'pack' so it has a width/height
        self.update_idletasks()

        # Canvas
        canvas = tk.Canvas(flow_container, bg=THEME["bg_sidebar"], highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        node_map = {
            "pv": ["Solar Array", 0.15, 0.5, "PV Input"],
            "inv": ["Inverter", 0.40, 0.5, "DC/AC Sync"],
            "bat": ["Battery Bank", 0.65, 0.25, "Storage"],
            "grid": ["Main Grid", 0.65, 0.75, "Utility"],
            "load": ["Home Load", 0.90, 0.5, "Consumption"]
        }

        # Use absolute coordinates derived from the forced update
        w = flow_container.winfo_width()
        h = flow_container.winfo_height()

        # Connections logic
        connections = [("pv", "inv"), ("inv", "bat"), ("inv", "grid"), ("bat", "load"), ("grid", "load")]
        
        for start, end in connections:
            x1, y1 = node_map[start][1] * w, node_map[start][2] * h
            x2, y2 = node_map[end][1] * w, node_map[end][2] * h
            canvas.create_line(x1, y1, x2, y2, fill=THEME["primary"], width=2, dash=(10, 5))

        # Create UI Nodes
        for key, data in node_map.items():
            n = ctk.CTkFrame(flow_container, fg_color=THEME["card"], width=150, height=90, 
                             corner_radius=10, border_width=1, border_color=THEME["primary"])
            # We place the frame AFTER the line is drawn to ensure it sits on top
            n.place(relx=data[1], rely=data[2], anchor="center")
            
            ctk.CTkLabel(n, text=data[0], font=(FONT_NAME, 12, "bold"), text_color=THEME["primary"]).place(relx=0.5, rely=0.3, anchor="center")
            ctk.CTkLabel(n, text=data[3], font=(FONT_NAME, 10), text_color=THEME["text_sub"]).place(relx=0.5, rely=0.6, anchor="center")
            ctk.CTkLabel(n, text="● ONLINE", font=(FONT_NAME, 9, "bold"), text_color=THEME["success"]).place(relx=0.5, rely=0.85, anchor="center")

    def _draw_tips(self):
        # Tip categories for better organization
        tip_categories = [
            {
                "category": "⚡ Energy Optimization",
                "color": THEME["primary"],
                "items": [
                    ("Heavy Loads", "Run high-drain appliances (washers, dishwashers) between 11 AM - 2 PM to utilize peak solar harvest."),
                    ("Stagger Usage", "Avoid starting the oven and dryer simultaneously; stagger heavy loads to prevent grid draw."),
                    ("Phantom Power", "Disable standby mode on non-essential electronics to save up to 5% of daily battery reserve.")
                ]
            },
            {
                "category": "🧹 Maintenance & Care",
                "color": THEME["success"],
                "items": [
                    ("Panel Cleaning", "Bird droppings or thick dust can drop efficiency by 25%. A soft rinse is recommended every 3 months."),
                    ("Vegetation Check", "Trim northern-side branches. Even a 5% shadow on one panel can bottle-neck an entire string."),
                    ("Inverter Airflow", "Ensure at least 15cm of clearance around the inverter; dust the cooling fins to prevent thermal throttling.")
                ]
            },
            {
                "category": "⚠️ Critical Safety & Warnings",
                "color": THEME["danger"],
                "items": [
                    ("Hot Spot Alert", "If one panel shows significantly lower voltage, check for 'hot spots' or cracked glass immediately."),
                    ("Battery Health", "Avoid discharging below 15%. Frequent deep cycles significantly reduce LiFePO4 lifespans."),
                    ("Storm Protocol", "In case of lightning, use the SCADA 'Soft Shutdown' to protect sensitive inverter logic boards.")
                ]
            }
        ]

        for cat in tip_categories:
            # Category Header
            ctk.CTkLabel(self.view_container, text=cat["category"], 
                         font=(FONT_NAME, 20, "bold"), text_color=cat["color"]).pack(anchor="w", pady=(25, 10), padx=5)
            
            # Grid/Container for items in this category
            cat_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
            cat_frame.pack(fill="x")
            
            for title, msg in cat["items"]:
                c = ctk.CTkFrame(cat_frame, fg_color=THEME["card"], corner_radius=12, border_width=1, border_color=THEME["border"])
                c.pack(fill="x", pady=5, padx=5)
                
                # Title and Message
                ctk.CTkLabel(c, text=title, text_color=cat["color"], font=(FONT_NAME, 13, "bold")).pack(anchor="w", padx=20, pady=(15, 0))
                ctk.CTkLabel(c, text=msg, font=(FONT_NAME, 13), text_color=THEME["text_main"], wraplength=800, justify="left").pack(anchor="w", padx=20, pady=(5, 15))

    def _draw_rewards(self):

    # Progress Overview
        profile = ctk.CTkFrame(
            self.view_container,
            fg_color=THEME["card"],
            corner_radius=15
        )
        profile.pack(fill="x", pady=10)

    # LEVEL LABEL
        self.lvl_lbl = ctk.CTkLabel(
            profile,
            text=f"Lvl {self.level}",
            font=("Segoe UI", 48, "bold"),
            text_color=THEME["accent"]
        )
        self.lvl_lbl.pack(side="right", padx=40)

        ctk.CTkLabel(
            profile,
            text=f"Operator: {self.current_user}",
        font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=30, pady=(30, 0))

    # XP LABEL
        self.xp_label = ctk.CTkLabel(
            profile,
            text=f"{self.xp} Total XP Accumulated",
            font=("Segoe UI", 14),
            text_color=THEME["text_sub"]
        )
        self.xp_label.pack(anchor="w", padx=30, pady=(5, 20))

    # XP PROGRESS BAR
        self.p_bar = ctk.CTkProgressBar(
            profile,
            width=400,
            progress_color=THEME["primary"]
        )

        self.p_bar.set((self.xp % 100) / 100)
        self.p_bar.pack(anchor="w", padx=30, pady=(0, 30))

    # Quest System
        ctk.CTkLabel(
            self.view_container,
            text="Active SolarQuests",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", pady=(30, 10))

        for quest in self.active_quests:

            q_box = ctk.CTkFrame(
                self.view_container,
                fg_color=THEME["card"],
                border_width=1,
                border_color=THEME["border"]
            )
            q_box.pack(fill="x", pady=5)

            ctk.CTkLabel(
                q_box,
                text=quest["title"],
                font=("Segoe UI", 14, "bold"),
                text_color=THEME["primary"]
            ).pack(side="left", padx=20, pady=20)

            ctk.CTkLabel(
                q_box,
                text=quest["desc"],
                font=("Segoe UI", 12),
                text_color=THEME["text_sub"]
            ).pack(side="left", padx=10)

            p = ctk.CTkProgressBar(
                q_box,
                width=200,
                progress_color=(
                    THEME["success"]
                    if quest["progress"] >= 1
                    else THEME["primary"]
                )
            )

            p.set(quest["progress"])
            p.pack(side="right", padx=20)
        
    def _update_loop(self):
        # Check if the app is still supposed to be running
        if not self._running: 
            return

        try:
            # Fetch the latest data from the engine
            data = engine.sync_sensors()
            if not data:
                return
            
            # Add reading to the model for the graph
            self.model.add_reading(data)
            
            # Update XP & Leveling Logic
            gained_xp = engine.calculate_xp(data)
            self.xp += gained_xp
            self.level = (self.xp // 100) + 1

            # --- WARNING & TOAST TRIGGERS ---
            # These check every 2 seconds regardless of which view you are in
            
            # Critical Battery Check
            if data.get('battery', 100) < 20:
                self._trigger_toast("CRITICAL ENERGY: Battery < 20%", "danger")
            
            # Thermal Check (Solar output affects temp)
            temp_val = 24 + (data.get('solar', 0) // 120)
            if temp_val > 45:
                self._trigger_toast(f"THERMAL ALERT: System Hot ({temp_val}°C)", "danger")

            # Efficiency Check
            efficiency = int(data.get('solar', 0) / 4.5)
            if data.get('solar', 0) > 100 and efficiency < 10:
                self._trigger_toast("LOW EFFICIENCY: Possible Shading", "warning")

            # Low Power / Night Mode
            if data.get('solar', 0) < 10 and data.get('battery', 0) < 30:
                self._trigger_toast("CONSERVATION MODE: Low Input", "warning")

            # --- VIEW SPECIFIC UPDATES ---
            
            # Dashboard Updates (Cards & Graph)
            if self.current_view == "Dashboard":
                self.cards["batt"].configure(text=f"{data.get('battery')}%")
                self.cards["solar"].configure(text=f"{data.get('solar')}W")
                self.cards["eff"].configure(text=f"{efficiency}%")
                self.cards["temp"].configure(text=f"{temp_val}°C")
                warning_message = None

                if data.get('battery', 100) < 20:
                    warning_message = "CRITICAL: Battery below 20%"

                elif temp_val > 45:
                    warning_message = f"THERMAL ALERT: {temp_val}°C"

                elif efficiency < 10:
                    warning_message = "LOW EFFICIENCY DETECTED"

                elif data.get('solar', 0) < 10:
                    warning_message = "LOW SOLAR INPUT"

            # SHOW / HIDE ALERT BOX
                if warning_message:
                    self.alert_lbl.configure(text=warning_message)
                    self.alert_box.pack(fill="x", pady=(0, 15))
                else:
                    self.alert_box.pack_forget()
                # Live Graph Update
                self.ax.clear()
                self.ax.set_title(
                    "Battery Telemetry",
                    color=THEME["text_main"],
                    fontsize=14,
                    fontweight="bold"
                )

                self.ax.set_xlabel(
                    "Time",
                    color=THEME["text_sub"],
                    fontsize=10
                )

                self.ax.set_ylabel(
                    "Battery %",
                    color=THEME["text_sub"],
                    fontsize=10
                )
                hist = self.model.get_recent('battery', 20)
                self.ax.plot(hist, color=THEME['primary'], linewidth=2)
                self.ax.set_facecolor(THEME["card"])
                self.ax.tick_params(colors=THEME['text_sub'], labelsize=8)
                for spine in self.ax.spines.values(): 
                    spine.set_visible(False)
                self.ax.grid(True, alpha=0.1, color=THEME['text_sub'])
                self.canvas.draw()

            # Rewards Updates (Progress Bar & XP Label)
            elif self.current_view == "Rewards":
                if hasattr(self, 'p_bar') and hasattr(self, 'xp_label'):
                    progress = (self.xp % 100) / 100
                    self.p_bar.set(progress)
                    self.xp_label.configure(text=f"{self.xp} Total XP Accumulated")
                    if hasattr(self, 'lvl_lbl'):
                        self.lvl_lbl.configure(text=f"Lvl {self.level}")

                        

        except Exception as e:
            logging.error(f"UI Update Failed: {e}")
            
        # Re-schedule the loop (2000ms = 2 seconds)
        self.after(2000, self._update_loop)
        
    def shutdown(self): 
        self._running = False
        self.destroy()


"""
    developer's note: the program is structured to allow easy expansion of features.
    additionally, the program isn't yet meant to be used for arduino and is running randomly generated data, 
    but the engine module is designed to be easily adaptable for real sensor integration in the future. 
    for the tips and recommendations section, the current implementation is static, 
    but it can be enhanced to use real-time data and machine learning for personalized insights.

    further recommendations: compiling every files and making an executable file using pyinstaller or similar tools, 
        and adding a settings page for user preferences and system configurations. 
        additionally, a database integration could be implemented for long-term data 
        storage and historical analysis.
"""
