import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from backend_park import (
    check_login,
    add_user,
    entry_vehicle,
    exit_vehicle,
    get_all_slots,
    get_parking_status,
    search_vehicle,
    get_parking_report,
    get_all_records,
    get_active_records,
    get_completed_records
)
root = tk.Tk()
root.title("ParkIt | Parking Management System")
root.geometry("1000x650")
root.configure(bg="#101827")

current_user = ""

# common functions
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def create_title(parent, text):
    tk.Label(
        parent,
        text=text,
        font=("Georgia", 25, "bold"),
        fg="black",
        bg="#7FFFD4"
    ).pack(pady=20)


def create_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Comic Sans MS", 16, "bold"),
        bg="#7FFFD4",
        fg="black",
        activebackground="#7FFFD4",
        activeforeground="white",
        width=20,
        height=1,
        relief="flat",
        cursor="hand2"
    )
def login_page():
    clear_window()

    frame = tk.Frame(root, bg="#101827")
    frame.pack(expand=True)

    tk.Label(
        frame,
        text="ParkIt",
        font=("Bradley Hand ITC", 50, "bold"),
        fg="#60a5fa",
        bg="#101827"
    ).pack(pady=10)

    tk.Label(
        frame,
        text="Move freely.Park easily.",
        font=("Bahnschrift SemiLight", 20, "italic"),
        fg="white",
        bg="#101827"
    ).pack(pady=5)

    tk.Label(
        frame,text="Username",font=("Times New Roman", 20, "italic"),fg="white",bg="#101827").pack(pady=(25, 5)
                                                                                                   )
    username_entry = tk.Entry(frame, width=30, font=("Arial", 12, "bold"))
    username_entry.pack()

    tk.Label(
        frame,
        text="Password",
        font=("Times New Roman", 20, "italic"),
        fg="white",
        bg="#101827"
    ).pack(pady=(15, 5))

    password_entry = tk.Entry(frame, width=30, font=("Arial", 12, "bold"), show="*")
    password_entry.pack()

    def login():
        global current_user

        username = username_entry.get().strip()
        password = password_entry.get()

        if check_login(username, password):
            current_user = username
            dashboard_page()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password!"
            )

    create_button(frame, "LOGIN", login).pack(pady=15)

    create_button(frame, "CREATE ACCOUNT", register_page).pack(pady=5)

    tk.Label(
        frame,
        text="AKHAND PRATAP SINGH",
        fg="#9ca3af",
        bg="#101827",
        font=("Comic Sans MS", 22)
    ).pack(pady=(15, 0))

def register_page():
    clear_window()

    frame = tk.Frame(root, bg="#101827")
    frame.pack(expand=True)

    tk.Label(
        frame,
        text="Create Account",
        font=("Bradley Hand ITC", 40, "bold"),
        fg="#60a5fa",
        bg="#101827"
    ).pack(pady=10)

    tk.Label(
        frame,
        text="Username",
        font=("Times New Roman", 20, "italic"),
        fg="white",
        bg="#101827"
    ).pack(pady=(20, 5))
    username_entry = tk.Entry(frame, width=30, font=("Arial", 12, "bold"))
    username_entry.pack()

    tk.Label(
        frame,
        text="Password",
        font=("Times New Roman", 20, "italic"),
        fg="white",
        bg="#101827"
    ).pack(pady=(15, 5))
    password_entry = tk.Entry(frame, width=30, font=("Arial", 12, "bold"), show="*")
    password_entry.pack()

    tk.Label(
        frame,
        text="Confirm Password",
        font=("Times New Roman", 20, "italic"),
        fg="white",
        bg="#101827"
    ).pack(pady=(15, 5))
    confirm_entry = tk.Entry(frame, width=30, font=("Arial", 12, "bold"), show="*")
    confirm_entry.pack()

    result_label = tk.Label(
        frame,
        text="",
        font=("Arial", 12, "bold"),
        fg="#ef4444",
        bg="#101827"
    )
    result_label.pack(pady=10)

    def register():
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm = confirm_entry.get()

        if username == "" or password == "":
            result_label.config(text="Please enter all details!", fg="#ef4444")
            return

        if password != confirm:
            result_label.config(text="Passwords do not match!", fg="#ef4444")
            return

        result = add_user(username, password)

        if result["success"]:
            messagebox.showinfo("Success", result["message"] + "\nPlease login.")
            login_page()
        else:
            result_label.config(text=result["message"], fg="#ef4444")

    create_button(frame, "REGISTER", register).pack(pady=20)
    create_button(frame, "BACK TO LOGIN", login_page).pack(pady=5)


