# CarRentalCLI 🚗💻

A lightweight, command-line car rental system built with Python and **SQLite**.  
It’s designed to be simple, easy to run, and demonstrate key programming concepts like **user roles**, **car management**, and **rental bookings** — all without needing a server or external database.

---

## ✨ What it does
- **User accounts** → customers can register/login, admins manage the system  
- **Cars** → admins add, remove, or toggle availability  
- **Bookings** → customers browse cars and create rental requests  
- **Approvals** → admins approve/reject bookings, customers see the status  
- **Fees** → rental cost is calculated automatically (`days * rate * 1.02`)  

---

## 🚀 Quick Start

### Requirements
- Python **3.10+**
- Nothing else — no external libraries needed 🎉

### Run from source
```bash
cd src
python -m car_rental.cli

```

👉 On the first run:

a local SQLite file carrental.db is created

seeded with admin/admin login + 3 sample cars

### Optional: package as a single file

```bash
cd src
python -m zipapp . -m "car_rental.cli:main" -o ../build/CarRentalCLI.pyz
python ../build/CarRentalCLI.pyz

```

### 🗂️ Project layout
CarRentalCLI/
├── src/
│   └── car_rental/
│       ├── cli.py          # CLI menus + UI
│       ├── db.py           # SQLite connection (singleton)
│       ├── seed.py         # Seeds admin + sample cars
│       ├── models/         # Dataclasses (User, Car, Booking)
│       └── services/       # Auth, Car, Booking, Notifications
└── build/                  # optional .pyz build output

### 📄 License

MIT — free to use, modify, and share.