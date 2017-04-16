#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

form="""
<!DOCTYPE html>
<head>
  <title> Sign Up </title>
  <style type="text/css">
    .label {text-align: right}
  </style>

</head>

<html>
  <h2>Signup</h2>
	<div>
		<form method="post">
      <table>
        <tr>
          <td class="label">
            Full Name:
          </td>
          <td>
            <input type="text" name="name" value="%(name)s"> 
          </td>
        </tr>

        <tr>
          <td class="label">
            Username:
          </td>
          <td>
            <input type="text" name="username" value="%(username)s"> 
          </td>
          <td>
            <b>
            <p style="color:red">%(username_error)s</p>
          <td>
        </tr>

        <tr>
          <td class="label">
            Password:
          </td>
          <td>
            <input type="password" name="password" value=""> 
          </td>
          <td>
            <b>
            <p style="color:red">%(pass_error)s</p>
          <td>
        </tr>

        <tr>
          <td class="label">
            Verify Password:
          </td>
          <td>
            <input type="password" name="verify" value=""> 
          </td>
          <td>
            <b>
            <p style="color:red">%(verify_error)s</p>
          <td>
        </tr>

        <tr>
          <td class="label">
            Email(Optional):
          </td>
          <td>
            <input type="text" name="email" value="%(email)s"> 
          </td>
          <td>
            <b>
            <p style="color:red">%(email_error)s</p>
          <td>
        </tr>


      </table>

			<br>
			<input type="submit" name="submit"> 

		</form>
	</div>
</html>
"""

welcomepage="""
<!DOCTYPE html>
<head> 

  <title> Welcome </title>
  <style type="text/css">
    .label {text-align: right}
  </style>


</head>

<html>

  <h1>Welcome, %(username)s!</h1>
  <table>
    <tr>
        <td class="label">
            Full Name:
        </td>
        <td>
            %(name)s
        </td>
    </tr>


    <tr>
        <td class="label">
            Email:
        </td>
        <td>
            %(email)s
        </td>
    </tr>

  </table>

</html>
"""

user_list = list()
maps = dict()
ID = 0



import re
import webapp2

def escape_html(s):
    s=s.replace("&","&amp;")
    s=s.replace(">","&gt;")
    s=s.replace("<","&lt;")
    s=s.replace('"',"&quot;")
    return s;


#minimum username length 3 and maximum username length 20
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def name_checker(username):
    return username and USER_RE.match(username)

#minimum pass length 3 and maximum pass length 20
PASS_RE = re.compile(r"^.{3,20}$")
def pass_checker(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def email_checker(email):
    return not email or EMAIL_RE.match(email)
 

def print_form(self,name,username,username_error,pass_error,verify_error,email,email_error):
    self.response.write(form%{"name":name,"username":escape_html(username),"username_error":username_error,"pass_error":pass_error,"verify_error":verify_error,"email":escape_html(email),"email_error":email_error } )  


def find_info(username):
    for i in user_list:
        if i[0]==username:
            return i

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print_form(self,"","","","","","","")
    def post(self):
        global ID,maps 

        name=self.request.get("name")
        username=self.request.get("username")
        password=self.request.get("password")
        verify=self.request.get("verify")
        email=self.request.get("email");

        username_error="";
        pass_error="";
        verify_error="";
        email_error="";

        ok=True;    


        if(name_checker(username) ==False):
            ok=False;
            username_error="That's not a valid username.";

        if not(pass_checker(password)):
            ok=False;
            pass_error="That's not a valid password.";
        elif(password!=verify):
            ok=False;
            verify_error="password dose not match.";
        if not(email_checker(email) ):
            ok=False;
            email_error="That's not a valid mail address"
        if len(email)==0:
            email= "Not available"

        if (ok==False):
            print_form(self,name,username,username_error,pass_error,verify_error,email,email_error);
        else:
            ID+=1
            maps[username] = ID
            user_list.append( [username,ID,name,password,email] )
            self.redirect('/welcome?username='+username)


class welcome(webapp2.RequestHandler):
  def get(self):
        username= self.request.get('username')        
        info = find_info(username)
        self.response.write(welcomepage%{"username":info[0],"name":info[2],"email":info[4] } )

class signin(webapp2.RequestHandler):
    def get(self):
        pass

#<a href="islam.html">Islam</a> and <a href="buddha.html">Buddhism</a>.

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', welcome),('/signin',signin)
], debug=True)
