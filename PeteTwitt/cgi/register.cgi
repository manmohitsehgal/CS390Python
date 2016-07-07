#!/usr/bin/python
#-*- coding: UTF-8 -*-

print "Content-type: text/plain;charset=utf-8"

import cgi, string, sys, os, re, random
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3


#Get Databasedir
MYLOGIN="msehgal"
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/Twitter.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"

##############################################################
# Define function to generate login HTML form.
def registerForm():
    html="""
<HTML>
<HEAD>
<TITLE>Registration Form</TITLE>
</HEAD>

<BODY BGCOLOR = white>

<center><H2>PictureShare User Administration</H2></center>

<H3>Registration</H3>

<TABLE BORDER = 0>
<FORM METHOD=post ACTION="register.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

<INPUT TYPE=hidden NAME="action" VALUE="Register">
<INPUT TYPE=submit VALUE="Enter">
</FORM>
</BODY>
</HTML>
"""
    #print_html_content_type()
    print(html)
    
###################################################################
# Define function to test the password.
def registerUser(uname, passwrd):

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    t = (user,)
    if (c.execute('INSERT INTO users VALUES',t)):
        return "passed"
    else:
        return "failed"

    conn.commit()       
    conn.close();

##########################################################

# Define main function.
def main():
    form = cgi.FieldStorage()
    if "action" in form:
        action=form["action"].value
        #print("action=",action)
        if action == "register":
            if "username" in form and "password" in form:
                username=form["username"].value
                password=form["password"].value
                registerUser(username,password)
            else:
                registerForm()
        else:
            registerForm()
    else:
        registerForm()

###############################################################
# Call main function.
main()
