from datetime import datetime
import sys
parking_slots = [
    ("P01", None),
    ("P02", None),
    ("P03", None),
    ("P04", None),
    ("P05", None),
    ("P06", None),
    ("P07", None),
    ("P08", None),
    ("P09", None),
    ("P10", None),
    ("P11", None),
    ("P12", None),
    ("P13", None),
    ("P14", None),
    ("P15", None),
    ("P16", None),
    ("P17", None),
    ("P18", None),
    ("P19", None),
    ("P20", None),
    ("P21", None),
    ("P22", None),
    ("P23", None),
    ("P24", None),
    ("P25", None),
    ("P26", None),
    ("P27", None),
    ("P28", None),
    ("P29", None),
    ("P30", None),
    ("P31", None),
    ("P32", None),
    ("P33", None),
    ("P34", None),
    ("P35", None)
]
parking_records = []
users = [("AKHAND", "akhand@123")]

def check_login(username, password):
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False
def add_user(username, password):
    for user in users:
        if user[0] == username:
            return {
                "success": False,
                "message": "Username already exists!"
            }
    users.append((username, password))
    return {
        "success": True,
        "message": "User added successfully!"
    }
def check_vehicle_already_parked(vehicle_number):
    vehicle_number = vehicle_number.upper()
    for slot, vehicle in parking_slots:
        if vehicle is not None:
            if vehicle["vehicle_number"] == vehicle_number:
                return True
    return False
def find_available_slot():
    for slot, vehicle in parking_slots:
        if vehicle is None:
            return slot
    return None
def create_vehicle_data(vehicle_number, owner_name, vehicle_type):
    return {
        "vehicle_number": vehicle_number.upper(),
        "owner_name": owner_name,
        "vehicle_type": vehicle_type,
        "entry_time": datetime.now(),
        "exit_time": None,
        "status": "Parked"
    }
def save_vehicle_in_slot(slot_number, vehicle_data):
    for index in range(len(parking_slots)):
        slot, vehicle = parking_slots[index]
        if slot == slot_number:
            parking_slots[index] = (slot, vehicle_data)
            return True
    return False
def create_entry_record(slot_number, vehicle_data):
    record = {
        "vehicle_number": vehicle_data["vehicle_number"],
        "owner_name": vehicle_data["owner_name"],
        "vehicle_type": vehicle_data["vehicle_type"],
        "slot": slot_number,
        "entry_time": vehicle_data["entry_time"],
        "exit_time": None,
        "status": "Parked",
        "amount": 0
    }
    parking_records.append(record)

def entry_vehicle(vehicle_number, owner_name, vehicle_type):
    vehicle_number = vehicle_number.strip().upper()
    owner_name = owner_name.strip()
    if vehicle_number == "" or owner_name == "":
        return {
            "success": False,
            "message": "Please enter all details!"
        }
    if check_vehicle_already_parked(vehicle_number):
        return {
            "success": False,
            "message": "Vehicle is already parked!"
        }
    available_slot = find_available_slot()
    if available_slot is None:
        return {
            "success": False,
            "message": "Parking is full!"
        }

    vehicle_data = create_vehicle_data(
        vehicle_number,
        owner_name,
        vehicle_type
    )

    save_vehicle_in_slot(
        available_slot,
        vehicle_data
    )

    create_entry_record(
        available_slot,
        vehicle_data
    )

    return {
        "success": True,
        "message": "Vehicle parked successfully!",
        "slot": available_slot,
        "entry_time": vehicle_data["entry_time"]
    }
def find_vehicle_slot(vehicle_number):
    """
    Finds the slot occupied by a vehicle.
    """

    vehicle_number = vehicle_number.upper()

    for index in range(len(parking_slots)):
        slot, vehicle = parking_slots[index]

        if vehicle is not None:
            if vehicle["vehicle_number"] == vehicle_number:
                return index, slot, vehicle

    return None, None, None


def calculate_parking_charges(vehicle_type, entry_time):
    exit_time = datetime.now()

    duration = exit_time - entry_time
    total_hours = duration.total_seconds() / 3600
    if total_hours < 1:
        total_hours = 1

    total_hours = int(total_hours)

    if vehicle_type.lower() == "bike":
        rate = 10
    else:
        rate = 20

    amount = total_hours * rate

    return exit_time, total_hours, amount


