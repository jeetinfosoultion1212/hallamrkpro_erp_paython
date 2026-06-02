import hashlib
import sqlite3
import os
import sys

try:
    import requests
except ImportError:
    requests = None

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from db.schema import get_connection

CLOUD_VERIFY_URL = "https://api.hallmarkpro.in/v1/verify"   # stub – replace with real endpoint


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def cloud_verify(username: str, password_hash: str) -> dict:
    """
    Calls the cloud API to verify credentials.
    Returns {"success": True/False, "user": {...}} or raises on network error.
    Falls back to local-only if CLOUD_SKIP env var is set or requests unavailable.
    """
    if os.environ.get("CLOUD_SKIP") or requests is None:
        return {"success": True, "cloud": False}
    try:
        r = requests.post(
            CLOUD_VERIFY_URL,
            json={"username": username, "password_hash": password_hash},
            timeout=5,
        )
        if r.status_code == 200:
            return r.json()
        return {"success": False, "message": r.json().get("message", "Auth failed")}
    except requests.exceptions.ConnectionError:
        # Offline → allow local login
        return {"success": True, "cloud": False, "offline": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


def login(username: str, password: str) -> dict:
    """
    Full login: local DB check + cloud verify.
    Returns {"ok": True, "admin": row_dict, "firm": row_dict} or {"ok": False, "error": "..."}
    """
    conn = get_connection()
    c = conn.cursor()

    # Check locked
    c.execute("SELECT * FROM admins WHERE username=? AND status=1", (username,))
    admin = c.fetchone()
    conn.close()

    if not admin:
        return {"ok": False, "error": "Invalid username or password."}

    import datetime
    if admin["locked_until"]:
        try:
            lock_dt = datetime.datetime.fromisoformat(admin["locked_until"])
            if datetime.datetime.now() < lock_dt:
                return {"ok": False, "error": f"Account locked until {lock_dt.strftime('%H:%M:%S')}."}
        except Exception:
            pass

    pw_hash = hash_password(password)
    if admin["password"] != pw_hash:
        # Increment failed attempts
        conn2 = get_connection()
        attempts = (admin["failed_attempts"] or 0) + 1
        locked_until = None
        if attempts >= 5:
            import datetime
            locked_until = (datetime.datetime.now() + datetime.timedelta(minutes=15)).isoformat()
        conn2.execute("UPDATE admins SET failed_attempts=?, locked_until=? WHERE id=?",
                      (attempts, locked_until, admin["id"]))
        conn2.commit()
        conn2.close()
        return {"ok": False, "error": "Invalid username or password."}

    # Cloud verify
    cloud = cloud_verify(username, pw_hash)
    if not cloud.get("success"):
        return {"ok": False, "error": cloud.get("message", "Cloud verification failed.")}

    # Reset failed attempts, update last_login
    import datetime
    conn3 = get_connection()
    conn3.execute("""UPDATE admins SET failed_attempts=0, locked_until=NULL,
                     last_login=?, last_activity=? WHERE id=?""",
                  (datetime.datetime.now().isoformat(),
                   datetime.datetime.now().isoformat(),
                   admin["id"]))
    conn3.commit()

    # Fetch firm
    c2 = conn3.cursor()
    c2.execute("SELECT * FROM firms WHERE id=?", (admin["firm_id"],))
    firm = c2.fetchone()
    conn3.close()

    return {
        "ok": True,
        "admin": dict(admin),
        "firm": dict(firm) if firm else {},
        "offline": cloud.get("offline", False),
    }
