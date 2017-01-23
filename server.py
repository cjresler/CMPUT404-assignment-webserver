#  coding: utf-8 
import SocketServer

import os.path

import time

import mimetypes

# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Connor Resler, Ryan Satyabrata
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
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    requestHeader = []
    responseHeader = ""
    body = ""

    def handleFile(self, path):
        #Open file, excluding leading '/'
        f = open(path[1:], 'r')
        
        #The extenstion that will tell the file type will be in the portion
        #of the URI following the last '/'
        temp = path.split('/')
        #https://docs.python.org/2/library/mimetypes.html
        ctype = mimetypes.guess_type(temp[-1])
        
        self.responseHeader += "HTTP/1.1 200 OK\r\n"
        self.responseHeader += "Content-Type: " + ctype[0] + "\r\n"
        
        #Code adapted from github user cournape from 
        #https://github.com/enthought/Python-2.7.3/blob/master/Lib/SimpleHTTPServer.py
        #Get length of content
        fs = os.fstat(f.fileno())
        self.responseHeader += "Content-Length: " + str(fs[6]) + "\r\n"
        self.body = f.read()

    #Some code here was written by Ryan Satyabrata under Apache-2.0 License
    #Taken from https://github.com/kobitoko/CMPUT404-assignment-webserver/blob/master/server.py#L45 on January 21, 2017
    def findPath(self, headerList):
        path = "/www/"

        if(len(headerList) > 1):
            path += headerList[1]

        #https://docs.python.org/2/library/os.path.html
        #Get path
        path = os.path.abspath(path)

        #Check if current path is a directory and add '/index.html'
        if(os.path.isdir(os.curdir + path)):
            path += "/index.html"

        #Check if current path is a file and handle it
        if(os.path.isfile(os.curdir + path)):
            self.handleFile(path)

        #Handle file not found. These lines were written by Ryan Satyabrata
        #Under Apache-2.0 License, taken from https://github.com/kobitoko/CMPUT404-assignment-webserver/blob/master/server.py#L45 on January 21, 2017
        else:
            self.responseHeader += "HTTP/1.1 404 NOT FOUND\r\n"
            self.responseHeader += "Content-Type: text/html;\r\n"
            self.body = "<html><head></head><body><h1>404 NOT FOUND</h1></body></html>"

    def handle(self):
        self.data = self.request.recv(1024).strip()
        requestHeader = self.data.split()

        if(requestHeader[0].upper() == "GET"):
            self.findPath(requestHeader)
        else:
            self.responseHeader += "HTTP/1.1 405 Method Not Allowed\r\n"

        #https://docs.python.org/2/library/time.html#module-time
        #Get current time and format it
        currentTime = time.localtime()
        currentTime = time.strftime("Date: %d %b %Y %H:%M:%S\r\n", currentTime)
        self.responseHeader += currentTime;
        #Send header and body
        self.request.sendall(self.responseHeader + "\r\n" + self.body)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()


