Email List Generator for Gmail Backup Archives with Wordpress Data
==================================================================
Here's the deal.  I use wordpress as the content management system for my website, [JeremyBlum.com](http://www.jeremyblum.com).  I get a ton of emails, some through the contact form, and others as comment notifications.  Associated with each of these emails is a name and and email address.  I also use [Got-Your-Back](https://code.google.com/p/got-your-back/) (a.k.a. GYB), a simple windows script that runs automatically on my computer every day and downloads and incremental backup of all the emails in my gmail account. I wanted a way to automatically parse through all my GYB emails and generate a comprehensive list of names/emails whom have been in contact with me. This python script accomplishes that, and can be easily modified to meet your need if they are similar.

How it Works
------------
* GYB Downloads my emails to .eml files on my computer once per day.  A nested folder structure is populated with emails.
* The python script contains a number of configuration variables for setting the date range to search through, the location of the email backups, the output CSV file name, search terms to identify, and spam terms to indicate that a message should be ignored.
* The script iterates through all the email to find the requested search terms (indicating the email came from my website as a contact or a comment.
* A name and email is extracted from each email that matches the search terms, and is added to a list.
* The list is then checked for duplicate email addresses, which are removed.
* Non-duplicate email addresses are validated by sending a query to their SMTP server of origin to determine if they are still valid mailboxes.
* If the address is determined to valid, then it is appended to a CSV output file.

Notes
-----
* Update the "CONFIGURATION OPTIONS" in the script to match your search scenario.
* This script was written to run in Windows with Python 2.7x 32-bit, and has not been tested in any other environments. I did not make any attemp to make it portable.
* GYB was used to download my email archive: https://code.google.com/p/got-your-back/
* The "Validate Email" Python Library is Used for SMTP verification: https://github.com/SyrusAkbary/validate_email
* This Script has been written by (Jeremy Blum)[www.jeremyblum.com] and is released under the GPL v3.  A copy of the GPL is included within this Repo.  Kindly share your improvements to this script, and maintain attribution to the original author (me).