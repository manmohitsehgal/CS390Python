#!/usr/bin/python
print("Content-Type: text/html\n\n")
	
# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session

#Get Databasedir
MYLOGIN="msehgal"
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/Twitter.db"

##############################################################
# Define function to generate login HTML form.
def change_password():
	html="""
HTML>

<FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
<input type="hidden" name="user" value="{user}">
<input type="hidden" name="session" value="{session}">
<input type="hidden" name="action" value="upload-pic-data">
<BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
<br>
<input type="submit" value="Press"> to upload the picture!
</form>
</HTML>
"""
	print_html_content_type()
	print(html)


