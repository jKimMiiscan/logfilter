# original log file paths
DEFAULT_JBOSS_EJB_LOGFILE_PATH_ORIGINAL = './logs/original/jboss.ejb.log'
DEFAULT_JBOSS_SERVLET_LOGFILE_PATH_ORIGINAL = './logs/original/jboss.servlet.log'
DEFAULT_APACHE_MIISCAN_LOGFILE_PATH_ORIGINAL = './logs/original/miiscan_error.log'
DEFAULT_ZEND_APPLICATION_LOGFILE_PATH_ORIGINAL = './logs/original/application.log'

# filtered log file paths
DEFAULT_JBOSS_EJB_LOGFILE_PATH_FILTERED = './logs/filtered/filtered.jboss.ejb.log'
DEFAULT_JBOSS_SERVLET_LOGFILE_PATH_FILTERED = './logs/filtered/filtered.jboss.servlet.log'
DEFAULT_APACHE_MIISCAN_LOGFILE_PATH_FILTERED = './logs/filtered/filtered.miiscan_error.log'
DEFAULT_ZEND_APPLICATION_LOGFILE_PATH_FILTERED = './logs/filtered/filtered.application.log'


# filtering words - means any lines including one of words will be stored in filtered log file
DEFAULT_JBOSS_EJB_FILTERING_WORDS = ["ERROR", "fail", "\tat", "Exception", "exception"]
DEFAULT_JBOSS_SERVLET_FILTERING_WORDS = ["ERROR", "fail", "\tat"]
DEFAULT_APPLICATION_FILTERING_WORDS = ["ERR"]

# excluding words - obviously lines which have following words will be removed from the filtered log file
JBOSS_EJB_EXTRA_EXCLUDING_WITH_STACKTRACES = ["Activation failure: javax.ejb.EJBException: Could not activate; failed to restore state", " DEBUG ", ", callbackMethod=MerchantApiBean.processResponse, errorCode=EVENT_CALLBACK_ERROR, nextAttempt=", "couldn't get loginUserSF by handle: Could not activate;", "ORA-00001: unique constraint (OFFNET.XCHG_RATE_UNIQ) violated"]
JBOSS_SERVLET_EXTRA_EXCLUDING_WITH_STACKTRACES = ["Illegal args exception validating", "couldn't get loginUserSF by handle: Could not activate;", "ORA-00001: unique constraint (OFFNET.XCHG_RATE_UNIQ) violated"]
DEFAULT_MIISCAN_ERROR_EXCLUDING_WORDS = [".txt", ".ico", ".jpg", ".jpeg", ".png", ".gif"]
