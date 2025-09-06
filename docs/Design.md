# Design & Architecture (UML-lite)

## Components
- `db.Database`: Singleton for SQLite connection and schema initialization.
- `models.user`: `User` (base), `Admin`, `Customer`, `UserFactory`.
- `models.car`: `Car` value object.
- `models.booking`: `Booking` value object.
- `services.auth_service`: registration & login.
- `services.car_service`: CRUD for cars.
- `services.booking_service`: booking workflow; fee calculation; admin approval/rejection.
- `services.notification`: Observer pattern to notify on booking status changes.

## Design Patterns
- **Singleton**: `Database` ensures a single connection across services.
- **Factory Method**: `UserFactory.create_user(role, **kwargs)` returns `Admin` or `Customer`.
- **Observer**: `NotificationCenter` with `ConsoleNotifier` for booking status events.

## UML (Textual)
```text
+----------------+         +-------------------+         +-------------------+
|  Database      |<>------>|  AuthService      |         |  CarService       |
| (Singleton)    |         +-------------------+         +-------------------+
| +conn: sqlite3 |         | +register()       |         | +add/update/del   |
+----------------+         | +login()          |         | +list()           |
        ^                  +-------------------+         +-------------------+
        |                         ^                                 ^
        |                         |                                 |
        |                  +---------------+                 +----------------+
        |                  |   User        |<--Factory--+    | BookingService |
        |                  | (Admin/Customer)            |    +----------------+
        |                  +---------------+             |    | +create()      |
        |                                                |    | +approve/reject|
        |                                                |    | +list()        |
        |                                                |    +----------------+
        |                                                |            ^
        |                                         +------------+      |
        |                                         | Notification|<-----
        |                                         | (Observer)  |
        |                                         +------------+
```

## Key Interactions (Sequence: Create Booking)
1. Customer selects car & dates in CLI.
2. `BookingService.create_booking()` validates date range & car availability.
3. Fee calculated: `days * daily_rate * 1.02`.
4. Booking stored with `PENDING` status.
5. Admin reviews and approves/rejects → observers notified.
