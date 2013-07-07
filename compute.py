import os
import urllib2
import json
import re
import urllib2
import sys
import time

folder = "sfbay.craigslist.org/sby/apa/"
for file in os.listdir(folder):
  if file.startswith("3") and file.endswith(".html"):
    price = 0
    with open(os.path.join(folder, file)) as current_file:
      for line in current_file:
        zz = re.search("\\$[0-9]{4,}", line)
        if zz:
          price = zz.group()
        m = line.find("maps.google.com")
        if m >= 0:
          qe = line.find("q=", m) + 2
          q = line.find('"', qe)
          a = line.find('&', qe)
          end = min(q,a)
          if end == -1:
            end = max(q,a)
          loc = line[qe:end]
          if loc.startswith("loc%3A+"):
            loc = loc[7:]
          times = []
          for googleapi in ["http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin=701+1st+Ave,+Sunnyvale,+CA&destination=%s" % (loc,), "http://maps.googleapis.com/maps/api/directions/json?sensor=false&3825+Fabian+Way,+Palo+Alto,+CA+94303&destination=%s" % (loc,)]:
            time.sleep(2.1)
            opened = urllib2.urlopen(googleapi)
            x = opened.read()
            opened.close()
            vals = json.loads(x)
            try:
              times.append(vals['routes'][0]['legs'][0]['duration']['value'])
            except IndexError:
              print vals
              raise
          print "http://sfbay.craigslist.org/sby/apa/"+file,price,times[0],times[1]
          sys.stdout.flush()
          break
