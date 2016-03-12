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


class AllHistory(webapp2.RequestHandler):
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

        if SelectedGraph=="Graphes des données météo".decode('utf-8'):
            ListeHeure = []
            ListeVentVitesse = []
            ListeTemperature = []
            ListeDirection = []
            ListeHumidite = []
            ListePluie = []
            ListePression = []
            CompassDict = {'N':0.0, 'NNE':22.5, 'NE':45.0, 'ENE':67.5, 'E':90.0, 'ESE':112.5, 'SE':135, 'SSE':157.5, 'S':180.0, 'SSW':202.5, 'SW':225.0, 'WSW':247.5, 'W':270.0, 'WNW':292.5, 'NW':315.0, 'NNW':337.5, '':-1}

            for ientity in qry3:
                ListeHeure.append(ientity.updateday + ' ' + ientity.updateheure + ':' + ientity.updateminute + ':00')
                if SelectedUnit=="km/h":
                    ListeVentVitesse.append(ientity.vitesse)
                if SelectedUnit=="noeud":
                    ListeVentVitesse.append(int(round(ientity.vitesse/1.852)))
                ListeTemperature.append(ientity.temperature)
                if ientity.direction!='':
                    ListeDirection.append(CompassDict[ientity.direction])
                else:
                    found_real_direction = 0
                    value_real_direction = 0
                    for index_direction in reversed(ListeDirection):
                        if found_real_direction == 0:
                            if index_direction != -1:
                               found_real_direction = 1
                               value_real_direction = index_direction
                    ListeDirection.append(value_real_direction)
                ListeHumidite.append(ientity.humidite)
                ListePluie.append(ientity.pluie)
                ListePression.append(ientity.pression)

            ListeHeureFmt = [datetime.datetime.strptime(DateIndex,"%Y-%m-%d %H:%M:%S") for DateIndex in ListeHeure]

            SelectedDateFrench = SelectedDate[8:10]+ "/" + SelectedDate[5:7]+ "/" + SelectedDate[0:4] + " de " + SelectedStartHour + "H00 à ".decode('utf-8') + SelectedEndHour + "H00"
            
            fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = matplotlib.pyplot.subplots(nrows=3,ncols=2) 
            hfmt = matplotlib.dates.DateFormatter("%H:%M")
            fig.autofmt_xdate()

            XMinDate = datetime.datetime.strptime(SelectedDate + ' ' + SelectedStartHour + ':00:00',"%Y-%m-%d %H:%M:%S")
            if SelectedEndHour=="00":
                XMaxDate = datetime.datetime.strptime(SelectedDate + ' 00:00:00',"%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
            else:
                XMaxDate = datetime.datetime.strptime(SelectedDate + ' ' + SelectedEndHour + ':00:00',"%Y-%m-%d %H:%M:%S")

            if SelectedSpot=="Lery-Poses":
               Spot = "Léry-Poses".decode('utf-8')
            if SelectedSpot=="Le Crotoy":
               Spot = SelectedSpot
            TitreGen = "Données météo à ".decode('utf-8') + Spot + ", le " + SelectedDateFrench 
            fig.suptitle(TitreGen, fontsize=16)

            ax1.plot(ListeHeureFmt,ListeVentVitesse,linewidth=0.4)
            if (SelectedUnit=="km/h"):
                ax1.set_title('Vitesse vent (km/h)',fontsize=10,ha='left')
            if (SelectedUnit=="noeud"):
                ax1.set_title('Vitesse vent (noeud)',fontsize=10,ha='left')
            ax1.tick_params(axis='y',labelsize=8)
            ax1.grid()
            ax1.set_xlim(xmin=XMinDate,xmax=XMaxDate)
            ax1ylim = ax1.get_ylim()
            ax1yper = (ax1ylim[1]-ax1ylim[0])*8/100
            ax1.set_ylim(ax1ylim[0]-ax1yper,ax1ylim[1]+ax1yper)



            ax3.scatter(ListeHeureFmt,ListeDirection,marker=',',s=3,linewidth=0)
            ax3.set_title('Direction vent'.decode('utf-8'),fontsize=10, ha='left')
            from matplotlib.ticker import FixedLocator
            ax3.yaxis.set_major_locator(FixedLocator([0,45,90,135,180,225,270,315]))
            ax3.yaxis.set_ticklabels(['N','NE','E','SE','S','SO','O','NO'])
            ax3.tick_params(axis='y',labelsize=8)
            ax3.grid()
            ax3.set_xlim(xmin=XMinDate,xmax=XMaxDate)

            ax2.plot(ListeHeureFmt,ListeHumidite,linewidth=0.4)
            ax2.set_title('Humidité (%)'.decode('utf-8'),fontsize=10, ha='left')
            ax2.tick_params(axis='y',labelsize=8)
            ax2.grid()
            ax2.set_xlim(xmin=XMinDate,xmax=XMaxDate)
            ax2ylim = ax2.get_ylim()
            ax2yper = (ax2ylim[1]-ax2ylim[0])*8/100
            ax2.set_ylim(ax2ylim[0]-ax2yper,ax2ylim[1]+ax2yper)

            ax4.plot(ListeHeureFmt,ListePluie,linewidth=0.4)
            ax4.set_title('Pluie (mm)',fontsize=10, ha='left')
            ax4.tick_params(axis='y',labelsize=8)
            ax4.grid()
            ax4.set_xlim(xmin=XMinDate,xmax=XMaxDate)
            ax4ylim = ax4.get_ylim()
            ax4yper = (ax4ylim[1]-ax4ylim[0])*8/100
            ax4.set_ylim(ax4ylim[0]-ax4yper,ax4ylim[1]+ax4yper)


            ax5.plot(ListeHeureFmt,ListeTemperature,linewidth=0.4)
            ax5.set_title('Température air (°C)'.decode('utf-8'),fontsize=10, ha='left')
            ax5.tick_params(axis='y',labelsize=8)
            ax5.grid()
            ax5.set_xlim(xmin=XMinDate,xmax=XMaxDate)
            ax5.xaxis.set_major_formatter(hfmt)
            ax5ylim = ax5.get_ylim()
            ax5.set_ylim(ax5ylim[0]-1,ax5ylim[1]+1)
            ax5.tick_params(axis='x',labelsize=8)

            ax6.plot(ListeHeureFmt,ListePression,linewidth=0.4)
            ax6.set_title('Pression (hPa)',fontsize=10, ha='left')
            ax6.tick_params(axis='y',labelsize=8)
            ax6.grid()
            ax6.set_xlim(xmin=XMinDate,xmax=XMaxDate)
            ax6ylim = ax6.get_ylim()
            ax6yper = (ax6ylim[1]-ax6ylim[0])*8/100
            ax6.set_ylim(ax6ylim[0]-ax6yper,ax6ylim[1]+ax6yper)
            ax6.xaxis.set_major_formatter(hfmt)
            ax6.tick_params(axis='x',labelsize=8)
            ax6.ticklabel_format(useOffset=False,axis='y')

            matplotlib.pyplot.subplots_adjust(hspace=0.5)

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

app = webapp2.WSGIApplication([('/allhistory',AllHistory)], debug=True)
