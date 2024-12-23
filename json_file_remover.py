import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter.ttk import Progressbar

class JSONRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Remover")
        
        self.path_label = tk.Label(root, text="Select Directory:")
        self.path_label.pack(pady=5)
        
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack(pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        self.filetype_label = tk.Label(root, text="Select File Type:")
        self.filetype_label.pack(pady=5)
        
        self.filetype_var = tk.StringVar(root)
        self.filetype_menu = tk.OptionMenu(root, self.filetype_var, "")
        self.filetype_menu.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_analysis)
        self.start_button.pack(pady=5)
        
        self.confirm_button = tk.Button(root, text="Confirm", command=self.start_removal, state=tk.DISABLED)
        self.confirm_button.pack(pady=5)
        self.confirm_button_tooltip = tk.Label(root, text="No files to remove", fg="grey")
        self.confirm_button_tooltip.pack(pady=5)
        
        self.progress = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=5)
        
        self.log_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.log_text.pack(pady=10)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)
            self.populate_filetypes(directory)
    
    def populate_filetypes(self, directory):
        filetypes = set()
        for root, dirs, files in os.walk(directory):
            for file in files:
                filetypes.add(file.split('.')[-1])
        
        self.filetype_var.set("")
        menu = self.filetype_menu["menu"]
        menu.delete(0, "end")
        for filetype in filetypes:
            menu.add_command(label=filetype, command=lambda value=filetype: self.filetype_var.set(value))
    
    def start_analysis(self):
        directory = self.path_entry.get()
        filetype = self.filetype_var.get()
        if directory and filetype:
            self.log_text.insert(tk.END, f"Analyzing directory: {directory} for *.{filetype} files\n")
            threading.Thread(target=self.analyze_directory, args=(directory, filetype)).start()
        else:
            self.log_text.insert(tk.END, "Please select a directory and file type first.\n")
    
    def analyze_directory(self, directory, filetype):
        total_folders = 0
        total_files = 0
        file_count = 0
        
        for root, dirs, files in os.walk(directory):
            total_folders += len(dirs)
            specific_files = [f for f in files if f.endswith(f'.{filetype}')]
            total_files += len(specific_files)
        
        self.progress['maximum'] = total_files
        
        for root, dirs, files in os.walk(directory):
            specific_files = [f for f in files if f.endswith(f'.{filetype}')]
            for file in specific_files:
                file_count += 1
                self.progress['value'] = file_count
                self.log_text.insert(tk.END, f"Analyzing: {os.path.join(root, file)}\n")
                self.log_text.see(tk.END)
        
        self.log_text.insert(tk.END, f"\nTotal folders: {total_folders}\n")
        self.log_text.insert(tk.END, f"Total {filetype.upper()} files: {total_files}\n")
        self.log_text.see(tk.END)  # Scroll to the end of the log
        
        if total_files > 0:
            self.confirm_button.config(state=tk.NORMAL)
            self.confirm_button_tooltip.config(text="")
        else:
            self.confirm_button.config(state=tk.DISABLED)
            self.confirm_button_tooltip.config(text=f"No {filetype.upper()} files to remove", fg="grey")
    
    def start_removal(self):
        directory = self.path_entry.get()
        filetype = self.filetype_var.get()
        if directory and filetype:
            self.log_text.insert(tk.END, f"Starting removal in directory: {directory} for *.{filetype} files\n")
            threading.Thread(target=self.remove_files, args=(directory, filetype)).start()
        else:
            self.log_text.insert(tk.END, "Please select a directory and file type first.\n")
    
    def remove_files(self, directory, filetype):
        file_count = 0
        for root, dirs, files in os.walk(directory):
            specific_files = [f for f in files if f.endswith(f'.{filetype}')]
            for file in specific_files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    file_count += 1
                    self.progress['value'] = file_count
                    self.log_text.insert(tk.END, f"Removed: {file_path}\n")
                except Exception as e:
                    self.log_text.insert(tk.END, f"Error removing {file_path}: {e}\n")
                self.log_text.see(tk.END)  # Scroll to the end of the log

if __name__ == "__main__":
    root = tk.Tk()
    app = JSONRemoverApp(root)
    root.mainloop()