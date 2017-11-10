#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import BaseHTTPServer
import CGIHTTPServer

import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
DOCUMENT_ROOT = 'www'

# serve from DOCUMENT_ROOT
os.chdir(os.path.join(CUR_DIR, DOCUMENT_ROOT))

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ('', 8000)
handler.cgi_directories = ['/']

httpd = server(server_address, handler)
httpd.serve_forever()
