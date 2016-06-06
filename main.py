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

      </table>


			<br>
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

import webapp2

def escape_html(s):
  s=s.replace("&","&amp;")
  s=s.replace(">","&gt;")
  s=s.replace("<","&lt;")
  s=s.replace('"',"&quot;")
  return s;

def name_checker(s):
  if (len(s)==0):
    return False
  for i in range(len(s)):
    if (s[i] .isalpha() ==False):
      return False
  return True    

def pass_checker(s):
  if (len(s)==0):
    return False
  for i in range(len(s)):
    if (s[i] .isalpha() ==False and (s[i]<'0' or s[i]>'9') ):
      return False
  return True


def print_form(self,name,name_error,pass_error,verify_error):
   self.response.write(form%{"name":escape_html(name),"name_error":name_error,"pass_error":pass_error,"verify_error":verify_error } )  

class MainHandler(webapp2.RequestHandler):
  def get(self):
    print_form(self,"","","","")
  def post(self):
    name=self.request.get("name")
    password=self.request.get("password")
    verify=self.request.get("verify")

    name_error="";
    pass_error="";
    verify_error="";

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
    if (ok==False):
      print_form(self,name,name_error,pass_error,verify_error);
    else:
      self.redirect('/welcome?username='+name)


class welcome(webapp2.RequestHandler):
  def get(self):
    name= self.request.get('username')
    self.response.write(welcomepage%{"name":name})


app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome', welcome)
], debug=True)
