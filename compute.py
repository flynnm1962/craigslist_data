import os
import urllib2
import json
import re
import urllib2
import sys

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
          try:
            for googleapi in ["http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin=1380+Willow+Road,+Menlo+Park,+CA+94025&destination=%s" % (loc,), "http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin=701+1st+Ave,+Sunnyvale,+CA&destination=%s" % (loc,), "http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin=Middlefield+%26+Shoreline,+United+States&destination=%s" % (loc,)]
              opened = urllib2.urlopen(googleapi)
              x = opened.read()
              opened.close()
              vals = json.loads(x)
              times.append(vals['routes'][0]['legs'][0]['duration']['value'])
            print "http://sfbay.craigslist.org/sby/apa/"+file,price,times[0],times[1]
            sys.stdout.flush()
          except:
            sys.stderr.write(str(sys.exc_info()[0]))
          break
