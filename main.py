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
        <td>
          <p>Username:</p>
        </td>
        <td>
          <input type="text" name="name" value="%(name)s"> 
        </td>

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


def print_form(self,name):
   self.response.write(form%{"name":escape_html(name) } )  

class MainHandler(webapp2.RequestHandler):
  def get(self):
    print_form(self,"")
  def post(self):
    name=self.request.get("name")
    print_form(self,name)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
