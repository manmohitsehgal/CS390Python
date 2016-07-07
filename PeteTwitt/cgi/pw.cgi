#!/usr/bin/python

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
<HTML>
<HEAD>
<TITLE>Change Password</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>Change Password</H2></center>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Enter Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Enter Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="change">
<INPUT TYPE=submit VALUE="Submit">

</FORM>
</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)

def changePassword(email,password):

	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	user = (username, password)	
	c.execute('SELECT email,password FROM users WHERE email=(?) and password=(?)',user)
	row = c.fetchone()
	
	if row != None:
		userEmail = row[0] 
		userPassword = row[1]
		if userPassword == password:
			c.execute('UPDATE users SET password=(?) WHERE email=(?)',password,email) 
		else:
			print("Password Invalid")
	else:
		print("something went wrong")
		
	conn.commit()	
	conn.close();
	
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
				password = form["password"].value
				changePassword(username,password)
			else:
				print("ddn work")
		else:
			print("something went wrong")
	else:
		print("fucked up shit")

main()
					
					
