#!/usr/bin/env python
from webbrowser import open_new_tab
import SimpleHTTPServer
import SocketServer
from threading import Timer

port = 8000


def ont():
    open_new_tab('http://localhost:' + str(port))

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", port), Handler)

print "serving at port", port
Timer(1, ont).start()
httpd.serve_forever()
