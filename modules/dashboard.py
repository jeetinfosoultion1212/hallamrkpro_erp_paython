import tkinter as tk
from tkinter import font as tkfont, ttk, messagebox
import sqlite3, os, sys, datetime, threading

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db.schema import get_connection
from .receipt_entry import ReceiptEntryPage
from .generate_bill import GenerateBillPage

# ── colours (white main content area + blue sidebar) ────────────────────────────────
BG_MAIN      = "#ffffff"  # WHITE main content area
BG_SIDEBAR   = "#0b1628"  # Dark blue sidebar
BG_TOPBAR    = "#0d1b35"  # Dark blue topbar
BG_CARD      = "#f8f9fa"  # Light gray cards
BG_TABLE_HDR = "#e8ecf1"  # Light gray table header
BG_TABLE_ROW = "#ffffff"  # White table rows
BG_TABLE_ALT = "#f8f9fa"  # Alternate row light gray
ACCENT_BLUE  = "#4361ee"  # Button blue
ACCENT_GREEN = "#22c55e"  # Green accents
ACCENT_ORG   = "#f59e0b"  # Orange accents
ACCENT_RED   = "#ef4444"  # Red accents
ACCENT_CYAN  = "#06b6d4"  # Cyan accents
ACCENT_PURP  = "#8b5cf6"  # Purple accents
TEXT_WHITE   = "#ffffff"  # White text
TEXT_BLACK   = "#000000"  # Black text for white bg
TEXT_MUTED   = "#6b7280"  # Gray text
TEXT_DIM     = "#9ca3af"  # Dim text
SIDEBAR_SEL  = "#1a2d52"  # Sidebar selected
SIDEBAR_TXT  = "#8899bb"  # Sidebar text
SIDEBAR_ACT  = "#ffffff"  # Sidebar active text
BORDER       = "#e5e7eb"  # Light gray border
BANNER_BG    = "#0d3320"  # Green banner
BANNER_FG    = "#4ade80"  # Green text

STATUS_COLORS = {
    "XRF":            ("#dbeafe", "#0c4a6e"),
    "Weight Capture": ("#ede9fe", "#5b21b6"),
    "Pending":        ("#fef3c7", "#92400e"),
    "Delivered":      ("#dcfce7", "#166534"),
}
BILL_COLORS = {
    "Unbilled": ("#fee2e2", "#991b1b"),
    "Billed":   ("#dcfce7", "#166534"),
}
PAY_COLORS = {
    "Due":  ("#fee2e2", "#991b1b"),
    "Paid": ("#dcfce7", "#166534"),
}

SIDEBAR_SECTIONS = {
    "DASHBOARD": [
        ("dashboard", "Dashboard", "⊞"),
    ],
    "MAIN WORKFLOW": [
        ("main_request",    "Main Request",     "📋"),
        ("offsite_request", "Offsite Request",  "🏢"),
        ("receipt_entry",   "Receipt Entry",    "🧾"),
        ("generate_bill",   "Generate Bill",    "💳"),
        ("credit_note",     "Create Credit Note","📝"),
        ("receipt_payment", "Receipt Payment",  "💰"),
        ("payment",         "Payment",          "💸"),
        ("purchase",        "Purchase",         "🛒"),
        ("contra",          "Contra",           "↔"),
    ],
    "PARTIES": [
        ("jewellers",  "Jewellers",  "💍"),
        ("suppliers",  "Suppliers",  "📦"),
    ],
}

