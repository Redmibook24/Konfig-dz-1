import os
import logging
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
import shutil  # Import shutil for cross-platform disk usage

# Set up logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(message)s')

def log_action(action):
    logging.info(action)

def list_directory():
    entries = os.listdir(os.getcwd())
    output = "\n".join(entries)
    return output

def change_directory(path):
    if path == "..":
        os.chdir("..")
        return f"Changed directory to: {os.getcwd()}"
    elif os.path.exists(path) and os.path.isdir(path):
        os.chdir(path)
        return f"Changed directory to: {path}"
    else:
        return "Directory does not exist."

def disk_usage():
    total, used, free = shutil.disk_usage(os.getcwd())
    available = free  # Available space is the free space
    return (f"Available: {available // (1024 * 1024)} MB\n"
            f"Used: {used // (1024 * 1024)} MB\n"
            f"Total: {total // (1024 * 1024)} MB")

def reverse_string(s):
    reversed_str = s[::-1]
    return f"Reversed: {reversed_str}"

def find_file(filename):
    found = False
    output = ""
    for root, dirs, files in os.walk(os.getcwd()):
        if filename in files:
            output += f"Found: {os.path.join(root, filename)}\n"
            found = True
    if not found:
        output = f"Not found: {filename}"
    return output

def process_command(command):
    log_action(command)
    
    if command == "exit":
        app.quit()
    elif command == "ls":
        return list_directory()
    elif command.startswith("cd "):
        return change_directory(command[3:])
    elif command == "du":
        return disk_usage()  # Disk usage command
    elif command.startswith("rev "):
        return reverse_string(command[4:])
    elif command.startswith("find "):
        return find_file(command[5:])
    else:
        return "Command not recognized."

def on_enter(event):
    command = entry.get()
    entry.delete(0, tk.END)
    result = process_command(command)
    output_box.configure(state='normal')
    output_box.insert(tk.END, f"{Path.cwd()}/:> {command}\n{result}\n")
    output_box.configure(state='disabled')
    output_box.see(tk.END)  # Scroll to the end

# Create the main application window
app = tk.Tk()
app.title("Linux Console Emulator")
app.geometry("600x400")  # Set the window size

# Create a frame for the output and input
frame = tk.Frame(app)
frame.pack(pady=10)

# Create a text box for output
output_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
output_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
output_box.configure(state='disabled')

# Create an entry for user input
entry = tk.Entry(frame, width=80)
entry.pack(side=tk.BOTTOM, pady=5)
entry.bind('<Return>', on_enter)

# Start the application
print("Welcome to the Linux Console Emulator!")
app.mainloop()
