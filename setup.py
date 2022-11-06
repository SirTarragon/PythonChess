from cx_Freeze import setup, Executable

packages = ["pygame"]
includefiles = ["resources"]
excludes = []

setup(
        name = "Chess",
        version = "1.0",
        icon = "resources\menu\icon.png",
        description = "A Chess Game implemented with pygame",
        options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
        executables = [Executable("game.py", base = "Win32GUI")])