def update_exit_record(vehicle_number, exit_time, amount):
    for record in parking_records:
        if (
            record["vehicle_number"] == vehicle_number
            and record["status"] == "Parked"
        ):
            record["exit_time"] = exit_time
            record["status"] = "Exited"
            record["amount"] = amount
            return True

    return False


def remove_vehicle_from_slot(index, slot_number):
    parking_slots[index] = (slot_number, None)
    
def exit_vehicle(vehicle_number):
    vehicle_number = vehicle_number.strip().upper()
    index, slot_number, vehicle = find_vehicle_slot(vehicle_number)
    if vehicle is None:
        return {
            "success": False,
            "message": "Vehicle not found!"
        }

    exit_time, duration, amount = calculate_parking_charges(
        vehicle["vehicle_type"],
        vehicle["entry_time"]
    )

    update_exit_record(
        vehicle_number,
        exit_time,
        amount
    )

    remove_vehicle_from_slot(
        index,
        slot_number
    )

    return {
        "success": True,
        "message": "Vehicle exited successfully!",
        "slot": slot_number,
        "entry_time": vehicle["entry_time"],
        "exit_time": exit_time,
        "duration": duration,
        "amount": amount
    }
def get_all_slots():
    return parking_slots
def get_available_slots():
    available_slots = []
    for slot, vehicle in parking_slots:
        if vehicle is None:
            available_slots.append(slot)

    return available_slots
def get_occupied_slots():
    occupied_slots = []

    for slot, vehicle in parking_slots:
        if vehicle is not None:
            occupied_slots.append(slot)

    return occupied_slots


def view_parking_slot(slot_number):
    slot_number = slot_number.upper()
    for slot, vehicle in parking_slots:
        if slot == slot_number:
            if vehicle is None:
                return {
                    "success": True,
                    "message": "Slot is available!",
                    "slot": slot
                }

            return {
                "success": True,
                "message": "Slot is occupied!",
                "slot": slot,
                "vehicle": vehicle
            }

    return {
        "success": False,
        "message": "Invalid slot number!"
    }
def search_current_vehicle(vehicle_number):
    vehicle_number = vehicle_number.upper()

    for slot, vehicle in parking_slots:

        if vehicle is not None:
            if vehicle["vehicle_number"] == vehicle_number:
                return {
                    "success": True,
                    "message": "Vehicle is currently parked.",
                    "slot": slot,
                    "vehicle": vehicle
                }

    return None


def search_vehicle_record(vehicle_number):
    vehicle_number = vehicle_number.upper()

    for record in parking_records:

        if record["vehicle_number"] == vehicle_number:
            return record

    return None


def search_vehicle(vehicle_number):
    vehicle_number = vehicle_number.strip().upper()

    current_vehicle = search_current_vehicle(vehicle_number)

    if current_vehicle is not None:
        return current_vehicle

    old_record = search_vehicle_record(vehicle_number)

    if old_record is not None:
        return {
            "success": True,
            "message": "Vehicle found in parking records.",
            "record": old_record
        }

    return {
        "success": False,
        "message": "Vehicle not found!"
    }

def get_all_records():
    return parking_records


def get_active_records():
    active_records = []

    for record in parking_records:
        if record["status"] == "Parked":
            active_records.append(record)

    return active_records


def get_completed_records():
    completed_records = []

    for record in parking_records:
        if record["status"] == "Exited":
            completed_records.append(record)

    return completed_records

def get_total_slots():
    return len(parking_slots)


def get_total_occupied_slots():
    count = 0

    for slot, vehicle in parking_slots:
        if vehicle is not None:
            count += 1

    return count


def get_total_available_slots():
    return get_total_slots() - get_total_occupied_slots()


def get_parking_status():
    return {
        "total": get_total_slots(),
        "occupied": get_total_occupied_slots(),
        "available": get_total_available_slots()
    }

def get_total_vehicles_parked():
    return len(parking_records)


def get_total_vehicles_exited():
    count = 0

    for record in parking_records:
        if record["status"] == "Exited":
            count += 1

    return count


def get_total_collection():
    total_amount = 0

    for record in parking_records:
        total_amount += record["amount"]

    return total_amount


def get_parking_report():
    return {
        "total_vehicles": get_total_vehicles_parked(),
        "exited_vehicles": get_total_vehicles_exited(),
        "total_collection": get_total_collection(),
        "available_slots": get_total_available_slots(),
        "occupied_slots": get_total_occupied_slots()
    }
def exit_program():
    print("Thank you for using the Parking Management System.")
    sys.exit()
