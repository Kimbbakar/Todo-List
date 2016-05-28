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
	<div>
		<form method="post">
      <table>
        <tr>
          <td>
            <p>Username:</p>
          </td>
          <td>
            <input type="text" name="name" value="%(name)s"> 
          </td>
          <td>
            <b>
            <p style="color:red">%(name_error)s</p>
          <td>
        </tr>

      </table>


			<br>
			<br>
			<input type="submit" name="submit">
		</form>
	</div>
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


def print_form(self,name,name_error):
   self.response.write(form%{"name":escape_html(name),"name_error":name_error } )  

class MainHandler(webapp2.RequestHandler):
  def get(self):
    print_form(self,"","")
  def post(self):
    name=self.request.get("name")
    if(name_checker(name) ==False):
      print_form(self,name,"That's not a valid username.")
    else:
      self.response.write(name)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
