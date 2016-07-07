#!/usr/bin/python

# Import the CGI, string, sys modules
import cgi, string, sys, os, re, random
import hashlib # hash passwords
import cgitb; cgitb.enable()  # for troubleshooting
import sqlite3
import session

#Get Databasedir
MYLOGIN="msehgal"
DATABASE="/homes/"+MYLOGIN+"/PeteTwitt/Twitter.db"
IMAGEPATH="/homes/"+MYLOGIN+"/PeteTwitt/images"

##############################################################
# Define function to generate login HTML form.
def login_form():
	html="""
<HTML>
<HEAD>
<TITLE>Pwitter</TITLE>
</HEAD>

<BODY BGCOLOR = "#CFB53B">
<br>
<br>
<br>
<center><b><font size="25" face ="Lato">P-TWITTER</b></font></center>
<br>
<br>
<br>
<br>
<br>
<center>
<TABLE BORDER = 0>
<FORM METHOD=post ACTION="login.cgi">
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<INPUT TYPE=hidden NAME="action" VALUE="login">
<INPUT TYPE=submit VALUE="Enter" size="10" style="height:30px; width:150px">
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="login.cgi?action=register"><font color="black">Create Account Here !</font></a>
</center>
<SCRIPT type="text/javascript">
    window.history.backward();
    function noBack() { window.history.backward(); }
</SCRIPT>
</FORM>
</BODY>
</HTML>
"""
	print_html_content_type()
	print(html)




##############################################################			REGISTER
def register_form():
    html="""
<HTML>
<HEAD>
<TITLE>Registration Form</TITLE>
<HEAD>
<br>
<br>
<br>
<center><H1> Register User Here </H1></center>
<br>
<br>
<center>
<BODY BGCOLOR = "#CFB53B"   >
<FORM METHOD=post ACTION="login.cgi">
<TABLE>
<TR><TH>Username:</TH><TD><INPUT TYPE=text NAME="username"></TD><TR><br>
<TR><TH>Password:</TH><TD><INPUT TYPE=password NAME="password"></TD></TR>
</TABLE>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<INPUT TYPE=hidden NAME="action" VALUE="registered" style="height:30px; width:150px">
<INPUT TYPE=submit VALUE="Register" size="10" style="height:30px; width:150px">
<br>

<br>
<br>

</FORM>
</BODY>
</HTML>
"""

    print_html_content_type()
    print(html)
    
    
##############################################################			TWITTER STARTS HERE
def twitter_form(user,session):
	html="""
	<HTML>
	<HEAD>
	<TITLE>P-TWITTER</TITLE>
	<HEAD>

	<BODY BGCOLOR = "#CFB53B">

	<center><h1>P-Twitter Welcomes You</h1></center>
	<a href="login.cgi?action=showOptions&username={user}&session={session}">Go to Options</a>
	<br>
    <center>
	<textarea rows="4" cols="50" name="twitter" form="twitter" required >
	</textarea>
	<FORM METHOD=post ACTION="login.cgi" id="twitter">
	<INPUT TYPE=hidden NAME="action" VALUE="tweeted">
	<input type="hidden" name="username" value="{user}">
	<input type="hidden" name="session" value="{session}">
    <br>
	<INPUT TYPE="submit" VALUE="Tweet" size=10 style="height:30px width:150px">
	</FORM>
    <TABLE BORDER = 1>
    
	"""
	html+= displayTweets(user)+"""
	
    </TABLE>
    </center>
    </BODY>
	</HTML>
	"""
	
	print_html_content_type()
	print(html.format(user=user,session=session))
	
	
