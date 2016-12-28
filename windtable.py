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

class WindTable(webapp2.RequestHandler):
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
        
        if SelectedGraph=="Tableau des données météo".decode('utf-8'):
            SelectedDateFrench = SelectedDate[8:10]+ "/" + SelectedDate[5:7]+ "/" + SelectedDate[0:4] + " de " + SelectedStartHour + "H00 à ".decode('utf-8') + SelectedEndHour + "H00"
            if SelectedSpot=="Lery-Poses":
                FullTitle = "Données météo à Léry-Poses, le ".decode('utf-8') + SelectedDateFrench
            if SelectedSpot=="Le Crotoy":
                FullTitle = "Données météo à Le Crotoy, le ".decode('utf-8') + SelectedDateFrench

            self.response.write("""
            <html><head><style> h2 { font-size: 1.8em; font-weight: normal; } </style>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65403806-1', 'auto');
  ga('send', 'pageview');

</script>
            <style>
            table, th, td { border: 1px solid black; border-collapse: collapse; }
            th, td { padding: 5px; text-align: left; }

            table#t01 tr: nth-child(even) { background-color: #eee; }
            table#t01 tr: nth-child(odd)  { background-color: #fff; }
            table#t01 th                  { background-color: black; color: white; }
            </style>
            <body><pre>
            """)
            self.response.write('<h2>' + FullTitle + '</h2>\n')
            if SelectedUnit=="km/h":
                self.response.write("""
                <table id="t01">
                    <tr>
                        <th>Heure (HH:MM)</th>
                        <th>Vitesse (km/h)</th>
                        <th>Direction</th>
                        <th>Température (°C)</th>
                        <th>Humidité (%)</th>
                        <th>Pluie (mm)</th>
                        <th>Pression (hPa)</th>
                    </tr>
                """)
            if SelectedUnit=="noeud":
                self.response.write("""
                <table id="t01">
                    <tr>
                        <th>Heure (HH:MM)</th>
                        <th>Vitesse (noeud)</th>
                        <th>Direction</th>
                        <th>Température (°C)</th>
                        <th>Humidité (%)</th>
                        <th>Pluie (mm)</th>
                        <th>Pression (hPa)</th>
                    </tr>
                """)
            first_ientity=True
            entity_count = 0
            sumvitesse = 0.0
            sumsqvitesse = 0.0
            for ientity in qry3:

                if first_ientity:
                   first_ientity=False
                   skip_data=False
                   entity_count = 1
                else:
                   if previous_ientity.updateheure==ientity.updateheure and previous_ientity.updateminute==ientity.updateminute:
                      skip_data=True
                   else:
                      skip_data=False
                      entity_count = entity_count + 1

                if not skip_data:
                    self.response.write('<tr><td>%2s:' % ientity.updateheure)
                    self.response.write('%2s</td>' % ientity.updateminute)
                    if SelectedUnit=="km/h":
                        ivitesse = ientity.vitesse
                        self.response.write('<td>%5d</td>' % (ivitesse))
                    if SelectedUnit=="noeud":
                        ivitesse = ientity.vitesse/1.852
                        self.response.write('<td>%5.1f</td>' % (round(ivitesse,1)))
                    self.response.write('<td>%3s</td>' % ientity.direction)
                    sumvitesse = sumvitesse + ivitesse
                    sumsqvitesse = sumsqvitesse + ivitesse*ivitesse
            
                    self.response.write('<td>%3d</td>' % ientity.temperature)
                    self.response.write('<td>%3d</td>' % ientity.humidite)
                    self.response.write('<td>%6.1f</td>' % ientity.pluie)
                    self.response.write('<td>%6.1f</td></tr>' % ientity.pression)

                previous_ientity = ientity 
            self.response.write('</table>')
            self.response.write("\nNombre d'échantillons: ".decode('utf-8')+str(entity_count))
            if not entity_count==0: 
                moyennevitesse = sumvitesse/entity_count
                self.response.write("\nMoyenne    de la vitesse: %5.1f " % moyennevitesse)
                self.response.write(" "+SelectedUnit)
                ecarttypevitesse = ((sumsqvitesse - sumvitesse*sumvitesse/entity_count)/entity_count)**0.5 
                self.response.write("\nEcart-type de la vitesse: %5.1f " % ecarttypevitesse)
                self.response.write(" "+SelectedUnit)
            self.response.write("""\n\nQuestions, commentaires ou bugs: <a href="mailto:myWindStats@gmail.com">myWindStats@gmail.com</a>""")
            if SelectedSpot=="Lery-Poses":
                self.response.write("""\nLes données météorologiques sont issues de la sonde de "troislacs - base de loisirs" """)
            self.response.write('</pre></body></html>') 

app = webapp2.WSGIApplication([('/windtable',WindTable)], debug=True)
