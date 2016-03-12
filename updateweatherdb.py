from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2
import re
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
    #eau          = ndb.FloatProperty('e')

class MainPage(webapp2.RequestHandler):
    def get(self):

        url = 'http://www.weatherlink.com/user/troislacs'
        result = urlfetch.fetch(url,deadline=15)

        if result.status_code == 200:
            reqdata = result.content

            p = re.compile(r'(>(-?\d+)<span class="degrees")')
            m = p.findall(str(reqdata))
            temperature = m[0][1]

            p = re.compile(r'>([NSEW]+)&nbsp;(\d+)|Calm')
            m = p.findall(str(reqdata))
            direction = m[0][0]
            vitesse = m[0][1] if m[0][1] else '0'

            p = re.compile(r'>(\d+)<span class="threequarter">%')
            m = p.findall(str(reqdata))
            humidite = m[0]

            p = re.compile(r'>(\d+\.\d+)mm</td>')
            m = p.findall(str(reqdata))
            pluie = m[0]

            p = re.compile(r'>(\d+\.\d+)hPa</td>')
            m = p.findall(str(reqdata))
            pression = m[0]

            p = re.compile(r'Current Conditions as of (\d+:\d+) (.*,) (.*) (\d+), (\d+)<Br>')
            m = p.findall(str(reqdata))

            MonthDict = {'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07'
,'August':'08','September':'09','October':'10','November':'11','December':'12'}
            if len(m[0][3])==1:
                tmpday='0'+m[0][3]
            else:
                tmpday=m[0][3]
            if len(m[0][0])==5:
                tmptime = m[0][0]
            else:
                tmptime = '0' + m[0][0]
            dtnow = datetime.datetime.now()
            datetxt=str(dtnow)[0:19]
            dateupdate = m[0][4] + "-" + MonthDict[m[0][2]] + "-" + tmpday + " " + tmptime + ":00"

            url2 = 'http://www.weatherlink.com/user/troislacs/index.php?view=summary&headers=0'
            result2 = urlfetch.fetch(url2,deadline=15)
         
            #if result2.status_code == 200:
            #     reqdata2 = result2.content
            #     p = re.compile(r'Extra Temp 2<\/td>\s*<td width="170" class="summary_data">(\d+\.\d+) C<\/td>')
            #     m = p.findall(str(reqdata2))
            #     eau = m[0]

            newentity = Weather(direction=direction,humidite=int(humidite),pluie=float(pluie),temperature=int(temperature),pression=float(pression), vitesse=int(vitesse), updateday=m[0][4] + "-" + MonthDict[m[0][2]] + "-" + tmpday, updateheure=tmptime[0:2], updateminute=tmptime[3:5], date=dtnow)
            newentity.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.http_status_message(200)

app = webapp2.WSGIApplication([('/tasks/updateweatherdb', MainPage)], debug=True)

