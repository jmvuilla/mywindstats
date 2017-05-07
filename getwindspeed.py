import cgi
from google.appengine.ext import ndb
import webapp2
import datetime
from pytz.gae import pytz

class PortableAnemometer(ndb.Model):
    date         = ndb.DateTimeProperty('d',auto_now_add=True)
    vitesse      = ndb.IntegerProperty('v')
    updateday    = ndb.StringProperty('a')
    updateheure  = ndb.StringProperty('b')
    updateminute = ndb.StringProperty('c')
    voltage      = ndb.IntegerProperty('u')
    temperature  = ndb.IntegerProperty('t')

class GetWindSpeed(webapp2.RequestHandler):
    def post(self):
        SelectedDevice = cgi.escape(self.request.get('device'))
        SelectedTime = cgi.escape(self.request.get('time'))
        SelectedSignal = cgi.escape(self.request.get('Signal'))
        SelectedData = cgi.escape(self.request.get('data'))
        SelectedWS = [cgi.escape(self.request.get('slot_ws0')),
                      cgi.escape(self.request.get('slot_ws1')),
                      cgi.escape(self.request.get('slot_ws2')),
                      cgi.escape(self.request.get('slot_ws3')),
                      cgi.escape(self.request.get('slot_ws4')),
                      cgi.escape(self.request.get('slot_ws5')),
                      cgi.escape(self.request.get('slot_ws6')),
                      cgi.escape(self.request.get('slot_ws7')),       
                      cgi.escape(self.request.get('slot_ws8')),
                      cgi.escape(self.request.get('slot_ws9'))]
        SelectedVolt = cgi.escape(self.request.get('slot_volt'))
        SelectedTemp = cgi.escape(self.request.get('slot_temp'))
        voltage = int(SelectedVolt)*16
        temperature = int(SelectedTemp)*4-300

        dtnow = datetime.datetime.now()
        utc=pytz.utc
        paris=pytz.timezone('Europe/Paris')
        
        for i in range(10):
            utc_dt = utc.localize(datetime.datetime.fromtimestamp(int(SelectedTime)))-datetime.timedelta(minutes=9-i)
            local_dt=utc_dt.astimezone(paris)
            updateday = local_dt.strftime("%Y-%m-%d")
            updateheure = local_dt.strftime("%H")
            updateminute = local_dt.strftime("%M")
            newentity = PortableAnemometer(date=dtnow, vitesse=int(SelectedWS[i]), updateday=updateday, updateheure=updateheure, updateminute=updateminute, voltage=voltage, temperature=temperature)
            newentity.put()

app = webapp2.WSGIApplication([('/getwindspeed',GetWindSpeed)], debug=True)
