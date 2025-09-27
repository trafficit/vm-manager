import subprocess
import tkinter as tk

def get_vm_list():
    output = subprocess.check_output(["VBoxManage", "list", "vms"]).decode()
    vms = []
    for line in output.strip().split("\n"):
        name = line.split('"')[1]
        vms.append(name)
    return vms

def get_vm_status(name):
    output = subprocess.check_output(["VBoxManage", "showvminfo", name, "--machinereadable"]).decode()
    for line in output.splitlines():
        if line.startswith("VMState="):
            return line.split("=")[1].strip('"')
    return "unknown"

def update_status(label, name):
    status = get_vm_status(name)
    label.config(text=f"Status: {status}", fg="green" if status == "running" else "red")

def start_vm(name, label):
    subprocess.run(["VBoxManage", "startvm", name, "--type", "headless"])
    update_status(label, name)

def stop_vm(name, label):
    subprocess.run(["VBoxManage", "controlvm", name, "poweroff"])
    update_status(label, name)

def start_all():
    for vm, label in vm_widgets:
        start_vm(vm, label)

def stop_all():
    for vm, label in vm_widgets:
        stop_vm(vm, label)

# GUI
root = tk.Tk()
root.title("VirtualBox VM Manager")

vm_widgets = []

for vm in get_vm_list():
    frame = tk.Frame(root)
    frame.pack(pady=5, fill="x")

    name_label = tk.Label(frame, text="   " + vm , width=25, anchor="w", font=("Arial", 10, "bold"))
    name_label.pack(side="left")

    status_label = tk.Label(frame, text="Status: ...", width=15)
    status_label.pack(side="left")
    update_status(status_label, vm)

    start_btn = tk.Button(frame, text="▶️ Start", command=lambda vm=vm, l=status_label: start_vm(vm, l))
    start_btn.pack(side="left", padx=5)

    stop_btn = tk.Button(frame, text="⏹️ Stop", command=lambda vm=vm, l=status_label: stop_vm(vm, l))
    stop_btn.pack(side="left", padx=5)

    vm_widgets.append((vm, status_label))

# Global buttons
global_frame = tk.Frame(root)
global_frame.pack(pady=10)

start_all_btn = tk.Button(global_frame, text="🟩 Start All", command=start_all, bg="lightgreen", width=20)
start_all_btn.pack(side="left", padx=10)

stop_all_btn = tk.Button(global_frame, text="🧊 Stop All", command=stop_all, bg="tomato", width=20)
stop_all_btn.pack(side="left", padx=10)

root.mainloop()
