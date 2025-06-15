
print("Memulai OS Simulasi...")

import tkinter as tk
from tkinter import Toplevel, Label, Frame
import time

# Global state
system_services = ["csrss.exe", "wininit.exe", "winlogon.exe", "halindows.exe"]
running_apps = []

# Waktu
def update_time():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)

# My Computer
def open_my_computer():
    window = Toplevel(root)
    window.title("My Computer")
    window.geometry("400x300")
    Label(window, text="Ini adalah jendela My Computer (simulasi)").pack(pady=50)
    running_apps.append("My Computer")

# Recycle Bin
def open_recycle_bin():
    window = Toplevel(root)
    window.title("Recycle Bin")
    window.geometry("300x200")
    Label(window, text="Recycle Bin kosong.").pack(pady=50)
    running_apps.append("Recycle Bin")

# File Explorer
filesystem = {
    "root": {
        "Local Disk (C:)": {
            "Users": {},
            "Windows": {}
        }
    }
}

def open_file_explorer():
    explorer = Toplevel(root)
    explorer.title("File Explorer")
    explorer.geometry("400x300")
    running_apps.append("File Explorer")

    path_stack = ["root"]

    content_frame = tk.Frame(explorer)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    path_label = tk.Label(explorer, text="Path: root")
    path_label.pack(anchor="w", padx=10)

    def show_folder_contents(current_path):
        for widget in content_frame.winfo_children():
            widget.destroy()

        current_dir = filesystem
        try:
            for p in current_path:
                current_dir = current_dir[p]
        except KeyError:
            current_dir = {}

        path_label.config(text="Path: " + " / ".join(current_path[1:]))

        for item in current_dir:
            b = tk.Button(content_frame, text="📁 " + item, anchor="w", width=30,
                          command=lambda i=item: enter_folder(i))
            b.pack(anchor="w", pady=2)

    def enter_folder(folder_name):
        path_stack.append(folder_name)
        show_folder_contents(path_stack)

    def go_back():
        if len(path_stack) > 1:
            path_stack.pop()
            show_folder_contents(path_stack)

    back_btn = tk.Button(explorer, text="⬅ Back", command=go_back)
    back_btn.pack(anchor="w", padx=10, pady=5)

    show_folder_contents(path_stack)

# Fake Terminal
def open_fake_terminal():
    term = Toplevel(root)
    term.title("Fake Terminal")
    term.geometry("500x300")
    term.configure(bg="black")
    running_apps.append("Fake Terminal")

    output = tk.Text(term, bg="black", fg="lime", insertbackground="white")
    output.pack(fill="both", expand=True)
    output.insert("end", "Halindows Terminal v0.1\nKetik 'help' untuk daftar perintah.\n\n")
    output.config(state="disabled")

    input_frame = tk.Frame(term, bg="black")
    input_frame.pack(fill="x")

    cmd_var = tk.StringVar()
    cmd_entry = tk.Entry(input_frame, textvariable=cmd_var, bg="black", fg="white", insertbackground="white")
    cmd_entry.pack(fill="x", padx=5, pady=5)

    def run_command(event=None):
        cmd = cmd_var.get().strip()
        cmd_var.set("")
        output.config(state="normal")
        output.insert("end", f"> {cmd}\n")

        if cmd == "help":
            output.insert("end", "Perintah yang tersedia:\n- help\n- dir\n- exit\n\n")
        elif cmd == "dir":
            output.insert("end", "C:\\Fake\\Folder1\nC:\\Fake\\Folder2\nC:\\Fake\\file.txt\n\n")
        elif cmd == "exit":
            term.destroy()
        else:
            output.insert("end", f"'{cmd}' tidak dikenali.\n\n")

        output.config(state="disabled")
        output.see("end")

    cmd_entry.bind("<Return>", run_command)
    cmd_entry.focus()

# Task Manager
def open_task_manager():
    tm = Toplevel(root)
    tm.title("Fake Task Manager")
    tm.geometry("300x300")

    listbox = tk.Listbox(tm)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    listbox.insert("end", "--- System Services ---")
    for svc in system_services:
        listbox.insert("end", f"[SYSTEM] {svc}")

    listbox.insert("end", "--- User Applications ---")
    for app in running_apps:
        listbox.insert("end", app)

    def end_task():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            value = listbox.get(index)
            if value.startswith("[SYSTEM]") or value.startswith("---"):
                print("Tidak bisa mengakhiri proses sistem.")
                return
            elif value in running_apps:
                running_apps.remove(value)
                listbox.delete(index)
                print(f"Menutup: {value}")

    tk.Button(tm, text="End Task", command=end_task).pack(pady=5)

# Shutdown
def shutdown():
    root.destroy()

# Klik kanan desktop
def show_context_menu(event):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Refresh", command=lambda: print("Merefresh desktop..."))
    context_menu.add_command(label="Properties", command=lambda: print("Menampilkan properties..."))
    context_menu.tk_popup(event.x_root, event.y_root)

# Root window
root = tk.Tk()
root.title("Halindows 98 Sim")
root.geometry("800x460")
root.configure(bg="skyblue")

tk.Button(root, text="🖥 My Computer", command=open_my_computer, bg="white").place(x=50, y=50)
tk.Button(root, text="🗑 Recycle Bin", command=open_recycle_bin, bg="white").place(x=50, y=100)

taskbar = tk.Frame(root, bg="gray20", height=30)
taskbar.pack(side="bottom", fill="x")

start_button = tk.Button(taskbar, text="Start", bg="lightgray")
start_button.pack(side="left", padx=5, pady=2)

clock_label = tk.Label(taskbar, bg="gray20", fg="white", font=("Consolas", 10))
clock_label.pack(side="right", padx=10)
update_time()

start_menu_visible = False

start_menu = tk.Frame(root, bg="#e0e0e0", width=250, height=300, highlightbackground="gray", highlightthickness=1)
tk.Label(start_menu, text="Welcome", bg="#004080", fg="white", font=("Segoe UI", 12, "bold")).pack(fill="x")
tk.Label(start_menu, text="", bg="#e0e0e0").pack(pady=3)
tk.Label(start_menu, text="Programs", bg="#e0e0e0", fg="black", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x", padx=10)
tk.Button(start_menu, text="🖥 My Computer", command=open_my_computer, anchor="w", width=25).pack(padx=10, pady=2)
tk.Button(start_menu, text="📁 File Explorer", command=open_file_explorer, anchor="w", width=25).pack(padx=10, pady=2)
tk.Button(start_menu, text="🖳 Fake Terminal", command=open_fake_terminal, anchor="w", width=25).pack(padx=10, pady=2)
tk.Button(start_menu, text="🧠 Task Manager", command=open_task_manager, anchor="w", width=25).pack(padx=10, pady=2)
tk.Label(start_menu, text="", bg="#e0e0e0").pack(pady=5)
tk.Label(start_menu, text="System", bg="#e0e0e0", fg="black", anchor="w", font=("Segoe UI", 10, "bold")).pack(fill="x", padx=10)
tk.Button(start_menu, text="⏻ Shutdown", command=shutdown, anchor="w", width=25).pack(padx=10, pady=2)

def toggle_start_menu():
    global start_menu_visible
    if start_menu_visible:
        start_menu.place_forget()
        start_menu_visible = False
    else:
        start_menu.place(x=0, y=root.winfo_height() - 330)
        start_menu_visible = True

start_button.config(command=toggle_start_menu)

root.bind("<Button-3>", show_context_menu)
root.mainloop()
