#!/usr/bin/env python3
"""
HallmarkPro Desktop ERP
Entry point – initialises DB then launches the Login window.
"""
import os
import sys

# allow imports from project root
sys.path.insert(0, os.path.dirname(__file__))

# ── 1. init DB ────────────────────────────────────────────────────────────────
from db.schema import init_db
init_db()

# ── 2. launch UI ─────────────────────────────────────────────────────────────
from modules.login import LoginWindow

app = LoginWindow()
app.mainloop()
