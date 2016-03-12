from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2
import re
import datetime

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

class MainPage(webapp2.RequestHandler):
    def get(self):
        url = 'http://www.vision-environnement.com/meteo/Le-Crotoy/wdl/clientraw.txt'
        result = urlfetch.fetch(url,deadline=15)

        if result.status_code == 200:
            ReqData = result.content
            ListOfFields = ReqData.split()
        
            temperature  = int(round(float(ListOfFields[4])))

            vitesse      = int(round(float(ListOfFields[2])*1.852))
            if vitesse==0:
                direction = ''
            else:
                direction_d  = int(ListOfFields[3])
                tablesecteur = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N']
                direction      = tablesecteur[int(round(direction_d/22.5))]

            humidite     = int(ListOfFields[5])
            pluie        = float(ListOfFields[7])
            pression     = float(ListOfFields[6])
            updateday    = ListOfFields[74][6:10]+"-"+ListOfFields[74][3:5]+"-"+ListOfFields[74][0:2]
            updateheure  = ListOfFields[29]
            updateminute = ListOfFields[30]
            dtnow = datetime.datetime.now()
            newentity = Weather_crotoy(direction=direction,humidite=int(humidite),pluie=float(pluie),temperature=int(temperature),pression=float(pression), vitesse=int(vitesse), updateday=updateday, updateheure=updateheure, updateminute=updateminute, date=dtnow)
            newentity.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.http_status_message(200)

app = webapp2.WSGIApplication([('/tasks/updateweatherdb_crotoy', MainPage)], debug=True)