def dashboard_page():
    clear_window()
    header = tk.Frame(root, bg="#101827")
    header.pack(fill="x", padx=30, pady=15)
    tk.Label(
        header,
        text="ParkIt DASHBOARD",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#101827"
    ).pack(side="left")

    tk.Label(
        header,
        text=f"Logged in as: {current_user}",
        font=("Arial", 13, "italic"),
        fg="#9ca3af",
        bg="#101827"
    ).pack(side="right")

    cards_frame = tk.Frame(root, bg="#101827")
    cards_frame.pack(pady=20)

    status = get_parking_status()

    create_card(
        cards_frame,
        "TOTAL SLOTS",
        status["total"],
        0
    )

    create_card(
        cards_frame,
        "OCCUPIED",
        status["occupied"],
        1
    )

    create_card(
        cards_frame,
        "AVAILABLE",
        status["available"],
        2
    )

    # BUTTONS
    button_frame = tk.Frame(root, bg="#101827")
    button_frame.pack(pady=25)

    create_button(
        button_frame,
        "VEHICLE ENTRY",
        vehicle_entry_page
    ).grid(row=0, column=0, padx=10, pady=10)

    create_button(
        button_frame,
        "VEHICLE EXIT",
        vehicle_exit_page
    ).grid(row=0, column=2, padx=10, pady=10)

    create_button(
        button_frame,
        "VIEW PARKING SLOTS",
        slot_status_page
    ).grid(row=1, column=0, padx=10, pady=10)

    create_button(
        button_frame,
        "SEARCH VEHICLE",
        search_vehicle_page
    ).grid(row=1, column=2, padx=10, pady=10)

    create_button(
        button_frame,
        "PARKING REPORT",
        report_page
    ).grid(row=2, column=0, padx=10, pady=10)

    create_button(
        button_frame,
        "VIEW PRICE",
        price_page
    ).grid(row=2, column=2, padx=10, pady=10)

    create_button(
        button_frame,
        "PARKING RECORDS",
        records_page
    ).grid(row=3, column=0, padx=10, pady=10)

    create_button(
        button_frame,
        "LOGOUT",
        login_page
    ).grid(row=3, column=2, padx=10, pady=10)


