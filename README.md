# Recursive Symlink Creator
---

Tired of manually managing symlinks for your media server? This handy utility automates the creation of recursive mirror symlinks, making it a breeze to keep your media organized and accessible.


#### Why use this?:
* Effortless Symlink Creation: Create a perfect mirror of your source folder's structure in the destination media server watchdog folder, all with a single click.
* Media Server Optimization: Ideal for Jellyfin, Plex, or other media servers. Freely use tools like FileBot to rename "files" -> symlinks for easy identification without sacrificing torrent seeding capabilities.


#### Features:
> ✅ Folder Selection: Browse and select source and destination folders using intuitive file dialogs and demonstrating directories | files count.

> ✅ Recursive Symlink Creation: Creates symlinks for all files and subfolders within the source folder, mirroring the directory structure in the destination.

> ✅ Existing Symlink and Folder Handling: Detects and handles existing symlinks and folders at the destination, allowing for options like overwriting or skipping.

> ✅ User Feedback: Provides informative messages and error dialogs to keep the user informed about the process.

> ✅ Administrator Rights: Checks for administrator privileges and attempts to elevate if necessary, ensuring proper symlink creation permissions.

> ✅ Window Management: Centers the GUI window and makes it topmost to enhance user experience.

> ✅ Logging: Selfloging tree view of most importan program nodes.

---

>GUI:
<p align="center">
<img src="https://telegra.ph/file/a820dcd5551593f220247.png">
</p>

---

#### Run/Build Instructions:
first install requirements.txt with pip  
```
> pip install -r requirements.txt
```


Next, you can run `main.py`

Or build the .exe file with the following command:
```
> pip install pyinstaller
> pyinstaller -F --onefile --noconsole ^
--clean --icon=".\icon.ico" ^
"main.py"
```
The executable will be created in `dist` directory

Or you can just download already built executable [here](https://github.com/smyhlin/Recursive-Symlink-Creator/releases)

#### Technologies Used:

* Python
* customtkinter (for Modern GUI)
* tkinter (for file dialogs and basic GUI elements)
* ctypes (for administrator rights handling)
* shutil (for folder removal)

## TODO:
* Get media single file info button

## Telegram Support:

[![ME](https://img.shields.io/badge/TG-ME-30302f?style=flat&logo=telegram)](https://t.me/s_myhlin)

#### LICENSE
- GPLv3