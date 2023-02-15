import os
import urllib.request
import tkinter as tk
import configparser
from tkinter import ttk
import threading

# Define the local directory for storing the downloaded files
local_dir = "dl/"


def create_directories():
    # Define the directory paths
    dl_dir = "./dl"
    scripts_dir = "./dl/scripts"
    inventory_dir = "./dl/inventory"
    
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)
    
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    
    if not os.path.exists(inventory_dir):
        os.makedirs(inventory_dir)



def download_files():
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    inventory_url = config['inventory']['url']
    script_url = config['scripts']['url']
    # Download the inventory file
    inventory_label.config(text="Downloading inventory file...")
    inventory_progress.start()
    urllib.request.urlretrieve(inventory_url, f"{local_dir}/inventory", reporthook=update_progress)
    inventory_label.config(text="Inventory file downloaded.")
    inventory_progress.stop()

    # Download the script files
    script_label.config(text="Downloading script files...")
    script_progress.start()
    urllib.request.urlretrieve(script_url, f"{local_dir}/scripts.tar.gz", reporthook=update_progress)
    script_label.config(text="Script files downloaded.")
    script_progress.stop()


def update_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    progress_bar["value"] = percent
    progress_bar.update()

def run_script():

    selected_script_index = script_listbox.curselection()[0]
    selected_script = ansible_scripts[selected_script_index]
    selected_inventory_index = inventory_listbox.curselection()[0]
    selected_inventory = inventory_groups[selected_inventory_index]
    
    os.system(f"ansible-playbook {directory_path}/{selected_script} -i {local_dir}/inventory --limit {selected_inventory}")


window = tk.Tk()
window.title("Ansible Script Runner")


progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)


inventory_label = tk.Label(window, text="")
inventory_label.pack()


inventory_progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='indeterminate')


script_label = tk.Label(window, text="")
script_label.pack()


script_progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='indeterminate')

create_directories()

download_thread = threading.Thread(target=download_files)
download_thread.start()


directory_path = f"{local_dir}/scripts"


config = configparser.ConfigParser()
config.read(f"{local_dir}/inventory")
inventory_groups = config.sections()

files = os.listdir(directory_path)
ansible_scripts = [f for f in files if f.endswith(('.yml', '.yaml'))]
script_label = tk.Label(window, text="Select a script to run:")
script_label.pack()

script_listbox = tk.Listbox(window)
for script in ansible_scripts:
    script_listbox.insert(tk.END, script)
script_listbox.pack()

inventory_label = tk.Label(window, text="Select a computer group:")
inventory_label.pack()

inventory_listbox = tk.Listbox(window)
for group in inventory_groups:
    inventory_listbox.insert(tk.END, group)
inventory_listbox.pack()

run_button = tk.Button(window, text="Run Script", command=run_script)
run_button.pack()

# Start the GUI event loop
window.mainloop()
