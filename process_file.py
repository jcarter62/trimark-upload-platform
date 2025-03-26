import os
import shutil
from datetime import datetime
from excel_reader import ExcelReader
from data_writer import DataWriter
from decouple import config


class Process_File:

    dataobj = None

    def __init__(self):
        self.dataobj = {
            "file": "",
            "source": "",
            "destination": "",
            "data": []
        }
        return


    def view_file(self, filename):
        self.dataobj["file"] = filename
        rd = ExcelReader(self.dataobj["file"])
        self.dataobj["data"] = rd.records
        print(self.dataobj["data"])


    def extract_file_name(self, file_path) -> str:
        return os.path.basename(file_path)


    def calculate_destination_file(self, file_path, destination_folder) -> str:
        file_name = self.extract_file_name(file_path)
        new_name = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{file_name}"
        # calculate the new file name
        new_file_name = os.path.join(destination_folder, new_name)
        return new_file_name


    def move_input_file(self, file_path, destination_folder) -> bool:
        new_file_name = self.calculate_destination_file(file_path, destination_folder)
        shutil.move(file_path, new_file_name)
        # determine if move succeeded
        if os.path.exists(new_file_name):
            return True
        else:
            return False


    def exec(self, filename):
        self.dataobj["file"] = filename
        self.dataobj["destination"] = config('DESTINATION_FOLDER')
        rd = ExcelReader(self.dataobj["file"])
        self.dataobj["data"] = rd.records
        #
        try:
            dw = DataWriter(self.dataobj)
            dw.execute()
            self.move_input_file(self.dataobj["file"], self.dataobj["destination"])
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        return

