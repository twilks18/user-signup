
import webapp2
import re
import cgi

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
psswrd_re= re.compile(r"^.{3,20}$")
email_re= re.compile(r'^[/S]+@[\S]+.[\s]+$')

def escape_symbols(s):
    return cgi.escape(s, quotes = True)

def valid_username(username):
     return user_re.match(username)

def valid_passwrd(password):
    return psswrd_re.match(password)

def valid_email(email):
     return email or email_re.match(email)


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
            <input type="text" name="username" value="%(username)s"/>
            <div>%(error_username)s</div>
        </label>
        <br>
        <br>
        <label>
            Password
            <input type="password" name="password"/>
            <div>%(error_password)s</div>
        </label>
        <br>
        <br>
        <label>
            Verify
            <input type="password" name="verify"/>
            <div>%(error_verify)s</div>error_verify
        </label>
        <br>
        <br>
        <label>
            Email (optional)
            <input type="text" name="email" value="%(email)s"/>
            <div>%(error_email)s</div>
        </label>
        <br>
        <br>
        <input type="submit" value="Submit"/>

    </form>
    """
page_content = page_header + sign_up + page_footer


class MainHandler(webapp2.RequestHandler):
    def write_form(self, errors=None, username="", email=""):
        if errors is None:
            errors = {}
        env = {
            "username":username,
            "email":email,
            error_username: '', error_password: '', error_verify: '', error_email: ''
            }
        env.update(errors)
        self.response.write(page_content % env)

    def get(self):

        self.write_form()

    def post(self):
        errors={}
        userName = self.request.get('username')
        passWord = self.request.get('password')
        eMail = self.request.get('email')
        veriFy = self.request.get('verify')

        username_1 = valid_username(userName)
        password_1 = valid_passwrd(passWord)
        email_1 = valid_email(eMail)

        if not username_1:
            errors["error_username"]="invalid username"

        if not password_1:
            errors["error_password"]="invalid password"

        if not (passWord == veriFy):
            errors["error_verify"]="Passwords do not match"


        if not (email_1):
            errors["error_email"]="invalid email"


        if not(username_1 and password_1 and (passWord == veriFy)):
            self.write_form(errors, userName, eMail)
        else:
            self.response.write("That's Great")


class thanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("thanks")










app = webapp2.WSGIApplication([
    ('/', MainHandler),('/thanks',thanksHandler)
], debug=True)
