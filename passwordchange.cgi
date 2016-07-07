#!/usr/bin/python

# Import login form

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import hashlib #hash passwords
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
<HTML>
<HEAD>
<TITLE>Change Password</TITLE>
</HEAD>

<BODY BGCOLOR = "#CFB53B">
<br>
<br>
<center><font face="Lato" size="15">Change Password</font></center>
<br>
<br>
<br>
<center>
<TABLE BORDER = 0>
<FORM METHOD=post ACTION="passwordchange.cgi">
<TR><TH>Enter Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Enter Old Password:</TH><TD><INPUT TYPE=password NAME="oldpassword"></TD></TR>
<TR><TH>Enter New Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>


<INPUT TYPE=hidden NAME="action" VALUE="change" size=10 style="height:30px width:150px">
<INPUT TYPE=submit VALUE="Submit" size=10 style="height:30px width:150px">
</center>

</FORM>
</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)

def changePassword(email,old, password):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	c.execute('UPDATE users SET password= ? WHERE email= ? AND password = ?',(password,email, old))	
	conn.commit()
	conn.close();
	print_html_content_type()
	print "<html></html>"
	print "<script>window.location.href=\"login.cgi\"</script>"
	
def print_html_content_type():

	print("Content-Type: text/html\n\n")
	
def check_password(user, passwd):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()

	t = (user,)
	c.execute('SELECT * FROM users WHERE email=?', t)

	row = stored_password=c.fetchone()
	conn.close();

	if row != None: 
	  stored_password=row[1]
	  if (stored_password==passwd):
		 return "passed"
	return "failed"

def main():
	form = cgi.FieldStorage()
	if "action" in form:
		action = form["action"].value
		if action == "change":
			if "username" in form and "password" in form:
				username = form["username"].value
				oldpass  = hashlib.md5(form['oldpassword'].value).hexdigest()
				password = hashlib.md5(form["password"].value).hexdigest()
				changePassword(username,oldpass,password)
			else:
				change_password()
		else:
			change_password()
	else:
		change_password()
		

main()
					
					
