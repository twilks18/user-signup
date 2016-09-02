
#
import webapp2
import re
import cgi

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
psswrd_re= re.compile(r"^.{3,20}$")
email_re= re.compile(r"^[\S]+@[\S]+.[\S]+$")

def escape_symbols(s):
    return cgi.escape(s, quotes = True)

def valid_username(username):
     return username and user_re.match(username)

def valid_passwrd(password):
    return password and  psswrd_re.match(password)

def valid_email(email):
    return not email or email_re.match(email)


page_header = """
<!DOCTYPE html>
<html>
    <head>
    <title>Signup</title>
    </head>
<body>
    <h1>Signup</h1>
"""


page_footer = """
</body>
</html>
"""
sign_up="""
    <form action='/' method="post">
        <label>
            Username
            <input type="text" name="username" value="%(username)s"/> %(user_error)s
          </label>

        </label>
        <br>
        <br>
        <label>
            Password
            <input type="password" name="password"/> %(psswrd)s
        </label>
        <br>
        <br>
        <label>
            Verify
            <input type="password" name="verify"/> %(verify)s
        </label>
        <br>
        <br>
        <label>
            Email (optional)
            <input type="text" name="email" value="%(email)s"/> %(email_error)s
        <br>
        <br>
        <input type="submit" value="Submit"/>

    </form>
    """
page_content = page_header + sign_up + page_footer



class MainHandler(webapp2.RequestHandler):


    def write_form(self,user_error="", username="", psswrd="", verify="", email="", email_error=""):
        self.response.write(page_content %{'username':username,'user_error':user_error,'email':email,'email_error':email_error,'psswrd':psswrd,'verify':verify })



    def get(self):
        self.write_form()

    def post(self):




        userName = self.request.get('username')
        passWord = self.request.get('password')
        eMail = self.request.get('email')
        veriFy = self.request.get('verify')

        username_1 = valid_username(userName)
        password_1 = valid_passwrd(passWord)
        email_1 = valid_email(eMail)

        if not username_1 or (userName == ""):

            self.write_form("Invalid Username",userName)




        elif not password_1:
            self.write_form("",userName,"Invalid  Password")



        elif not (passWord == veriFy):
            self.write_form("",userName,"","Passwords Do Not Match")

        elif username_1 and password_1 and veriFy:
            self.redirect('/thanks?username=%s' % userName)




        elif not email_1 or (eMail == ""):

            self.write_form("",userName,"","",eMail,"Invalid Email")



        else:
            self.redirect('/thanks?username=%s' % userName)


class thanksHandler(webapp2.RequestHandler):
    def get(self):

        welcome_user= self.request.get('username')
        welcome = "Welcome " + welcome_user + "!"
        self.response.write(welcome)





app = webapp2.WSGIApplication([
    ('/', MainHandler),('/thanks', thanksHandler)
], debug=True)
