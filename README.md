# HallmarkPro Desktop ERP

A modern Python desktop ERP application for Hallmark Centres (AHC).
Pixel-perfect match to the HallmarkPro Admin web UI.

## Features
- **Login** with cloud API verification + local fallback (offline mode)
- **Dashboard** with live stat cards (Pieces Today, Requests, Pending, etc.)
- **Main Request** list with date filter, search, status badges
- Full database: Firms, Admins, Jewellers, Job Cards, Transactions
- Shared SQLite database — usable across multiple PCs on same network
- Role-based access (SuperAdmin, Admin, Staff)

## Quick Start

### Windows
1. Install Python 3.10+ from https://python.org
2. Double-click `launch.bat`

### Mac / Linux
```bash
pip install -r requirements.txt
python main.py
```

## Default Login
| Field    | Value         |
|----------|---------------|
| Username | 9810359334    |
| Password | admin123      |

**Change the password immediately after first login.**

## Shared Database (Multi-PC)
The database is stored at `hallmarkpro.db` in the app folder.

**Option 1 – Network Share:**
- Place the entire app folder on a shared network drive (NAS / Windows Share)
- Each PC runs `main.py` pointing to the same folder

**Option 2 – SQLite over LAN:**
- Use [rclone](https://rclone.org/) or a sync tool to keep the DB in sync
- Or upgrade to PostgreSQL for true multi-user concurrent access

## Project Structure
```
hallmarkpro/
├── main.py               ← entry point
├── launch.bat            ← Windows launcher
├── requirements.txt
├── hallmarkpro.db        ← created on first run
├── db/
│   └── schema.py         ← DB init, all table definitions
├── utils/
│   └── auth.py           ← login logic + cloud verify
└── modules/
    ├── login.py          ← Login window (left panel + right form)
    └── dashboard.py      ← Dashboard + Main Request page
```

## Cloud API
Edit `utils/auth.py` → `CLOUD_VERIFY_URL` to point to your API endpoint.
Expected request: `POST /v1/verify` with `{"username": "...", "password_hash": "..."}`
Expected response: `{"success": true, "user": {...}}`

Set `CLOUD_SKIP=1` environment variable to bypass cloud check (dev/offline use).

## Customisation
- Colours: edit the palette constants at the top of `login.py` / `dashboard.py`
- Sidebar menu: edit `SIDEBAR_SECTIONS` in `dashboard.py`
- DB path: change `DB_PATH` in `db/schema.py` to a network path
