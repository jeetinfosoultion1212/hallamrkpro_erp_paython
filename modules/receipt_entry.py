"""
Receipt Entry Module - HallmarkPro ERP
Handles jewelry receipt entry with dynamic items
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
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
ACCENT_RED   = "#ef4444"
TEXT_WHITE   = "#ffffff"
TEXT_BLACK   = "#000000"
TEXT_MUTED   = "#6b7280"
TEXT_DIM     = "#9ca3af"


class ReceiptEntryPage:
    """Receipt Entry page for jewelry receipts"""
    
    def __init__(self, parent, admin):
        self.parent = parent
        self.admin = admin
        self.items_list = []
        self.build()
    
    def build(self):
        """Build the Receipt Entry page UI"""
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        
        # Scrollable frame
        canvas = tk.Canvas(self.parent, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_MAIN)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Title
        tk.Label(scrollable_frame, text="Receipt Entry", font=("Segoe UI", 18, "bold"),
                 bg=BG_MAIN, fg=TEXT_BLACK).pack(anchor="w", padx=14, pady=(20,10))
        
        tk.Label(scrollable_frame, text="Enter jewelry receipt details with item line items",
                 font=("Segoe UI", 10), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", padx=14, pady=(0,20))

        # Form frame
        form = tk.Frame(scrollable_frame, bg=BG_MAIN)
        form.pack(padx=14, fill="x")

        # Two column form
        col1 = tk.Frame(form, bg=BG_MAIN)
        col1.pack(side="left", fill="both", expand=True, padx=(0,8))

        col2 = tk.Frame(form, bg=BG_MAIN)
        col2.pack(side="left", fill="both", expand=True, padx=(8,0))

        # Left column fields
        tk.Label(col1, text="Jeweller *", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0,4))
        self.jeweller_var = tk.StringVar()
        jeweller_entry = tk.Entry(col1, textvariable=self.jeweller_var, width=30,
                                  bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                                  relief="flat", font=("Segoe UI", 9), bd=0)
        jeweller_entry.pack(fill="x", pady=(0,14), ipady=6)

        tk.Label(col1, text="Request No. *", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0,4))
        self.request_var = tk.StringVar()
        tk.Entry(col1, textvariable=self.request_var, width=30,
                bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                relief="flat", font=("Segoe UI", 9), bd=0).pack(fill="x", pady=(0,14), ipady=6)

        tk.Label(col1, text="Date *", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0,4))
        self.date_var = tk.StringVar(value=datetime.date.today().strftime("%m/%d/%Y"))
        tk.Entry(col1, textvariable=self.date_var, width=30,
                bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                relief="flat", font=("Segoe UI", 9), bd=0).pack(fill="x", pady=(0,14), ipady=6)

        # Right column fields
        tk.Label(col2, text="Receipt No. (Optional)", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0,4))
        self.receipt_var = tk.StringVar()
        tk.Entry(col2, textvariable=self.receipt_var, width=30,
                bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                relief="flat", font=("Segoe UI", 9), bd=0).pack(fill="x", pady=(0,14), ipady=6)

        tk.Label(col2, text="Address", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0,4))
        self.addr_var = tk.StringVar(value="Auto-filled from jeweller")
        addr_entry = tk.Entry(col2, textvariable=self.addr_var, width=30,
                             bg=BG_CARD, fg=TEXT_MUTED, insertbackground=TEXT_BLACK,
                             relief="flat", font=("Segoe UI", 9), bd=0, state="disabled")
        addr_entry.pack(fill="x", pady=(0,14), ipady=6)

        tk.Label(col2, text="Urgency Type *", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", pady=(0,4))
        self.urgency_var = tk.StringVar(value="Moderate Priority")
        urgency_combo = ttk.Combobox(col2, textvariable=self.urgency_var,
                                     values=["Low Priority", "Moderate Priority", "High Priority", "Urgent"],
                                     state="readonly", width=27)
        urgency_combo.pack(fill="x", pady=(0,14), ipady=6)

        # Items section
        tk.Label(scrollable_frame, text="Items", font=("Segoe UI", 12, "bold"),
                 bg=BG_MAIN, fg=TEXT_BLACK).pack(anchor="w", padx=14, pady=(20,10))

        items_frame = tk.Frame(scrollable_frame, bg=BG_MAIN)
        items_frame.pack(padx=14, fill="both", expand=True)

        # Item columns header
        hdr_frame = tk.Frame(items_frame, bg=BG_TABLE_HDR)
        hdr_frame.pack(fill="x", pady=(0,2))
        
        for text, width in [("Item Name", 120), ("Pieces", 60), ("Weight (g)", 80), ("Purity", 80), ("Job No", 100), ("Remove", 60)]:
            tk.Label(hdr_frame, text=text, font=("Segoe UI", 9, "bold"),
                     bg=BG_TABLE_HDR, fg=TEXT_MUTED, width=10).pack(side="left", padx=4, pady=6)

        # Items list (initially one empty row)
        self._add_item_row(items_frame)

        # Add item button
        add_btn = tk.Button(items_frame, text="+ Add Item", bg=ACCENT_BLUE, fg=TEXT_WHITE,
                           font=("Segoe UI", 9, "bold"), relief="flat", bd=0,
                           cursor="hand2", pady=8,
                           command=lambda: self._add_item_row(items_frame))
        add_btn.pack(fill="x", pady=(10,0))

        # Remark
        tk.Label(scrollable_frame, text="Remark", font=("Segoe UI", 9, "bold"),
                 bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w", padx=14, pady=(20,4))
        self.remark_text = tk.Text(scrollable_frame, height=4, width=80,
                             bg=BG_CARD, fg=TEXT_BLACK, insertbackground=TEXT_BLACK,
                             relief="flat", font=("Segoe UI", 9), bd=0)
        self.remark_text.pack(padx=14, fill="both", expand=False, ipady=8)

        # Action buttons
        btn_frame = tk.Frame(scrollable_frame, bg=BG_MAIN)
        btn_frame.pack(padx=14, pady=20, fill="x", justify="right")

        tk.Button(btn_frame, text="Save Receipt", bg=ACCENT_BLUE, fg=TEXT_WHITE,
                 font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                 cursor="hand2", padx=20, pady=10,
                 command=self.save_receipt_entry).pack(side="left", padx=4)

        tk.Button(btn_frame, text="Reset", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI", 10), relief="flat", bd=0,
                 cursor="hand2", padx=20, pady=10,
                 command=self.reset_form).pack(side="left", padx=4)

    def _add_item_row(self, parent):
        """Add an item row to the receipt entry form"""
        row_frame = tk.Frame(parent, bg=BG_TABLE_ROW)
        row_frame.pack(fill="x", pady=2)

        item_var = tk.StringVar()
        pieces_var = tk.StringVar()
        weight_var = tk.StringVar()
        purity_var = tk.StringVar()
        job_var = tk.StringVar()

        tk.Entry(row_frame, textvariable=item_var, bg=BG_CARD, fg=TEXT_BLACK,
                insertbackground=TEXT_BLACK, relief="flat", font=("Segoe UI", 9),
                bd=0, width=14).pack(side="left", padx=4, pady=4, ipady=6)
        
        tk.Entry(row_frame, textvariable=pieces_var, bg=BG_CARD, fg=TEXT_BLACK,
                insertbackground=TEXT_BLACK, relief="flat", font=("Segoe UI", 9),
                bd=0, width=6).pack(side="left", padx=4, pady=4, ipady=6)
        
        tk.Entry(row_frame, textvariable=weight_var, bg=BG_CARD, fg=TEXT_BLACK,
                insertbackground=TEXT_BLACK, relief="flat", font=("Segoe UI", 9),
                bd=0, width=8).pack(side="left", padx=4, pady=4, ipady=6)
        
        tk.Entry(row_frame, textvariable=purity_var, bg=BG_CARD, fg=TEXT_BLACK,
                insertbackground=TEXT_BLACK, relief="flat", font=("Segoe UI", 9),
                bd=0, width=8).pack(side="left", padx=4, pady=4, ipady=6)
        
        tk.Entry(row_frame, textvariable=job_var, bg=BG_CARD, fg=TEXT_BLACK,
                insertbackground=TEXT_BLACK, relief="flat", font=("Segoe UI", 9),
                bd=0, width=10).pack(side="left", padx=4, pady=4, ipady=6)

        def remove_row():
            row_frame.destroy()
            self.items_list.remove((row_frame, item_var, pieces_var, weight_var, purity_var, job_var))

        tk.Button(row_frame, text="🗑", bg=BG_TABLE_ROW, fg=ACCENT_RED,
                 relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 10),
                 command=remove_row).pack(side="left", padx=4, pady=4)

        self.items_list.append((row_frame, item_var, pieces_var, weight_var, purity_var, job_var))

    def save_receipt_entry(self):
        """Save receipt entry to database"""
        jeweller = self.jeweller_var.get().strip()
        request_no = self.request_var.get().strip()
        
        if not jeweller or not request_no:
            messagebox.showerror("Error", "Jeweller and Request No. are required")
            return
        
        try:
            conn = get_connection()
            c = conn.cursor()
            firm_id = self.admin.get("firm_id", 1)
            
            # Create job card entry
            c.execute("""
                INSERT INTO job_cards (
                    firm_id, date_of_request, request_no, status, 
                    urgency_type, remark, created_by, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (firm_id, self.date_var.get(), request_no, "Pending", 
                  self.urgency_var.get(), self.remark_text.get("1.0", "end-1c"), self.admin.get("id", 1)))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Receipt entry created: {request_no}")
            self.reset_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save receipt: {str(e)}")

    def reset_form(self):
        """Reset form fields"""
        self.jeweller_var.set("")
        self.request_var.set("")
        self.receipt_var.set("")
        self.date_var.set(datetime.date.today().strftime("%m/%d/%Y"))
        self.urgency_var.set("Moderate Priority")
        self.remark_text.delete("1.0", "end")
