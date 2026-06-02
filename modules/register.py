import tkinter as tk
from tkinter import font as tkfont, ttk, messagebox, filedialog
import threading
import os, sys
import hashlib
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db.schema import get_connection

# ── Exact colours from screenshot ────────────────────────────────────────────
BG_LEFT      = "#0d1b3e"
BG_RIGHT     = "#08111f"
ACCENT_BLUE  = "#4361ee"
ACCENT_GOLD  = "#f59e0b"
ACCENT_CYAN  = "#38bdf8"
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


class RegisterWindow(tk.Tk):
    def __init__(self, on_back_to_login=None):
        super().__init__()
        self.title("HallmarkPro – Register Firm")
        self.geometry("1366x720")
        self.minsize(1100, 600)
        self.configure(bg=BG_LEFT)
        self.resizable(True, True)
        self.on_back_to_login = on_back_to_login
        self.logo_path = None
        self.selected_logo = None
        
        # Create folders for logos
        self._setup_directories()
        
        self._load_fonts()
        self._build_ui()
        self.after(100, self.center_window)

    def _setup_directories(self):
        """Create necessary directories for logo storage"""
        self.logos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logos")
        if not os.path.exists(self.logos_dir):
            os.makedirs(self.logos_dir, exist_ok=True)

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

    def _build_ui(self):
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

        # ── dot-grid canvas ──
        self.grid_canvas = tk.Canvas(left, bg=BG_LEFT, highlightthickness=0)
        self.grid_canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_canvas.bind("<Configure>", self._redraw_grid)

        # ── centred content ──
        content = tk.Frame(left, bg=BG_LEFT)
        content.place(relx=0.5, rely=0.5, anchor="center")

        # ── HP logo circle ──
        logo_c = tk.Canvas(content, width=100, height=100,
                           bg=BG_LEFT, highlightthickness=0)
        logo_c.pack(pady=(0, 18))
        logo_c.create_oval(4, 4, 96, 96,
                           outline="#1e4080", width=1, fill=BG_LEFT)
        logo_c.create_oval(8, 8, 92, 92,
                           outline=ACCENT_BLUE, width=2, fill="#0d1e3c")
        logo_c.create_oval(14, 14, 86, 86,
                           outline="#162d55", width=1, fill="#0a1628")
        logo_c.create_text(42, 50, text="H",
                           font=tkfont.Font(family="Segoe UI", size=22, weight="bold"),
                           fill=ACCENT_GOLD, anchor="e")
        logo_c.create_text(58, 50, text="P",
                           font=tkfont.Font(family="Segoe UI", size=22, weight="bold"),
                           fill=ACCENT_BLUE, anchor="w")

        # ── Registration badge ──
        badge_outer = tk.Frame(content, bg=BADGE_BG,
                               highlightbackground=BADGE_BORDER,
                               highlightthickness=1)
        badge_outer.pack(pady=(0, 24))
        badge_inner = tk.Frame(badge_outer, bg=BADGE_BG, padx=16, pady=6)
        badge_inner.pack()
        tk.Label(badge_inner, text="★ REGISTRATION",
                 font=self.fn(9), bg=BADGE_BG, fg=TEXT_MUTED).pack()

        # ── Headline ──
        tk.Label(content, text="Join Our",
                 font=tkfont.Font(family="Segoe UI", size=30, weight="bold"),
                 bg=BG_LEFT, fg=TEXT_WHITE).pack()
        tk.Label(content, text="Community",
                 font=tkfont.Font(family="Segoe UI", size=30, weight="bold"),
                 bg=BG_LEFT, fg=ACCENT_CYAN).pack()

        # ── taglines ──
        tk.Label(content, text="Manage your jewelry business with ease.",
                 font=self.fn(10), bg=BG_LEFT, fg=TEXT_MUTED).pack(pady=(14, 2))
        tk.Label(content,
                 text="Trusted by 60+ hallmark centres across India.",
                 font=self.fn(10), bg=BG_LEFT, fg=TEXT_MUTED).pack()

        # ── stats row ──
        stats = [
            ("60+",    "CENTRES",     ACCENT_GOLD),
            ("17.5K+", "ENTRIES",     TEXT_WHITE),
        ]
        row = tk.Frame(content, bg=BG_LEFT)
        row.pack(pady=(24, 0))
        for val, lbl, color in stats:
            cell = tk.Frame(row, bg=BG_LEFT)
            cell.pack(side="left", padx=22)
            tk.Label(cell, text=val,
                     font=tkfont.Font(family="Segoe UI", size=22, weight="bold"),
                     bg=BG_LEFT, fg=color).pack()
            tk.Label(cell, text=lbl,
                     font=self.fn(7), bg=BG_LEFT, fg=TEXT_DIM).pack()

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

    # ══════════════════════════════════════════════════════════════════════════
    #  RIGHT PANEL  (40%)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_right_panel(self):
        right = tk.Frame(self, bg=BG_RIGHT)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        # vertical divider
        divider = tk.Frame(right, bg="#0d2040", width=1)
        divider.place(x=0, y=0, relheight=1)

        # Scrollable form
        canvas = tk.Canvas(right, bg=BG_RIGHT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_RIGHT)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        right.rowconfigure(0, weight=1)

        # ── card content ──
        card = tk.Frame(scrollable_frame, bg=BG_RIGHT)
        card.pack(padx=20, pady=20, fill="both", expand=True)

        # ── title ──
        tk.Label(card, text="Create Your Account",
                 font=tkfont.Font(family="Segoe UI", size=18, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_WHITE).pack(pady=(0, 4))
        tk.Label(card, text="Fill in the details below to open your admin centre",
                 font=self.fn(9), bg=BG_RIGHT, fg=TEXT_MUTED).pack(pady=(0, 20))

        # ── Two column form ──
        form_row1 = tk.Frame(card, bg=BG_RIGHT)
        form_row1.pack(fill="x", pady=(0, 14))

        col1 = tk.Frame(form_row1, bg=BG_RIGHT)
        col1.pack(side="left", fill="both", expand=True, padx=(0, 8))

        col2 = tk.Frame(form_row1, bg=BG_RIGHT)
        col2.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # ── FIRM NAME ──
        tk.Label(col1, text="FIRM NAME *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.firm_name_var = tk.StringVar()
        self._build_input(col1, self.firm_name_var, "e.g. ABC Hallmarking", 200)

        # ── FULL NAME ──
        tk.Label(col2, text="FULL NAME *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.full_name_var = tk.StringVar()
        self._build_input(col2, self.full_name_var, "John Doe", 200)

        # ── Row 2 ──
        form_row2 = tk.Frame(card, bg=BG_RIGHT)
        form_row2.pack(fill="x", pady=(0, 14))

        col3 = tk.Frame(form_row2, bg=BG_RIGHT)
        col3.pack(side="left", fill="both", expand=True, padx=(0, 8))

        col4 = tk.Frame(form_row2, bg=BG_RIGHT)
        col4.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # ── PHONE NUMBER ──
        tk.Label(col3, text="PHONE NUMBER *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.phone_var = tk.StringVar()
        self._build_input(col3, self.phone_var, "10 digit mobile", 200)

        # ── EMAIL ADDRESS ──
        tk.Label(col4, text="EMAIL ADDRESS *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.email_var = tk.StringVar()
        self._build_input(col4, self.email_var, "email@example.com", 200)

        # ── Row 3 ──
        form_row3 = tk.Frame(card, bg=BG_RIGHT)
        form_row3.pack(fill="x", pady=(0, 14))

        col5 = tk.Frame(form_row3, bg=BG_RIGHT)
        col5.pack(side="left", fill="both", expand=True, padx=(0, 8))

        col6 = tk.Frame(form_row3, bg=BG_RIGHT)
        col6.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # ── ADDRESS ──
        tk.Label(col5, text="ADDRESS",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.address_var = tk.StringVar()
        self._build_input(col5, self.address_var, "Street address", 200)

        # ── STATE ──
        tk.Label(col6, text="STATE",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.state_var = tk.StringVar(value="Select State")
        states = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
        state_combo = ttk.Combobox(col6, textvariable=self.state_var,
                                   values=states, state="readonly", width=30)
        state_combo.pack(fill="x", pady=(5, 14))

        # ── Row 4 ──
        form_row4 = tk.Frame(card, bg=BG_RIGHT)
        form_row4.pack(fill="x", pady=(0, 14))

        col7 = tk.Frame(form_row4, bg=BG_RIGHT)
        col7.pack(side="left", fill="both", expand=True, padx=(0, 8))

        col8 = tk.Frame(form_row4, bg=BG_RIGHT)
        col8.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # ── PASSWORD ──
        tk.Label(col7, text="PASSWORD *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.password_var = tk.StringVar()
        self._build_password_input(col7, self.password_var)

        # ── CONFIRM PASSWORD ──
        tk.Label(col8, text="CONFIRM PASSWORD *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w")
        self.confirm_pw_var = tk.StringVar()
        self._build_password_input(col8, self.confirm_pw_var)

        # ── FIRM TYPE ──
        tk.Label(card, text="FIRM TYPE *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 5))
        self.firm_type_var = tk.StringVar(value="Select Firm Type")
        firm_types = ["Hallmark Centre", "Jewelry Workshop", "Manufacturing", "Retail Store"]
        firm_combo = ttk.Combobox(card, textvariable=self.firm_type_var,
                                  values=firm_types, state="readonly", width=46)
        firm_combo.pack(fill="x", pady=(0, 14))

        # ── FIRM LOGO UPLOAD ──
        tk.Label(card, text="FIRM LOGO (Round Shape) *",
                 font=tkfont.Font(family="Segoe UI", size=8, weight="bold"),
                 bg=BG_RIGHT, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 8))

        logo_frame = tk.Frame(card, bg=BG_RIGHT)
        logo_frame.pack(fill="x", pady=(0, 14))

        self.logo_btn = tk.Button(logo_frame, text="📁 Upload Logo (PNG/JPG)",
                                 bg=ACCENT_BLUE, fg=TEXT_WHITE,
                                 font=self.fn(9), relief="flat", bd=0,
                                 cursor="hand2", padx=20, pady=10,
                                 command=self._select_logo)
        self.logo_btn.pack(side="left", padx=(0, 10))

        self.logo_status = tk.Label(logo_frame, text="No logo selected",
                                   bg=BG_RIGHT, fg=TEXT_MUTED,
                                   font=self.fn(8))
        self.logo_status.pack(side="left")

        # ── error label ──
        self.error_var = tk.StringVar()
        tk.Label(card, textvariable=self.error_var,
                 fg="#f87171", bg=BG_RIGHT,
                 font=self.fn(8), wraplength=320).pack(pady=(0, 10))

        # ── Create Account button ──
        self.create_btn = tk.Button(
            card,
            text="🏛  Create Account",
            font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
            bg=ACCENT_BLUE, fg=TEXT_WHITE,
            activebackground="#3451d1",
            activeforeground=TEXT_WHITE,
            relief="flat", bd=0,
            cursor="hand2",
            pady=12,
            command=self._do_register
        )
        self.create_btn.pack(fill="x", pady=(10, 14))

        # ── bottom links ──
        links = tk.Frame(card, bg=BG_RIGHT)
        links.pack(pady=(10, 0))

        back = tk.Label(links, text="◄ Already have an account? Login",
                       fg=ACCENT_BLUE, bg=BG_RIGHT,
                       cursor="hand2", font=self.fn(9))
        back.pack()
        back.bind("<Button-1>", lambda e: self._go_back_to_login())

    def _build_input(self, parent, var, placeholder, width):
        wrap = tk.Frame(parent, bg=INPUT_BG,
                       highlightbackground="#c8d4e8",
                       highlightthickness=1)
        wrap.pack(fill="x", pady=(5, 14), ipady=0)
        inner = tk.Frame(wrap, bg=INPUT_BG)
        inner.pack(fill="x", padx=4)

        entry = tk.Entry(inner, textvariable=var, width=width // 9,
                        bg=INPUT_BG, fg=INPUT_FG, relief="flat", bd=0,
                        font=tkfont.Font(family="Segoe UI", size=11),
                        insertbackground=INPUT_FG)
        entry.pack(fill="x", expand=True, pady=10, padx=8)
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=INPUT_FG)

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="#9aaccc")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _build_password_input(self, parent, var):
        wrap = tk.Frame(parent, bg=INPUT_BG,
                       highlightbackground="#c8d4e8",
                       highlightthickness=1)
        wrap.pack(fill="x", pady=(5, 14), ipady=0)
        inner = tk.Frame(wrap, bg=INPUT_BG)
        inner.pack(fill="x", padx=4)

        entry = tk.Entry(inner, textvariable=var, show="●",
                        bg=INPUT_BG, fg=INPUT_FG, relief="flat", bd=0,
                        font=tkfont.Font(family="Segoe UI", size=11),
                        insertbackground=INPUT_FG)
        entry.pack(fill="x", expand=True, pady=10, padx=8)

    def _select_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Firm Logo (Round Shape)",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")]
        )
        if file_path:
            self.logo_path = file_path
            filename = os.path.basename(file_path)
            self.logo_status.config(text=f"✓ {filename}", fg=ACCENT_GREEN)

    def _do_register(self):
        firm_name = self.firm_name_var.get().strip()
        full_name = self.full_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        state = self.state_var.get()
        password = self.password_var.get()
        confirm_pw = self.confirm_pw_var.get()
        firm_type = self.firm_type_var.get()

        # Validation
        if not firm_name or not full_name or not phone or not email:
            self.error_var.set("All marked fields (*) are required.")
            return

        if not password or len(password) < 6:
            self.error_var.set("Password must be at least 6 characters.")
            return

        if password != confirm_pw:
            self.error_var.set("Passwords do not match.")
            return

        if firm_type == "Select Firm Type":
            self.error_var.set("Please select a firm type.")
            return

        if not self.logo_path:
            self.error_var.set("Please upload a firm logo.")
            return

        self.error_var.set("")
        self.create_btn.config(state="disabled", text="Creating account…")

        def _run():
            result = self._register_firm(
                firm_name, full_name, phone, email, address, state, 
                password, firm_type, self.logo_path
            )
            self.after(0, lambda: self._on_register_result(result))

        threading.Thread(target=_run, daemon=True).start()

    def _register_firm(self, firm_name, full_name, phone, email, address, state, password, firm_type, logo_path):
        try:
            # Save logo to assets folder
            saved_logo_path = self._save_logo(logo_path, phone)
            
            conn = get_connection()
            c = conn.cursor()

            # Insert firm
            c.execute("""
                INSERT INTO firms (firm_name, contact_person, phone_number, email, address1, state, 
                                 firm_type, logo_path, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, datetime('now'))
            """, (firm_name, full_name, phone, email, address, state, firm_type, saved_logo_path))

            firm_id = c.lastrowid

            # Insert admin
            pw_hash = hashlib.sha256(password.encode()).hexdigest()
            c.execute("""
                INSERT INTO admins (username, name, phone_number, email, password, role, firm_id, status, created_at)
                VALUES (?, ?, ?, ?, ?, 'admin', ?, 1, datetime('now'))
            """, (phone, full_name, phone, email, pw_hash, firm_id))

            conn.commit()
            conn.close()

            return {"ok": True, "message": "Registration successful! You can now login."}

        except Exception as e:
            return {"ok": False, "error": f"Registration failed: {str(e)}"}

    def _save_logo(self, logo_path, phone):
        """Save logo to assets directory"""
        try:
            # Get file extension
            file_ext = os.path.splitext(logo_path)[1]
            if not file_ext:
                file_ext = ".png"
            
            # Generate unique filename
            filename = f"{phone}_logo{file_ext}"
            dest_path = os.path.join(self.logos_dir, filename)

            # Copy logo file
            shutil.copy2(logo_path, dest_path)
            return dest_path

        except Exception as e:
            raise Exception(f"Failed to save logo: {str(e)}")

    def _on_register_result(self, result):
        self.create_btn.config(state="normal", text="🏛  Create Account")
        if result["ok"]:
            messagebox.showinfo("Success", result["message"])
            self._go_back_to_login()
        else:
            self.error_var.set(result.get("error", "Registration failed."))

    def _go_back_to_login(self):
        if self.on_back_to_login:
            self.on_back_to_login()
        self.destroy()
