LOG FILTER SCRIPT - README
=============================
@author Jason Kim <jkim@riavera.com>


----------------------
PRE-REQUIREMENT
----------------------
Python version 2.6.x or up



----------------------
MODIFY CONFIGURATION
----------------------
The file is located at 'src/log_analyzer/config/configs.py'.
You may change default original/filtered log file paths.



----------------------
HOW TO RUN SCRIPT?
----------------------
0. Prepare Zend application log file from marvin2 server:
    - Zend application log is a huge single file. You'd better to filter by date before you download the log file into your local machine.
    - How to filter:
        a. Access marvin2 server
        b. $ cat /var/www/miiscan.com/app/miiscan/log/application.log | grep 2012-10-05T > ./application.log
            - You need to change '2012-10-05T' to your target date.

1. SSH Copy from remote servers:
    a. Jboss EJB log
        $ scp thor:/var/log/riavera/prod/jboss.ejb.log.YEAR-MONTH-DATE /PATH_TO_ORIGINAL_LOGS/jboss.ejb.log
            eg) $ scp thor:/var/log/riavera/prod/jboss.ejb.log.2012-10-08 ./logs/original/jboss.ejb.log

    b. Jboss Servlet log
        $ scp thor:/var/log/riavera/prod/jboss.servlet.log.YEAR-MONTH-DATE /PATH_TO_ORIGINAL_LOGS/jboss.servlet.log
            eg) $ scp thor:/var/log/riavera/prod/jboss.ejb.log.2012-10-08 ./logs/original/jboss.servlet.log

    c. Apache Miiscan log
        $ scp marvin2.intssn.tor.riavera.com:/var/log/apache2/miiscan_error.log ./PATH_TO_ORIGINAL_LOGS/miiscan_error.log
            eg) $ scp marvin2.intssn.tor.riavera.com:/var/log/apache2/miiscan_error.log ./logs/original/miiscan_error.log

    c. Zend Application log
        $ scp marvin2.intssn.tor.riavera.com:/PATH_YOU_STORED/application.log ./PATH_TO_ORIGINAL_LOGS/application.log
            eg) $ scp marvin2.intssn.tor.riavera.com:~/application.log ./logs/original/application.log

2. Run script:
    $ ./logfilter [OPTION]

    - you have four different OPTIONs:
        'ejb' - jboss.ejb.log
        'servlet' - jboss.servlet.log
        'miiscan' - apache miiscan_error.log
        'zend' - zend application.log

3. Check your filtered logs:
    - by default, filtered log files are stored in './logs/filtered/'



----------------------
IS IT DONE?
----------------------
Unfortunately not. You still need to look into log files in order to remove duplicate logs, manually.

