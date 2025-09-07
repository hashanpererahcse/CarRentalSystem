from .db import Database
from .services import Auth, Cars
from .models import Car

def seed():
    db=Database.instance(); a=Auth(db); c=Cars(db)
    # ensure admin
    try: a.register('admin','admin','ADMIN')
    except Exception: pass
    # create tables and data if admin lohgin for the first time
    if not c.list():
        c.add(Car(None,'Toyota','Corolla',2020,30000,True,1,14,55.0))
        c.add(Car(None,'Honda','Civic',2019,40000,True,2,21,50.0))
        c.add(Car(None,'Tesla','Model 3',2022,15000,True,1,7,120.0))

if __name__=='__main__':
    seed(); print('created admin/admin + sample cars')
