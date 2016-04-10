from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import os.path

PORT = 7000


class MySimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            if (not os.path.isfile('index.html') and os.path.isfile('gui/index.html')):
                self.path = '/gui'
        return SimpleHTTPRequestHandler.do_GET(self)

httpd = SocketServer.TCPServer(("", PORT), MySimpleHTTPRequestHandler)

print "serving at port", PORT
httpd.serve_forever()
