import customtkinter as ctk
import customtkinter
from tkinter import filedialog, Label
from CTkMessagebox import CTkMessagebox
import os
import sys
import ctypes
import shutil


class RecursiveSymlinkGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.folder_count = 0
        self.file_count = 0
        self.replace_existence_symlink_folders = False

        self.title("Recursive Symlink Creator")
        self.geometry("720x255")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        #! configure root grid layout (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Source sub-box
        self.source_frame = ctk.CTkFrame(self)
        self.source_frame.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

        self.source_label = Label(self.source_frame, text="Source Folder:", bg='#2b2b2b', fg='#fff', font='Helvetica 12 bold')
        self.source_label.grid(padx=5,sticky="we")

        self.source_entry = ctk.CTkEntry(self.source_frame)
        self.source_entry.grid(padx=5,sticky="we")

        self.browse_source_button = ctk.CTkButton(self.source_frame, text="Browse", command=self.browse_source)
        self.browse_source_button.grid(pady=5,sticky="n")
        #! configure source_frame grid layout (2x1)
        self.source_frame.grid_columnconfigure(0, weight=1)
        self.source_frame.grid_rowconfigure(2, weight=1)

        # Destination sub-box
        self.dest_frame = ctk.CTkFrame(self)
        self.dest_frame.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

        self.dest_label = Label(self.dest_frame, text="Destination Folder:", bg='#2b2b2b', fg='#fff', font='Helvetica 12 bold')
        self.dest_label.grid(padx=5, sticky="we")

        self.dest_entry = ctk.CTkEntry(self.dest_frame)
        self.dest_entry.grid(padx=5, sticky="we")

        self.browse_dest_button = ctk.CTkButton(self.dest_frame, text="Browse", command=self.browse_dest)
        self.browse_dest_button.grid(pady=5, sticky="n")
        #! configure dest_frame grid layout (2x1)
        self.dest_frame.grid_columnconfigure(0, weight=1)
        self.dest_frame.grid_rowconfigure(2, weight=1)
        
        # Root sub-box
        self.root_frame = ctk.CTkFrame(self)
        self.root_frame.grid(row=2, column=0, pady=5, padx=5, sticky="nswe")

        # Create Symlinks button
        self.create_button = ctk.CTkButton(self.root_frame, text="Create Symlinks", width=200, command=self.create_symlinks)
        self.create_button.grid(row=1, column=0, pady=5, padx=5)

        # Disable(default) \ Enable delete of allready existed folders radio button
        self.create_button = ctk.CTkRadioButton(self.root_frame, text="Create Symlinks", command=self.operate_existence_folders)
        self.create_button.grid(row=1, column=0, pady=5, padx=5, sticky="w")

        #! configure dest_frame grid layout (2x1)
        self.root_frame.grid_columnconfigure(0, weight=1)
        self.root_frame.grid_rowconfigure(2, weight=1)

        self.center_window(self)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry('+{}+{}'.format(x, y))
        window.focus_force()
        window.wm_attributes("-topmost", True)


    def update_label_info(self, entry, label):
        """Updates the label with folder and file counts."""
        path = entry.get()
        if os.path.exists(path):
            self.count_folders_and_files(path)
            label.config(text=f"{label.cget('text').split(':')[0]}: ({self.folder_count} folders, {self.file_count} files)")
            self.folder_count = 0
            self.file_count = 0
        else:
            label.config(text=f"{label.cget('text').split(':')[0]}: 0")

    def count_folders_and_files(self, path):
        """Counts folders and files within the given path."""
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                self.folder_count += 1
                self.count_folders_and_files(entry_path)
            else:
                self.file_count += 1

    def browse_source(self):
        self.browse_folder(self.source_entry)
        self.update_label_info(self.source_entry, self.source_label)

    def browse_dest(self):
        self.browse_folder(self.dest_entry)

    def browse_folder(self, entry):
        folder_path = filedialog.askdirectory()
        entry.delete(0, ctk.END)
        entry.insert(0, folder_path)

    def operate_existence_folders(self):
        pass

    def create_symlinks(self):
        source_path = self.source_entry.get()
        dest_path = self.dest_entry.get()
        try:
            self.recursive_symlink(source_path, dest_path)
            CTkMessagebox(title="Info", message="Symlink created successfully!")
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def recursive_symlink(self, source, destination):
        for entry in os.listdir(source):
            source_path = os.path.join(source, entry)
            dest_path = os.path.join(destination, entry)

            if os.path.islink(source_path):
                continue  # Skip existing symlinks in the source

            if os.path.exists(dest_path):
                if os.path.islink(dest_path):
                    os.remove(dest_path)  # Remove existing symlink
                elif os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)  # Remove existing folder
                else:
                    os.remove(dest_path)  # Remove existing file

            if os.path.isdir(source_path):
                os.makedirs(dest_path)
                self.recursive_symlink(source_path, dest_path)
            else:
                os.symlink(source_path, dest_path)

    def on_closing(self, event=0):
        self.destroy()


def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
        return True
    except Exception as e:
        print("Error:", e)
        return False
    
def isUserAdmin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        if not isUserAdmin():
            run_as_admin()
            sys.exit()
        app = RecursiveSymlinkGUI()
        app.mainloop()
