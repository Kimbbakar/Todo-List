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
            Username:
          </td>
          <td>
            <input type="text" name="name" value="%(name)s"> 
          </td>
          <td>
            <b>
            <p style="color:red">%(name_error)s</p>
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
            Email:
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
</head>

<html>

  <h1>Welcome, %(name)s!</h1>

</html>
"""

import re
import webapp2

def escape_html(s):
  s=s.replace("&","&amp;")
  s=s.replace(">","&gt;")
  s=s.replace("<","&lt;")
  s=s.replace('"',"&quot;")
  return s;

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def name_checker(username):
  return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def pass_checker(password):
  return len(password)>0 and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def email_checker(email):
  return len(email)==0 or EMAIL_RE.match(email)!=None
 

def print_form(self,name,name_error,pass_error,verify_error,email,email_error):
   self.response.write(form%{"name":escape_html(name),"name_error":name_error,"pass_error":pass_error,"verify_error":verify_error,"email":escape_html(email),"email_error":email_error } )  

class MainHandler(webapp2.RequestHandler):
  def get(self):
    print_form(self,"","","","","","")
  def post(self):
    name=self.request.get("name")
    password=self.request.get("password")
    verify=self.request.get("verify")
    email=self.request.get("email");

    name_error="";
    pass_error="";
    verify_error="";
    email_error="";

    ok=True;    


    if(name_checker(name) ==False):
      ok=False;
      name_error="That's not a valid username.";

    if(pass_checker(password)==False ):
      ok=False;
      pass_error="That's not a valid password.";
    elif(password!=verify):
      ok=False;
      verify_error="password dose not match.";
    if(email_checker(email)==False ):
      ok=False;
      email_error="That's not a valid mail address"

    if (ok==False):
      print_form(self,name,name_error,pass_error,verify_error,email,email_error);
    else:
      self.redirect('/welcome?username='+name)


class welcome(webapp2.RequestHandler):
  def get(self):
    name= self.request.get('username')
    self.response.write(welcomepage%{"name":name})


app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', welcome)
], debug=True)