def show_users(user,session): ############################ SHOW USERS
	html="""
	<HTML>
	<HEAD>
	<TITLE>Users</TITLE>
	<HEAD>

	<BODY BGCOLOR = "#CFB53B">
    	<br>
	<center><h1>Subscription Center</h1>
    	<br>
    	<br>
	<a href="login.cgi?action=showOptions&username={user}&session={session}">Go to Options</a>
	<br>
    	<br>
    	<br>
	<input type="hidden" name="username" value="{user}">
	<input type="hidden" name="session" value="{session}">
	<TABLE BORDER =1 width="40%">
	<TR>
	<TH>
	<font face ="Lato">
	"""
	html+=getAllUsers(user)+"""
	</font>
	</TH>
	</TR>
	</TABLE>
    	</center>
	</FORM>
	</BODY>
	</HTML>
	"""
	
	print_html_content_type()
	print(html.format(user=user,session=session))
    
    
# Define function to test the password.
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




	
#Register New user
def registerNewUser(username,password):
	#Check for valid email
	if not re.match(r"[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]+", username):
		login_form()
		print "<H1>Bad email!</H1>"
		return
		
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	c.execute('SELECT email FROM users WHERE email LIKE ?', (username,))
	if c.fetchone():
		login_form()
		print "<H1>Email already in use!</H1>"
		return
	
	user = (username, password, username+',')
	
	c.execute('INSERT INTO users(email,password, subscriptions) VALUES(?,?,?)',user)
	
	conn.commit()
	conn.close()
	
	login_form()
	print '<center><H3>Log in now!!!</H1></center>'

##########################################################
# Diplay the options of admin
def display_admin_options(user, session):
	html="""
		<HTML>
		<HEAD>
		</HEAD>
		<BODY id ="tweeter" BGCOLOR = "#CFB53B">
		<H1> <center> P-TWITTER </center></H1>
        <br>
	    <center>	
		 &nbsp;&nbsp;&nbsp;&nbsp;<a href="login.cgi?action=upload&username={user}&session={session}">Change Avatar</a>
		 &nbsp;&nbsp;&nbsp;&nbsp;<a href="login.cgi?action=show_image&username={user}&session={session}">Show Current Avatar</a>
		 &nbsp;&nbsp;&nbsp;<a href="passwordchange.cgi?action=change_password&username={user}&session={session}">Change Password</a>
		 &nbsp;&nbsp;&nbsp;<a href="login.cgi?action=showUsers&username={user}&session={session}">Show Users</a>
		 &nbsp;&nbsp;&nbsp;<a href="login.cgi?action=logout&username={user}&session={session}">Logout</a>

         <br>
         <br>
         <br>
        <textarea rows="4" cols="50" name="twitter" form="twitter" required >
		</textarea>
		<FORM METHOD=post ACTION="login.cgi" id="twitter">
		<INPUT TYPE=hidden NAME="action" VALUE="tweeted">
		
		<INPUT TYPE="submit" VALUE="Tweet" size=10 style="height:30px width:150px">
        
        <input type="hidden" name="username" value="{user}">
		<input type="hidden" name="session" value="{session}">
		
        <br>
        <br>
		"""
        html+=displayTweets(user)+"""
        </center>
        </BODY>
        </HTML>"""
        
        reloadscript = """<html>
		<script language="JavaScript" type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
		<script type="text/javascript">
		    setInterval(function() {
		        $("#tweeter").load("login.cgi?action=showOptions&user="""+user+"""&session="""+session+""" #tweeter");
		    }, 5000);
		</script></html>
		"""
	print_html_content_type()
	print(html.format(user=user,session=session))

	

#################################################################
def create_new_session(user):
	return session.create_session(user)

##############################################################

	
def new_album(form):

	html="""
		<H1> New Album</H1>
		"""
	print_html_content_type()
	print(html);

##############################################################
def show_image(form):

	# Your code should get the user album and picture and verify that the image belongs to this
	# user and this album before loading it

	username=form["username"].value
	image = getImage(username)
	print_html_content_type()
	print '<H1>This is your current avatar:</H1>'
	print('<img src="'+image+'" style=\'max-height: 140px; max-width: 140px\'>')
	

###############################################################################