def create_card(parent, title, value, column):
    card = tk.Frame(
        parent,
        bg="#1e293b",
        width=220,
        height=110
    )
    card.grid(row=0, column=column, padx=10)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 11, "bold"),
        fg="#9ca3af",
        bg="#1e293b"
    ).pack(pady=(15, 5))

    tk.Label(
        card,
        text=str(value),
        font=("Arial", 28, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack()


def vehicle_entry_page():
    clear_window()

    create_title(root, "VEHICLE ENTRY")

    frame = tk.Frame(root, bg="#101827")
    frame.pack(pady=10)

    tk.Label(
        frame,
        text="Vehicle Number",
        font=("Arial",20,"bold"),
        fg="white",
        bg="#101827"
    ).grid(row=0, column=0, padx=10, pady=10)

    vehicle_entry = tk.Entry(frame, width=30)
    vehicle_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Owner Name",
        font=("Arial",20,"bold"),
        fg="white",
        bg="#101827"
    ).grid(row=1, column=0, padx=10, pady=10)

    owner_entry = tk.Entry(frame, width=30)
    owner_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(
        frame,
        text="Vehicle Type",
        font=("Arial",20,"bold"),
        fg="white",
        bg="#101827"
    ).grid(row=2, column=0, padx=10, pady=10)

    vehicle_type = ttk.Combobox(
        frame,
        values=["Bike", "Car"],
        width=27,
        state="readonly"
    )
    vehicle_type.set("Car")
    vehicle_type.grid(row=2, column=1, padx=10, pady=10)

    result_label = tk.Label(
        root,
        text="",
        font=("Arial", 14, "bold"),
        fg="#22c55e",
        bg="#101827"
    )
    result_label.pack(pady=20)

    def submit_entry():
        result = entry_vehicle(
            vehicle_entry.get(),
            owner_entry.get(),
            vehicle_type.get()
        )

        if result["success"]:
            result_label.config(
                text=(
                    f"✓ {result['message']}\n"
                    f"ALLOTTED SLOT: {result['slot']}\n"
                    f"ENTRY TIME: "
                    f"{result['entry_time'].strftime('%d-%m-%Y %H:%M:%S')}"
                ),
                fg="#22c55e"
            )

            vehicle_entry.delete(0, tk.END)
            owner_entry.delete(0, tk.END)

        else:
            result_label.config(
                text=result["message"],
                fg="#ef4444"
            )

    create_button(
        root,
        "PARK VEHICLE",
        submit_entry
    ).pack(pady=10)

    create_button(
        root,
        "BACK TO DASHBOARD",
        dashboard_page
    ).pack(pady=10)


def vehicle_exit_page():
    clear_window()

    create_title(root, "VEHICLE EXIT")

    frame = tk.Frame(root, bg="#101827")
    frame.pack(pady=20)

    tk.Label(
        frame,
        text="Vehicle Number",
        font=("Arial",20,"bold"),
        fg="white",
        bg="#101827"
    ).grid(row=0, column=0, padx=10, pady=10)

    vehicle_entry = tk.Entry(frame, width=30)
    vehicle_entry.grid(row=0, column=1, padx=10, pady=10)

    result_label = tk.Label(
        root,
        text="",
        font=("Arial", 14, "bold"),
        fg="#22c55e",
        bg="#101827"
    )
    result_label.pack(pady=20)

    def submit_exit():
        result = exit_vehicle(vehicle_entry.get())

        if result["success"]:
            result_label.config(
                text=(
                    f"✓ {result['message']}\n"
                    f"SLOT: {result['slot']}\n"
                    f"DURATION: {result['duration']} hour(s)\n"
                    f"AMOUNT: ₹{result['amount']}\n"
                    f"EXIT TIME: "
                    f"{result['exit_time'].strftime('%d-%m-%Y %H:%M:%S')}"
                ),
                fg="#22c55e"
            )

            vehicle_entry.delete(0, tk.END)

        else:
            result_label.config(
                text=result["message"],
                fg="#ef4444"
            )

    create_button(
        root,
        "EXIT VEHICLE",
        submit_exit
    ).pack(pady=10)

    create_button(
        root,
        "BACK TO DASHBOARD",
        dashboard_page
    ).pack(pady=10)


def slot_status_page():
    clear_window()
    create_title(root, "PARKING SLOT STATUS")
    
    slots = get_all_slots()
    
    table_frame = tk.Frame(root, bg="#101827")
    table_frame.pack(pady=10)
    
    columns = ("Slot", "Status", "Vehicle Number", "Owner")
    
    tree = ttk.Treeview(
        table_frame, columns=columns, show="headings", height=15
    )
    
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=180)
        
    for slot, vehicle in slots:
        if vehicle is None:
            tree.insert(
                "", "end", values=(slot, "AVAILABLE", "-", "-")
            )
        else:
            tree.insert(
                "", "end", values=(
                    slot, "OCCUPIED", vehicle["vehicle_number"], vehicle["owner_name"]
                )
            )
            
    create_button(
        root, "BACK TO DASHBOARD", dashboard_page
    ).pack(pady=15)
    
def search_vehicle_page():
    clear_window()

    create_title(root, "SEARCH VEHICLE")

    frame = tk.Frame(root, bg="#101827")
    frame.pack(pady=20)

    tk.Label(
        frame,
        text="Vehicle Number",
        font=("Arial",20,"bold"),
        fg="white",
        bg="#101827"
    ).grid(row=0, column=0, padx=10, pady=10)

    vehicle_entry = tk.Entry(frame, width=30)
    vehicle_entry.grid(row=0, column=1, padx=10, pady=10)

    result_label = tk.Label(
        root,
        text="",
        font=("Arial", 13),
        fg="white",
        bg="#101827",
        justify="left"
    )
    result_label.pack(pady=20)

    def search():
        result = search_vehicle(vehicle_entry.get())

        if result["success"]:
            if "slot" in result:
                vehicle = result["vehicle"]

                result_label.config(
                    text=(
                        f"✓ {result['message']}\n\n"
                        f"Vehicle: {vehicle['vehicle_number']}\n"
                        f"Owner: {vehicle['owner_name']}\n"
                        f"Type: {vehicle['vehicle_type']}\n"
                        f"Slot: {result['slot']}\n"
                        f"Entry Time: "
                        f"{vehicle['entry_time'].strftime('%d-%m-%Y %H:%M:%S')}"
                    ),
                    fg="#22c55e"
                )

            else:
                record = result["record"]

                result_label.config(
                    text=(
                        f"✓ {result['message']}\n\n"
                        f"Vehicle: {record['vehicle_number']}\n"
                        f"Owner: {record['owner_name']}\n"
                        f"Type: {record['vehicle_type']}\n"
                        f"Slot: {record['slot']}\n"
                        f"Amount: ₹{record['amount']}"
                    ),
                    fg="#22c55e"
                )

        else:
            result_label.config(
                text=result["message"],
                fg="#ef4444"
            )

    create_button(
        root,
        "SEARCH",
        search
    ).pack(pady=10)

    create_button(
        root,
        "BACK TO DASHBOARD",
        dashboard_page
    ).pack(pady=10)

