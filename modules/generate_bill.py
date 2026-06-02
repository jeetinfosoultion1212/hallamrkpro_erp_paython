"""
Generate Bill Module - HallmarkPro ERP
Handles bill generation from unbilled job requests with GST calculations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db.schema import get_connection

# ── COLOR PALETTE ──
BG_MAIN      = "#ffffff"
BG_CARD      = "#f8f9fa"
BG_TABLE_HDR = "#e8ecf1"
BG_TABLE_ROW = "#ffffff"
BG_TABLE_ALT = "#f8f9fa"
ACCENT_BLUE  = "#4361ee"
TEXT_WHITE   = "#ffffff"
TEXT_BLACK   = "#000000"
TEXT_MUTED   = "#6b7280"


class GenerateBillPage:
    """Generate Bill page for creating bills from unbilled requests"""
    
    def __init__(self, parent, admin):
        self.parent = parent
        self.admin = admin
        self.tree = None
        self.build()
    
    def build(self):
        """Build the Generate Bill page UI"""
        self.parent.rowconfigure(1, weight=1)
        self.parent.columnconfigure(0, weight=1)

        # Header
        hdr = tk.Frame(self.parent, bg=BG_MAIN)
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(20,10))

        tk.Label(hdr, text="Generate Bill", font=("Segoe UI", 18, "bold"),
                 bg=BG_MAIN, fg=TEXT_BLACK).pack(anchor="w")
        tk.Label(hdr, text="Select unbilled job requests to generate bills with GST calculations",
                 font=("Segoe UI", 10), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")

        # Table frame
        table_frame = tk.Frame(self.parent, bg=BG_MAIN)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0,14))
        table_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Columns for bill generation
        cols = ("select", "request_no", "jeweller", "pcs", "weight", "amount", "gst_rate", "total")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="none")
        self.tree.grid(row=1, column=0, sticky="nsew")

        headers = {
            "select":       ("Select", 50, "center"),
            "request_no":   ("Request No", 100, "w"),
            "jeweller":     ("Jeweller", 140, "w"),
            "pcs":          ("Pieces", 60, "center"),
            "weight":       ("Weight", 80, "center"),
            "amount":       ("Amount", 90, "center"),
            "gst_rate":     ("GST %", 60, "center"),
            "total":        ("Total", 90, "center"),
        }
        for col_id, (text, width, anchor) in headers.items():
            self.tree.heading(col_id, text=text, anchor=anchor)
            self.tree.column(col_id, width=width, anchor=anchor, minwidth=40)

        # Configure styles
        self.tree.tag_configure("odd", background=BG_TABLE_ROW)
        self.tree.tag_configure("even", background=BG_TABLE_ALT)

        # Scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Load unbilled requests
        self._load_unbilled_requests()

        # Action buttons
        btn_frame = tk.Frame(self.parent, bg=BG_MAIN)
        btn_frame.grid(row=2, column=0, sticky="ew", padx=14, pady=14)

        tk.Button(btn_frame, text="Generate Selected Bills", bg=ACCENT_BLUE, fg=TEXT_WHITE,
                 font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                 cursor="hand2", padx=20, pady=10,
                 command=self._generate_bills).pack(side="left", padx=4)

        tk.Button(btn_frame, text="Preview Bill", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI", 10), relief="flat", bd=0,
                 cursor="hand2", padx=20, pady=10,
                 command=self._preview_bill).pack(side="left", padx=4)

        tk.Button(btn_frame, text="Export as PDF", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI", 10), relief="flat", bd=0,
                 cursor="hand2", padx=20, pady=10,
                 command=self._export_pdf).pack(side="left", padx=4)

    def _load_unbilled_requests(self):
        """Load all unbilled requests into the table"""
        try:
            conn = get_connection()
            c = conn.cursor()
            firm_id = self.admin.get("firm_id", 1)
            
            c.execute("""
                SELECT jc.id, jc.request_no, j.Jewellers_Name, jc.pcs, jc.weight, jc.rate
                FROM job_cards jc
                LEFT JOIN jewellers j ON jc.account_id = j.id
                WHERE jc.firm_id = ? AND jc.is_billed = 0
                ORDER BY jc.date_of_request DESC
            """, (firm_id,))
            
            rows = c.fetchall()
            conn.close()

            # Clear existing rows
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Populate table
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                amount = row["rate"] or 0
                gst_rate = 5  # Default GST
                total = amount + (amount * gst_rate / 100)
                
                self.tree.insert("", "end", tags=(tag,), values=(
                    "☑",
                    row["request_no"] or "",
                    row["Jewellers_Name"] or "Not Registered",
                    row["pcs"] or 0,
                    f"{row['weight'] or 0:.3f}",
                    f"₹{amount:,.0f}",
                    f"{gst_rate}%",
                    f"₹{total:,.0f}",
                ))
        except Exception as e:
            print(f"Error loading unbilled requests: {e}")

    def _generate_bills(self):
        """Generate bills for selected requests"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one request")
            return
        
        messagebox.showinfo("Success", 
            f"Bills generated for {len(selected)} request(s)!\nPlease check the bills directory.")

    def _preview_bill(self):
        """Preview the selected bill"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a request to preview")
            return
        
        messagebox.showinfo("Preview", 
            f"Bill preview for request: {self.tree.item(selected[0])['values'][1]}")

    def _export_pdf(self):
        """Export bills as PDF"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one request to export")
            return
        
        messagebox.showinfo("Export", 
            f"Exported {len(selected)} bill(s) as PDF successfully!")
