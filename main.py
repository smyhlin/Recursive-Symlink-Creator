from http.client import LineTooLong
import customtkinter as ctk
from tkinter import filedialog, Label, END
from CTkMessagebox import CTkMessagebox
import os
import sys
import ctypes
import shutil
from io import StringIO
from pymediainfo import MediaInfo
from rich.tree import Tree
from rich.console import Console
ctk.set_appearance_mode("System")


class FileInfo:
    def __init__(self, file_path):
        self.file_path = file_path
        self.mediainfo = MediaInfo.parse(file_path)
        self.file_stats = os.stat(file_path)
        self.key_mappings = {
        "other_unique_id": "Unique ID",
        "file_name": "Complete name",
        "other_format": "Format",
        "format_version": "Format version",
        "other_file_size": "File size",
        "other_overall_bit_rate": "Overall bit rate",
        "movie_name": "Movie name",
        "encoded_date": "Encoded date",
        "other_writing_application": "Writing application",
        "format_profile": "Format profile",
        "format_settings": "Format settings",
        "other_format_settings__cabac": "Format settings, CABAC",
        "other_format_settings__reframes": "Format settings, RefFrames",
        "other_width": "Width",
        "other_height": "Height",
        "other_display_aspect_ratio": "Display aspect ratio",
        "other_frame_rate_mode": "Frame rate mode",
        "color_space": "Color space",
        "other_chroma_subsampling": "Chroma subsampling",
        "other_scan_type": "Scan type",
        "bits__pixel_frame": "Bits/(Pixel*Frame)",
        "other_writing_library": "Writing library",
        "encoding_settings": "Encoding settings",
        "color_range": "Color range",
        "color_primaries": "Color primaries",
        "matrix_coefficients": "Matrix coefficients",
        "format_info": "Format/Info",
        'other_overall_bit_rate_mode': "Overall bit rate mode",
        "other_bit_rate_mode": "Bit rate mode",
        "other_channel_s": "Channel(s)",
        "channel_positions": "Channel positions",
        "channel_layout": "Channel layout",
        "other_sampling_rate": "Sampling rate",
        "other_commercial_name": "Commercial name",
        "other_frame_rate": "Frame rate",
        "other_bit_depth": "Bit depth",
        "other_compression_mode": "Compression mode",
        "other_service_kind": "Service kind",
        "track_id": "ID",
        "codec_id": "Codec ID",
        "codec_id_info": "Codec ID/Info",
        "other_duration": "Duration",
        "other_bit_rate": "Bit rate",
        "count_of_elements": "Count of elements",
        "other_stream_size": "Stream size",
        "other_language": "Language",
        "other_default": "Default",
        "other_forced": "Forced",
        "muxing_mode": "Muxing mode"
    }

    def get_media_info_detailed(self):
        tree = Tree(f"[bold blue]File Info: {self.file_path}[/]")
        for track in self.mediainfo.tracks:
            if track.track_type == "General":
                general_tree = tree.add("[bold magenta]General[/]")
                for key, value in track.to_data().items():
                    if isinstance(value, list):
                        value = ", ".join(value)
                    general_tree.add(f"[bold white]{key}:[/] {value}")
            elif track.track_type in ["Video", "Audio", "Text", "Image", "Menu"]:
                track_tree = tree.add(f"[bold magenta]{track.track_type}[/]")
                for key, value in track.to_data().items():
                    if isinstance(value, list):
                        value = ", ".join(value)
                    track_tree.add(f"[bold white]{key}:[/] {value}")
        return tree

    def get_media_info_compact(self):
        media_info = []
        tracks = self.mediainfo.to_data()['tracks']
        for track in tracks:
            track_type = track['track_type']
            if int(track['count_of_stream_of_this_kind']) > 1:
                media_info.append(f'{track_type} #{int(track["stream_identifier"]) + 1}')
            else:
                media_info.append(track_type)
            for k, v in track.items():
                if k in self.key_mappings:
                    if 'other' in k:
                        media_info.append(self.formatted(self.key_mappings[k], track[k][0]))
                    else:
                        media_info.append(self.formatted(self.key_mappings[k], track[k]))
                elif k.strip('other_') in self.key_mappings:
                    media_info.append(self.formatted(self.key_mappings[k.strip('other_')], track[k]))
                elif k[:1].isdigit():
                    media_info.append(self.formatted((k[:8] + '.' + k[8:]).replace('_', ':'), v))
            media_info.append('')

        return '\n'.join(media_info)


    def formatted(self, left, right):
        fixed = f"{left:<41}: {right}"
        return fixed

    def get_system_info(self):
        tree = Tree(f"[bold blue]System Info: {self.file_path}[/]")
        file_stats_tree = tree.add("[bold magenta]File Stats[/]")
        for key in dir(self.file_stats):
            if not key.startswith('_'):
                value = getattr(self.file_stats, key)
                file_stats_tree.add(f"[bold white]{key}:[/] {value}")
        return tree

    def print_info_to_text_widget(self, log_box):
        # console = Console()
        output_stream = StringIO()
        console = Console(file=output_stream, width=180)

        try:
            media_tree = self.get_media_info_detailed()

            console.print(media_tree)
        except Exception as e:
            console.print(f"[bold red]Error parsing media info: {e}[/]")
        system_tree = self.get_system_info()
        console.print('\n\n\n')
        console.print(system_tree)

        log_box.see(END)
        for line in output_stream.getvalue().splitlines():
            for tag in ["── General", "── Video", "── Audio", "── Text", "── Image", "── Menu"]:
                if tag in line:
                    log_box.tag_config("tag", foreground='SteelBlue1')
                    log_box.insert(END, line, "tag")
                    log_box.insert(END, '\n')
                    break
            else:
                log_box.insert(END, line)
                log_box.insert(END, '\n')

