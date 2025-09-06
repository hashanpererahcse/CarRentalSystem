# CarRentalCLI — CLI-based Car Rental System (SQLite)

A simple, object-oriented, **CLI** car rental system that uses a **file-based SQLite database**.  
Implements **user management** (admin & customer), **car management**, **rental booking** with fee calculation, and **rental management** (approve/reject).  
Includes basic design patterns: **Singleton** (DB), **Factory Method** (User creation), **Observer** (notifications on booking status changes).

## Quick Start
### Requirements
- Python 3.10+


### 1) Run
```bash
cd src
python -m car_rental.cli
```
On first run, the DB is created (`carrental.db`) and seeded with:
- **Admin**: username `admin`, password `admin`
- 3 sample cars

### 2) Build a self-contained zipapp (optional)
```bash
cd CarRentalCLI/src
python -m zipapp -m "car_rental.cli:main" -o ../build/CarRentalCLI.pyz
```
Then run with:
```bash
python ../build/CarRentalCLI.pyz
```

## Features (maps to assignment requirements)
- **User Management**: register/login; roles `ADMIN` and `CUSTOMER`.
- **Car Management (Admin)**: add/update/delete cars; fields include: ID, make, model, year, mileage, available_now, min/max rent period, daily_rate.
- **Rental Booking (Customer)**: view available cars, select a car, choose dates; fee = `daily_rate * days + service_fee(2%)`.
- **Rental Management (Admin)**: view pending bookings; approve/reject; customers notified via console (Observer).

## Project Structure
```
CarRentalCLI/
├── LICENSE
├── README.md
├── docs/
│   ├── Design.md
│   └── Maintenance.md
├── src/
│   └── car_rental/
│       ├── __init__.py
│       ├── cli.py
│       ├── db.py
│       ├── seed.py
│       ├── models/
│       │   ├── user.py
│       │   ├── car.py
│       │   └── booking.py
│       └── services/
│           ├── auth_service.py
│           ├── car_service.py
│           ├── booking_service.py
│           └── notification.py
└── build/
    └── (optional) CarRentalCLI.pyz
```

## Known Issues
- Password hashing is simple (SHA256, no salt) to keep the demo dependency-free.
- No concurrency control (single-user CLI).

## License
MIT — see LICENSE.
