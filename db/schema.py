import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hallmarkpro.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS firms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_name TEXT NOT NULL,
        contact_person TEXT,
        phone_number TEXT,
        additional_phone TEXT,
        email TEXT,
        address1 TEXT,
        address2 TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        gst_no TEXT,
        pan_no TEXT,
        msme_no TEXT,
        llpin_no TEXT,
        cin_no TEXT,
        license_no TEXT,
        validity_date TEXT,
        financial_year TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        website TEXT,
        company_type TEXT,
        annual_turnover REAL,
        logo_path TEXT,
        status INTEGER DEFAULT 1,
        upi_id TEXT,
        bank_name TEXT,
        branch TEXT,
        bank_account_number TEXT,
        bank_ifsc TEXT,
        tag_line TEXT,
        State_Code TEXT,
        plan_type TEXT,
        amc_date TEXT,
        plan_amount REAL,
        request_generate_url TEXT,
        firm_type TEXT,
        main_firm_id INTEGER,
        secure_key TEXT,
        watermark_path TEXT,
        signature_path TEXT,
        stamp_path TEXT,
        header_image_path TEXT,
        header_left_logo_path TEXT,
        updated_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        phone_number TEXT,
        email TEXT,
        password TEXT NOT NULL,
        password_changed_at TEXT,
        two_factor_secret TEXT,
        two_factor_enabled INTEGER DEFAULT 0,
        role TEXT DEFAULT 'admin',
        firm_id INTEGER REFERENCES firms(id),
        one_signal_id TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        status INTEGER DEFAULT 1,
        profile_image TEXT,
        signature_path TEXT,
        last_login TEXT,
        last_activity TEXT,
        failed_attempts INTEGER DEFAULT 0,
        locked_until TEXT
    );

    CREATE TABLE IF NOT EXISTS jewellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Jewellers_Name TEXT NOT NULL,
        Party_type TEXT,
        Address1 TEXT,
        Address2 TEXT,
        City TEXT,
        Contact_no TEXT,
        email TEXT,
        O_Bal REAL DEFAULT 0,
        C_Bal REAL DEFAULT 0,
        normal_balance REAL DEFAULT 0,
        Logo TEXT,
        licence_no TEXT,
        Validity_date TEXT,
        Rate REAL,
        silver_rate REAL,
        PAN TEXT,
        GST TEXT,
        State TEXT,
        STCODE TEXT,
        firm_id INTEGER REFERENCES firms(id),
        account_id INTEGER,
        updated_at TEXT DEFAULT (datetime('now')),
        created_at TEXT DEFAULT (datetime('now')),
        subsidiary_ledger_id INTEGER,
        Address TEXT,
        logo_path TEXT,
        qrcode_link TEXT,
        owner_name TEXT,
        date_of_birth TEXT,
        special_day TEXT
    );

    CREATE TABLE IF NOT EXISTS job_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_id INTEGER REFERENCES firms(id),
        date_of_request TEXT,
        licence_no TEXT,
        request_no TEXT,
        job_no TEXT,
        item TEXT,
        pcs INTEGER DEFAULT 0,
        purity TEXT,
        weight REAL DEFAULT 0,
        huid_pcs INTEGER DEFAULT 0,
        fail_pcs INTEGER DEFAULT 0,
        bill_no TEXT,
        is_billed INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Pending',
        urgency_type TEXT,
        financial_year TEXT,
        cut_pcs INTEGER DEFAULT 0,
        melt_pcs INTEGER DEFAULT 0,
        scrp_cornet_weight REAL DEFAULT 0,
        strip_weight REAL DEFAULT 0,
        button_weight REAL DEFAULT 0,
        cornet_weight REAL DEFAULT 0,
        date_of_delivery TEXT,
        order_no TEXT,
        delivery_voucher_no TEXT,
        updated_at TEXT DEFAULT (datetime('now')),
        last_status_change TEXT,
        invoice_generated INTEGER DEFAULT 0,
        material_type TEXT,
        account_id INTEGER,
        refer_party_id INTEGER,
        description TEXT,
        remark TEXT,
        created_at TEXT DEFAULT (datetime('now')),
        created_by INTEGER,
        rate REAL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_id INTEGER REFERENCES firms(id),
        bill_party_id INTEGER,
        payment_party_id INTEGER,
        is_third_party_payment INTEGER DEFAULT 0,
        payment_reference_note TEXT,
        account_id INTEGER,
        licence_no TEXT,
        request_no TEXT,
        jewellers_page_token TEXT,
        total_amount REAL DEFAULT 0,
        base_amount REAL DEFAULT 0,
        additional_charges REAL DEFAULT 0,
        gst_amount REAL DEFAULT 0,
        cgst_amount REAL DEFAULT 0,
        sgst_amount REAL DEFAULT 0,
        igst_amount REAL DEFAULT 0,
        gst_rate REAL DEFAULT 0,
        tds_applicable INTEGER DEFAULT 0,
        tds_amount REAL DEFAULT 0,
        voucher_id INTEGER,
        narration TEXT,
        bill_no TEXT,
        date TEXT,
        payment_status TEXT DEFAULT 'Due',
        payment_date TEXT,
        payment_mode TEXT,
        refer_party_id INTEGER,
        paid_amount REAL DEFAULT 0,
        credit_note_amount REAL DEFAULT 0,
        financial_year TEXT,
        total_pcs INTEGER DEFAULT 0,
        transaction_status TEXT DEFAULT 'Active',
        round_off REAL DEFAULT 0,
        reference_no TEXT,
        transaction_type TEXT,
        billing_type TEXT,
        excluded_job_ids TEXT,
        invoice_id INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        scrap_weight REAL DEFAULT 0,
        button_weight REAL DEFAULT 0,
        strip_weight REAL DEFAULT 0,
        reminents_weight REAL DEFAULT 0,
        cornent_weight REAL DEFAULT 0,
        issue_weight REAL DEFAULT 0,
        updated_at TEXT DEFAULT (datetime('now')),
        is_jobs_wise INTEGER DEFAULT 0,
        payment_receipt_id INTEGER,
        billing_mode TEXT
    );
    """)

    # Seed default firm and admin if empty
    c.execute("SELECT COUNT(*) FROM firms")
    if c.fetchone()[0] == 0:
        c.execute("""INSERT INTO firms (firm_name, contact_person, phone_number, address1, city, state,
                     gst_no, license_no, financial_year, tag_line, plan_type, status)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  ("HALLMARKPRO ADMIN",
                   "Prosenjit",
                   "9810359334",
                   "SY-3/667GR FLR,1STFLR,Daliya Shori, Navapura Karva Road, Nr. Parekh Complex,bhagal",
                   "NEW DELHI",
                   "DELHI - 110059",
                   "07AABCU9603R1ZM",
                   "HP/2024/001",
                   "2025-2026",
                   "Run Your AHC Like a Pro",
                   "Professional",
                   1))
        firm_id = c.lastrowid

        import hashlib
        pw = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("""INSERT INTO admins (username, name, phone_number, email, password, role, firm_id, status)
                     VALUES (?,?,?,?,?,?,?,?)""",
                  ("9810359334", "Prosenjit Halder", "9810359334",
                   "admin@hallmarkpro.in", pw, "SuperAdmin", firm_id, 1))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_PATH)
