import unittest
from mock import log_analyzer

class LogAnalyzerTestCase(unittest.TestCase):
    """ Testing log analyzer
            - test reading log file
                - test the log file exist
                - test the log file is valid
            - test filtering logs
                - from jboss.ejb.log and jboss.servlet.log
                    - find all lines which enclude " ERROR " and "Exception"
                    - and find stacktraces as well if appear
                - from miiscan_error.log
                    - find all lines which enclude " File does not exist", but not ".txt", ".ico", ".css", ".jpg", ".png", ".jpeg", ".gif" files
            - test storing filtered line in list
            - test generating csv file with a list

        *** filtering words from jboss log
            "INFO", "WARN", "ERROR"
            especially "ERROR" : get all stacktraces
    """

    def setUp(self):
        self.analyzer = log_analyzer.MockLogAnalyzer()


    def tearDown(self):
        self.analyzer = None

    def test_string_to_lower(self):
        self.assertEqual("jBoss".lower(), "jboss")

    def test_no_argument_raise_error(self):
        try:
            arguments = []
            self.analyzer.set_args(arguments)
        except Exception:
            self.assertEqual("Please enter log type and the filename.", self.analyzer.get_invalid_file_error_message())
        except e:
            self.fail('Unexpected exception thrown:', e)
        else:
            self.fail('Exception not thrown')


    def test_wrong_log_filetype_raise_error(self):
        try:
            arguments = ['php', './correctlogfile.log']
            self.analyzer.set_args(arguments)
        except Exception:
            self.assertEqual("Invalid log type. Please enter 'apache' or 'jboss' for the log type.", self.analyzer.get_invalid_file_error_message())
        except e:
            self.fail('Unexpected exception thrown:', e)
        else:
            self.fail('Exception not thrown')


    def test_log_analyzer_class_file_does_not_exist_raise_error(self):
        try:
            arguments = ['jBoss', './wrongjbossfilename.log']
            self.analyzer.set_args(arguments)
        except Exception:
            self.assertEqual("Passed file does not exist.", self.analyzer.get_invalid_file_error_message())
        except e:
            self.fail('Unexpected exception thrown:', e)
        else:
            self.fail('Exception not thrown')





    """
    def test_log_analyzer_class_file_does_not_exist_raise_error(self):
        arguments = ['Apache', './somethingcorrect.log']
        analyser = self.analyzer(arguments)
        self.assertRaises(Exception, self.analyzer, arguments)
    """



if __name__ == '__main__':
    unittest.main()
