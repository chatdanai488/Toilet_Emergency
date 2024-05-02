import pip
import sys
import os
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


# Replace 'your_program.exe' with the path to your executable file
# os.system("\"_install.py\"")

class install_files:

    def find_exe_files(self, directory):
        exe_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    exe_files.append(os.path.join(root, file))
                if file.endswith(".EXE"):
                    exe_files.append(os.path.join(root, file))
        return exe_files

    def search_files(self, directory, filename):
        found_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if filename in file:
                    found_files.append(os.path.join(root, file))
        return found_files

    def install(self, package):
        pip.main(['install', package])

    def find_folder(self, folder_name="arduino-cli_0.35.3_Windows_64bit"):

        # Get the current working directory
        current_directory = os.getcwd()

        # Construct the path of the folder
        folder_path = os.path.join(current_directory, folder_name)

        # Get the absolute path of the folder
        absolute_folder_path = os.path.abspath(folder_path)

        return absolute_folder_path.capitalize()

    def add_path_to_env(self, new_path):
        # Get the current value of the PATH environment variable
        current_path = os.environ.get('PATH')

        # Append the new path to the current value of PATH, separated by the appropriate delimiter
        new_path_value = current_path + new_path + os.pathsep

        # Set the updated PATH environment variable
        os.environ['PATH'] = new_path_value
# -----------------------------------------------------------------------
# download programe
# Example usage:
# exe_path = []
# ins_files = install_files()
# directory_to_search = "setup_program\\already_extract"
# exe_files = ins_files.find_exe_files(directory_to_search)

# for exe_file in exe_files:
#     print(exe_file)
#     exe_path.append(exe_file)

# for i in exe_path:
#     try:
#         os.system(i)
#     except KeyError as e:
#         print(e)

# # download wemos d1 r32 core
# try:
#     os.system("arduino-cli core install esp32:esp32")
# except Exception as e:
#     print(e)


# sys.path.append(
#     "setup_program\\already_extract\\arduino-cli_0.35.3_Windows_64bit")
# ---------------------------------------------

# package_name = "esptool"

# if importlib.util.find_spec(package_name) is not None:
#     print(f"{package_name} is installed.")
# else:
#     print(f"{package_name} is not installed.")
#     package_name = 'esptool'
#     install(package_name)
#     if importlib.util.find_spec(package_name) is not None:
#         print(f"{package_name} is installed.")
#     else:
#         filename_to_search = "setup.py"
#         found_files = search_files(directory_to_search, filename_to_search)

#         if found_files:
#             print("Found files:")
#             for file in found_files:
#                 print(file)
#                 subprocess.run(['python', file])
#         else:
#             print("No files found with the specified name pattern.")
