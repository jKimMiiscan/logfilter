import os
from optparse import OptionParser

class MockLogAnalyzer():
    log_file = None
    invalid_file_error_message = None

    def __init__(self):
        pass


    def set_args(self, args):
        if self.is_valid_args(args) == False:
            raise Exception(self.invalid_file_error_message)
        else:
            return True


    def is_valid_args(self, args):
        if args == []:
            self.invalid_file_error_message = "Please enter log type and the filename."
            return False
        elif args[0].lower() != "apache" and args[0].lower() != "jboss":
            self.invalid_file_error_message = "Invalid log type. Please enter 'apache' or 'jboss' for the log type."
            return False
        elif not os.path.exists(args[1]):
            self.invalid_file_error_message = "Passed file does not exist."
            return False
        else:
            return True


    def get_invalid_file_error_message(self):
        return self.invalid_file_error_message
        



if __name__ == '__main__':
    parser = OptionParser("You may enter a jboss (either ejb or servlet) log filename or an apache error log filename.")
    (options, args) = parser.parse_args()
    analyzer = MockLogAnalyzer()
    analyzer.set_args(args)
