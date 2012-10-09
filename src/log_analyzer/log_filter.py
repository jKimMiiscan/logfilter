#!/usr/bin/env python
###########################################################################################
######################################## SETUP SYS.PATH ###################################
import os
import sys

current_path = os.getcwd()
module_path = os.path.join(current_path, "src", "log_analyzer")

if module_path not in sys.path:
    sys.path.append(module_path)
###########################################################################################

from optparse import OptionParser
from config.configs import *
from handler.filter import *

if __name__ == '__main__':
    parser = OptionParser("You need to enter a jboss (either 'ejb' or 'servlet'), 'miiscan', or 'zend'.")
    (options, args) = parser.parse_args()

    try:
        if args[0].lower() == 'ejb':
            original_logfile = args[1] if 1 in args else DEFAULT_JBOSS_EJB_LOGFILE_PATH_ORIGINAL
            filtered_logfile = args[2] if 2 in args else DEFAULT_JBOSS_EJB_LOGFILE_PATH_FILTERED
            log_filter = JbossEjbFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        elif args[0].lower() == 'servlet':
            original_logfile = args[1] if 1 in args else DEFAULT_JBOSS_SERVLET_LOGFILE_PATH_ORIGINAL
            filtered_logfile = args[2] if 2 in args else DEFAULT_JBOSS_SERVLET_LOGFILE_PATH_FILTERED
            log_filter = JbossServletFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        elif args[0].lower() == 'miiscan':
            original_logfile = args[1] if 1 in args else DEFAULT_APACHE_MIISCAN_LOGFILE_PATH_ORIGINAL
            filtered_logfile = args[2] if 2 in args else DEFAULT_APACHE_MIISCAN_LOGFILE_PATH_FILTERED
            log_filter = ApacheMiiscanErrorFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        elif args[0].lower() == 'zend':
            original_logfile = args[1] if 1 in args else DEFAULT_ZEND_APPLICATION_LOGFILE_PATH_ORIGINAL
            filtered_logfile = args[2] if 2 in args else DEFAULT_ZEND_APPLICATION_LOGFILE_PATH_FILTERED
            log_filter = ApplicationErrorFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        else:
            print "Please enter 'ejb', 'servlet', 'miiscan', or 'zend' as an option"
    
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror) + " - " + original_logfile
    except:
        print "Please enter an option: 'ejb', 'servlet', 'miiscan', or 'zend'"
        print "Unexpected error:", sys.exc_info()[0]
