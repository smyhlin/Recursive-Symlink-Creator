# Recursive Symlink Creator
---

An utility for automatic creation recursive mirror symlinks from a source folder to a destination folder.

#### Features:
> ✅ Folder Selection: Browse and select source and destination folders using intuitive file dialogs and demonstrating directories | files count.

> ✅ Recursive Symlink Creation: Creates symlinks for all files and subfolders within the source folder, mirroring the directory structure in the destination.

> ✅ Existing Symlink and Folder Handling: Detects and handles existing symlinks and folders at the destination, allowing for options like overwriting or skipping.

> ✅ User Feedback: Provides informative messages and error dialogs to keep the user informed about the process.

> ✅ Administrator Rights: Checks for administrator privileges and attempts to elevate if necessary, ensuring proper symlink creation permissions.

> ✅ Window Management: Centers the GUI window and makes it topmost to enhance user experience.

---
---

>GUI:
<p align="center">
<img src="https://telegra.ph/file/70ef7c313617d951a9a88.jpg">
</p>

---
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

Or you can just download already built executable [here](https://github.com/smyhlin/TODO)

#### Technologies Used:

* Python
* customtkinter (for Modern GUI)
* tkinter (for file dialogs and basic GUI elements)
* ctypes (for administrator rights handling)
* shutil (for folder removal)



## Telegram Support:

[![ME](https://img.shields.io/badge/TG-ME-30302f?style=flat&logo=telegram)](https://t.me/s_myhlin)

#### LICENSE
- GPLv3