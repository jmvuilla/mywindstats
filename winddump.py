import cgi
from google.appengine.ext import ndb
import webapp2
import matplotlib
import matplotlib.pyplot
import datetime
import StringIO

class Weather(ndb.Model):
    direction    = ndb.StringProperty('i')
    humidite     = ndb.IntegerProperty('h')
    pluie        = ndb.FloatProperty('p')
    temperature  = ndb.IntegerProperty('t')
    date         = ndb.DateTimeProperty('d',auto_now_add=True)
    pression     = ndb.FloatProperty('r')
    vitesse      = ndb.IntegerProperty('v')
    updateday    = ndb.StringProperty('a')
    updateheure  = ndb.StringProperty('b')
    updateminute = ndb.StringProperty('c')

class Weather_crotoy(ndb.Model):
    direction    = ndb.StringProperty('i')
    humidite     = ndb.IntegerProperty('h')
    pluie        = ndb.FloatProperty('p')
    temperature  = ndb.IntegerProperty('t')
    date         = ndb.DateTimeProperty('d',auto_now_add=True)
    pression     = ndb.FloatProperty('r')
    vitesse      = ndb.IntegerProperty('v')
    updateday    = ndb.StringProperty('a')
    updateheure  = ndb.StringProperty('b')
    updateminute = ndb.StringProperty('c')

class WindDump(webapp2.RequestHandler):
    def post(self):
        SelectedSpot = cgi.escape(self.request.get('S_Spot'))
        SelectedDate = cgi.escape(self.request.get('S_SelectedDate'))

        self.response.write("""
        <html><head>
        <body><pre>
        \n""")

# range(1,11) or range(11,21) or range(21,32)
        for iday in range(21,32):
            if iday<10:
                idate = SelectedDate[0:8]+"0"+str(iday)
            else:
                idate = SelectedDate[0:8]+str(iday)
            if SelectedSpot=="Lery-Poses":
                qry1 = Weather.query(Weather.updateday == idate)

            if SelectedSpot=="Le Crotoy":
                qry1 = Weather_crotoy.query(Weather_crotoy.updateday == idate)
        
            for ientity in qry1:
                self.response.write(ientity.updateday + ',' + ientity.updateheure + ',' + ientity.updateminute + ',')
                self.response.write(str(ientity.vitesse) + ',' + ientity.direction + ',' + str(ientity.temperature) + ',')
                self.response.write(str(ientity.humidite) + ',' + str(ientity.pluie) + ',' + str(ientity.pression) + '\n')
           
        self.response.write('</pre></body></html>') 

app = webapp2.WSGIApplication([('/winddump',WindDump)], debug=True)
