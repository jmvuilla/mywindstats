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

class PortableAnemometer(ndb.Model):
    date         = ndb.DateTimeProperty('d',auto_now_add=True)
    vitesse      = ndb.IntegerProperty('v')
    updateday    = ndb.StringProperty('a')
    updateheure  = ndb.StringProperty('b')
    updateminute = ndb.StringProperty('c')

class WindHistory(webapp2.RequestHandler):
    def post(self):
        SelectedSpot = cgi.escape(self.request.get('S_Spot'))
        SelectedDate = cgi.escape(self.request.get('S_SelectedDate'))
        SelectedStartHour = cgi.escape(self.request.get('S_StartHour'))
        SelectedEndHour = cgi.escape(self.request.get('S_EndHour'))
        SelectedUnit = cgi.escape(self.request.get('S_Unit'))
        SelectedGraph = cgi.escape(self.request.get('S_Graphe'))

        if SelectedEndHour=="00":
            SelectedEndHourQuery="24"
        else:
            SelectedEndHourQuery=SelectedEndHour

        if SelectedSpot=="Lery-Poses":
            qry1 = Weather.query(Weather.updateday == SelectedDate)
            qry2 = qry1.filter(ndb.AND(Weather.updateheure >= SelectedStartHour,Weather.updateheure < SelectedEndHourQuery))
            qry3 = qry2.order(Weather.updateheure,Weather.updateminute)

        if SelectedSpot=="Le Crotoy":
            qry1 = Weather_crotoy.query(Weather_crotoy.updateday == SelectedDate)
            qry2 = qry1.filter(ndb.AND(Weather_crotoy.updateheure >= SelectedStartHour,Weather_crotoy.updateheure < SelectedEndHourQuery))
            qry3 = qry2.order(Weather_crotoy.updateheure,Weather_crotoy.updateminute)

        if SelectedSpot=="Mobile Anemometer":
            qry1 = PortableAnemometer.query(PortableAnemometer.updateday == SelectedDate)
            qry2 = qry1.filter(ndb.AND(PortableAnemometer.updateheure >= SelectedStartHour,PortableAnemometer.updateheure < SelectedEndHourQuery))
            qry3 = qry2.order(PortableAnemometer.updateheure,PortableAnemometer.updateminute)

        if SelectedGraph=="Graphe de la vitesse du vent":
            ListeHeure = []
            ListeVentVitesse = []
            for ientity in qry3:
                ListeHeure.append(ientity.updateday + ' ' + ientity.updateheure + ':' + ientity.updateminute + ':00')
                if SelectedUnit=="km/h":
                    ListeVentVitesse.append(ientity.vitesse)
                if SelectedUnit=="noeud":
                    ListeVentVitesse.append(round(ientity.vitesse/1.852,1))

            ListeHeureFmt = [datetime.datetime.strptime(DateIndex,"%Y-%m-%d %H:%M:%S") for DateIndex in ListeHeure]

            SelectedDateFrench = SelectedDate[8:10]+ "/" + SelectedDate[5:7]+ "/" + SelectedDate[0:4] + " de " + SelectedStartHour + "H00 à ".decode('utf-8') + SelectedEndHour + "H00"
            
            matplotlib.pyplot.title("Vitesse du vent à Léry-Poses, le ".decode('utf-8') + SelectedDateFrench)
            if SelectedSpot=="Le Crotoy":
                matplotlib.pyplot.title("Vitesse du vent à Le Crotoy, le ".decode('utf-8') + SelectedDateFrench)
            if SelectedSpot=="Mobile Anemometer":
                matplotlib.pyplot.title("Vitesse du vent sur l'anémomètre portable, le ".decode('utf-8') + SelectedDateFrench)

            matplotlib.pyplot.xlabel('Temps')
            if (SelectedUnit=="km/h"):
                matplotlib.pyplot.ylabel('Vitesse (km/h)')
            if (SelectedUnit=="noeud"):
                matplotlib.pyplot.ylabel('Vitesse (noeud)')
            matplotlib.pyplot.grid(True)
            matplotlib.pyplot.plot(ListeHeureFmt,ListeVentVitesse,linewidth=0.4)

            XMinDate = datetime.datetime.strptime(SelectedDate + ' ' + SelectedStartHour + ':00:00',"%Y-%m-%d %H:%M:%S")
            if SelectedEndHour=="00":
                XMaxDate = datetime.datetime.strptime(SelectedDate + ' 00:00:00',"%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
            else:
                XMaxDate = datetime.datetime.strptime(SelectedDate + ' ' + SelectedEndHour + ':00:00',"%Y-%m-%d %H:%M:%S")
            matplotlib.pyplot.xlim(xmin=XMinDate,xmax=XMaxDate)

            hfmt = matplotlib.dates.DateFormatter("%H:%M")
            matplotlib.pyplot.gca().xaxis.set_major_formatter(hfmt)
            matplotlib.pyplot.gcf().autofmt_xdate()
            rv = StringIO.StringIO()
            matplotlib.pyplot.savefig(rv,format="png")
            matplotlib.pyplot.clf()
            self.response.write('<html>')
            self.response.write("""
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65403806-1', 'auto');
  ga('send', 'pageview');

</script>
                                """) 
            self.response.write('<body><pre>')
            self.response.write("""<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip()) 
            self.response.write("""\n\nQuestions, commentaires ou bugs: <a href="mailto:myWindStats@gmail.com">myWindStats@gmail.com</a>""")
            if SelectedSpot=="Lery-Poses":
                self.response.write("""\nLes données météorologiques sont issues de la sonde de "troislacs - base de loisirs" """)
            self.response.write('</pre></body></html>') 

app = webapp2.WSGIApplication([('/windhistory',WindHistory)], debug=True)
