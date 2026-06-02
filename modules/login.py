import tkinter as tk
from tkinter import font as tkfont
import threading
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.auth import login
from modules.register import RegisterWindow

# ── Exact colours from screenshot ────────────────────────────────────────────
BG_LEFT      = "#0d1b3e"   # deep navy left — dot grid panel
BG_RIGHT     = "#08111f"   # very dark navy right panel
ACCENT_BLUE  = "#4361ee"   # buttons / active links
ACCENT_GOLD  = "#f59e0b"   # 86+ / 99.9% orange stats
ACCENT_CYAN  = "#38bdf8"   # "Like a Pro" blue text
TEXT_WHITE   = "#ffffff"
TEXT_MUTED   = "#94a3b8"
TEXT_SUBTLE  = "#334d70"
TEXT_DIM     = "#253a55"
INPUT_BG     = "#ffffff"
INPUT_FG     = "#0f172a"
BADGE_BG     = "#0f1e36"
BADGE_BORDER = "#1e3456"
PILL_BG      = "#0f1e36"
PILL_BORDER  = "#1e3456"
GRID_DOT     = "#162340"
ACCENT_GREEN = "#22c55e"


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HallmarkPro – Admin Login")
        self.geometry("1366x720")
        self.minsize(1100, 600)
        self.configure(bg=BG_LEFT)
        self.resizable(True, True)
        self._load_fonts()
        self._build_ui()
        self.after(100, self.center_window)

    def _load_fonts(self):
        self.fn = lambda sz, bold=False: tkfont.Font(
            family="Segoe UI", size=sz,
            weight="bold" if bold else "normal")

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width(); h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Use PanedWindow so columns stay proportional on resize
        self.columnconfigure(0, weight=60)
        self.columnconfigure(1, weight=40)
        self.rowconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    # ══════════════════════════════════════════════════════════════════════════
    #  LEFT PANEL  (60%)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_left_panel(self):
        left = tk.Frame(self, bg=BG_LEFT)
        left.grid(row=0, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        # ── dot-grid canvas (behind everything) ──
        self.grid_canvas = tk.Canvas(left, bg=BG_LEFT, highlightthickness=0)
        self.grid_canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_canvas.bind("<Configure>", self._redraw_grid)

        # ── centred content frame (floated on top of canvas) ──
        content = tk.Frame(left, bg=BG_LEFT)
        content.place(relx=0.5, rely=0.5, anchor="center")

        # ── HP logo circle ──
        logo_c = tk.Canvas(content, width=100, height=100,
                           bg=BG_LEFT, highlightthickness=0)
        logo_c.pack(pady=(0, 18))
        # outer glow ring
        logo_c.create_oval(4, 4, 96, 96,
                           outline="#1e4080", width=1, fill=BG_LEFT)
        # main circle border (blue)
        logo_c.create_oval(8, 8, 92, 92,
                           outline=ACCENT_BLUE, width=2, fill="#0d1e3c")
        # inner dark circle
        logo_c.create_oval(14, 14, 86, 86,
                           outline="#162d55", width=1, fill="#0a1628")
        # HP text — gradient-ish using two labels stacked (H orange, P blue)
        logo_c.create_text(42, 50, text="H",
                           font=tkfont.Font(family="Segoe UI", size=22, weight="bold"),
                           fill="#f59e0b", anchor="e")
        logo_c.create_text(58, 50, text="P",
                           font=tkfont.Font(family="Segoe UI", size=22, weight="bold"),
                           fill=ACCENT_BLUE, anchor="w")

        # ── HALLMARKPRO ADMIN badge ──
        badge_outer = tk.Frame(content, bg=BADGE_BG,
                               highlightbackground=BADGE_BORDER,
                               highlightthickness=1)
        badge_outer.pack(pady=(0, 24))
        badge_inner = tk.Frame(badge_outer, bg=BADGE_BG, padx=16, pady=6)
        badge_inner.pack()
        tk.Label(badge_inner, text="⚙  HALLMARKPRO ADMIN",
                 font=self.fn(9), bg=BADGE_BG, fg=TEXT_MUTED).pack()

        # ── Headline ──
        tk.Label(content, text="Run Your AHC",
                 font=tkfont.Font(family="Segoe UI", size=30, weight="bold"),
                 bg=BG_LEFT, fg=TEXT_WHITE).pack()
        tk.Label(content, text="Like a Pro",
                 font=tkfont.Font(family="Segoe UI", size=30, weight="bold"),
                 bg=BG_LEFT, fg=ACCENT_CYAN).pack()

        # ── taglines ──
        tk.Label(content, text="Trusted by 86+ hallmark centres across India.",
                 font=self.fn(10), bg=BG_LEFT, fg=TEXT_MUTED).pack(pady=(14, 2))
        tk.Label(content,
                 text="Faster billing.  Smarter compliance.  Zero hassle.",
                 font=self.fn(10), bg=BG_LEFT, fg=TEXT_MUTED).pack()

        # ── POWERFUL FEATURES label ──
        tk.Label(content, text="POWERFUL FEATURES",
                 font=self.fn(8), bg=BG_LEFT, fg=TEXT_DIM).pack(pady=(22, 8))

        # ── feature pill row ──
        self._build_feature_pills(content)

        # ── stats row ──
        self._build_stats_row(content)

        # ── footer ──
        tk.Label(content, text="Powered by HallmarkPro © 2026",
                 font=self.fn(8), bg=BG_LEFT, fg=TEXT_DIM).pack(pady=(24, 2))
        tk.Label(content,
                 text="Developed & Maintained by Prosenjit · 9810359334",
                 font=self.fn(8), bg=BG_LEFT, fg=TEXT_DIM).pack()

    def _redraw_grid(self, event=None):
        c = self.grid_canvas
        c.delete("dot")
        w = c.winfo_width()
        h = c.winfo_height()
        step = 28
        for x in range(0, w + step, step):
            for y in range(0, h + step, step):
                c.create_oval(x - 1, y - 1, x + 1, y + 1,
                              fill=GRID_DOT, outline="", tags="dot")

    def _build_feature_pills(self, parent):
        features = [
            ("▣", "GST Reports"),
            ("▦", "Stock Management"),
            ("⬡", "Multi-Role Access"),
            ("✦", "Staff Management"),
            ("◈", "Billing"),
            ("☰", "Job Cards"),
        ]
        row = tk.Frame(parent, bg=BG_LEFT)
        row.pack()
        for icon, label in features:
            pill = tk.Frame(row, bg=PILL_BG,
                            highlightbackground=PILL_BORDER,
                            highlightthickness=1,
                            padx=10, pady=6)
            pill.pack(side="left", padx=4)
            tk.Label(pill, text=f"{icon}  {label}",
                     font=self.fn(8), bg=PILL_BG, fg=TEXT_MUTED).pack()

    def _build_stats_row(self, parent):
        stats = [
            ("86+",    "AHC CENTRES",      ACCENT_GOLD),
            ("17.5K+", "ENTRIES MANAGED",  TEXT_WHITE),
            ("16K+",   "JOBS ENTRY",       TEXT_WHITE),
            ("99.9%",  "UPTIME",           ACCENT_GOLD),
        ]
        row = tk.Frame(parent, bg=BG_LEFT)
        row.pack(pady=(24, 0))
        for val, lbl, color in stats:
            cell = tk.Frame(row, bg=BG_LEFT)
            cell.pack(side="left", padx=22)
            tk.Label(cell, text=val,
                     font=tkfont.Font(family="Segoe UI", size=22, weight="bold"),
                     bg=BG_LEFT, fg=color).pack()
            tk.Label(cell, text=lbl,
                     font=self.fn(7), bg=BG_LEFT, fg=TEXT_DIM).pack()

    # ══════════════════════════════════════════════════════════════════════════
    #  RIGHT PANEL  (40%)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_right_panel(self):
        right = tk.Frame(self, bg=BG_RIGHT)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        # vertical divider line on left edge of right panel
        divider = tk.Frame(right, bg="#0d2040", width=1)
        divider.place(x=0, y=0, relheight=1)

        # centred card
        card = tk.Frame(right, bg=BG_RIGHT)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # ── HALLMARK PRO logo row ──
        logo_row = tk.Frame(card, bg=BG_RIGHT)
        logo_row.pack(pady=(0, 6))

        # hexagon icon
        hc = tk.Canvas(logo_row, width=40, height=40,
                       bg=BG_RIGHT, highlightthickness=0)
        hc.pack(side="left", padx=(0, 8))
        # draw hexagon
        pts = []
        import math
        cx, cy, r = 20, 20, 17
        for i in range(6):
            angle = math.radians(60 * i - 30)
            pts += [cx + r * math.cos(angle), cy + r * math.sin(angle)]
        hc.create_polygon(pts, fill="", outline=ACCENT_BLUE, width=2)
        # HP inside hex
        hc.create_text(18, 20, text="H",
                       font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
                       fill=ACCENT_GOLD, anchor="e")
        hc.create_text(22, 20, text="P",
                       font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
                       fill=ACCENT_BLUE, anchor="w")

        tk.Label(logo_row, text="HALLMARK PRO",
                 font=tkfont.Font(family="Segoe UI", size=13, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_WHITE).pack(side="left")
        tk.Label(logo_row, text=" ›",
                 font=tkfont.Font(family="Segoe UI", size=14),
                 bg=BG_RIGHT, fg=ACCENT_BLUE).pack(side="left")

        # ── Welcome back ──
        tk.Label(card, text="Welcome back",
                 font=tkfont.Font(family="Segoe UI", size=26, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_WHITE).pack(pady=(18, 4))
        tk.Label(card, text="Sign in to your admin dashboard",
                 font=self.fn(10), bg=BG_RIGHT, fg=TEXT_MUTED).pack(pady=(0, 28))

        # ── form (fixed width 320px matching screenshot) ──
        form = tk.Frame(card, bg=BG_RIGHT)
        form.pack(padx=0)
        FORM_W = 320

        # ── Username field ──
        tk.Label(form, text="PHONE NUMBER OR USERNAME",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")

        un_wrap = tk.Frame(form, bg=INPUT_BG,
                           highlightbackground="#c8d4e8",
                           highlightthickness=1)
        un_wrap.pack(fill="x", pady=(5, 16), ipady=0)
        un_inner = tk.Frame(un_wrap, bg=INPUT_BG)
        un_inner.pack(fill="x", padx=4)

        tk.Label(un_inner, text="👤", bg=INPUT_BG, fg="#9aaccc",
                 font=self.fn(11)).pack(side="left", padx=(8, 0), pady=10)
        self.username_var = tk.StringVar(value="9810359334")
        tk.Entry(un_inner, textvariable=self.username_var, width=FORM_W // 8,
                 bg=INPUT_BG, fg=INPUT_FG, relief="flat", bd=0,
                 font=tkfont.Font(family="Segoe UI", size=12),
                 insertbackground=INPUT_FG).pack(
            side="left", fill="x", expand=True, pady=10, padx=8)

        # ── Password field ──
        tk.Label(form, text="PASSWORD",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")

        pw_wrap = tk.Frame(form, bg=INPUT_BG,
                           highlightbackground="#c8d4e8",
                           highlightthickness=1)
        pw_wrap.pack(fill="x", pady=(5, 10), ipady=0)
        pw_inner = tk.Frame(pw_wrap, bg=INPUT_BG)
        pw_inner.pack(fill="x", padx=4)

        tk.Label(pw_inner, text="🔒", bg=INPUT_BG, fg="#9aaccc",
                 font=self.fn(11)).pack(side="left", padx=(8, 0), pady=10)
        self.password_var = tk.StringVar()
        self.pw_entry = tk.Entry(pw_inner, textvariable=self.password_var,
                                 show="●", width=FORM_W // 9,
                                 bg=INPUT_BG, fg=INPUT_FG, relief="flat", bd=0,
                                 font=tkfont.Font(family="Segoe UI", size=12),
                                 insertbackground=INPUT_FG)
        self.pw_entry.pack(side="left", fill="x", expand=True, pady=10, padx=6)
        self.pw_entry.bind("<Return>", lambda e: self._do_login())

        self._show_pw = False
        eye = tk.Label(pw_inner, text="🙈", bg=INPUT_BG, fg="#9aaccc",
                       cursor="hand2", font=self.fn(11))
        eye.pack(side="right", padx=10)
        eye.bind("<Button-1>", self._toggle_pw)
        self._eye_lbl = eye

        # ── Remember me / Forgot ──
        opt = tk.Frame(form, bg=BG_RIGHT)
        opt.pack(fill="x", pady=(4, 20))

        self.remember_var = tk.BooleanVar()
        cb = tk.Checkbutton(opt, variable=self.remember_var,
                            text="Remember me (30 days)",
                            bg=BG_RIGHT, fg=TEXT_MUTED,
                            activebackground=BG_RIGHT,
                            selectcolor="#0f1e36",
                            font=self.fn(9))
        cb.pack(side="left")

        forgot = tk.Label(opt, text="Forgot password?",
                          fg=ACCENT_BLUE, bg=BG_RIGHT,
                          cursor="hand2", font=self.fn(9))
        forgot.pack(side="right")

        # ── error label ──
        self.error_var = tk.StringVar()
        tk.Label(form, textvariable=self.error_var,
                 fg="#f87171", bg=BG_RIGHT,
                 font=self.fn(8), wraplength=FORM_W).pack(pady=(0, 6))

        # ── Sign In button ──
        self.sign_btn = tk.Button(
            form,
            text="  ⊡   Sign In",
            font=tkfont.Font(family="Segoe UI", size=12, weight="bold"),
            bg=ACCENT_BLUE, fg=TEXT_WHITE,
            activebackground="#3451d1",
            activeforeground=TEXT_WHITE,
            relief="flat", bd=0,
            cursor="hand2",
            pady=14,
            command=self._do_login
        )
        self.sign_btn.pack(fill="x")
        self.sign_btn.bind("<Enter>", lambda e: self.sign_btn.config(bg="#3451d1"))
        self.sign_btn.bind("<Leave>", lambda e: self.sign_btn.config(bg=ACCENT_BLUE))

        # ── bottom links ──
        links = tk.Frame(card, bg=BG_RIGHT)
        links.pack(pady=(20, 0))

        reg = tk.Label(links, text="🏛  Register Centre",
                       fg=ACCENT_BLUE, bg=BG_RIGHT,
                       cursor="hand2", font=self.fn(9))
        reg.pack(side="left", padx=20)
        reg.bind("<Button-1>", lambda e: self._open_register())

        sup = tk.Label(links, text="💬  Support",
                       fg=ACCENT_GREEN, bg=BG_RIGHT,
                       cursor="hand2", font=self.fn(9))
        sup.pack(side="left", padx=20)

        # loading text
        self.loading_var = tk.StringVar()
        tk.Label(card, textvariable=self.loading_var,
                 fg=ACCENT_CYAN, bg=BG_RIGHT, font=self.fn(9)).pack(pady=6)

    # ─────────────────────────────────────────────────────────────────────────
    def _toggle_pw(self, _=None):
        self._show_pw = not self._show_pw
        self.pw_entry.config(show="" if self._show_pw else "●")
        self._eye_lbl.config(text="👁" if self._show_pw else "🙈")

    def _do_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            self.error_var.set("Please enter username and password.")
            return
        self.error_var.set("")
        self.loading_var.set("Verifying…")
        self.sign_btn.config(state="disabled", text="Signing in…")

        def _run():
            result = login(username, password)
            self.after(0, lambda: self._on_result(result))

        threading.Thread(target=_run, daemon=True).start()

    def _on_result(self, result):
        self.loading_var.set("")
        self.sign_btn.config(state="normal", text="  ⊡   Sign In")
        if result["ok"]:
            self._open_dashboard(result["admin"], result["firm"],
                                 " (Offline)" if result.get("offline") else "")
        else:
            self.error_var.set(result.get("error", "Login failed."))

    def _open_dashboard(self, admin, firm, offline_note=""):
        from modules.dashboard import DashboardWindow
        self.withdraw()
        dash = DashboardWindow(admin, firm, offline_note,
                               on_logout=self._on_logout)
        dash.protocol("WM_DELETE_WINDOW",
                      lambda: (dash.destroy(), self.destroy()))

    def _on_logout(self):
        self.deiconify()
        self.password_var.set("")

    def _open_register(self):
        self.withdraw()
        reg_window = RegisterWindow(on_back_to_login=lambda: (reg_window.destroy(), self.deiconify()))
        reg_window.protocol("WM_DELETE_WINDOW", lambda: (reg_window.destroy(), self.deiconify()))