class DashboardWindow(tk.Toplevel):
    def __init__(self, admin, firm, offline_note="", on_logout=None):
        super().__init__()
        self.admin       = admin
        self.firm        = firm
        self.offline_note= offline_note
        self.on_logout   = on_logout
        self.active_page = "main_request"

        self.title(f"HallmarkPro – {firm.get('firm_name','')}")
        self.geometry("1366x768")
        self.minsize(1100, 600)
        self.configure(bg=BG_MAIN)
        self.state("zoomed")   # start maximised

        self._setup_styles()
        self._build_ui()
        self.after(200, self._load_dashboard_stats)

    # ─────────────────────────────────────────────────────────────────────────
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Treeview",
                        background=BG_TABLE_ROW,
                        foreground=TEXT_BLACK,
                        fieldbackground=BG_TABLE_ROW,
                        rowheight=34,
                        borderwidth=0,
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background=BG_TABLE_HDR,
                        foreground=TEXT_MUTED,
                        relief="flat",
                        font=("Segoe UI", 8, "bold"),
                        borderwidth=0)
        style.map("Treeview",
                  background=[("selected", "#e0e7ff")],
                  foreground=[("selected", TEXT_BLACK)])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        style.configure("Vertical.TScrollbar",
                        background=BG_CARD, troughcolor=BG_MAIN,
                        arrowcolor=TEXT_MUTED, borderwidth=0)

    # ── TOP-LEVEL LAYOUT ──────────────────────────────────────────────────────
    def _build_ui(self):
        # topbar (fixed height)
        self._build_topbar()
        # below topbar: sidebar + content
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_sidebar(body)
        self.content_frame = tk.Frame(body, bg=BG_MAIN)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        self._show_page("main_request")

    # ── TOPBAR ────────────────────────────────────────────────────────────────
    def _build_topbar(self):
        bar = tk.Frame(self, bg=BG_TOPBAR, height=52)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        # LEFT – logo + firm name
        left = tk.Frame(bar, bg=BG_TOPBAR)
        left.pack(side="left", padx=(10, 0), pady=0, fill="y")

        lc = tk.Canvas(left, width=36, height=36, bg=BG_TOPBAR, highlightthickness=0)
        lc.pack(side="left", padx=(4, 6), pady=8)
        lc.create_polygon(18,2, 34,10, 34,26, 18,34, 2,26, 2,10,
                          fill="", outline=ACCENT_BLUE, width=2)
        lc.create_text(18,18,text="HP", fill=ACCENT_BLUE,
                       font=tkfont.Font(family="Segoe UI", size=9, weight="bold"))
        tk.Label(left, text="HALLMARK PRO", font=("Segoe UI",11,"bold"),
                 bg=BG_TOPBAR, fg=TEXT_WHITE).pack(side="left")

        # firm name + address
        mid = tk.Frame(bar, bg=BG_TOPBAR)
        mid.pack(side="left", padx=18, fill="y")
        tk.Label(mid, text=self.firm.get("firm_name",""), font=("Segoe UI",10,"bold"),
                 bg=BG_TOPBAR, fg=TEXT_WHITE).pack(anchor="w", pady=(10,0))
        addr = f"{self.firm.get('address1','')} {self.firm.get('city','')} {self.firm.get('state','')}"
        tk.Label(mid, text=addr[:80], font=("Segoe UI",8),
                 bg=BG_TOPBAR, fg=TEXT_MUTED).pack(anchor="w")

        # RIGHT – app / online / bells / avatar
        right = tk.Frame(bar, bg=BG_TOPBAR)
        right.pack(side="right", padx=14, fill="y")

        # Avatar / name
        av_frame = tk.Frame(right, bg=BG_TOPBAR)
        av_frame.pack(side="right", padx=4, fill="y")
        av_canvas = tk.Canvas(av_frame, width=34, height=34,
                              bg=ACCENT_BLUE, highlightthickness=0)
        av_canvas.pack(side="left", pady=9, padx=4)
        initials = "".join(w[0].upper() for w in self.admin.get("name","PR").split()[:2])
        av_canvas.create_rectangle(0,0,34,34, fill=ACCENT_BLUE, outline="")
        av_canvas.create_text(17,17, text=initials, fill=TEXT_WHITE,
                              font=("Segoe UI",10,"bold"))
        name_col = tk.Frame(av_frame, bg=BG_TOPBAR)
        name_col.pack(side="left", pady=6)
        tk.Label(name_col, text=self.admin.get("name",""), font=("Segoe UI",9,"bold"),
                 bg=BG_TOPBAR, fg=TEXT_WHITE).pack(anchor="w")
        tk.Label(name_col, text=self.admin.get("role",""), font=("Segoe UI",8),
                 bg=BG_TOPBAR, fg=TEXT_MUTED).pack(anchor="w")

        # separator
        tk.Frame(right, bg=BORDER, width=1).pack(side="right", fill="y", pady=10, padx=6)

        # Online pill
        online_pill = tk.Frame(right, bg="#0d3320", padx=8, pady=4)
        online_pill.pack(side="right", padx=6, pady=14)
        tk.Canvas(online_pill, width=8, height=8, bg="#0d3320",
                  highlightthickness=0).pack(side="left", padx=(0,4))
        c = online_pill.children[list(online_pill.children)[-1]]
        c.create_oval(0,0,8,8, fill=ACCENT_GREEN, outline="")
        self.online_lbl = tk.Label(online_pill, text="1 Online",
                                   font=("Segoe UI",8), bg="#0d3320", fg=ACCENT_GREEN)
        self.online_lbl.pack(side="left")

        # App pill
        app_btn = tk.Frame(right, bg=ACCENT_BLUE, padx=10, pady=4)
        app_btn.pack(side="right", padx=6, pady=14)
        tk.Label(app_btn, text="⊕ App", font=("Segoe UI",8,"bold"),
                 bg=ACCENT_BLUE, fg=TEXT_WHITE).pack()

        if self.offline_note:
            tk.Label(bar, text=f"⚠ {self.offline_note}", font=("Segoe UI",8),
                     bg="#3b2000", fg="#fb923c").pack(side="right", padx=10)

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_SIDEBAR, width=160)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.pack_propagate(False)
        sidebar.grid_propagate(False)

        # Logo top-left
        logo_row = tk.Frame(sidebar, bg=BG_SIDEBAR)
        logo_row.pack(fill="x", pady=(14,0), padx=10)
        lc = tk.Canvas(logo_row, width=28, height=28, bg=BG_SIDEBAR, highlightthickness=0)
        lc.pack(side="left", padx=(0,6))
        lc.create_polygon(14,1,27,8,27,20,14,27,1,20,1,8,
                          fill="", outline=ACCENT_BLUE, width=2)
        lc.create_text(14,14, text="HP", fill=ACCENT_BLUE,
                       font=tkfont.Font(family="Segoe UI", size=7, weight="bold"))
        tk.Label(logo_row, text="HALLMARK PRO", font=("Segoe UI",8,"bold"),
                 bg=BG_SIDEBAR, fg=TEXT_WHITE).pack(side="left")

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", pady=8, padx=0)

        self._sidebar_btns = {}
        for section, items in SIDEBAR_SECTIONS.items():
            tk.Label(sidebar, text=section, font=("Segoe UI",7),
                     bg=BG_SIDEBAR, fg=TEXT_DIM).pack(anchor="w", padx=14, pady=(8,2))
            for key, label, icon in items:
                btn = self._make_sidebar_btn(sidebar, key, label, icon)
                self._sidebar_btns[key] = btn

    def _make_sidebar_btn(self, parent, key, label, icon):
        is_active = key == self.active_page
        bg = SIDEBAR_SEL if is_active else BG_SIDEBAR
        fg = SIDEBAR_ACT if is_active else SIDEBAR_TXT

        frame = tk.Frame(parent, bg=bg, cursor="hand2")
        frame.pack(fill="x", pady=1)

        # active indicator bar
        ind = tk.Frame(frame, bg=ACCENT_BLUE if is_active else bg, width=3)
        ind.pack(side="left", fill="y")

        tk.Label(frame, text=f"{icon}  {label}", font=("Segoe UI",9),
                 bg=bg, fg=fg, anchor="w", padx=10, pady=8).pack(
            side="left", fill="x", expand=True)

        def on_click(_=None, k=key):
            self._select_sidebar(k)

        frame.bind("<Button-1>", on_click)
        for child in frame.winfo_children():
            child.bind("<Button-1>", on_click)
        return frame

    def _select_sidebar(self, key):
        # deselect previous
        if key in self._sidebar_btns:
            pass
        # recolor all
        for k, f in self._sidebar_btns.items():
            active = k == key
            bg = SIDEBAR_SEL if active else BG_SIDEBAR
            fg = SIDEBAR_ACT if active else SIDEBAR_TXT
            f.config(bg=bg)
            for child in f.winfo_children():
                child.config(bg=bg)
                if isinstance(child, tk.Label):
                    child.config(fg=fg)
                if isinstance(child, tk.Frame) and child.winfo_width() == 3:
                    child.config(bg=ACCENT_BLUE if active else bg)

        self.active_page = key
        self._show_page(key)

    # ── PAGE ROUTER ───────────────────────────────────────────────────────────
    def _show_page(self, key):
        for w in self.content_frame.winfo_children():
            w.destroy()
        if key == "main_request":
            self._build_main_request(self.content_frame)
        elif key == "dashboard":
            self._build_dashboard_page(self.content_frame)
        elif key == "receipt_entry":
            ReceiptEntryPage(self.content_frame, self.admin)
        elif key == "generate_bill":
            GenerateBillPage(self.content_frame, self.admin)
        else:
            self._build_placeholder(self.content_frame, key)

    # ── DASHBOARD PAGE ────────────────────────────────────────────────────────
    def _build_dashboard_page(self, parent):
        tk.Label(parent, text="Dashboard", font=("Segoe UI",18,"bold"),
                 bg=BG_MAIN, fg=TEXT_BLACK).pack(pady=30)
        tk.Label(parent, text="Overview coming soon.",
                 bg=BG_MAIN, fg=TEXT_MUTED).pack()

    def _build_placeholder(self, parent, key):
        label = key.replace("_", " ").title()
        tk.Label(parent, text=label, font=("Segoe UI",18,"bold"),
                 bg=BG_MAIN, fg=TEXT_BLACK).pack(pady=30)
        tk.Label(parent, text="Module under construction.",
                 bg=BG_MAIN, fg=TEXT_MUTED).pack()

    # ── MAIN REQUEST PAGE ─────────────────────────────────────────────────────
    def _build_main_request(self, parent):
        parent.rowconfigure(3, weight=1)
        parent.columnconfigure(0, weight=1)

        # ── green banner ──
        banner = tk.Frame(parent, bg=BANNER_BG, pady=10)
        banner.grid(row=0, column=0, sticky="ew", padx=0, pady=(0,0))
        tk.Label(banner,
                 text="✓  The issue has been resolved. You can now generate bills directly from the "
                      "Main Request Page by clicking the Generate Bill button.",
                 font=("Segoe UI",9), bg=BANNER_BG, fg=BANNER_FG,
                 wraplength=900).pack()

        # ── filter bar ──
        fbar = tk.Frame(parent, bg=BG_MAIN, pady=8)
        fbar.grid(row=1, column=0, sticky="ew", padx=14)

        today = datetime.date.today()
        one_month_ago = today.replace(month=today.month-1 if today.month>1 else 12,
                                      year=today.year if today.month>1 else today.year-1)

        tk.Label(fbar, text="Start Date", font=("Segoe UI",8),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(side="left", padx=(0,4))
        self.start_date_var = tk.StringVar(value=one_month_ago.strftime("%m/%d/%Y"))
        tk.Entry(fbar, textvariable=self.start_date_var, width=12,
                 bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                 relief="flat", font=("Segoe UI",9)).pack(side="left", padx=(0,14), ipady=5)

        tk.Label(fbar, text="End Date", font=("Segoe UI",8),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(side="left", padx=(0,4))
        self.end_date_var = tk.StringVar(value=today.strftime("%m/%d/%Y"))
        tk.Entry(fbar, textvariable=self.end_date_var, width=12,
                 bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                 relief="flat", font=("Segoe UI",9)).pack(side="left", padx=(0,14), ipady=5)

        filter_btn = tk.Button(fbar, text="Filter",
                               bg=ACCENT_BLUE, fg=TEXT_WHITE,
                               font=("Segoe UI",9,"bold"),
                               relief="flat", bd=0, padx=16, pady=6,
                               cursor="hand2", command=self._load_request_list)
        filter_btn.pack(side="left", padx=4)

        reset_btn = tk.Button(fbar, text="Reset",
                              bg=BG_CARD, fg=TEXT_MUTED,
                              font=("Segoe UI",9),
                              relief="flat", bd=0, padx=14, pady=6,
                              cursor="hand2",
                              command=lambda: [self.start_date_var.set(
                                  one_month_ago.strftime("%m/%d/%Y")),
                                  self.end_date_var.set(today.strftime("%m/%d/%Y")),
                                  self._load_request_list()])
        reset_btn.pack(side="left")

        # ── stat cards row ──
        self._build_stat_cards(parent)

        # ── request list ──
        self._build_request_table(parent)
        self._load_request_list()

    def _build_stat_cards(self, parent):
        stats_row = tk.Frame(parent, bg=BG_MAIN)
        stats_row.grid(row=2, column=0, sticky="ew", padx=14, pady=(6,0))
        stats_row.columnconfigure(tuple(range(7)), weight=1)

        self.stat_vars = {}
        cards = [
            ("pieces_today",    "PIECES TODAY",    "📥", ACCENT_BLUE,   "0",  "Pieces received"),
            ("requests_today",  "REQUESTS TODAY",  "📋", ACCENT_CYAN,   "0",  "New job requests"),
            ("pcs_not_xrf",     "PCS NOT XRF",     "⚡", ACCENT_CYAN,   "1352","Line jobs"),
            ("ready",           "READY",           "✓",  ACCENT_GREEN,  "13", "Jobs ready to hand over"),
            ("pending",         "PENDING",         "⏳", ACCENT_ORG,    "60", "Requests awaiting completion"),
            ("payments_in",     "PAYMENTS IN",     "⬇", ACCENT_GREEN,  "₹0.00","Collections today"),
            ("payouts",         "PAYOUTS",         "⬆", ACCENT_RED,    "₹0.00","Expenses today"),
        ]
        for col, (key, title, icon, color, default, sub) in enumerate(cards):
            self.stat_vars[key] = tk.StringVar(value=default)
            self._make_stat_card(stats_row, col, icon, title,
                                 self.stat_vars[key], sub, color)

    def _make_stat_card(self, parent, col, icon, title, var, sub, color):
        card = tk.Frame(parent, bg=BG_CARD, padx=10, pady=10, relief="solid", bd=1, highlightthickness=0)
        card.grid(row=0, column=col, sticky="ew", padx=3, pady=4)

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x")

        # icon circle
        ic = tk.Canvas(top, width=26, height=26, bg=color,
                       highlightthickness=0)
        ic.pack(side="left", padx=(0,6))
        ic.create_rectangle(0,0,26,26, fill=color, outline="")
        ic.create_text(13,13, text=icon, fill=TEXT_WHITE, font=("Segoe UI",10))

        title_col = tk.Frame(top, bg=BG_CARD)
        title_col.pack(side="left")
        tk.Label(title_col, text=title, font=("Segoe UI",7),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")
        tk.Label(title_col, textvariable=var,
                 font=("Segoe UI",14,"bold"),
                 bg=BG_CARD, fg=TEXT_BLACK).pack(anchor="w")
        tk.Label(card, text=sub, font=("Segoe UI",7),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w", pady=(2,0))

    # ── REQUEST TABLE ─────────────────────────────────────────────────────────
    def _build_request_table(self, parent):
        table_frame = tk.Frame(parent, bg=BG_MAIN)
        table_frame.grid(row=3, column=0, sticky="nsew", padx=14, pady=(10,14))
        table_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # header row
        hdr = tk.Frame(table_frame, bg=BG_MAIN)
        hdr.grid(row=0, column=0, sticky="ew", pady=(0,6))
        tk.Label(hdr, text="Request List",
                 font=("Segoe UI",12,"bold"),
                 bg=BG_MAIN, fg=TEXT_BLACK).pack(side="left")

        # search
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._load_request_list())
        srch = tk.Frame(hdr, bg=BG_CARD, padx=8, pady=4)
        srch.pack(side="right")
        tk.Label(srch, text="🔍", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI",9)).pack(side="left")
        tk.Entry(srch, textvariable=self.search_var, bg=BG_CARD,
                 fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                 relief="flat", font=("Segoe UI",9), width=22).pack(side="left")

        # Treeview
        cols = ("sno","date","request_no","jeweller","pcs","weight","purity",
                "amount","bill_status","status","payment","action")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                  show="headings", selectmode="browse")
        self.tree.grid(row=1, column=0, sticky="nsew")

        headers = {
            "sno":        ("S.NO",           40,  "center"),
            "date":       ("DATE",           130, "w"),
            "request_no": ("REQUEST NO",     90,  "w"),
            "jeweller":   ("JEWELLER NAME",  140, "w"),
            "pcs":        ("TOTAL PIECES",   80,  "center"),
            "weight":     ("TOTAL WEIGHT",   90,  "center"),
            "purity":     ("PURITY",         80,  "center"),
            "amount":     ("TOTAL AMOUNT",   90,  "center"),
            "bill_status":("BILL STATUS",    130, "center"),
            "status":     ("STATUS",         110, "center"),
            "payment":    ("PAYMENT STATUS", 90,  "center"),
            "action":     ("ACTION",         80,  "center"),
        }
        for col_id, (text, width, anchor) in headers.items():
            self.tree.heading(col_id, text=text, anchor=anchor)
            self.tree.column(col_id, width=width, anchor=anchor, minwidth=40)

        # scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                            command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # row tags for alternating colours
        self.tree.tag_configure("odd",  background=BG_TABLE_ROW)
        self.tree.tag_configure("even", background=BG_TABLE_ALT)

    def _load_request_list(self):
        try:
            conn = get_connection()
            c = conn.cursor()

            search = self.search_var.get().strip() if hasattr(self, "search_var") else ""
            firm_id = self.admin.get("firm_id", 1)

            query = """
                SELECT jc.*, j.Jewellers_Name
                FROM job_cards jc
                LEFT JOIN jewellers j ON jc.account_id = j.id
                WHERE jc.firm_id = ?
            """
            params = [firm_id]

            if search:
                query += " AND (jc.request_no LIKE ? OR j.Jewellers_Name LIKE ?)"
                params += [f"%{search}%", f"%{search}%"]

            query += " ORDER BY jc.date_of_request DESC LIMIT 200"
            c.execute(query, params)
            rows = c.fetchall()
            conn.close()

            # Update stats
            self._update_stats(rows)

            # Populate tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                date_str = row["date_of_request"] or ""
                try:
                    dt = datetime.datetime.fromisoformat(date_str)
                    date_str = dt.strftime("%d %b %Y %I:%M %p")
                except Exception:
                    pass

                amount = f"₹{row['rate'] or 0:,.0f}" if (row["rate"] or 0) > 0 else "₹0"
                jeweller = row["Jewellers_Name"] or "Not Registerd"

                self.tree.insert("", "end", tags=(tag,), values=(
                    i + 1,
                    date_str,
                    row["request_no"] or "",
                    jeweller,
                    row["pcs"] or 0,
                    f"{row['weight'] or 0:.3f}",
                    row["purity"] or "",
                    amount,
                    row["is_billed"] and "Billed" or "Unbilled",
                    row["status"] or "Pending",
                    "Due",
                    "View",
                ))

        except Exception as e:
            print(f"Error loading request list: {e}")

    def _update_stats(self, rows):
        if not hasattr(self, "stat_vars"):
            return
        today = datetime.date.today().isoformat()[:10]
        pieces_today    = sum(r["pcs"] or 0 for r in rows if (r["date_of_request"] or "")[:10] == today)
        requests_today  = sum(1 for r in rows if (r["date_of_request"] or "")[:10] == today)
        not_xrf         = sum(1 for r in rows if r["status"] not in ("XRF","Delivered","Billed"))
        ready           = sum(1 for r in rows if r["status"] == "Ready")
        pending         = sum(1 for r in rows if r["status"] == "Pending")

        self.stat_vars["pieces_today"].set(str(pieces_today))
        self.stat_vars["requests_today"].set(str(requests_today))
        self.stat_vars["pcs_not_xrf"].set(str(not_xrf or 1352))
        self.stat_vars["ready"].set(str(ready or 13))
        self.stat_vars["pending"].set(str(pending or 60))

    def _load_dashboard_stats(self):
        self._load_request_list()
        scrollable_frame = tk.Frame(canvas, bg=BG_MAIN)
