from optparse import OptionParser
from handler.filter import *

if __name__ == '__main__':
    parser = OptionParser("You need to enter a jboss (either 'ejb' or 'servlet') or 'apache'.")
    (options, args) = parser.parse_args()

    try:
        if args[0].lower() == 'ejb':
            #original_logfile = '../../data/original/jboss.ejb.log'
            #filtered_logfile = '../../data/filtered/filtered.jboss.ejb.log'        
            original_logfile = args[1] if 1 in args else '../../data/original/jboss.ejb.log'
            filtered_logfile = args[2] if 2 in args else '../../data/filtered/filtered.jboss.ejb.log'
            log_filter = JbossEjbFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        elif args[0].lower() == 'servlet':
            #original_logfile = '../../data/original/jboss.servlet.log'
            #filtered_logfile = '../../data/filtered/filtered.jboss.servlet.log'        
            original_logfile = args[1] if 1 in args else '../../data/original/jboss.servlet.log'
            filtered_logfile = args[2] if 2 in args else '../../data/filtered/filtered.jboss.servlet.log'
            log_filter = JbossServletFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        elif args[0].lower() == 'apache':
            #original_logfile = '../../data/original/miiscan_error.log'
            #filtered_logfile = '../../data/filtered/filtered.miiscan_error.log'
            original_logfile = args[1] if 1 in args else '../../data/original/miiscan_error.log'
            filtered_logfile = args[2] if 2 in args else '../../data/filtered/filtered.miiscan_error.log'
            log_filter = ApacheErrorFilter(original_logfile, filtered_logfile)
            log_filter.generate_filtered_log()
        else:
            print "Please enter 'ejb', 'servlet', or 'apache' as an option"
    except:
            print "Please enter an option: 'ejb', 'servlet', or 'apache'"
