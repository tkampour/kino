#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os.path
import sys
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import MySQLdb
import memcache
import torndb
import urllib2

from tornado.options import define, options
#from tornado_utils.tornado_static import (
#  StaticURL, Static, PlainStaticURL, PlainStatic) 

define("port", default=8888, help="App Server running on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r"/", mainHandler),
            (r"/last5torn", AjaxLast5torn),
            (r"/mostseen", AjaxMostSeen),
            (r"/mostseen/([^/]*)", AjaxMostSeen),
            (r"/notseen", AjaxLeastSeen),
            (r"/about/?", AboutHandler),
            (r"/rules.html", rulesHandler),
            (r"/main.html", mainHandler),
            (r"/check.html", checkHandler),
            (r"/full.html", fullHandler),
            (r"/fill.html", fillHandler),
            (r"/check/([\d\D?]*)", AjaxCheck),
            (".*", DefaultHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            gzip=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
#    def set_default_headers(self):
#        self.set_header("Access-Control-Allow-Origin", "othermachine.com")

    def return_json(self, data_dict):
        """
        acessory method to return json objects
        """
        self.set_header('Content-Type', 'application/json')
        json_ = tornado.escape.json_encode(data_dict)
        self.write(json_)
        self.finish()

    def write_error(self, status_code, **kwargs):
        self.write("Wow, that was unexpected! You caused a %d error." % status_code)

    def RESTcall(self, url):
        try:
            json_data = urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            conn.close()
            sys.exit()
        except urllib2.URLError, e:
            print "Network error!!!: %s" % e.reason.args[1]
            conn.close()
            sys.exit()
        return json_data

    def mostseen(self, input):
        topnums = memc.get('mostseen')
        if not topnums:
            db = torndb.Connection(
                host="localhost", database="Kino",
                user="tkampour", password="github")
            rows = db.query("Select Number, Times from Month_Stats order by Times desc")
            db.close()
            topnums = rows[0:int(input)]
            print "Loaded from MySQL"
        else:
            print "Loaded from memcache"        
        return topnums;

    def leastseen(self):
        rarenums = memc.get('leastseen')
        if not rarenums:
            db = torndb.Connection(
                host="localhost", database="Kino",
                user="tkampour", password="github")
            rarenums = db.query("Select Number, lastDrawNo from Month_Stats order by LastDrawNo asc")
            db.close()
            print "Loaded from MySQL"
        else:
            print "Loaded from memcache"
        return rarenums;

class MainHandler(BaseHandler):
   def get(self):
        self.render("index.html")

# class AjaxLast5(BaseHandler):
#    def get(self):
#        try:
#            conn = MySQLdb.connect(host= "localhost",
#                                   user="tkampour",
#                                   passwd="github",
#                                   db="Kino")
#            last5 = memc.get('last5kino')
#            if not last5:
#                x = conn.cursor()
#                x.execute("Select * from snumbers order by drawNo desc LIMIT 5")
#                my_row = x.fetchall()
#                last5 = my_row[0:5]
#                memc.set('last5kino',last5, 300)
#                print "Loaded from MySQL"
#            else:
#                print "Loaded from memcache"

#            print last5
#            self.return_json(last5)
#        except MySQLdb.Error, e:
#            print "Error %d: %s" % (e.args[0], e.args[1])
#            pass
#        except Exception , e:
#            print "Unhandled Exception: " , e
#            pass

class AjaxLast5torn(BaseHandler):
    #@is_ajax
    def get(self):
       try:
           last5 = memc.get('last5kino')
           if not last5:
               db = torndb.Connection(
                   host="localhost", database="Kino",
                   user="tkampour", password="github")
               rows = db.query("Select * from snumbers order by drawNo desc LIMIT 5")
               db.close()
               last5 = rows[0:5]
               memc.set('last5kino',last5, 300)
               print "Loaded from MySQL"
           else:
               print "Loaded from memcache"
           self.return_json(last5)
       except Exception , e:
           print "Unhandled Exception: " , e
           db.close()

class AjaxMostSeen(BaseHandler):
    def get(self, input=5):
        print input
        if not input:
            input=5;
        try:
            self.return_json(self.mostseen(input))
        except Exception , e:
            print "Unhandled Exception: " , e

class AjaxLeastSeen(BaseHandler):
    def get(self):
       try:
           self.return_json(self.leastseen())
       except Exception , e:
           print "Unhandled Exception: " , e

class AjaxCheck(BaseHandler):
  def get(self, input):
      json_data = []
      json_data = self.RESTcall(input)
      self.write(json_data)

class AboutHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render("about.html")

class rulesHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render("rules.html")

class mainHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render("main.html")

class checkHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render("check.html")

class fillHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render("fill.html", most=self.mostseen(12),least=self.leastseen())

class fullHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        try:
            db = torndb.Connection(
                host="localhost", database="Kino",
                user="tkampour", password="github")
            stats = db.query("Select Number, Times, lastDrawNo from Month_Stats order by Number asc")
            lastdraw =db.query("Select max(lastDrawNo) as max from Month_Stats")
            db.close()
        except Exception , e:
            print "Unhandled Exception: " , e
        lastdraw = lastdraw[0].max
        statsd = []
        statsd.append(['Number', 'Klirwseis', 'Kathisteriseis', 'Chance'])
        for i in range(0,80):
            if int(stats[i].Times) > 100/4 and int(lastdraw - stats[i].lastDrawNo) > 4 :
                statsd.append([str(i), int(stats[i].Times), int(lastdraw - stats[i].lastDrawNo), 2])
            elif int(stats[i].Times) > 100/4:
                statsd.append([str(i), int(stats[i].Times), int(lastdraw - stats[i].lastDrawNo), 1])
            elif int(lastdraw - stats[i].lastDrawNo) > 4:
                statsd.append([str(i), int(stats[i].Times), int(lastdraw - stats[i].lastDrawNo), 1])
            else:
                statsd.append([str(i), int(stats[i].Times), int(lastdraw - stats[i].lastDrawNo), 0])
        print statsd
        self.render("full.html", stats=statsd)

class DefaultHandler(BaseHandler):
    def get(self):
        self.render("50x.html")

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    memc = memcache.Client(['127.0.0.1:11211'], debug=1);
    try:
        main()
    except Exception, e:
        print "Unexpected Error", e
