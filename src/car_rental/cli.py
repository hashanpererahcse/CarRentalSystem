from .db import Database
from .services import Auth, Cars, Bookings
from .seed import seed
from .models import Car
import os, sys

# --- UI helpers ---
RESET = "\033[0m"; BOLD = "\033[1m"; DIM="\033[2m"; GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"; CYAN="\033[36m"

def clear():
    try:
        os.system('cls' if os.name=='nt' else 'clear')
    except Exception:
        pass

def title(text): print(f"{BOLD}{text}{RESET}")

def prompt_nonempty(label:str)->str:
    while True:
        s=input(f"{label}: ").strip()
        if s: return s
        print(f"{YELLOW}Value cannot be empty.{RESET}")

def prompt_int(label:str, min_val=None, max_val=None)->int:
    while True:
        s=input(f"{label}: ").strip()
        try:
            v=int(s)
            if min_val is not None and v<min_val: print(f"{YELLOW}Must be >= {min_val}{RESET}"); continue
            if max_val is not None and v>max_val: print(f"{YELLOW}Must be <= {max_val}{RESET}"); continue
            return v
        except: print(f"{YELLOW}Enter a valid integer.{RESET}")

def prompt_float(label:str, min_val=None, max_val=None)->float:
    while True:
        s=input(f"{label}: ").strip()
        try:
            v=float(s)
            if min_val is not None and v<min_val: print(f"{YELLOW}Must be >= {min_val}{RESET}"); continue
            if max_val is not None and v>max_val: print(f"{YELLOW}Must be <= {max_val}{RESET}"); continue
            return v
        except: print(f"{YELLOW}Enter a valid number.{RESET}")

def pause(): input(f"\n{DIM}Press ENTER to continue...{RESET}")

def print_table(headers, rows):
    widths=[len(h) for h in headers]
    for r in rows:
        for i,cell in enumerate(r):
            widths[i]=max(widths[i], len(str(cell)))
    line="+".join("-"*(w+2) for w in widths)
    print("+"+line+"+")
    print("|"+"|".join(f" {headers[i].ljust(widths[i])} " for i in range(len(headers)))+"|")
    print("+"+line+"+")
    for r in rows:
        print("|"+"|".join(f" {str(r[i]).ljust(widths[i])} " for i in range(len(r)))+"|")
    print("+"+line+"+")

# --- Menus ---
def admin_menu(user, cars: Cars, bookings: Bookings):
    while True:
        clear(); title("Admin Menu")
        print("1) List cars")
        print("2) Add car")
        print("3) Delete car")
        print("4) Toggle car availability")
        print("5) View all bookings")
        print("6) Set booking status (APPROVED/REJECTED)")
        print("7) Logout")
        choice=input("Select: ").strip()

        if choice=='1':
            cs=cars.list()
            if not cs: print(f"{YELLOW}No cars.{RESET}")
            else:
                rows = [
                        (c.id, c.make, c.model, c.year, f"{c.mileage}km",
                        "Yes" if c.available else "No",
                        f"{c.min_days}-{c.max_days}",
                        f"${c.daily_rate:.2f}")
                        for c in cs
                    ]
            print_table(['ID','Make','Model','Year','Mileage','Avail','Days','Rate'], rows)
            pause()
        elif choice=='2':
            make=prompt_nonempty("Make"); model=prompt_nonempty("Model")
            year=prompt_int("Year", 1980, 2100); mileage=prompt_int("Mileage (km)", 0)
            available=input("Available now? (y/n): ").strip().lower().startswith('y')
            min_days=prompt_int("Min rent days",1); max_days=prompt_int("Max rent days",min_days)
            rate=prompt_float("Daily rate",1.0)
            cid=cars.add(Car(None, make, model, year, mileage, available, min_days, max_days, rate))
            print(f"{GREEN}Added car ID {cid}.{RESET}"); pause()
        elif choice=='3':
            car_id=prompt_int("Car ID",1)
            cars.delete(car_id); print(f"{GREEN}Deleted (if existed).{RESET}"); pause()
        elif choice=='4':
            car_id=prompt_int("Car ID",1)
            car=cars.get(car_id)
            if not car: print(f"{RED}Car not found.{RESET}")
            else:
                cars.set_availability(car_id, not car.available)
                print(f"{GREEN}Availability set to {'Yes' if not car.available else 'No'}.{RESET}")
            pause()
        elif choice=='5':
            bs = bookings.list()
            if not bs:
                print(f"{YELLOW}No bookings.{RESET}")
            else:
                rows = [
                    (b.id, b.car_id, b.user_id, b.start, b.end, f"${b.fee:.2f}", b.status)
                    for b in bs
                ]
                print_table(['ID','Car','User','Start','End','Fee','Status'], rows)
            pause()
        elif choice=='6':
            bid = prompt_int("Booking ID", 1)
            status = input("New status (APPROVED/REJECTED): ").strip().upper()
            if status not in ('APPROVED', 'REJECTED'):
                print(f"{YELLOW}Invalid status.{RESET}")
                pause()
                continue
            bookings.set_status(bid, status)
            print(f"{GREEN}Set.{RESET}")
            pause()
        elif choice == '7':
            break
        else:

            print(f"{YELLOW}Invalid choice.{RESET}"); pause()

def customer_menu(user, cars: Cars, bookings: Bookings):
    while True:
        clear(); title(f"Customer Menu — {user.username}")
        print("1) List available cars")
        print("2) Create booking")
        print("3) My bookings")
        print("4) Logout")
        choice=input("Select: ").strip()

        if choice=='1':
            cs=[c for c in cars.list() if c.available]
            if not cs: print(f"{YELLOW}No available cars.{RESET}")
            else:
                rows=[(c.id, c.make, c.model, c.year, f"{c.mileage}km\", f\"{c.min_days}-{c.max_days}\", f\"${c.daily_rate:.2f}") for c in cs]
                print_table(['ID','Make','Model','Year','Mileage','Days','Rate'], rows)
            pause()
        elif choice=='2':
            car_id=prompt_int("Car ID",1); car=cars.get(car_id)
            if not car: print(f"{RED}Car not found.{RESET}"); pause(); continue
            if not car.available: print(f"{YELLOW}Car not available.{RESET}"); pause(); continue
            start=prompt_nonempty("Start (YYYY-MM-DD)"); end=prompt_nonempty("End (YYYY-MM-DD)")
            try:
                bid,fee=bookings.create(car, user, start, end)
                print(f"{GREEN}Created booking {bid}. Fee ${fee:.2f}{RESET}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
            pause()
        elif choice=='3':
            bs=bookings.list_for_user(user.id)
            if not bs: print(f"{YELLOW}No bookings yet.{RESET}")
            else:
                rows=[(b.id, b.car_id, b.start, b.end, f"${b.fee:.2f}", b.status) for b in bs]
                print_table(['ID','Car','Start','End','Fee','Status'], rows)
            pause()
        elif choice=='4':
            break
        else:
            print(f"{YELLOW}Invalid choice.{RESET}"); pause()

def main():
    seed()
    db=Database.instance()
    auth=Auth(db); cars=Cars(db); bookings=Bookings(db)

    while True:
        clear(); title("CarRentalCLI — Simple & Clean UI")
        print("1) Register"); print("2) Login"); print("3) Exit")
        choice=input("Select: ").strip()

        if choice=='1':
            u=prompt_nonempty("Usernam"); p=prompt_nonempty("Password")
            try:
                auth.register(u,p); print(f"{GREEN}Registered! Please login.{RESET}"); pause()
            except Exception as e:
                print(f"{RED}Registration failed: {e}{RESET}"); pause()
        elif choice=='2':
            u=prompt_nonempty("Username"); p=prompt_nonempty("Password")
            user=auth.login(u,p)
            if not user: print(f"{RED}Invalid credentials.{RESET}"); pause(); continue
            if user.role=='ADMIN': admin_menu(user, cars, bookings)
            else: customer_menu(user, cars, bookings)
        elif choice=='3':
            print("Bye!"); break
        else:
            print(f"{YELLOW}Invalid choice.{RESET}"); pause()

if __name__=='__main__':
    main()
