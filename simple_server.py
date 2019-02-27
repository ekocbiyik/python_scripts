#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

__author__ = 'ekocbiyik'

PORT_NUMBER = 6161


class simpleServer(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200, message='POST request OK')

    def do_PUT(self):
        self.send_response(200, message='PUT request OK')

    def do_GET(self):
        self.send_response(200, message='GET request OK')


try:
    server = HTTPServer(('', PORT_NUMBER), simpleServer)
    print 'simple server started on port ', PORT_NUMBER
    server.serve_forever()

except KeyboardInterrupt:
    print 'shutting down the simple server'
    server.socket.close()
