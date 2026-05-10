import logging
import datetime
import tkinter as tk
from tkinter import font as tkfont
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import engine 

# --- UI Configuration & Constants ---
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
    "bg_main": "#f8fafc",
    "bg_sidebar": "#ffffff",
    "card": "#ffffff",
    "primary": "#2d8ab5",
    "text_main": "#1e293b",
    "text_sub": "#64748b",
    "warning": "#fff7ed",
    "warning_border": "#fb923c",
    "accent": "#10b981",
    "danger": "#ef4444",
    "border": "#e2e8f0"
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Light")
        self.title("SolarSync SCADA Professional")
        self.geometry("1200x900")
        
        # Core Application State
        self.model = engine.DataModel(maxlen=500)
        self._running = True
        self.xp = 1904 
        self.level = 20
        self.current_user = None
        self.user_role = "System Administrator"
        self.login_time = None
        self.current_view = "Dashboard"
        
        # Toast/Notification State
        self.active_toasts = []
        self.creds = {
            "admin": "1234",
            "operator": "solar123"
        }

        self._build_login()

    # --- Authentication Layer ---
    def _build_login(self):
        self.login_frame = ctk.CTkFrame(self, fg_color=THEME["bg_main"])
        self.login_frame.pack(fill="both", expand=True)
        
        inner = ctk.CTkFrame(self.login_frame, fg_color=THEME["card"], corner_radius=15, width=450, height=500, border_width=1, border_color=THEME["border"])
        inner.place(relx=0.5, rely=0.5, anchor="center")
        inner.pack_propagate(False)
        
        ctk.CTkLabel(inner, text="☀️ SolarSync", font=(FONT_NAME, 32, "bold"), text_color=THEME["primary"]).pack(pady=(50, 10))
        ctk.CTkLabel(inner, text="Secure SCADA Login", font=(FONT_NAME, 14), text_color=THEME["text_sub"]).pack(pady=(0, 30))
        
        self.u_ent = ctk.CTkEntry(inner, placeholder_text="Username", width=300, height=45); self.u_ent.pack(pady=10)
        self.p_ent = ctk.CTkEntry(inner, placeholder_text="Password", show="*", width=300, height=45); self.p_ent.pack(pady=10)
        
        self.login_err = ctk.CTkLabel(inner, text="", text_color=THEME["danger"], font=(FONT_NAME, 12))
        self.login_err.pack(pady=5)
        
        ctk.CTkButton(inner, text="Authorize System Access", command=self._check_login, 
                      fg_color=THEME["primary"], hover_color="#236d8e", width=300, height=45).pack(pady=20)

    def _check_login(self):
        u, p = self.u_ent.get().lower(), self.p_ent.get()
        if u in self.creds and p == self.creds[u]:
            self.current_user = u.capitalize()
            self.login_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.login_frame.destroy()
            self._init_main_ui()
        else:
            self.login_err.configure(text="Invalid credentials. Please try again.")

    def _handle_signout(self):
        self._running = False
        for widget in self.winfo_children(): widget.destroy()
        self.__init__()

    # --- Main UI Shell ---
    def _init_main_ui(self):
        self._running = True
        self.configure(fg_color=THEME["bg_main"])
        
        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=THEME["bg_sidebar"], corner_radius=0, border_width=1, border_color=THEME["border"])
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="☀️ SolarSync", font=(FONT_NAME, 22, "bold"), text_color=THEME["primary"]).pack(pady=40, padx=25, anchor="w")
        
        self.nav_btns = {}
        nav_items = [
            ("Dashboard", "📊"), ("Fault Line", "⚡"), 
            ("Tips & Recs", "💡"), ("Rewards", "🏆")
        ]
        
        for item, icon in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=f"{icon}  {item}", anchor="w", font=(FONT_NAME, 14),
                                fg_color="transparent", text_color=THEME["text_main"],
                                hover_color="#f1f5f9", height=45, corner_radius=8,
                                command=lambda x=item: self.switch_view(x))
            btn.pack(fill="x", padx=15, pady=5)
            self.nav_btns[item] = btn

        # Personalized User Badge (Bottom of Sidebar)
        user_panel = ctk.CTkFrame(self.sidebar, fg_color="#f8fafc", corner_radius=12, border_width=1, border_color=THEME["border"])
        user_panel.pack(side="bottom", fill="x", padx=15, pady=30)
        
        ctk.CTkLabel(user_panel, text=self.current_user, font=(FONT_NAME, 14, "bold"), text_color=THEME["text_main"]).pack(pady=(15, 0))
        ctk.CTkLabel(user_panel, text=self.user_role, font=(FONT_NAME, 11), text_color=THEME["text_sub"]).pack()
        
        ctk.CTkButton(user_panel, text="Sign Out", font=(FONT_NAME, 12, "bold"), text_color=THEME["danger"],
                      fg_color="transparent", hover_color="#fee2e2", command=self._handle_signout).pack(pady=10)

        # View Container
        self.view_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.view_container.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        self.switch_view("Dashboard")
        self._update_loop()

    # --- View Manager ---
    def switch_view(self, view_name):
        self.current_view = view_name
        for name, btn in self.nav_btns.items():
            is_active = (name == view_name)
            btn.configure(fg_color=THEME["primary"] if is_active else "transparent",
                          text_color="white" if is_active else THEME["text_main"])
        
        for child in self.view_container.winfo_children(): child.destroy()
        
        # Header
        header = ctk.CTkFrame(self.view_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        ctk.CTkLabel(header, text=view_name, font=(FONT_NAME, 32, "bold"), text_color=THEME["text_main"]).pack(side="left")
        
        if view_name == "Dashboard": self._draw_dashboard()
        elif view_name == "Fault Line": self._draw_fault_line()
        elif view_name == "Tips & Recs": self._draw_tips()
        elif view_name == "Rewards": self._draw_rewards()

    # --- Warning Popup (Toast) System ---
    def _trigger_toast(self, message, level="danger"):
        # Prevent duplicate toasts for the same issue
        for t in self.active_toasts:
            if t['msg'] == message: return

        color = THEME["danger"] if level == "danger" else THEME["warning_border"]
        
        toast = ctk.CTkFrame(self, fg_color=color, corner_radius=10, border_width=1, border_color="#ffffff")
        toast.place(relx=0.98, rely=0.05, anchor="ne") # Top Right
        
        ctk.CTkLabel(toast, text=f"⚠️ {message}", text_color="white", font=(FONT_NAME, 13, "bold"), padx=20, pady=15).pack()
        
        toast_data = {'widget': toast, 'msg': message}
        self.active_toasts.append(toast_data)
        
        # Auto-destruct after 5 seconds
        self.after(5000, lambda: self._remove_toast(toast_data))

    def _remove_toast(self, toast_data):
        if toast_data in self.active_toasts:
            toast_data['widget'].destroy()
            self.active_toasts.remove(toast_data)

    # --- Specific Views ---
    def _draw_dashboard(self):
        # Alert Banner (Static Warnings)
        self.alert_box = ctk.CTkFrame(self.view_container, fg_color=THEME["warning"], border_width=1, border_color=THEME["warning_border"])
        self.alert_lbl = ctk.CTkLabel(self.alert_box, text="", text_color=THEME["warning_border"], font=(FONT_NAME, 14, "bold"))
        self.alert_lbl.pack(pady=15)
        self.alert_box.pack_forget()

        # Metrics Grid
        self.cards = {}
        grid = ctk.CTkFrame(self.view_container, fg_color="transparent")
        grid.pack(fill="x", pady=10); grid.columnconfigure((0,1,2,3), weight=1)
        
        specs = [
            ("Battery Level", "batt", "Health: Optimal"), 
            ("Solar Output", "solar", "Input: Active"), 
            ("Efficiency", "eff", "Grid: Tied"), 
            ("Temperature", "temp", "Thermal: Stable")
        ]
        
        for i, (title, key, sub) in enumerate(specs):
            card = ctk.CTkFrame(grid, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            ctk.CTkLabel(card, text=title, text_color=THEME["text_sub"], font=(FONT_NAME, 13, "bold")).pack(anchor="w", padx=20, pady=(20,0))
            v_lbl = ctk.CTkLabel(card, text="--", font=(FONT_NAME, 28, "bold"), text_color=THEME["text_main"])
            v_lbl.pack(anchor="w", padx=20)
            ctk.CTkLabel(card, text=f"● {sub}", font=(FONT_NAME, 11), text_color=THEME["accent"]).pack(anchor="w", padx=20, pady=(5,20))
            self.cards[key] = v_lbl

        # Detailed Chart Section
        chart_card = ctk.CTkFrame(self.view_container, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
        chart_card.pack(fill="both", expand=True, pady=25)
        
        ctk.CTkLabel(chart_card, text="Battery Voltage Trends (Live)", font=(FONT_NAME, 16, "bold"), text_color=THEME["text_main"]).pack(anchor="w", padx=25, pady=(20, 0))
        
        self.fig, self.ax = plt.subplots(figsize=(10, 4), dpi=100)
        self.fig.patch.set_facecolor(THEME["card"])
        self.ax.set_facecolor("#fcfcfc")
        self.canvas = FigureCanvasTkAgg(self.fig, chart_card)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    def _draw_fault_line(self):
        # Connection Status Overview
        status_card = ctk.CTkFrame(self.view_container, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
        status_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(status_card, text="System Connectivity Map", font=(FONT_NAME, 18, "bold")).pack(side="left", padx=25, pady=25)
        ctk.CTkLabel(status_card, text="System Optimal", fg_color=THEME["accent"], text_color="white", corner_radius=8, padx=15, pady=5, font=(FONT_NAME, 12, "bold")).pack(side="right", padx=25)

        # Elaborate Flowchart Representation
        flow_frame = ctk.CTkFrame(self.view_container, fg_color="white", height=450, corner_radius=15, border_width=1, border_color=THEME["border"])
        flow_frame.pack(fill="x", pady=20)
        
        nodes = [
            ("Solar Array", 0.1, 0.4, "DC Power Source"),
            ("Inverter Unit", 0.35, 0.4, "DC to AC Conversion"),
            ("Battery Bank", 0.65, 0.2, "Energy Storage"),
            ("Main Switch", 0.65, 0.6, "Power Routing"),
            ("AC Load / Home", 0.9, 0.4, "Terminal Output")
        ]
        
        for name, px, py, desc in nodes:
            n = ctk.CTkFrame(flow_frame, fg_color="#f1f5f9", width=160, height=100, corner_radius=10, border_width=1, border_color="#cbd5e1")
            n.place(relx=px, rely=py, anchor="center")
            ctk.CTkLabel(n, text=name, font=(FONT_NAME, 13, "bold"), text_color=THEME["text_main"]).place(relx=0.5, rely=0.35, anchor="center")
            ctk.CTkLabel(n, text=desc, font=(FONT_NAME, 10), text_color=THEME["text_sub"]).place(relx=0.5, rely=0.65, anchor="center")
            ctk.CTkLabel(n, text="● Connected", font=(FONT_NAME, 9, "bold"), text_color=THEME["accent"]).place(relx=0.5, rely=0.85, anchor="center")

    def _draw_tips(self):
        # Knowledge Base Sections
        sections = [
            ("Current Insights", [
                ("Efficiency", "Run heavy appliances during peak sun hours (10 AM - 3 PM) for 0% grid impact."),
                ("Optimization", "Check for shading on panel 4; current yield is 12% lower than neighbors.")
            ]),
            ("Maintenance Log", [
                ("Panels", "Next cleaning cycle due in 14 days to maintain 98% transmittance."),
                ("Inverter", "Firmware v2.4 available. Update to improve conversion efficiency by 1.2%.")
            ]),
            ("Safety Protocols", [
                ("Thermal", "Battery temp is rising. Ensure ventilation fans are clear of debris."),
                ("Emergency", "Manual shut-off switch is located on the North side of the inverter.")
            ])
        ]
        
        for title, items in sections:
            ctk.CTkLabel(self.view_container, text=title, font=(FONT_NAME, 20, "bold")).pack(anchor="w", pady=(20, 10))
            row = ctk.CTkFrame(self.view_container, fg_color="transparent")
            row.pack(fill="x")
            
            for tag, msg in items:
                c = ctk.CTkFrame(row, fg_color=THEME["card"], corner_radius=12, border_width=1, border_color=THEME["border"])
                c.pack(side="left", padx=10, pady=5, fill="both", expand=True)
                
                tag_clr = "#dcfce7" if tag == "Efficiency" else "#fee2e2" if tag == "Thermal" else "#fef3c7"
                tag_txt = "#166534" if tag == "Efficiency" else "#991b1b" if tag == "Thermal" else "#92400e"
                
                ctk.CTkLabel(c, text=tag, fg_color=tag_clr, text_color=tag_txt, corner_radius=5, font=(FONT_NAME, 10, "bold"), padx=10).pack(anchor="w", padx=15, pady=15)
                ctk.CTkLabel(c, text=msg, wraplength=300, font=(FONT_NAME, 13), justify="left").pack(anchor="w", padx=15, pady=(0, 20))

    def _draw_rewards(self):
        # Elaborate User Details
        profile = ctk.CTkFrame(self.view_container, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
        profile.pack(fill="x", pady=10)
        
        left = ctk.CTkFrame(profile, fg_color="transparent")
        left.pack(side="left", padx=30, pady=30)
        ctk.CTkLabel(left, text=f"User: {self.current_user}", font=(FONT_NAME, 24, "bold")).pack(anchor="w")
        ctk.CTkLabel(left, text=f"Role: {self.user_role}", font=(FONT_NAME, 14), text_color=THEME["text_sub"]).pack(anchor="w")
        ctk.CTkLabel(left, text=f"Session Start: {self.login_time}", font=(FONT_NAME, 12), text_color=THEME["text_sub"]).pack(anchor="w")

        # Progress Logic
        target_xp = self.level * 100 + 100
        progress = self.xp / target_xp

        stats = ctk.CTkFrame(profile, fg_color="transparent")
        stats.pack(side="right", padx=30)
        ctk.CTkLabel(stats, text=f"Level {self.level}", font=(FONT_NAME, 48, "bold"), text_color="#f59e0b").pack()
        ctk.CTkLabel(stats, text=f"{self.xp} Total XP Accumulated", font=(FONT_NAME, 14, "bold")).pack()

        # Large Progress Bar
        bar_card = ctk.CTkFrame(self.view_container, fg_color=THEME["card"], corner_radius=15, border_width=1, border_color=THEME["border"])
        bar_card.pack(fill="x", pady=20)
        
        ctk.CTkLabel(bar_card, text=f"Progress to Level {self.level + 1}", font=(FONT_NAME, 16, "bold")).pack(pady=(25, 5))
        p_bar = ctk.CTkProgressBar(bar_card, fg_color="#e2e8f0", progress_color=THEME["primary"], height=15)
        p_bar.set(progress); p_bar.pack(fill="x", padx=100, pady=20)
        ctk.CTkLabel(bar_card, text=f"{self.xp} / {target_xp} XP", font=(FONT_NAME, 12, "bold")).pack(pady=(0, 25))

    # --- System Update Loop ---
    def _update_loop(self):
        if not self._running: return
        try:
            data = engine.sync_sensors()
            self.model.add_reading(data)
            
            # Update Rewards State
            self.xp += engine.calculate_xp(data)
            self.level = self.xp // 100 + 1
            
            # Dashboard Specific Updates
            if self.current_view == "Dashboard":
                self.cards["batt"].configure(text=f"{data.get('battery')}%")
                self.cards["solar"].configure(text=f"{data.get('solar')}W")
                self.cards["eff"].configure(text=f"{int(data.get('solar',0)/4.5)}%")
                self.cards["temp"].configure(text=f"{24 + (data.get('solar',0)//120)}°C")
                
                # Logic for WARNING POPUPS (Toasts)
                if data.get('battery') < 20:
                    self._trigger_toast("CRITICAL ENERGY RESERVE: Battery < 20%", "danger")
                if data.get('solar') > 450:
                    self._trigger_toast("High Solar Irradiance Detected", "warning")
                
                # Update Graph
                self.ax.clear()
                hist = self.model.get_recent('battery', 30)
                self.ax.plot(hist, color=THEME['primary'], linewidth=3)
                self.ax.fill_between(range(len(hist)), hist, color=THEME['primary'], alpha=0.1)
                self.ax.set_ylim(0, 100)
                self.ax.axis('off')
                self.canvas.draw()

        except Exception as e:
            logging.error(f"UI Update Failed: {e}")
            
        self.after(2000, self._update_loop)

    def shutdown(self):
        self._running = False
        self.destroy()
