import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox

class JSONRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON File Remover")
        
        self.path_label = tk.Label(root, text="Select Directory:")
        self.path_label.pack(pady=5)
        
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_analysis)
        self.start_button.pack(pady=5)
        
        self.confirm_button = tk.Button(root, text="Confirm", command=self.start_removal, state=tk.DISABLED)
        self.confirm_button.pack(pady=5)
        self.confirm_button_tooltip = tk.Label(root, text="No JSON files to remove", fg="grey")
        self.confirm_button_tooltip.pack(pady=5)
        
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.log_text.pack(pady=10)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.insert(0, directory)
    
    def start_analysis(self):
        directory = self.path_entry.get()
        if directory:
            self.log_text.insert(tk.END, f"Analyzing directory: {directory}\n")
            threading.Thread(target=self.analyze_directory, args=(directory,)).start()
        else:
            self.log_text.insert(tk.END, "Please select a directory first.\n")
    
    def analyze_directory(self, directory):
        total_folders = 0
        total_json_files = 0
        total_non_json_files = 0
        
        for root, dirs, files in os.walk(directory):
            total_folders += len(dirs)
            json_files = [f for f in files if f.endswith('.json')]
            non_json_files = [f for f in files if not f.endswith('.json')]
            
            total_json_files += len(json_files)
            total_non_json_files += len(non_json_files)
            
            self.log_text.insert(tk.END, f"Folder: {root}\n")
            self.log_text.insert(tk.END, f"  JSON files: {len(json_files)}\n")
            self.log_text.insert(tk.END, f"  Non-JSON files: {len(non_json_files)}\n")
        
        self.log_text.insert(tk.END, f"\nTotal folders: {total_folders}\n")
        self.log_text.insert(tk.END, f"Total JSON files: {total_json_files}\n")
        self.log_text.insert(tk.END, f"Total Non-JSON files: {total_non_json_files}\n")
        self.log_text.see(tk.END)  # Scroll to the end of the log
        
        if total_json_files > 0:
            self.confirm_button.config(state=tk.NORMAL)
            self.confirm_button_tooltip.config(text="")
        else:
            self.confirm_button.config(state=tk.DISABLED)
            self.confirm_button_tooltip.config(text="No JSON files to remove", fg="grey")
    
    def start_removal(self):
        directory = self.path_entry.get()
        if directory:
            self.log_text.insert(tk.END, f"Starting removal in directory: {directory}\n")
            threading.Thread(target=self.remove_json_files, args=(directory,)).start()
        else:
            self.log_text.insert(tk.END, "Please select a directory first.\n")
    
    def remove_json_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        self.log_text.insert(tk.END, f"Removed: {file_path}\n")
                    except Exception as e:
                        self.log_text.insert(tk.END, f"Error removing {file_path}: {e}\n")
            self.log_text.see(tk.END)  # Scroll to the end of the log

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONRemoverApp(root)
    root.mainloop()