class App(ctk.CTk):
    WIDTH = 960
    HEIGHT = 590
    DEBUG_ME=False
    def __init__(self):
        super().__init__()
        self.folder_count = 0
        self.file_count = 0
        self.recursive_count = 1
        self.app_path = getattr(sys, "_MEIPASS", os.getcwd())
        self.operate_folder_var = ctk.BooleanVar()
        self.title("Recursive Symlink Creator")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")  # Increased height for log area
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure root grid layout (3x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Source sub-box
        self.source_frame = ctk.CTkFrame(self)
        self.source_frame.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")

        self.source_label = Label(self.source_frame, text="Source Folder:", bg='#2b2b2b', fg='#fff', font='Helvetica 11 bold')
        self.source_label.grid(padx=5,sticky="we")

        self.source_entry = ctk.CTkEntry(self.source_frame, )
        self.source_entry.grid(padx=5,sticky="we")
        if self.DEBUG_ME:
            self.source_entry.delete(0, ctk.END)
            self.source_entry.insert(0, r'F:\Media\Serials')
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
        if self.DEBUG_ME:
            self.dest_entry.delete(0, ctk.END)
            self.dest_entry.insert(0, r'F:\smsm')

        self.browse_dest_button = ctk.CTkButton(self.dest_frame, text="Browse", command=self.browse_dest)
        self.browse_dest_button.grid(pady=5, sticky="n")
        #! configure dest_frame grid layout (2x1)
        self.dest_frame.grid_columnconfigure(0, weight=1)
        self.dest_frame.grid_rowconfigure(2, weight=1)

        # Root sub-box
        self.root_frame = ctk.CTkFrame(self)
        self.root_frame.grid(row=2, column=1, pady=5, padx=5, sticky="nswe")

        # Symlink-box
        self.symlink_frame = ctk.CTkFrame(self.root_frame)
        self.symlink_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nwe")
        # Create Symlinks button
        self.create_symlinks_button = ctk.CTkButton(self.symlink_frame, text="Create Symlinks", width=180, command=self.create_symlinks)
        self.create_symlinks_button.grid(row=0, column=1, pady=5, padx=5, sticky="we")
        
        # Disable(default) \ Enable delete of allready existed folders checkbox
        self.delete_checkbox = ctk.CTkCheckBox(self.symlink_frame, 
                                            text="Delete prev. created symlinks", 
                                            variable=self.operate_folder_var,
                                            command=self.push_checkbox,
                                            onvalue=True, 
                                            offvalue=False)
        self.delete_checkbox.grid(row=2, column=1, pady=5, padx=5, sticky="nwe")

        # Tree-box
        self.tree_frame = ctk.CTkFrame(self.root_frame)
        self.tree_frame.grid(row=1, column=1, pady=5, padx=5, sticky="nwe")

        self.source_label = ctk.CTkLabel(self.tree_frame, text="Generate Folder tree view:")
        self.source_label.grid(row=1, column=0, columnspan=2, padx=5,sticky="we")

        # Create Mini tree button
        self.create_mini_tree_button = ctk.CTkButton(self.tree_frame, text="Mini", width=90, command=self.create_minitree)
        self.create_mini_tree_button.grid(row=2, column=0, pady=5, padx=5, sticky="nwse")

        # Create Full tree button
        self.create_full_tree_button = ctk.CTkButton(self.tree_frame, text="Full", width=90, command=self.create_tree)
        self.create_full_tree_button.grid(row=2, column=1, pady=5, padx=5, sticky="nwse")

        # Clear log box function
        self.create_clear_logbox_button = ctk.CTkButton(self.root_frame, text="Clear Log Box", width=180, command=self.clear_logbox)
        self.create_clear_logbox_button.grid(row=2, column=1, pady=5, padx=5, sticky="we")

        # Gem media info log box function
        self.create_get_media_info_button = ctk.CTkButton(self.root_frame, text="Get media info", width=180, command=self.get_media_info)
        self.create_get_media_info_button.grid(row=3, column=1, pady=5, padx=5, sticky="we")

        # Log area
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=2, column=0, pady=5, padx=5,sticky="nswe")

        self.log_box = ctk.CTkTextbox(self.log_frame, font=("Helvetica", 12), wrap="none")
        self.log_box.grid(row=0, column=0, rowspan=2, sticky="nswe")
        # self.log_box.configure(state="disabled")

        # Configure root_frame grid layout (2x2)
        self.root_frame.grid_columnconfigure(2, weight=1)
        self.root_frame.grid_rowconfigure(1, weight=1)

        # Configure log_frame grid layout (2x2)
        self.log_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_rowconfigure(1, weight=1)

        self.log_operation("►►► Launch completed successfully ◄◄◄", foreground='SteelBlue4')
        self.center_window(self)

    def center_window(self, window):
        """Centers the window on the screen."""
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - App.WIDTH) / 2
        y = (sh - App.HEIGHT) / 2
        self.geometry("%dx%d+%d+%d" % (App.WIDTH, App.HEIGHT, x, y))
        window.focus_force()
        window.wm_attributes("-topmost", True)

    def push_checkbox(self):
        if self.operate_folder_var.get():
            self.log_operation('►►► Program will delete allready existed folders checkbox', foreground='SteelBlue1')
        else:
            self.log_operation('►►► Program will skip allready existed folders checkbox', foreground='SteelBlue1')

    def clear_logbox(self):
        self.log_box.delete('1.0', END)

    def get_media_info(self):
        file_path = filedialog.askopenfilename()
        file_info = FileInfo(file_path)
        # self.log_operation(file_info.print_info())
        file_info.print_info_to_text_widget(self.log_box)

    def update_label_info(self, entry, label):
        """Updates the label with folder and file counts."""
        path = entry.get()
        if os.path.exists(path):
            self.count_folders_and_files(path)
            label.config(text=f"{label.cget('text').split(':')[0]}: ({self.folder_count} folders, {self.file_count} files)")
            self.log_operation(f"►►► {label.cget('text').split(':')[0]}: ({self.folder_count} folders, {self.file_count} files)", foreground='SteelBlue1')
            self.folder_count = 0
            self.file_count = 0
        else:
            label.config(text=f"{label.cget('text').split(':')[0]}: 0")
            self.log_operation(f"►►► {label.cget('text').split(':')[0]}: 0", foreground='SteelBlue1')

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
        self.log_operation(f'►►► Folder {folder_path} was selected', foreground='SteelBlue1')

    def log_operation(self, message, foreground="standart"):
        """Logs an operation message to the log area."""
        if foreground != 'standart':
            self.log_box.tag_config("folder", foreground=foreground)
            self.log_box.insert(END, message + "\n", "folder") # add folder tag to line which make it as described in config
        else:
            self.log_box.insert(END, message + "\n")

        self.log_box.see(END)  # Scroll to the end

    def create_minitree(self):
        folder_path = filedialog.askdirectory()
        minitree = os.popen(f"tree {folder_path}").read()
        self.log_operation('\n\n'+minitree, foreground='SteelBlue4')

    def create_tree(self):
        folder_path = filedialog.askdirectory()
        minitree = os.popen(f"tree /f {folder_path}").read()
        self.log_operation('\n\n'+minitree, foreground='SteelBlue4')

    def create_symlinks(self):
        """main init function that run all processes."""
        source_path = self.source_entry.get()
        dest_path = self.dest_entry.get()

        try:
            self.log_operation("►►► Creating symlinks...")
            self.recursive_symlink(source_path, dest_path)
            self.log_operation("►►► Symlinks created successfully! ◄◄◄", foreground='SteelBlue4')

            minitree = os.popen(f"tree {self.dest_entry.get()}").read()
            self.log_operation('\n\n'+minitree, foreground='SteelBlue4')

            self.recursive_count=0
            CTkMessagebox(title="Info", message="Symlink created successfully!")

        except Exception as e:
            self.log_operation(f"►►► Error: {str(e)}", foreground='SteelBlue1')
            CTkMessagebox(title="Error", message=str(e), icon="cancel")


    def recursive_symlink(self, source, destination):
        """Recursively creates symlinks from the source to the destination folder logick."""
        for entry in os.listdir(source):
            source_path = os.path.join(source, entry)
            dest_path = os.path.join(destination, entry)

            if os.path.islink(source_path):
                self.log_operation(f"Skipping existing symlink: {source_path}", foreground='SteelBlue1')
                continue

            if os.path.exists(dest_path):
                # If Delete_Checkbox selected, "operate_folder_var" = True
                if self.operate_folder_var.get():
                    if os.path.islink(dest_path):
                        os.remove(dest_path)
                        self.log_operation(f"Removed existing symlink: {dest_path}", foreground='SteelBlue1')
                    elif os.path.isdir(dest_path):
                        shutil.rmtree(dest_path)
                        self.log_operation(f"Removed existing directory: {dest_path}", foreground='SteelBlue1')
                    else:
                        os.remove(dest_path)
                        self.log_operation(f"Removed existing file: {dest_path}", foreground='SteelBlue1')
                else:
                    self.log_operation(f"Skipping existing file/folder: {dest_path}", foreground='SteelBlue1')
                    continue

            if os.path.isdir(source_path):
                os.makedirs(dest_path)
                folder_log = (' '*(self.recursive_count*3 if self.recursive_count>1 else 0) + ('--- ' if self.recursive_count>1 else '')+ f"Created directory: {dest_path}")
                self.log_operation(folder_log)
                
                self.recursive_count+=1
                self.recursive_symlink(source_path, dest_path)
                self.recursive_count-=1
            else:
                os.symlink(source_path, dest_path)
                self.log_operation(' '*(self.recursive_count*3 if self.recursive_count>1 else 0) + ('|--- ' if self.recursive_count>1 else '') + f"Created symlink': {dest_path} -> {source_path}")

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
        app = App()
        app.mainloop()
