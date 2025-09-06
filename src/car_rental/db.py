import sqlite3
from threading import Lock

class Database:
    _instance=None; _lock=Lock()
    def __init__(self, path='carrental.db'):
        self.conn=sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory=sqlite3.Row
        self._init_schema()
    @classmethod
    def instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance: cls._instance=Database()
        return cls._instance
    def _init_schema(self):
        c=self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS cars(id INTEGER PRIMARY KEY AUTOINCREMENT, make TEXT, model TEXT, year INT, mileage INT, available INT, min_days INT, max_days INT, daily_rate REAL)')
        c.execute('CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT, car_id INT, user_id INT, start TEXT, end TEXT, fee REAL, status TEXT)')
        self.conn.commit()
    def cursor(self): return self.conn.cursor()
    def commit(self): self.conn.commit()
