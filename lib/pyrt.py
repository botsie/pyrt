#!/usr/bin/env python

import urllib
import urllib2
import email
import re

import pprint

class RT_Server:
    """Abstract an RT Server"""

    def __init__(self):
        self.server = "sysrt.ops.directi.com"
        self.port = 443
        self.user ='biju.ch'
        self.password = 'Achjarcod3!'
        self.use_ssl = True

        
    def login(self):
        login_form_values = {
            'user' : self.user,
            'pass' : self.password
            }
        login_form_data = urllib.urlencode(login_form_values)

        request = urllib2.Request("https://" + self.server, login_form_data)
        response = urllib2.urlopen(request)
        headers = response.info()
        self.cookie = headers['set-cookie'].split(';')[0]

    def get(self, url):
        request = urllib2.Request("https://" + self.server + "/REST/1.0" + url)
        request.add_header('Cookie', self.cookie)
        print request.get_full_url()
        response = urllib2.urlopen(request)
        return response.read()

    def ticket(self, id):
        url = "/ticket/" + str(id) + "/show" 
        return RT_Document(self.get(url))
        
    def tickets_where(self, condition):
        url = "/search/ticket?query=" + urllib.quote(condition) + "&format=l"
        ticket_strings = self.get(url).split('--')

        tickets = list()
        for ticket_string in ticket_strings: 
            tickets.append(RT_Document(ticket_string))

        return tickets



class RT_Document(dict):
    """Model a Record Returned by RT"""
    
    def __str__(self):
        return str(self.db)

    def __init__(self, data):
        self.raw = data
        self.db = self.parse(data)
        for key in self.db.keys():
            self[key] = self.db[key]
        
        
    def parse(self, data_string):
        data_string = re.sub('RT\/\d+\.\d+\.\d+\s\d{3}\s.*\n\n',"", data_string) # toss the HTTP response
        data_string = re.sub('\n\n',"\n", data_string) # remove double spacing
        data_string = re.sub('^\n',"", data_string) # spec doesn't allow messages to start with a newline

        data = email.message_from_string(data_string)
        
        return data
        

class RT_DocumentCollection:
    pass

if __name__ == "__main__":
    s = RT_Server()
    s.login()
    s.ticket(845829)
    
