import tkinter
import customtkinter as ctk
from tkinter import filedialog, Label, Text, END, NONE
from CTkMessagebox import CTkMessagebox
import os
import sys
import ctypes
import shutil


class RecursiveSymlinkGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.folder_count = 0
        self.file_count = 0
        self.operate_folder_var = ctk.BooleanVar()
        self.title("Recursive Symlink Creator")
        self.geometry("960x590")  # Increased height for log area
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure root grid layout (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Source sub-box
        self.source_frame = ctk.CTkFrame(self)
        self.source_frame.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")

        self.source_label = Label(self.source_frame, text="Source Folder:", bg='#2b2b2b', fg='#fff', font='Helvetica 11 bold')
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
        self.dest_frame.grid(row=1, column=0, pady=5, padx=5, sticky="nswe", columnspan=2)

        self.dest_label = Label(self.dest_frame, text="Destination Folder:", bg='#2b2b2b', fg='#fff', font='Helvetica 11 bold')
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
        self.root_frame.grid(row=2, column=1, pady=5, padx=5, sticky="nswe")

        # Create Symlinks button
        self.create_button = ctk.CTkButton(self.root_frame, text="Create Symlinks", width=200, command=self.create_symlinks)
        self.create_button.grid(row=0, column=1, pady=5, padx=5, sticky="ne")

        # Disable(default) \ Enable delete of allready existed folders checkbox
        self.delete_checkbox = ctk.CTkCheckBox(self.root_frame, 
                                            text="Delete prev created symlinks", 
                                            variable=self.operate_folder_var,
                                            command=self.push_checkbox,
                                            onvalue=True, 
                                            offvalue=False)
        self.delete_checkbox.grid(row=1, column=1, pady=5, padx=5, sticky="ne")

        # Log area
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=2, column=0, pady=5, padx=5,sticky="nswe")

        self.log_text = Text(self.log_frame, state="normal", undo=True, wrap=NONE, font=("Helvetica", 9), bg='#2b2b2b', fg='#fff')
        self.log_text.grid(row=0, column=0, sticky="nswe")

        self.log_scrollbar_y = ctk.CTkScrollbar(self.log_frame, 
                                            command=self.log_text.yview, orientation="vertical")
        self.log_scrollbar_y.grid(row=0, column=1, sticky="sn")

        self.log_scrollbar_x = ctk.CTkScrollbar(self.log_frame, 
                                            command=self.log_text.xview, orientation="horizontal")
        self.log_scrollbar_x.grid(row=1, column=0, sticky="we")
        self.log_text.config(yscrollcommand=self.log_scrollbar_y.set, xscrollcommand=self.log_scrollbar_x.set)

        # Configure root_frame grid layout (2x2)
        self.root_frame.grid_columnconfigure(2, weight=1)
        self.root_frame.grid_rowconfigure(1, weight=1)

        # Configure log_frame grid layout (2x2)
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)

        self.log_operation("►►► Launch completed successfully ◄◄◄")
        self.center_window(self)

    def center_window(self, window):
        """Centers the window on the screen."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"+{x}+{y}")
        window.focus_force()
        window.wm_attributes("-topmost", True)

    def push_checkbox(self):
        if self.operate_folder_var.get():
            self.log_operation('►►► Program will delete allready existed folders checkbox')
        else:
            self.log_operation('►►► Program will skip allready existed folders checkbox')

    def update_label_info(self, entry, label):
        """Updates the label with folder and file counts."""
        path = entry.get()
        if os.path.exists(path):
            self.count_folders_and_files(path)
            label.config(text=f"{label.cget('text').split(':')[0]}: ({self.folder_count} folders, {self.file_count} files)")
            self.log_operation(f"►►► {label.cget('text').split(':')[0]}: ({self.folder_count} folders, {self.file_count} files)")
            self.folder_count = 0
            self.file_count = 0
        else:
            label.config(text=f"{label.cget('text').split(':')[0]}: 0")
            self.log_operation(f"►►► {label.cget('text').split(':')[0]}: 0")

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
        """Opens a file dialog to select the source folder."""
        self.browse_folder(self.source_entry)
        self.update_label_info(self.source_entry, self.source_label)

    def browse_dest(self):
        """Opens a file dialog to select the destination folder."""
        self.browse_folder(self.dest_entry)

    def browse_folder(self, entry):
        """Opens a file dialog to select a folder and updates the given entry."""
        folder_path = filedialog.askdirectory()
        entry.delete(0, ctk.END)
        entry.insert(0, folder_path)
        self.log_operation(f'►►► Folder {folder_path} was selected')

    def log_operation(self, message, foreground="white"):
        """Logs an operation message to the log area."""
        if foreground != 'white':
            self.log_text.tag_config("folder", foreground=foreground)
            self.log_text.insert(END, message + "\n", "folder") # add folder tag to line which make it as described in config
        else:
            self.log_text.insert(END, message + "\n")

        self.log_text.see(END)  # Scroll to the end

    def create_symlinks(self):
        """main init function that run all processes."""
        source_path = self.source_entry.get()
        dest_path = self.dest_entry.get()

        try:
            self.log_operation("►►► Creating symlinks...")
            self.recursive_symlink(source_path, dest_path)
            self.log_operation("►►► Symlinks created successfully!")
            CTkMessagebox(title="Info", message="Symlink created successfully!")

        except Exception as e:
            self.log_operation(f"►►► Error: {str(e)}")
            CTkMessagebox(title="Error", message=str(e), icon="cancel")


    def recursive_symlink(self, source, destination):
        """Recursively creates symlinks from the source to the destination folder logick."""
        for entry in os.listdir(source):
            source_path = os.path.join(source, entry)
            dest_path = os.path.join(destination, entry)

            if os.path.islink(source_path):
                self.log_operation(f"Skipping existing symlink: {source_path}")
                continue

            if os.path.exists(dest_path):
                # If Delete_Checkbox selected, "operate_folder_var" = True
                if self.operate_folder_var.get():
                    if os.path.islink(dest_path):
                        os.remove(dest_path)
                        self.log_operation(f"Removed existing symlink: {dest_path}")
                    elif os.path.isdir(dest_path):
                        shutil.rmtree(dest_path)
                        self.log_operation(f"Removed existing directory: {dest_path}")
                    else:
                        os.remove(dest_path)
                        self.log_operation(f"Removed existing file: {dest_path}")
                else:
                    self.log_operation(f"Skipping existing file/folder: {dest_path}")
                    continue

            if os.path.isdir(source_path):
                os.makedirs(dest_path)
                self.log_operation(f"►►► Created directory: {dest_path}", foreground='steel blue')
                self.recursive_symlink(source_path, dest_path)
            else:
                os.symlink(source_path, dest_path)
                self.log_operation(f"Created symlink: {dest_path} -> {source_path}")


    def on_closing(self, event=0):
        """Closes the application."""
        self.destroy()


def run_as_admin():
    """Attempts to run the script as administrator."""
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
        return True
    except Exception as e:
        print("Error:", e)
        return False
    
def is_user_admin():
    """Checks if the user is an administrator."""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        if not is_user_admin():
            run_as_admin()
            sys.exit()
        #run only when compiled (windwos specific run as admin behavior mechanism)
        app = RecursiveSymlinkGUI()
        app.mainloop()
