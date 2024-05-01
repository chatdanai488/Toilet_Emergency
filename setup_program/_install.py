import glob
import sys
import os
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


# Replace 'your_program.exe' with the path to your executable file
# os.system("\"_install.py\"")

exe_path = []


def find_exe_files(directory):
    exe_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".exe"):
                exe_files.append(os.path.join(root, file))
    return exe_files


# Example usage:
directory_to_search = "already_extract"
exe_files = find_exe_files(directory_to_search)

for exe_file in exe_files:
    print(exe_file)
    exe_path.append(exe_file)

for i in exe_path:
    try:
        os.system(i)
    except KeyError as e:
        print(e)
