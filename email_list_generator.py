# This Script Searches through your "Got Your Back (GYB)" Gmail Backups
# to generate a list of email addresses/names that match a certain criteria.
# This list is returns as a CSV File within this folder titled "list.csv".
# This script is designed to run in Windows with Python 2.7x 32-bit.

# GYB Can be found here: https://code.google.com/p/got-your-back/
# The "Validate Email" Python Library is Used: https://github.com/SyrusAkbary/validate_email

# This Script has been written by Jeremy Blum (www.jeremyblum.com).  Licensed via GPL v3.

######
# IMPORT LIBRARIES
######
import datetime
import calendar
import os
import re
import string
import csv
from validate_email import validate_email

######
# CONFIGURATION OPTIONS
######
gyb_abs_directory       = 'C:\\gyb\\jeremy@jeremyblum.com\\'
start_year              = 2006
end_year                = 2013
contact_search_term     = 'Subject: JeremyBlum.com Contact'
comment_search_term     = 'Subject: [JeremyBlum.com] Comment'
spam_term               = 'Akismet: Spam'
output_file             = 'emails.csv'

######
# ITERATE AND FIND EMAILS!
######

output = []

#Go Through each year.
for y in range(start_year, end_year+1):
   for m in range(1,13):
      for d in range(1,calendar.monthrange(y, m)[1]+1):
         present_date = datetime.date(y,m,d)
         file_location = gyb_abs_directory + present_date.strftime("%Y") + '\\' + str(int(present_date.strftime("%m"))) + '\\' + str(int(present_date.strftime("%d")))
         if os.path.isdir(file_location):
            print 'Searching Emails from {0}'.format(present_date.strftime("%B %d, %Y"))
            #Look at all the email in this directory
            for filename in os.listdir (file_location):
               email = open(file_location + '\\' + filename).read()
               email = email.replace('> ','') #erase RE: arrows
               #Is this an email from a contact form?
               if contact_search_term in email and spam_term not in email:
                  result = re.search('From:\n(.*)\n\nMessage:\n', email, re.DOTALL)
                  if result is not None:
                     info = result.group(0).split('\n')
                     name = info[1]
                     email_address = info[2]
                     print '\t' + filename + ' (Contact Form): ' + name + ', ' + email_address
                     #Put the name and email address in a 2D list
                     output.append([name,email_address])
               #Is this an email notifying me of a comment?
               elif comment_search_term in email and spam_term not in email:
                  result1 = re.search('Author : (.*) \(IP: ', email, re.DOTALL)
                  if result1 is not None:
                     info = result1.group(0).split(' : ')
                     info = info[1].split(' (IP: ')
                     name = info[0]
                  result2 = re.search('E-mail : (.*)\n', email, re.DOTALL)
                  if result2 is not None:
                     info = result2.group(0).split(' : ')
                     info = info[1].split('\n')
                     email_address = info[0]
                  if result1 is not None and result2 is not None:
                     print '\t' + filename + ' (Commenter): ' + name + ', ' + email_address
                     #Put the name and email address in a 2D list
                     output.append([name,email_address])

######
# Remove Duplicates, Deal with Empty Emails, Check for SMTP mailbox existance, & Write to CSV
######
CSVfile = open(output_file,'wb')
writer = csv.writer(CSVfile,dialect='excel')
duplicates_removed = set()
count = 0
print '\nChecking Email Addresses and Writing to CSV File...'
for row in output:
   if row[1] not in duplicates_removed:
      if row[1] != '':
         try:
            good = validate_email(row[1],verify=True)
         except:
            good = True #if SMTP server is having problems, just assume it's good.
         if good:
            writer.writerow(row)
            duplicates_removed.add(row[1])
            count = count + 1
            print '\tAdded ' + row[1] + '!'
         else:
            print '\t' + row[1] + ' is not a real email address!'
CSVfile.close()
print '\nFound and Recorded ' + str(count) + ' unique Email Addresses into '+ output_file + '!'
