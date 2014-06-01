web2py_error_watch
==================

Python script to notify an admin if a 500 system error has occurred in Web2Py.  
Every 30 seconds, the run loop will scan for new error files, parse them and
email a summary message to the email address specified.  The entire error pickle
is not emailed.  The reason is for safety of potentially sensitive information.
No form data should EVER be emailed because it could contain passwords, PII
or credit card information.  Proceed with caution.  There is still a chance private
information could be sent in the clear.  If that is the case, perhaps consider
modifying the script or delivering the mail to an @localhost address and pop the mail
from there securely.  Consider yourself warned.  I will assume no risk for data leakage 
from your use of this software.


IMPORTANT:  You will need to either copy/link the Web2Py gluon directory to the working directory
of this script or modify your python environment so that "from gluon import *" will succeed.

Modify the variables at the top of the script.  They are fairly self explanatory.  Ensure that 
app_error_path actually refers to the app_name/error directory or the script will fail.

Run the script by making it executable and typing ./watch.py OR, python watch.py.  In a production
environment, you will likely launch it with nohup or background the process and disown it so that 
it continues to run after you disconnect from your VTY.  STDERR will have debug messages printed to 
it.  So, if you like, redirect STDERR to a file when you start the script.

Enjoy.  This was a quick and dirty solution to making sure I knew when a particular customer's site
had a visitor experienc a 500 error.  I needed to know before the visitor called the site owner.  There
are many more things that could be done with this, and I am sure it could be prettier.  If you have
suggestions or additions, feel free to fork and send me a merge request.  My email address is:
dave<dot>stoll<at>gmail<dot>com.  Thanks  