def upload(form):
	html="""
		<HTML>
		<br>
		<br>
		<H1> Upload Avatar <H1>
		<br>
		<br>
		<center>
		<BODY BGCOLOR = "#CFB53B">
		<FORM ACTION="login.cgi" METHOD="POST" enctype="multipart/form-data">
			<input type="hidden" name="username" value="{user}">
			<input type="hidden" name="session" value="{session}">
			<input type="hidden" name="action" value="upload-pic-data">
			<BR><I>Browse Picture:</I> <INPUT TYPE="FILE" NAME="file">
			<br>
			<input type="submit" value="Press"> to upload the picture!
			</form>
		</center>
		</BODY>
		</HTML>
	"""

	user=form["username"].value
	s=form["session"].value
	print_html_content_type()
	print(html.format(user=user,session=s))

#######################################################

def upload_pic_data(form):

	#Get file info
	fileInfo = form['file']

	#Get user
	user=form["username"].value
	s=form["session"].value

	# Check if the file was uploaded
	if fileInfo.filename:
		# Remove directory path to extract name only
		fileName = os.path.basename(fileInfo.filename)
		if not os.path.exists('images/'+user):
   			os.makedirs('images/'+user)
		open('images/'+user+'/'+fileName, 'wb').write(fileInfo.file.read())
		addImageToDB(user, 'images/'+user+'/'+fileName)
			
		display_admin_options(user,s)
		print ('<br><br><H2>The picture ' + fileName + ' was uploaded successfully</H2>')
		print('<img src="images/'+user+'/'+fileName+'" style=\'max-height: 140px; max-width: 140px\'>')
	else:
		display_admin_options(user,s)
		print '<h1>Error uploading</h1>'

def print_html_content_type():
	# Required header that tells the browser how to render the HTML.
	print("Content-Type: text/html\n\n")

##############################################################
def addImageToDB(user, filename):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	user = (filename, user)
	c.execute('Update users set image = ? where email LIKE ?', user)
	conn.commit()
	conn.close()

############################################################## ADD TWEETS HERE !!!

def addTweets(username,tweetDescp):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	user = (username, tweetDescp)
	
	c.execute('INSERT INTO tweets(username,tweet)VALUES(?,?)',user)
	
	conn.commit()
	conn.close()
	
	

############################################################## REPLY TO TWEET

def replyToTweet(toReplyUser, tweetDescp):
	
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	replyTo = toReplyUser
	c.execute('SELECT email FROM users WHERE email LIKE ?',(replyTo,))
	
	user = (replyTo, tweetDescp)

	c.execute('INSERT INTO tweets(username,tweet)VALUES(?,?)',replyTo)
	
	html+="@"+toReplyUser
	
	conn.commit()
	conn.close()
	
	return html
	
	
############################################################## DISPLAY TWEETS HERE !!!

def displayTweets(currentUser):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	c.execute('SELECT subscriptions FROM users WHERE email LIKE ?',(currentUser,))
	subs = c.fetchone()[0]
	c.execute('SELECT * FROM tweets ORDER BY timestamp DESC')
	tweets = c.fetchall()
	
	html="<div id='tweets'>"
	for tweet in tweets:
		if tweet[0] in subs:
			image = getImage(tweet[0])
			html+="<TABLE BORDER =2 WIDTH=80%><TR><TH height=50%><img src=\'"+image+"\' style=\'max-height: 140px; max-width: 140px\'></TH><TH><h2>"+tweet[1]+"</h2><h5>"+tweet[0]+" "+tweet[2]+"</h5></TH></TR></TABLE><br>"
	html += '</div>'
	conn.close()
	return html

