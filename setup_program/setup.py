from install_pip import install_pip_
from extract import Setup
from _install import install_files
import os
import sys

# install pip
pip = install_pip_()

# extract files
setup = Setup()
setup.create_folder()
setup.get_file_names_in_folder("setup_program\set_up_files")


if not os.listdir("setup_program\\already_extract"):
    setup.create_folder()
    setup.extract_zip()
else:
    print("already have")


# install files
exe_path = []
ins_files = install_files()
directory_to_search = "setup_program\\already_extract"
exe_files = ins_files.find_exe_files(directory_to_search)

for exe_file in exe_files:
    print(exe_file)
    exe_path.append(exe_file)

for i in exe_path:
    try:
        os.system(i)
    except KeyError as e:
        print(e)

# download wemos d1 r32 core
try:
    os.system("arduino-cli core install esp32:esp32")
except Exception as e:
    print(e)

try:
    file_cli = ins_files.find_folder()
    # New path to add
    ins_files.add_path_to_env(file_cli)
except Exception as e:
    print(e)
