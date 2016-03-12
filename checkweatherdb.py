import webapp2
from google.appengine.api import mail
from google.appengine.ext import ndb
import datetime

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

class MainPage(webapp2.RequestHandler):
    def get(self):
        CurrentTime = datetime.datetime.now()
        SelectedDate = CurrentTime.strftime("%Y-%m-%d")
        SelectedHour = CurrentTime.strftime("%H")
        SelectedMinute = CurrentTime.strftime("%M")
 
        qry1 = Weather.query(Weather.updateday == SelectedDate)
        qry2 = qry1.filter(Weather.updateheure == SelectedHour)
        qry3 = qry2.order(Weather.updateheure,Weather.updateminute)

        for ientity in qry3:
            LastUpdateYear   = int(ientity.updateday[0:4])
            LastUpdateMonth  = int(ientity.updateday[5:7])
            LastUpdateDay    = int(ientity.updateday[8:10])
            LastUpdateHour   = int(ientity.updateheure)
            LastUpdateMinute = int(ientity.updateminute)
            LastUpdateTime   = datetime.datetime(LastUpdateYear,LastUpdateMonth,LastUpdateDay,LastUpdateHour,LastUpdateMinute)
            Diff = CurrentTime - LastUpdateTime

        EmailBody = "Lery-Poses: " + CurrentTime.strftime("%Y-%m-%d %H:%M")
        mail.send_mail(sender="weighty-wonder-91207@appspot.gserviceaccount.com" ,
                      to="Jean-Michel Vuillamy <jmvuilla@gmail.com>",
                      subject="Weather station data collection issue",
                      body=EmailBody)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.http_status_message(200)

app = webapp2.WSGIApplication([('/tasks/checkweatherdb', MainPage)], debug=True)

