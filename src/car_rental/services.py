from .db import Database
from .models import User, Car, Booking
import hashlib, datetime

def h(p): return hashlib.sha256(p.encode()).hexdigest()

class Auth:
    def __init__(self, db=None): self.db=db or Database.instance()
    def register(self, u, p, role='CUSTOMER'):
        c=self.db.cursor(); c.execute('INSERT INTO users(username,password,role) VALUES(?,?,?)',(u,h(p),role)); self.db.commit()
        return User(c.lastrowid, u, role)
    def login(self, u, p):
        c=self.db.cursor(); c.execute('SELECT * FROM users WHERE username=?',(u,)); r=c.fetchone()
        return User(r['id'],r['username'],r['role']) if r and r['password']==h(p) else None

class Cars:
    def __init__(self, db=None): self.db=db or Database.instance()
    def add(self, car:Car):
        c=self.db.cursor()
        c.execute('INSERT INTO cars(make,model,year,mileage,available,min_days,max_days,daily_rate) VALUES(?,?,?,?,?,?,?,?)',
                  (car.make,car.model,car.year,car.mileage,int(car.available),car.min_days,car.max_days,car.daily_rate))
        self.db.commit(); return c.lastrowid
    def list(self):
        c=self.db.cursor(); c.execute('SELECT * FROM cars ORDER BY id')
        return [Car(r['id'],r['make'],r['model'],r['year'],r['mileage'],bool(r['available']),r['min_days'],r['max_days'],r['daily_rate']) for r in c.fetchall()]
    def delete(self, car_id:int):
        self.db.cursor().execute('DELETE FROM cars WHERE id=?',(car_id,)); self.db.commit()
    def get(self, car_id:int):
        c=self.db.cursor(); c.execute('SELECT * FROM cars WHERE id=?',(car_id,)); r=c.fetchone()
        return None if not r else Car(r['id'],r['make'],r['model'],r['year'],r['mileage'],bool(r['available']),r['min_days'],r['max_days'],r['daily_rate'])
    def set_availability(self, car_id:int, available:bool):
        self.db.cursor().execute('UPDATE cars SET available=? WHERE id=?',(int(available),car_id)); self.db.commit()

class Bookings:
    def __init__(self, db=None): self.db=db or Database.instance()
    def create(self, car:Car, user:User, start:str, end:str):
        days=(datetime.date.fromisoformat(end)-datetime.date.fromisoformat(start)).days
        if days<=0: raise ValueError('End must be after start')
        if days<car.min_days or days>car.max_days: raise ValueError(f'Must be between {car.min_days}-{car.max_days} days')
        fee=round(days*car.daily_rate*1.02,2)
        c=self.db.cursor(); c.execute('INSERT INTO bookings(car_id,user_id,start,end,fee,status) VALUES(?,?,?,?,?,?)',
            (car.id,user.id,start,end,fee,'PENDING')); self.db.commit(); return c.lastrowid,fee
    def list(self):
        c=self.db.cursor(); c.execute('SELECT * FROM bookings ORDER BY id DESC'); return [Booking(**dict(r)) for r in c.fetchall()]
    def list_for_user(self, uid:int):
        c=self.db.cursor(); c.execute('SELECT * FROM bookings WHERE user_id=? ORDER BY id DESC',(uid,)); return [Booking(**dict(r)) for r in c.fetchall()]
    def set_status(self, bid:int, status:str):
        self.db.cursor().execute('UPDATE bookings SET status=? WHERE id=?',(status,bid)); self.db.commit()
