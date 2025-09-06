import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class NodeModulesManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Node_modules Manager")
        self.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        # Folder selection button
        self.select_folder_btn = tk.Button(self, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack(pady=10)

        # Display the selected folder path
        self.folder_path_label = tk.Label(self, text="", wraplength=350)
        self.folder_path_label.pack(pady=5)

        # Button to count node_modules folders
        self.count_btn = tk.Button(self, text="Count Node_modules", command=self.count_node_modules, state=tk.DISABLED)
        self.count_btn.pack(pady=5)

        # Button to delete node_modules folders
        self.delete_btn = tk.Button(self, text="Delete Node_modules", command=self.delete_node_modules, state=tk.DISABLED)
        self.delete_btn.pack(pady=5)

        # Button to list files by size
        self.list_files_btn = tk.Button(self, text="List Files by Size", command=self.list_files_by_size, state=tk.DISABLED)
        self.list_files_btn.pack(pady=5)

        # Display the result of counting, deletion, or file listing
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=10)

        # Text box to display files sorted by size
        self.files_text = tk.Text(self, width=50, height=10)
        self.files_text.pack(pady=5)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select Folder")
        if self.folder_path:
            self.folder_path_label.config(text=self.folder_path)
            self.count_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            self.list_files_btn.config(state=tk.NORMAL)

    def count_node_modules(self):
        if not self.folder_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return

        node_modules_count = 0
        for root, dirs, files in os.walk(self.folder_path):
            if 'node_modules' in dirs:
                node_modules_count += 1

        self.result_label.config(text=f"Found {node_modules_count} 'node_modules' folders.")

    def delete_node_modules(self):
        if not self.folder_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return

        deleted_count = 0
        for root, dirs, files in os.walk(self.folder_path):
            if 'node_modules' in dirs:
                node_modules_path = os.path.join(root, 'node_modules')
                shutil.rmtree(node_modules_path)
                deleted_count += 1

        self.result_label.config(text=f"Deleted {deleted_count} 'node_modules' folders.")
        messagebox.showinfo("Deletion Complete", f"Deleted {deleted_count} 'node_modules' folders.")

    def list_files_by_size(self):
        if not self.folder_path:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return

        file_sizes = []
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_sizes.append((file, file_size))

        # Sort files by size in descending order
        file_sizes.sort(key=lambda x: x[1], reverse=True)

        self.files_text.delete(1.0, tk.END)
        for file, size in file_sizes:
            size_mb = size / (1024 * 1024)
            self.files_text.insert(tk.END, f"{file}: {size_mb:.2f} MB\n")

        self.result_label.config(text="Files listed by size.")

if __name__ == "__main__":
    app = NodeModulesManager()
    app.mainloop()
