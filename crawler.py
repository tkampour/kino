import json
from pprint import pprint
import urllib2
import MySQLdb
import memcache
from time import gmtime, strftime
import sys
import torndb

conn = MySQLdb.connect(host= "localhost",
                  user="tkampour",
                  passwd="github",
                  db="Kino")
x = conn.cursor()
memc = memcache.Client(['127.0.0.1:11211'])

def RESTcall(url):
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

def saveStats(lastREST):
    try:        
        columns = "(Number, Times, lastDrawNo)"         

        x.execute("delete from Month_Stats where 1=1")

        for num in range(1,81):
            selectSTMT = "Insert into Month_Stats (Number, Times, lastDrawNo) select '%d', count(*), max(drawNo) from snumbers where drawNo>%d and (Num1=%d or Num2=%d or Num3=%d or Num4=%d or Num5=%d or Num6=%d or Num7=%d or Num8=%d or Num9=%d or Num10=%d or Num11=%d or Num12=%d or Num13=%d or Num14=%d or Num15=%d or Num16=%d or Num17=%d or Num18=%d or Num19=%d or Num20=%d)" % (num, lastREST-(100), num, num,num, num,num, num,num, num,num, num,num, num,num, num,num, num,num, num,num, num)

#            insertSTMT = """INSERT INTO %s %s VALUES (%s)""" % ("Month_Stats", columns, stringList)
#            print selectSTMT
#            print selectSTMT2
            x.execute(selectSTMT)
#            print x.fetchall()
#            x.execute(selectSTMT2)
#            print x.fetchone()
#            memc.delete('last5kino')
            conn.commit()
    except Exception, e:
        print "Exception:" , e
        conn.close()
        sys.exit()
try: 
    x.execute("Select MAX(drawNo) from snumbers")
    lastDB = x.fetchone()[0]
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    conn.close()
    sys.exit()

print 'last Number:' , lastDB
lastDB = lastDB if lastDB is not None else 0

lasturl = 'http://applications.opap.gr/DrawsRestServices/kino/last.json'
extension = '.json'
prefix = 'http://applications.opap.gr/DrawsRestServices/kino/'

json_data = []
json_data = RESTcall(lasturl)
#try:
#    json_data = urllib2.urlopen(lasturl).read()
#except urllib2.HTTPError, e:
#    print "HTTP error: %d" % e.code
#except urllib2.URLError, e:
#    print "Network error!!!: %s" % e.reason.args[1]

data = json.loads(json_data)
lastREST = data["draw"]["drawNo"]

memc.set('lastdraw', lastREST);

if (lastDB < lastREST) :
    print 'lastDBNo:', lastDB,' lastRESTNo: ', lastREST
    for game in range(lastDB+1, lastREST+1):
        url = (prefix+str(game)+extension)
        if (lastDB != lastREST-1):
            json_data = RESTcall(url)
#        try:
#            json_data = urllib2.urlopen(url).read()
#        except urllib2.HTTPError, e:
#            print "HTTP error: %d" % e.code
#        except urllib2.URLError, e:
#            print "Network error!!!: %s" % e.reason.args[1]
        try:
            data = json.loads(json_data)
            columns = "(drawNo, drawTime, Num1,Num2,Num3,Num4,Num5,Num6,Num7,Num8,Num9,Num10,Num11,Num12,Num13,Num14,Num15,Num16,Num17,Num18,Num19,Num20)"  
            values = [conn.literal(aNum) for aNum in data["draw"]["results"]]
    
            stringList = str(data["draw"]["drawNo"]) +', \''+ str(data["draw"]["drawTime"])+'\', '
            stringList += "%s" % (", ".join(values))

            insertSTMT = """INSERT INTO %s %s VALUES (%s)""" % ("snumbers", columns, stringList)
            print insertSTMT
            x.execute(insertSTMT)
            conn.commit()
            memc.delete('last5kino')
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            conn.rollback()
            conn.close()
            sys.exit()
        try:
            db = torndb.Connection(
               host="localhost", database="Kino",
               user="tkampour", password="github")
            rows = db.query("Select * from snumbers order by drawNo desc LIMIT 5")
            db.close()
            last5 = rows[0:5]
            memc.set('last5kino',last5, 300)    
        except Exception , e:
            print "Unhandled TornDB Exception: " , e
            db.close()


        if (game % 100 == 0):
            print strftime("%a, %d %b %Y %X +0000", gmtime())
            saveStats(game)
            print strftime("%a, %d %b %Y %X +0000", gmtime())

print strftime("%a, %d %b %Y %X +0000", gmtime())
saveStats(lastREST)
print strftime("%a, %d %b %Y %X +0000", gmtime())

conn.close()
