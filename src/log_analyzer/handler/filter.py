import os
import sys
from os.path import isfile, join
from config.configs import *


class Filter(object):
    log_file = None
    filtered_log_file = None
    error_message = ""
    filtering_words = []
    extra_excludings_with_following_stacktraces = []
    next_debug_lines_to_output = 5
    filter_name = None
    log_filename = None
    filtered_log_filename = None
    skip_stacktrace = False
    max_stacktrace_count = 7

    def __init__(self, log_filename, filtered_log_filename, filtering_words=[], extra_excludings_with_following_stacktraces=[]):
        self.log_filename = log_filename
        self.filtered_log_filename = filtered_log_filename
        self.log_file = self.open_log_file(log_filename)
        self.filtered_log_file = self.open_filtered_log_file(filtered_log_filename)
        self.filtering_words = filtering_words
        self.extra_excludings_with_following_stacktraces = extra_excludings_with_following_stacktraces


    def generate_filtered_log(self):
        stacktrace_count = 0

        try: 
            for line in self.log_file:
                if self.skip_stacktrace == True:
                    if self.is_stacktrace(line) == False:
                        self.skip_stacktrace = False
                else:
                    filtered_line = self.filter_log_each_line(line)
                    if filtered_line != False:
                        if self.is_stacktrace(line) == True:
                            stacktrace_count += 1
                            if stacktrace_count > self.max_stacktrace_count:
                                continue
                        else:
                            stacktrace_count = 0

                        self.write_filtered_log(filtered_line)

            print "Your " + self.filter_name + " has been filtered successfully. Please check '" + self.filtered_log_filename + "' for your filtered file."

        except:
            print "[Error] " + self.error_message

    def filter_log_each_line(self, line):
        for string in self.filtering_words:
            if line.find(string) >= 0:
                for exclude_string in self.extra_excludings_with_following_stacktraces: # check extra excluding line exist
                    if line.find(exclude_string) >= 0:
                        self.skip_stacktrace = True
                        return False
                return line
        return False


    def is_stacktrace(self, line, line_starts_with=None):
        stacktrace_starts_with = line_starts_with if line_starts_with != None else ["\tat", "Caused by: "]
        for string in stacktrace_starts_with:
            if line.find(string) == 0:
                return True
        return False


    def get_next_debug_lines(self):
        pass


    def open_log_file(self, log_filename):
        """ read log file and store each line of logs in a single list """
        try:
            return open(log_filename, 'r')

        except IOError as e:
            self.error_message = "I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
        except ValueError as e:
            self.error_message = "Could not convert data to an integer."
            return False
        except:
            self.error_message = "Unexpected error:", sys.exc_info()[0]
            return False


    def open_filtered_log_file(self, filtered_log_filename):
        """ read log file and store each line of logs in a single list """
        try:
            return open(filtered_log_filename, 'a+')

        except IOError as e:
            self.error_message = "I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
        except ValueError as e:
            self.error_message = "Could not convert data to an integer."
            return False
        except:
            self.error_message = "Unexpected error:", sys.exc_info()[0]
            return False


    def write_filtered_log(self, line):
        try:
            self.filtered_log_file.write(line)
            return True
        except IOError as e:
            self.error_message = "I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
        except:
            self.error_message = "Unexpected error:", sys.exc_info()[0]
            return False


class JbossEjbFilter(Filter):

    filter_name = 'Jboss Ejb'

    def __init__(self, log_filename, filtered_log_filename, filtering_words=[]):
        jboss_ejb_filtering_words = DEFAULT_JBOSS_EJB_FILTERING_WORDS if not filtering_words else filtering_words
        super(JbossEjbFilter, self).__init__(log_filename, filtered_log_filename, jboss_ejb_filtering_words, JBOSS_EJB_EXTRA_EXCLUDING_WITH_STACKTRACES)

class JbossServletFilter(Filter):

    filter_name = 'Jboss Servlet'

    def __init__(self, log_filename, filtered_log_filename, filtering_words=[]):
        jboss_servlet_filtering_words = DEFAULT_JBOSS_SERVLET_FILTERING_WORDS if not filtering_words else filtering_words
        super(JbossServletFilter, self).__init__(log_filename, filtered_log_filename, jboss_servlet_filtering_words, JBOSS_SERVLET_EXTRA_EXCLUDING_WITH_STACKTRACES)


class ApacheMiiscanErrorFilter(Filter):

    filter_name = 'Miiscan Access Error'

    def __init__(self, log_filename, filtered_log_filename, filtering_words=[]):
        apache_error_excluding_words = DEFAULT_MIISCAN_ERROR_EXCLUDING_WORDS if not filtering_words else filtering_words
        super(ApacheMiiscanErrorFilter, self).__init__(log_filename, filtered_log_filename, apache_error_excluding_words)

    def filter_log_each_line(self, line):
        default_filtering_word = "File does not exist"
        for string in self.filtering_words:
            if line.find(string) >= 0 and line.find(default_filtering_word) >= 0:
                return False
        return line


class ApplicationErrorFilter(Filter):

    filter_name = 'Zend Application Error'

    def __init__(self, log_filename, filtered_log_filename, filtering_words=None):
        application_filtering_words = DEFAULT_APPLICATION_FILTERING_WORDS if filtering_words == None else filtering_words
        super(ApplicationErrorFilter, self).__init__(log_filename, filtered_log_filename, application_filtering_words)
