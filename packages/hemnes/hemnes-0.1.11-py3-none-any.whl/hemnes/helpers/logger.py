# import
from datetime import datetime

class Logger:
    """Class for logging process results"""

    def __init__(self):
        self.time = datetime.now().strftime('%m-%d %H:%M:%S')
        self.log_path = 'hemnes-%s.log' % (self.time)
        self.log_file = None

    def open(self):
        self.log_file = open(self.log_path, "w+")
        header = '=======================================\nhemnes logs from - %s\n=======================================' % (self.time)
        self.log_file.write(header)
        print(header)

    def log_if_active(self, message):
        """Writes given message to the log file and to console"""
        if self.log_file is not None:
            self.log_file.write('\n'+message)
            print(message)

    def close_if_open(self):
        if self.log_file is not None:
            print('\n=======================================\nsee logs at %s\n=======================================' % (self.log_path))
            self.log_file.close()
