import webapp2
from google.appengine.api import mail
from google.appengine.ext import ndb
import datetime
from pytz.gae import pytz

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
        Paris = pytz.timezone('Europe/Paris')
        LocalCurrentTime = pytz.timezone('UTC').localize(CurrentTime).astimezone(Paris)
        SelectedDate   = LocalCurrentTime.strftime("%Y-%m-%d")
        SelectedHour   = LocalCurrentTime.strftime("%H")
        SelectedMinute = LocalCurrentTime.strftime("%M")
 
        qry1 = Weather.query(Weather.updateday == SelectedDate)
        qry2 = qry1.filter(Weather.updateheure == SelectedHour)
        qry3 = qry2.order(Weather.updateheure,Weather.updateminute)

        Samples = [False]*60

        for ientity in qry3:
            Samples[int(ientity.updateminute)] = True

        IntSelectedMinute = int(SelectedMinute)
        NumberOfSamples   = 0
        for I in range(IntSelectedMinute-14,IntSelectedMinute+1):
            if (Samples[I]):
                NumberOfSamples = NumberOfSamples + 1

        # For Lery-Poses, 2 samples every 3mn. This translates into about 10 samples during a 15mn period
        if (NumberOfSamples < 10):
            EmailBody = "Lery-Poses:\n\tLocal current time = " + LocalCurrentTime.strftime("%Y-%m-%d %H:%M") + "\n\tNumber of samples during the last 15mn: " + str(NumberOfSamples)
            mail.send_mail(sender="weighty-wonder-91207@appspot.gserviceaccount.com" ,
                          to="Jean-Michel Vuillamy <jmvuilla@gmail.com>",
                          subject="Weather station data collection issue",
                          body=EmailBody)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.http_status_message(200)

app = webapp2.WSGIApplication([('/tasks/checkweatherdb', MainPage)], debug=True)

