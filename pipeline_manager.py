import file_utils
import db_manager


class WebManager():
    def __init__(self):
        self.io_manager = file_utils.IO_Manager()

    def save_file(self, app, file_list, user):
        self.io_manager.save_file(app, file_list, user)