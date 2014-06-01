#!/usr/bin/env python

#***************************************************************************
# *                                                                         *
# *  Web2Py Exception Watcher                                               * 
# *  Copyright (C) 2014                                                     *
# *  Dave Stoll dave<dot>stoll<at>gmail<dot>com                             *
# *                                                                         *
# *  This program is free software: you can redistribute it and/or modify   *
# *  it under the terms of the GNU General Public License as published by   *
# *  the Free Software Foundation, either version 3 of the License, or      *
# *  (at your option) any later version.                                    *
# *                                                                         *
# *  This program is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
# *  GNU General Public License for more details.                           *
# *                                                                         *
# *  You should have received a copy of the GNU General Public License      *
# *  along with this program.  If not, see <http://www.gnu.org/licenses/>.  *
# *                                                                         *
# ***************************************************************************


##
## IMPORTANT:  the gluon directory from you web2py installation needs to be
## copied to the directory you run this script from.  Otherwise, you must modify
## your python runtime so this script knows where to find the gluon modules that
## are part of python
##

email_to='helpdesk@none.none'
email_from='helpdesk@none.none'
email_host='localhost'
app_error_path='/home/www-data/web2py/applications/welcome/error'

from gluon import *
import pickle, os, time, cStringIO, smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def senderror(path, errorfile):
    infile = open(path + '/' + errorfile)
    thiserror = pickle.load(infile)
    infile.close()

    string_buffer = cStringIO.StringIO()
    
    string_buffer.write("""<html><body><h2>An error has occurred.</h2><br/>\n""")
    string_buffer.write("<h4>Exception:</h4><br/>\n")    
    string_buffer.write('%s' % BEAUTIFY(thiserror['snapshot']['exception']))
    string_buffer.write('<br/><br/>\n')

    string_buffer.write("<h4>Error Type:</h4><br/>\n")    
    string_buffer.write('%s' % BEAUTIFY(thiserror['snapshot']['etype']))
    string_buffer.write('<br/><br/>\n')
    string_buffer.write("<h4>Locals:</h4><br/>\n")    
    string_buffer.write('%s' % BEAUTIFY(thiserror['snapshot']['locals']))
    string_buffer.write('<br/><br/>\n')
    
    string_buffer.write("<h4>Traceback:</h4><br/>\n<pre>")    
    string_buffer.write('%s' % BEAUTIFY(thiserror['traceback']))
    string_buffer.write('</pre><br/><br/>\n')
    string_buffer.write("<h4>Code:</h4><br/>\n<pre>")    
    string_buffer.write('%s' % BEAUTIFY(thiserror['code']))
    string_buffer.write('</pre><br/><br/>\n')
    
    string_buffer.write("</body></html>\n")
    
    msg = MIMEMultipart('alternative')
    text = "An error has occurred at cellarangels.  Please investigate."
    html = string_buffer.getvalue()
        
    msg['Subject'] = 'Cellar Angels ERROR: ' + errorfile
    msg['From'] = 'dstoll@almostgurus.com'
    msg['To'] = 'dave.stoll@gmail.com'
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    s = smtplib.SMTP(email_host)
    s.sendmail(email_from, email_to, msg.as_string())
    s.quit()


def main():    
    before = dict ([(f, None) for f in os.listdir (app_error_path)])
    while 1:
        time.sleep (30)
        after = dict ([(f, None) for f in os.listdir (app_error_path)])
        added = [f for f in after if not f in before]
        if added: print "Errors found."
        for error in added:
            print 'sending email for file: ', error
            senderror(app_error_path, error)
        
        before = after
  
if __name__ == "__main__":
    main()