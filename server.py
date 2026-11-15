import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="VaniKhata OS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = "/tmp/vanikhata.db" if os.getenv("VERCEL") else str(BASE_DIR / "vanikhata.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS udhaar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    items TEXT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supplier_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    qty TEXT NOT NULL,
    vendor TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Dispatched',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS team_shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff TEXT NOT NULL,
    task TEXT NOT NULL,
    shift_time TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS labor_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker TEXT NOT NULL,
    trade TEXT NOT NULL,
    skill_score TEXT NOT NULL,
    factory TEXT NOT NULL,
    distance TEXT NOT NULL,
    wage INTEGER NOT NULL,
    escrow_locked INTEGER NOT NULL DEFAULT 1,
    map_url TEXT NOT NULL
);
""")
conn.commit()


def ensure_seeded():
    if cur.execute("SELECT COUNT(*) FROM udhaar").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO udhaar (name, items, amount, status, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                ("Suresh (Auto Driver)", "4 Masala Chai + 2 Bun Maska", 60, "Pending", "09:20 AM"),
                ("Anil Sharma", "6 Special Chai + Samosa", 120, "Pending", "11:45 AM"),
                ("Deepak (Electrician)", "3 Chai + Biscuit", 65, "Pending", "02:15 PM"),
            ],
        )
        cur.executemany(
            "INSERT INTO supplier_orders (item, qty, vendor, status, created_at) VALUES (?, ?, ?, ?, ?)",
            [
                ("Assam CTC Tea Leaves", "5 kg", "Sharma Wholesale Traders", "Dispatched", "08:30 AM"),
                ("Disposable Kulhad Cups", "500 pcs", "Kolkata Packaging Co.", "Dispatched", "10:10 AM"),
            ],
        )
        cur.executemany(
            "INSERT INTO team_shifts (staff, task, shift_time, status) VALUES (?, ?, ?, ?)",
            [
                ("Chotu (Tea Master)", "Morning Rush & Milk Prep", "07:00 AM – 02:00 PM", "Active"),
                ("Raju (Counter Helper)", "Parcel Packing & Counter", "02:00 PM – 09:00 PM", "Scheduled"),
            ],
        )
        cur.executemany(
            "INSERT INTO labor_matches (worker, trade, skill_score, factory, distance, wage, escrow_locked, map_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("Manoj Kumar", "Arc & MIG Welder", "96% Skill Verified", "Shree Balaji Fabrication Works", "2.4 km", 850, 1, "https://maps.google.com/?q=Industrial+Estate+Kolkata"),
                ("Subhash Mondal", "Industrial Electrician", "94% Voice Verified", "Panihati Polymers Ltd.", "3.8 km", 900, 1, "https://maps.google.com/?q=Panihati+Industrial+Area"),
                ("Farhan Ali", "Civil Mason (Rajmistri)", "91% Skill Verified", "Metro Warehouse Extension", "4.5 km", 800, 0, "https://maps.google.com/?q=Barrackpore+Trunk+Road"),
            ],
        )
        conn.commit()


ensure_seeded()


class CommandRequest(BaseModel):
    text: str
    channel: Optional[str] = "Voice"


class WorkerRequest(BaseModel):
    worker: str
    trade: str
    has_video: bool = False


def now_str() -> str:
    return datetime.now().strftime("%I:%M %p")


def normalize_digits(text: str) -> str:
    for idx, ch in enumerate("०१२३४५६७८९"):
        text = text.replace(ch, str(idx))
    for idx, ch in enumerate("০১২৩৪৫६७८৯"):
        text = text.replace(ch, str(idx))
    return text


@app.get("/")
def serve_home():
    return FileResponse(str(BASE_DIR / "index.html"))


@app.get("/api/state")
def get_state():
    ensure_seeded()
    udhaar_rows = [dict(r) for r in cur.execute("SELECT * FROM udhaar ORDER BY id DESC").fetchall()]
    order_rows = [dict(r) for r in cur.execute("SELECT * FROM supplier_orders ORDER BY id DESC").fetchall()]
    shift_rows = [dict(r) for r in cur.execute("SELECT * FROM team_shifts ORDER BY id DESC").fetchall()]
    labor_rows = [dict(r) for r in cur.execute("SELECT * FROM labor_matches ORDER BY id DESC").fetchall()]
    paid_sum = sum(r["amount"] for r in udhaar_rows if r["status"] == "Paid")
    return {
        "collected": 1420 + paid_sum,
        "udhaar": udhaar_rows,
        "orders": order_rows,
        "shifts": shift_rows,
        "labor": labor_rows,
    }


@app.post("/api/command")
def process_command(req: CommandRequest):
    ensure_seeded()
    raw = req.text.strip()
    norm = normalize_digits(raw)
    lower = norm.lower()
    replies = []
    ts = now_str()

    stop_words = {"kal", "order", "kar", "ke", "ka", "ki", "ko", "aur", "liye", "कल", "ऑर्डर", "कर", "के", "का", "की", "को", "और", "लिए", "आज"}
    words = [w for w in re.split(r"[\s,।]+", norm) if len(w) > 1 and not w.isdigit()]
    person = ""
    for w in words:
        if w.lower() not in stop_words:
            person = w[0].upper() + w[1:]
            break

    if any(k in lower for k in ["shift", "break", "duty", "assign", "शिफ्ट", "ड्यूटी"]):
        staff = person or "Chotu"
        cur.execute(
            "INSERT INTO team_shifts (staff, task, shift_time, status) VALUES (?, ?, ?, ?)",
            (staff, "Lunch Relief & Counter Duty", "02:00 PM Slot", "Updated"),
        )
        replies.append(f"{staff} की शिफ्ट और ब्रेक अपडेट कर दी गई है।")

    elif any(k in lower for k in ["jama", "paid", "de diye", "जमा", "दिए", "clear"]):
        row = None
        if person:
            row = cur.execute(
                "SELECT * FROM udhaar WHERE status = 'Pending' AND LOWER(name) LIKE ? ORDER BY id DESC LIMIT 1",
                (f"%{person.lower()}%",),
            ).fetchone()
        if not row:
            row = cur.execute("SELECT * FROM udhaar WHERE status = 'Pending' ORDER BY id DESC LIMIT 1").fetchone()
        if row:
            cur.execute("UPDATE udhaar SET status = 'Paid' WHERE id = ?", (row["id"],))
            replies.append(f"{row['name']} के ₹{row['amount']} जमा कर लिए गए हैं।")

    elif any(k in lower for k in ["udhaar", "उधार", "likh", "लिख", "rupaye", "रुपये", "रुपए"]) or (
        person and person.lower() not in {"doodh", "दूध", "cheeni", "चीनी", "bread", "ब्रेड", "adrak", "अदरक"}
    ):
        amt_match = re.search(r"(\d+)", norm)
        if amt_match:
            amt = int(amt_match.group(1))
            cust = person or "Ramesh"
            item_desc = "Chai & Samosa" if ("samosa" in lower or "समोसा" in lower) else "Chai & Snacks"
            cur.execute(
                "INSERT INTO udhaar (name, items, amount, status, created_at) VALUES (?, ?, ?, 'Pending', ?)",
                (cust, item_desc, amt, ts),
            )
            replies.append(f"{cust} के ₹{amt} उधार खाते में लिख दिए गए हैं।")

    catalog = [
        (["doodh", "milk", "दूध", "দুধ"], "Full Cream Milk", "Maa Tara Dairy Farm"),
        (["cheeni", "sugar", "चीनी", "চিনি"], "Refined Sugar", "Sharma Wholesale Traders"),
        (["bread", "pav", "ब्रेड", "पाव"], "Sandwich Bread", "Modern City Bakery"),
        (["adrak", "ginger", "अदरक", "আদা"], "Fresh Ginger (Adrak)", "Koley Market Mandi"),
        (["patti", "tea", "पत्ती", "चाय"], "Assam CTC Tea Leaves", "Sharma Wholesale Traders"),
    ]
    for keys, label, vendor in catalog:
        for k in keys:
            if k in lower:
                qm = re.search(rf"(\d+\s*(?:packet|packets|पैकेट|kilo|kg|किलो)?)\s*{re.escape(k)}", norm, re.IGNORECASE)
                qty = qm.group(1).strip() if (qm and qm.group(1).strip()) else "10 Units"
                cur.execute(
                    "INSERT INTO supplier_orders (item, qty, vendor, status, created_at) VALUES (?, ?, ?, 'Dispatched', ?)",
                    (label, qty, vendor, ts),
                )
                replies.append(f"{qty} {label} का ऑर्डर {vendor} को भेज दिया गया है।")
                break

    conn.commit()
    if not replies:
        replies.append("आवाज़ समझ ली गई और खाता अपडेट कर दिया गया है।")
    return {"reply": " ".join(replies), "state": get_state()}


@app.post("/api/udhaar/{entry_id}/settle")
def settle_udhaar(entry_id: int):
    ensure_seeded()
    cur.execute("UPDATE udhaar SET status = 'Paid' WHERE id = ?", (entry_id,))
    conn.commit()
    return {"status": "ok", "state": get_state()}


@app.post("/api/labor")
def add_labor(req: WorkerRequest):
    ensure_seeded()
    score = "98% Skill Verified" if req.has_video else "94% Voice Verified"
    cur.execute(
        "INSERT INTO labor_matches (worker, trade, skill_score, factory, distance, wage, escrow_locked, map_url) VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
        (
            req.worker or "Raju Paswan",
            req.trade,
            score,
            "Bengal Precision Engineering",
            "1.9 km",
            950,
            "https://maps.google.com/?q=Bengal+Precision+Engineering",
        ),
    )
    conn.commit()
    return {"status": "ok", "state": get_state()}


@app.post("/api/labor/{labor_id}/toggle_escrow")
def toggle_escrow(labor_id: int):
    ensure_seeded()
    row = cur.execute("SELECT escrow_locked FROM labor_matches WHERE id = ?", (labor_id,)).fetchone()
    if row:
        new_val = 0 if row["escrow_locked"] == 1 else 1
        cur.execute("UPDATE labor_matches SET escrow_locked = ? WHERE id = ?", (new_val, labor_id))
        conn.commit()
    return {"status": "ok", "state": get_state()}