def deleteUser(currentUser):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	c.execute('SELECT email FROM users WHERE email LIKE ?',(currentUser,))
	subs = c.fetchone()[0]
	
		
	html=""
	for tweet in tweets:
		if tweet[0] in subs:
			image = getImage(tweet[0])
			html+="<TABLE BORDER =1 WIDTH=80%><TR><TH><img src=\'"+image+"\' style=\'max-height: 140px; max-width: 140px\'></TH><TH><h2>"+tweet[1]+"</h2><h5>"+tweet[0]+" "+tweet[2]+"</h5></TH></TR></TABLE><br>"
	conn.close()
	return html
	
	

##############################################################
def getImage(user):
	try:
		conn = sqlite3.connect(DATABASE)
		c = conn.cursor()
	
		user = (user,)
	
		c.execute('SELECT image from users where email like ?',user)
		result = c.fetchone()[0]
		conn.close()
		if result is None:
			return 'images/grr.gif'
		return result
	except:
		return 'images/grr.gif'
	
############################################################## SUBSCRIBE TWEETS HERE !!!

def getAllUsers(currentUser):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	c.execute('SELECT * FROM users')
	
	users = c.fetchall()
	
	html=""
	for user in users:
		if user[0] != currentUser:
			html+="""<a href="login.cgi?action=subscribeToUsers&username={user}&session={session}&subto="""+user[0]+'">'+user[0]+"""</a><br>"""
			
	conn.close()
	
	return html

############################################################## GET SPECIFIED EMAIL



############################################################## SUBSCRIBE TWEETS HERE !!!

def insertToSubs(username,subto):
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	
	c.execute('SELECT subscriptions FROM users WHERE email LIKE ?',(username,))
	
	row = c.fetchone()
	subList = row[0]
	
	subList = subList + subto+ ","
	
	c.execute('UPDATE users SET subscriptions = ? WHERE email LIKE ?',(subList, username))
	
	conn.commit()
	conn.close()

##############################################################


# Define main function.
def main():
	form = cgi.FieldStorage()			
	if "action" in form:
		action=form["action"].value
		if action == 'show':
			username=cgi.escape(form["username"].value)
			password=hashlib.md5(form["password"].value).hexdigest()
			display_admin_options(username, session)
		if action == 'registered':
			username=cgi.escape(form["username"].value)
			password=hashlib.md5(form["password"].value).hexdigest()
			registerNewUser(username,password)
		elif action == "login":
			if "username" in form and "password" in form:
				username=form["username"].value
				password=hashlib.md5(form["password"].value).hexdigest()
				if check_password(username, password)=="passed":
					session=create_new_session(username)
					display_admin_options(username, session)
				else:
					login_form()
					print("<center><H3><font color=\"red\">Incorrect user/password</font></H3></center>")
		elif (action == "new-album"):
			new_album(form)
		elif (action == "showOptions"):
			session = form["session"].value
			username= form["username"].value
			display_admin_options(username, session)
		elif (action == "tweeted"):
			if "username" in form and "twitter" in form:
				session = form["session"].value
				username=form["username"].value
				tweetDescp = form["twitter"].value
				addTweets(username,tweetDescp)
				display_admin_options(username,session)
			else:
				session = form["session"].value
				username= form["username"].value
				display_admin_options(username, session)
		elif (action == "showTwitterForm"):
			session = form["session"].value
			username= form["username"].value
			display_admin_options(username,session)
		elif (action == "register"):
			register_form()
		elif (action == "upload"):
			upload(form)
		elif (action == "show_image"):
			show_image(form)
			
		elif (action == "subscribeToUsers"):
			subto = form["subto"].value
			session = form["session"].value
			username= form["username"].value
			insertToSubs(username,subto)
			display_admin_options(username,session)
		elif action == "upload-pic-data":
			upload_pic_data(form)
		elif (action == "showUsers"):
			session = form["session"].value
			username= form["username"].value
			show_users(username,session)
		elif (action == "logout"):
			login_form()
		else:
			session = form["session"].value
			username= form["username"].value
			session = session.close()
			login_form()
	else:
		login_form()
		

###############################################################
# Call main function.
main()
