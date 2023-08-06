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

    def log(self, message):
        """Writes given message to the log file and to console"""
        self.log_file.write('\n'+message)
        print(message)

    def close(self):
        print('\n=======================================\nsee logs at %s\n=======================================' % (self.log_path))
        self.log_file.close()
