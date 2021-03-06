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
import webapp2
import cgi

form = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color:red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""
rot13_form = """
<form method="post">
    <h1>Enter some text to ROT13:</h1>
    <br>
        <input size="50" height="50" type="text" name="text" value="%(txt)s">
    <br>
    <input type="submit">
</form>
"""
signup_form= """
<form method="post">
    <h1>Please Enter your information</h1>
    <br>
        Username
        <input size="25" height="50" type="text" name="username" value="%(txt)s">
    <br>
    <br>
        Password
        <input size="25" height="50" type="text" name="password" value="%(txt)s">
    <br>
    <br>
        Verify password
        <input size="25" height="50" type="text" name="verify" value="%(txt)s">
    <br>
    <br>
        Email
        <input size="25" height="50" type="text" name="email" value="%(txt)s">
    <br>
    <input type="submit">
</form>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <=31:
            return day

def valid_year(year):
    if year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year

def escape_html(s):
    return cgi.escape(s, quote=True)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error":error,
                                    "month":escape_html(month),
                                    "day":escape_html(day),
                                    "year":escape_html(year)})
        
    def get(self):
        self.write_form()
        
    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)
        
        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend.",
                        user_month, user_day, user_year)
        else:
            self.redirect("/thanks")
     
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")
        
class Rot13(webapp2.RequestHandler):
    def write_form(self, txt=""):
        self.response.out.write(rot13_form % {"txt":txt})

    def rot13(self, text):
        asciiupper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        asciilower = 'abcdefghijklmnopqrstuvwxyz'
        new_str = []
        for c in text:
            ordc = ord(c)
            new_char = ordc + 13
            if c in asciiupper:
                if new_char > 90:
                    new_char = new_char - 90 + 64
                new_str.append(chr(new_char))
            elif c in asciilower:
                if new_char > 122:
                    new_char = new_char - 122 + 96
                new_str.append(chr(new_char))
            else:
                new_str.append(c)
        return "".join(new_str)

    def get(self):
        self.write_form()
    
    def post(self):
        txt = self.request.get('text')
        self.write_form(self.rot13(txt))

class Signup(webapp2.RequestHandler):
    def write_form(self, txt=""):
        self.response.out.write(signup_form % {"txt":txt})

    def get(self):
        self.write_form()

    def post(self):
        txt = self.request.get('username')
        self.write_form(self.signup(txt))

app = webapp2.WSGIApplication([('/', MainHandler), ('/thanks', ThanksHandler), ('/unit2/rot13', Rot13), ('/unit2/signup', Signup)], debug=True)
                              
