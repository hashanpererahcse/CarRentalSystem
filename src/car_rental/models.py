from dataclasses import dataclass
@dataclass
class User: id:int; username:str; role:str
@dataclass
class Car: id:int|None; make:str; model:str; year:int; mileage:int; available:bool; min_days:int; max_days:int; daily_rate:float
@dataclass
class Booking: id:int|None; car_id:int; user_id:int; start:str; end:str; fee:float; status:str
