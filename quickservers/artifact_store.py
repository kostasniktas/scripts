import SimpleHTTPServer
import BaseHTTPServer
from datetime import datetime
import os

# python 2

files_seen = dict()

class SputHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_PUT(self):
        print datetime.now()
        print self.headers
        print self.path
        length = int(self.headers["Content-Length"])
        path = self.translate_path(self.path)
        dirname = os.path.dirname(path)
        if path.strip() != "" and path.strip() != "/":
          try:
            os.makedirs(dirname)
          except:
            pass # probably created
        with open(path, "wb") as dst:
            print "Writing " + path
            dst.write(self.rfile.read(length))
            print "\t Writing done"
        if path in files_seen:
            files_seen[path] += 1
            print "We've seen this file before", files_seen[path], "times total now"
        else:
            files_seen[path] = 1
        print "=========="
        print ""


if __name__ == '__main__':
    SimpleHTTPServer.test(HandlerClass=SputHTTPRequestHandler)
