# import os
# os.system("\"_install.py\"")
import os
import sys
from _install import install_files
# import importlib.util
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")
# import importlib
# print(dir(importlib.util))
# print(sys.path)

# # Get the current value of the PATH environment variable
# current_path = os.environ.get('PATH')

# # Set the PATH environment variable to its current value
# os.environ['PATH'] = current_path

# print(current_path)


# def find_folder(root_folder, folder_name):
#     for root, dirs, files in os.walk(root_folder):
#         if folder_name in dirs:
#             return os.path.join(root, folder_name)
#     return None


# ins_files = install_files()
# file_cli = ins_files.find_folder()
# # New path to add
# new_path = file_cli

# # Get the current value of the PATH environment variable
# current_path = os.environ.get('PATH')

# # Append the new path to the current value of PATH, separated by the appropriate delimiter
# new_path_value = current_path + new_path + os.pathsep

# # Set the updated PATH environment variable
# os.environ['PATH'] = new_path_value
# last_path = os.environ.get('PATH')
# print(last_path)
# # Folder name
# folder_name = "arduino-cli_0.35.3_Windows_64bit"

# # Get the current working directory
# current_directory = os.getcwd()

# # Construct the path of the folder
# folder_path = os.path.join(current_directory, folder_name)

# # Get the absolute path of the folder
# absolute_folder_path = os.path.abspath(folder_path)

# print("Absolute path of the folder:", absolute_folder_path)


# --------------------------------------------------
# # New path to add
# new_path = "setup_program\\already_extract\\arduino-cli_0.35.3_Windows_64bit"

# # Get the current value of the PATH environment variable
# current_path = os.environ.get('PATH')

# # Append the new path to the current value of PATH, separated by the appropriate delimiter
# new_path_value = current_path + new_path + os.pathsep

# # Set the updated PATH environment variable
# os.environ['PATH'] = new_path_value

# print(new_path_value)
