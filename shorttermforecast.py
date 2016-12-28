# -*- coding: utf-8 -*-
import cgi
from google.appengine.ext import ndb
import webapp2
import matplotlib
import matplotlib.pyplot
import datetime
import StringIO
import numpy
import numpy.random
import model_M1
import model_M2
import model_M3
import model_M3_v2
import model_M6

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


class ShortTermForecast(webapp2.RequestHandler):
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

        if SelectedGraph==u"Prévision du vent dans l'heure":
            if SelectedSpot=="Lery-Poses":
                ListeHeure = []
                ListeVentVitesse = []
                ListeAirTemperature = []
                ListePression = []
                for ientity in qry3:
                    ListeHeure.append(ientity.updateday + ' ' + ientity.updateheure + ':' + ientity.updateminute + ':00')
                    ListeVentVitesse.append(ientity.vitesse)
                    ListeAirTemperature.append(ientity.temperature)
                    ListePression.append(ientity.pression)

                ListeHeureFmt = [datetime.datetime.strptime(DateIndex,"%Y-%m-%d %H:%M:%S") for DateIndex in ListeHeure]

                SelectedDateFrench = SelectedDate[8:10]+ "/" + SelectedDate[5:7]+ "/" + SelectedDate[0:4] + " de " + SelectedStartHour + "H00 à ".decode('utf-8') + SelectedEndHour + "H00"
            
                matplotlib.pyplot.title("Vitesse du vent à Léry-Poses, le ".decode('utf-8') + SelectedDateFrench)
                if SelectedSpot=="Le Crotoy":
                    matplotlib.pyplot.title("Vitesse du vent à Le Crotoy, le ".decode('utf-8') + SelectedDateFrench)

                matplotlib.pyplot.xlabel('Temps')
                if (SelectedUnit=="km/h"):
                    matplotlib.pyplot.ylabel('Vitesse (km/h)')
                    ListeVentVitesseAjustee = ListeVentVitesse
                if (SelectedUnit=="noeud"):
                    matplotlib.pyplot.ylabel('Vitesse (noeud)')
                    ListeVentVitesseAjustee = [round(l/1.852,1) for l in ListeVentVitesse] 
                matplotlib.pyplot.grid(True)
                matplotlib.pyplot.plot(ListeHeureFmt,ListeVentVitesseAjustee,linewidth=0.4,label=u"Relevés")
                # Linear interpolation of the data in order to have wind speed every minutes
                if ListeHeureFmt==[]:
                    NewListeHeureFmt = []
                    NewListeVentVitesse = []
                    NewListeAirTemperature = []
                    NewListePression = []
                else:
                    xp = []
                    for item in ListeHeureFmt:
                       xp.append((item-ListeHeureFmt[0]).total_seconds())
                    x = numpy.arange(0,xp[-1]+60,60)
                    NewListeVentVitesse = numpy.interp(x,xp,ListeVentVitesse)
                    NewListeAirTemperature = numpy.interp(x,xp,ListeAirTemperature)
                    NewListePression = numpy.interp(x,xp,ListePression)
                    NewListeHeureFmt = []
                    for item in x:
                        NewListeHeureFmt.append(ListeHeureFmt[0]+datetime.timedelta(seconds=item))
                
                (model_M1.ListeHeureFmtPrediction, model_M1.ListeVentVitessePrediction) = model_M1.predict(SelectedEndHourQuery,NewListeHeureFmt,NewListeVentVitesse,NewListeAirTemperature,NewListePression)
                (model_M2.ListeHeureFmtPrediction, model_M2.ListeVentVitessePrediction) = model_M2.predict(SelectedEndHourQuery,NewListeHeureFmt,NewListeVentVitesse,NewListeAirTemperature,NewListePression)
                (model_M3.ListeHeureFmtPrediction, model_M3.ListeVentVitessePrediction) = model_M3.predict(SelectedEndHourQuery,NewListeHeureFmt,NewListeVentVitesse,NewListeAirTemperature,NewListePression)
                (model_M3_v2.ListeHeureFmtPrediction, model_M3_v2.ListeVentVitessePrediction) = model_M3_v2.predict(SelectedEndHourQuery,NewListeHeureFmt,NewListeVentVitesse,NewListeAirTemperature,NewListePression)
                (model_M6.ListeHeureFmtPrediction, model_M6.ListeVentVitessePrediction) = model_M6.predict(SelectedEndHourQuery,NewListeHeureFmt,NewListeVentVitesse,NewListeAirTemperature,NewListePression)

                if (SelectedUnit=="km/h"):
                    M1_ListeVentVitessePredictionAjustee = model_M1.ListeVentVitessePrediction
                    M2_ListeVentVitessePredictionAjustee = model_M2.ListeVentVitessePrediction
                    M3_ListeVentVitessePredictionAjustee = model_M3.ListeVentVitessePrediction
                    M3_v2_ListeVentVitessePredictionAjustee = model_M3_v2.ListeVentVitessePrediction
                    M6_ListeVentVitessePredictionAjustee = model_M6.ListeVentVitessePrediction
                if (SelectedUnit=="noeud"):
                    M1_ListeVentVitessePredictionAjustee = [round(l/1.852,1) for l in model_M1.ListeVentVitessePrediction]
                    M2_ListeVentVitessePredictionAjustee = [round(l/1.852,1) for l in model_M2.ListeVentVitessePrediction] 
                    M3_ListeVentVitessePredictionAjustee = [round(l/1.852,1) for l in model_M3.ListeVentVitessePrediction]
                    M3_v2_ListeVentVitessePredictionAjustee = [round(l/1.852,1) for l in model_M3_v2.ListeVentVitessePrediction]
                    M6_ListeVentVitessePredictionAjustee = [round(l/1.852,1) for l in model_M6.ListeVentVitessePrediction]

                #matplotlib.pyplot.plot(model_M1.ListeHeureFmtPrediction,M1_ListeVentVitessePredictionAjustee,linewidth=0.4,color='r',label=u"Prévisions - M1")
                #matplotlib.pyplot.plot(model_M2.ListeHeureFmtPrediction,M2_ListeVentVitessePredictionAjustee,linewidth=0.8,color='r',label=u"Prévisions - M2")
                #matplotlib.pyplot.plot(model_M3.ListeHeureFmtPrediction,M3_ListeVentVitessePredictionAjustee,linewidth=0.6,color='y',label=u"Prévisions - M3")
                matplotlib.pyplot.plot(model_M3_v2.ListeHeureFmtPrediction,M3_v2_ListeVentVitessePredictionAjustee,linewidth=0.6,color='r',label=u"Prévisions - M3_v2")
                matplotlib.pyplot.plot(model_M6.ListeHeureFmtPrediction,M6_ListeVentVitessePredictionAjustee,linewidth=0.6,color='g',label=u"Prévisions - M6")

                matplotlib.pyplot.legend(loc='upper left')
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

            if SelectedSpot=="Lery-Poses":
                self.response.write("""<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip()) 
            if SelectedSpot=="Le Crotoy":
                self.response.write("""\n\nPas de modèle de prévision du vent dans l'heure pour Le Crotoy\n""") 
 
            self.response.write("""\n\nQuestions, commentaires ou bugs: <a href="mailto:myWindStats@gmail.com">myWindStats@gmail.com</a>""")
            if SelectedSpot=="Lery-Poses":
                self.response.write("""\n\nATTENTION: Les modèles de prévision du vent dans l'heure sont disponibles en version beta!\n           La qualité des prévisions est en cours de validation!\n""")
                self.response.write("""           Les modèles M3 et M6 sont basés sur les données météorologiques du 13 avril 2015 au 31 décembre 2015\n""")
                #self.response.write("""           M3   : prédiction 60mn à l'avance en utilisant les  3 derniers relevés (température, pression, vitesse vent)\n""")
                self.response.write("""           M3_v2: prédiction 60mn à l'avance en utilisant les  3 derniers relevés (température, pression, vitesse vent) - version vectorisée\n""")
                self.response.write("""           M6   : prédiction 20mn à l'avance en utilisant les 60 derniers relevés (température, pression, vitesse vent)\n""")
                self.response.write("""\nLes données météorologiques sont issues de la sonde de "troislacs - base de loisirs" """)
                if False:
                    self.response.write('\n\n')
                    for i,j in zip(ListeHeureFmt,ListeVentVitesse):
                        self.response.write(i)
                        self.response.write(' ')
                        self.response.write(j)
                        self.response.write('\n')
                    self.response.write(ListeHeureFmt)
                    self.response.write('\n')
                    self.response.write(ListeVentVitesse)
                    self.response.write('\n')
                if False:
                    for item in NewListeHeureFmt:
                        self.response.write(item)
                        self.response.write('\n')
                    for item in model_M1.ListeVentVitessePrediction:
                        self.response.write(item)
                        self.response.write('\n')

            self.response.write('</pre></body></html>') 

app = webapp2.WSGIApplication([('/shorttermforecast',ShortTermForecast)], debug=True)
