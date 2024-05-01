import zipfile
import os


class Setup():
    def __init__(self) -> None:
        self.create_extract()
        self.files_name = []
        self.files_zip = []
        self.extract_folder = 'setup_program/already_extract/'
        self.zip_folder = 'setup_program/set_up_files/'
        self.extract_path = []

    def create_extract(self):
        os.makedirs("setup_program\\already_extract", exist_ok=True)

    def extract_zip(self):
        count = 0
        for zip_file in self.files_zip:
            self.zip_folder += zip_file
            with zipfile.ZipFile(self.zip_folder, 'r') as zip_ref:
                zip_ref.extractall(self.extract_path[count])
            self.zip_folder = self.zip_folder.replace(zip_file, "")
            count += 1

    def create_folder(self):
        for i in self.files_name:
            self.extract_folder += i
            try:
                os.makedirs(self.extract_folder)
                print(f"Folder '{self.extract_folder}' created successfully.")
                self.extract_path.append(self.extract_folder)
                self.extract_folder = self.extract_folder.replace(i, "")
            except OSError as e:
                print(f"Error creating folder '{self.extract_folder}': {e}")
        print(self.extract_path)

    def get_file_names_in_folder(self, folder_path):
        files = os.listdir(folder_path)
        for i in files:
            self.files_zip.append(i)
            file_name = i.split(".zip")
            self.files_name.append(file_name[0])
            print(file_name[0])
        print(self.files_zip)




# Example usage
# folder_path = 'set_up_files'

# file_names = get_file_names_in_folder(folder_path)
# print("File names in folder:", file_names)


#

# create_folder(folder_path)
# # Example usage
# zip_file = 'CH341SER.zip'
# extract_to = 'already_extract/Port'

# extract_zip(zip_file, extract_to)
# print(f"Files extracted to {extract_to}")
