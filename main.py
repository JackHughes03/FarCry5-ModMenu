import pymem
import pymem.process
import customtkinter
import threading
import time
import psutil

process_name = "FarCry5.exe"
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("Far Cry 5 Mod Menu")
app.geometry("400x240")
app.configure(padx=20, pady=20)


def check_process_running():
    if not any(proc.name() == process_name for proc in psutil.process_iter()):
        print("Process not found")
        exit(1)


# Add 10k Money
def get_money_addr():
    global MoneyAmount
    base_address = module + 0x05069F88
    offsets = [0xC0, 0x20, 0x20, 0x240, 0x10, 0x18, 0x120, 0x28, 0x4C]

    MoneyAmount = base_address
    for offset in offsets:
        MoneyAmount = pm.read_longlong(MoneyAmount) + offset


def update_money():
    pm.write_int(MoneyAmount, pm.read_int(MoneyAmount) + 20000)
    MoneyLabel.configure(text="Money: " + str(pm.read_int(MoneyAmount)))


# Add 500 Points
def get_points_addr():
    global PointsAmount
    base_address = module + 0x0506BEF8
    offsets = [0x8, 0x20, 0x8, 0x8, 0x208, 0xE8]

    PointsAmount = base_address
    for offset in offsets:
        PointsAmount = pm.read_longlong(PointsAmount) + offset
    return


def update_points():
    pm.write_int(PointsAmount, pm.read_int(PointsAmount) + 500)
    PointsLabel.configure(text="Points: " + str(pm.read_int(PointsAmount)))


def get_ammo_addr():
    global AmmoAmount
    base_address = module + 0x04FBE828
    offsets = [0x48, 0x8, 0x50, 0x48, 0x38, 0xA0, 0x0, 0x188]

    AmmoAmount = base_address
    for offset in offsets:
        AmmoAmount = pm.read_longlong(AmmoAmount) + offset
    return


def check_ammo():
    while not stop_ammo_thread.is_set():
        if pm.read_int(AmmoAmount) < 10:
            pm.write_int(AmmoAmount, 50)


def on_ammo_checkbox_click():
    global ammo_thread

    if AmmoCheckbox.get():
        stop_ammo_thread.clear()
        ammo_thread = threading.Thread(target=check_ammo)
        ammo_thread.start()
    else:
        stop_ammo_thread.set()
        ammo_thread.join()


def get_jump_addr():
    global SuperJumpAmount
    base_address = module + 0x0508FF38
    offsets = [0xB8, 0x7A8]

    SuperJumpAmount = base_address
    for offset in offsets:
        SuperJumpAmount = pm.read_longlong(SuperJumpAmount) + offset
    return

def on_superjump_click():
    if SuperJumpCheckbox.get():
        pm.write_int(SuperJumpAmount, 1077550388)
    else:
        pm.write_int(SuperJumpAmount, 1067550388)


check_process_running()

pm = pymem.Pymem(process_name)
module = pymem.process.module_from_name(pm.process_handle, "FC_m64.dll").lpBaseOfDll

get_money_addr()
get_points_addr()
get_ammo_addr()
get_jump_addr()

AmmoCheckbox = customtkinter.CTkCheckBox(app,
                                         text="Infinite Ammo",
                                         corner_radius=3,
                                         border_width=2,
                                         command=on_ammo_checkbox_click)
AmmoCheckbox.grid(row=2, column=0)

AddPointsButton = customtkinter.CTkButton(app,
                                          text="Add 500 Points",
                                          command=update_points,
                                          height=25,
                                          corner_radius=4,
                                          width=120)

AddPointsButton.grid(row=1, column=0)

# Initialize the label with the current points amount
PointsLabel = customtkinter.CTkLabel(app, text="Points: " + str(pm.read_int(PointsAmount)))
PointsLabel.grid(row=1, column=1)

AddMoneyButton = customtkinter.CTkButton(app,
                                         text="Add 20k Money",
                                         command=update_money,
                                         height=25,
                                         corner_radius=4,
                                         width=120)
AddMoneyButton.grid(row=0, column=0)

# Initialize the label with the current money amount
MoneyLabel = customtkinter.CTkLabel(app, text="Money: " + str(pm.read_int(MoneyAmount)))
MoneyLabel.grid(row=0, column=1, padx=10)

# Super jump
SuperJumpCheckbox = customtkinter.CTkCheckBox(app,
                                         text="Super Jump",
                                         corner_radius=3,
                                         border_width=2,
                                         command=on_superjump_click)
SuperJumpCheckbox.grid(row=2, column=0)

# Infinite Ammo
stop_ammo_thread = threading.Event()
ammo_thread = None

app.mainloop()