def report_page():
    clear_window()
    create_title(root, "PARKING REPORT")
    report = get_parking_report()

    frame = tk.Frame(root, bg="#1e293b")
    frame.pack(pady=20, padx=20)

    report_text = (
        f"TOTAL VEHICLES: {report['total_vehicles']}\n\n"
        f"EXITED VEHICLES: {report['exited_vehicles']}\n\n"
        f"TOTAL COLLECTION: ₹{report['total_collection']}\n\n"
        f"OCCUPIED SLOTS: {report['occupied_slots']}\n\n"
        f"AVAILABLE SLOTS: {report['available_slots']}"
    )

    tk.Label(
        frame,
        text=report_text,
        font=("Arial", 16),
        fg="white",
        bg="#1e293b",
        justify="left",
        padx=40,
        pady=30
    ).pack()

    create_button(
        root,
        "BACK TO DASHBOARD",
        dashboard_page
    ).pack(pady=15)

def price_page():
    clear_window()
    create_title(root, "PRICE LIST")
    
    frame = tk.Frame(root, bg="#1e293b")
    frame.pack(pady=20, padx=20)

    report_text = (
        f"CAR: ₹20/hour\n\n"
        f"BIKE: ₹10/hour\n\n"
    )

    tk.Label(
        frame,
        text=report_text,
        font=("Arial", 16),
        fg="white",
        bg="#1e293b",
        justify="left",
        padx=40,
        pady=30
    ).pack()

    create_button(
        root,
        "BACK TO DASHBOARD",
        dashboard_page
    ).pack(pady=15)


def records_page():
    clear_window()
    create_title(root, "PARKING RECORDS")

    filter_frame = tk.Frame(root, bg="#101827")
    filter_frame.pack(pady=10)

    tk.Label(
        filter_frame,
        text="Show:",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#101827"
    ).pack(side="left", padx=(0, 10))

    filter_box = ttk.Combobox(
        filter_frame,
        values=["All Records", "Currently Parked", "Exited"],
        width=25,
        state="readonly"
    )
    filter_box.set("All Records")
    filter_box.pack(side="left")

    table_frame = tk.Frame(root, bg="#101827")
    table_frame.pack(pady=10)

    columns = ("Vehicle", "Owner", "Type", "Slot", "Entry Time", "Exit Time", "Status", "Amount")

    tree = ttk.Treeview(
        table_frame, columns=columns, show="headings", height=14
    )

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=110)

    def load_records(*_):
        tree.delete(*tree.get_children())

        choice = filter_box.get()

        if choice == "Currently Parked":
            records = get_active_records()
        elif choice == "Exited":
            records = get_completed_records()
        else:
            records = get_all_records()

        for record in records:
            entry_str = record["entry_time"].strftime("%d-%m-%Y %H:%M:%S")

            if record["exit_time"] is not None:
                exit_str = record["exit_time"].strftime("%d-%m-%Y %H:%M:%S")
            else:
                exit_str = "-"

            tree.insert(
                "", "end",
                values=(
                    record["vehicle_number"],
                    record["owner_name"],
                    record["vehicle_type"],
                    record["slot"],
                    entry_str,
                    exit_str,
                    record["status"],
                    f"₹{record['amount']}"
                )
            )

    filter_box.bind("<<ComboboxSelected>>", load_records)
    load_records()

    create_button(
        root,
        "BACK TO DASHBOARD",
        dashboard_page
    ).pack(pady=15)
login_page()
root.mainloop()
