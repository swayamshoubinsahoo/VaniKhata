# 🎙️ VaniKhata (वाणीखाता) — Bolkar Hisaab, UPI Recovery & 5 km Kaam Bridge

**Track 1 Submission — VibeX Codes Hackathon**  
*Built for India’s 63M+ micro-shopkeepers (chaiwalas, kirana stores, food vendors), small-team co-workers, and daily-wage workers.*

---

## 🔗 Live Project Links

* **🌐 Live Deployed App (Vercel):** [https://vanikhata.vercel.app](https://vanikhata.vercel.app)
* **💻 GitHub Repository:** [https://github.com/swayamshoubinsahoo/VaniKhata](https://github.com/swayamshoubinsahoo/VaniKhata)
* **🎥 2:30 Live Demo Video:** `[PASTE_YOUR_YOUTUBE_DEMO_LINK_HERE]`

---

## 🚨 The Real-World Problem (Track 1)

1. **The Busy Chaiwala & Co-Worker Exhaustion:**  
   Local chaiwalas, street food vendors, and kirana owners work 14 hours a day. When 20 customers are shouting orders and the vendor's hands are wet, they cannot stop making tea to unlock a smartphone and type in English to record credit (*udhaar*), track payments, coordinate co-worker lunch breaks, or order morning milk and sugar. As a result, they forget credit, lose daily revenue, and remain exhausted.
2. **The Big Labor Confusion ("Kaam Nahi Hai" vs. "Labor Nahi Mil Rahi"):**  
   Daily-wage masons, welders, electricians, and plumbers stand at street corners every morning saying *"Kaam nahi hai"*, while nearby factories and builders say *"Labor nahi mil rahi"*—because workers lack printed English resumes or certificates, and employers do not know whom to trust within a 5 km radius.

---

## 💡 The Solution: What VaniKhata Does

**VaniKhata** is a **zero-typing, hands-free voice operating system** designed specifically so a shopkeeper or daily-wage laborer can use it in 10 seconds with **zero technical jargon** on the screen:

### 1. 🎙️ Voice Munim (*Bolkar Hisaab Likhein*)
* **Multilingual & Wet-Hands Ready:** Tap the microphone (or speak via a basic earphone in loud street noise) in **Hindi, Bengali, or Hinglish**.
* **Multi-Intent Command Engine:** A single spoken sentence like *"रमेश के 40 रुपये उधार लिख दो और 20 पैकेट दूध ऑर्डर करो"* simultaneously logs Ramesh's ₹40 credit in the ledger, queues 20 packets of full-cream milk for 6:00 AM delivery, and speaks back audio confirmation in Hindi so the vendor never has to look at the screen.
* **Instant Payment Settlement:** Saying *"Suresh ne 60 rupaye jama kar diye"* marks the pending entry as `Paid` and updates `Today's Cash & UPI` in real time.

### 2. 📒 Udhaar Khata & Polite Evening UPI Recovery
* **Dynamic UPI QR Codes:** Selecting any customer generates a live, scannable UPI QR (`upi://pay?...`) compatible with GPay, PhonePe, Paytm, and BHIM.
* **1-Click WhatsApp Reminders:** Generates a polite Hindi/Hinglish payment message with a direct UPI link, plus a bulk **"Send Evening UPI Link to All Pending"** trigger.

### 3. 📦 Milk & Team (Automated Supply Orders & Co-Worker Relief)
* **Morning Wholesale Restock:** Voice-triggered dairy, sugar, tea leaf, and packaging orders are automatically formatted and dispatched to wholesale suppliers.
* **Stress-Free Co-Worker Shifts:** Assigns counter duties and lunch breaks (*"Chotu ko 2 baje lunch break aur counter shift assign karo"*) for small shop teams.

### 4. 👷 Kaam & Mazdoor (*ShramikSetu 5 km Labor Bridge*)
* **No English Resume Required:** Welders, electricians, masons (*rajmistri*), and plumbers verify their skills via native voice dialing or a **15-second work video clip**.
* **< 5 km Factory Matching & Wage Escrow Lock:** Matches verified workers with factories within 5 km, locks their daily wage safely (`🔒 Wage Safe & Locked`) to prevent wage theft, and sends the factory GPS location directly on WhatsApp.

### 5. 📞 WhatsApp & Free Phone Call Interface (Keypad Phone Ready)
* **Zero-App Access:** Vendors and daily-wage workers on basic smartphones or feature keypad phones without internet can log *udhaar*, place morning milk orders, or request factory work via **WhatsApp messages** (`+91 9800-KHATA`) or a **Toll-Free Phone Call** (`1800-120-VANI`).

---

## 🛠️ Tech Stack & Architecture

| Layer | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Backend API** | **Python 3 + FastAPI + Pydantic** | High-speed REST endpoints (`/api/state`, `/api/command`, `/api/udhaar/{id}/settle`, `/api/labor`) with multilingual NLP intent & digit normalization (`०-९` / `০-৯` to `0-9`). |
| **Database** | **SQLite3** | Relational persistence across 4 tables (`udhaar`, `supplier_orders`, `team_shifts`, `labor_matches`) with `/tmp` serverless runtime compatibility on Vercel. |
| **Frontend UI** | **HTML5 + Tailwind CSS + Vanilla JS** | High-contrast, zero-jargon shopkeeper dashboard designed for instant readability. |
| **Voice & Speech** | **Web Speech API + SpeechSynthesis** | Live streaming speech-to-text (`hi-IN`, `bn-IN`, `en-IN`) and spoken Hindi audio confirmation. |
| **Payments & Sharing** | **QRCode.js + UPI URI + WhatsApp Deep Links** | Instant scannable UPI QR generation, WhatsApp reminder links, and 1-click CSV khata export. |

---

## 🧪 Judge Quick-Test Guide (30 Seconds on Live Link)

1. Open **[https://vanikhata.vercel.app](https://vanikhata.vercel.app)**.
2. On **Voice Munim**, tap **Bolkar Likhein** (or click the preset button `"रमेश के ₹40 उधार + 20 पैकेट दूध"`) and watch `Pending Udhaar`, `Morning Milk & Supplies`, and `Aaj Ke Taaza Hisaab` update live with spoken Hindi confirmation.
3. Open **Udhaar & UPI**, click any customer to inspect the dynamic UPI QR code, and click **✓ Mark Paid**.
4. Open **Milk & Team** to view auto-dispatched morning orders and co-worker shift assignments.
5. Open **Kaam & Mazdoor** to match a worker to a factory within 5 km and toggle **🔒 Wage Safe & Locked**.
6. Open **WhatsApp & Call** to test the WhatsApp Khata Helper and Toll-Free Worker Call simulator.

---
## 💻 Run Locally

```bash
git clone [https://github.com/swayamshoubinsahoo/VaniKhata.git](https://github.com/swayamshoubinsahoo/VaniKhata.git)
cd VaniKhata
pip install -r requirements.txt
uvicorn server:app --reload
```

Open **`http://127.0.0.1:8000`** in Google Chrome or Microsoft Edge.

---

## 👤 Built By

**Swayam Shoubin Sahoo**  
B.Tech Biomedical Engineering (Machine Intelligence) • Adamas University  
GitHub: [@swayamshoubinsahoo](https://github.com/swayamshoubinsahoo)
