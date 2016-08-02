import cgi
import webapp2

MAIN_PAGE_HTML = """\
<html>
<head>
<link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
<link rel="icon" type="image/png" sizes="192x192"  href="/static/android-icon-192x192.png">
<link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
<link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
<link rel="manifest" href="/static/manifest.json">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
<meta name="theme-color" content="#ffffff">

<link rel="Stylesheet" type="text/css" href="/static/jquery-ui.min.css">
<script src="/static/jquery.js"></script>
<script src="/static/jquery-ui.min.js"></script>
<script>
    $(function() {
        if ( $( "#SelectedDate" ).prop('type') != 'date') {
            $( "#SelectedDate" ).datepicker({dateFormat:"yy-mm-dd",minDate:"2015-04-13",changeMonth:true,changeYear:true}).datepicker("setDate", new Date());
        } else {
            document.getElementById('SelectedDate').valueAsDate = new Date();
        }
});
</script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65403806-1', 'auto');
  ga('send', 'pageview');

</script>
</head>

<body>
<h1>myWindStats.com</h1>

<form action="/windhistory" method="post">
Spot:
<select name="S_Spot" id="Spot">
<option value="Le Crotoy">Le Crotoy</option>
<option value="Lery-Poses" selected>L&#233ry-Poses</option>
<option value="Mobile Anemometer">An&#233mom&#232tre portable</option>
</select>

<br><br>
Date: 
<input type="date" name="S_SelectedDate" id="SelectedDate" min="2015-04-13"><br><br>

Heure (d&#233but):
<select name="S_StartHour" id="StartHour">
<option value="00">0H00</option>
<option value="01">1H00</option>
<option value="02">2H00</option>
<option value="03">3H00</option>
<option value="04">4H00</option>
<option value="05">5H00</option>
<option value="06">6H00</option>
<option value="07">7H00</option>
<option value="08" selected>8H00</option>
<option value="09">9H00</option>
<option value="10">10H00</option>
<option value="11">11H00</option>
<option value="12">12H00</option>
<option value="13">13H00</option>
<option value="14">14H00</option>
<option value="15">15H00</option>
<option value="16">16H00</option>
<option value="17">17H00</option>
<option value="18">18H00</option>
<option value="19">19H00</option>
<option value="20">20H00</option>
<option value="21">21H00</option>
<option value="22">22H00</option>
<option value="23">23H00</option>
</select>
  Heure (fin):
<select name="S_EndHour" id="EndHour">
<option value="00">0H00</option>
<option value="01">1H00</option>
<option value="02">2H00</option>
<option value="03">3H00</option>
<option value="04">4H00</option>
<option value="05">5H00</option>
<option value="06">6H00</option>
<option value="07">7H00</option>
<option value="08">8H00</option>
<option value="09">9H00</option>
<option value="10">10H00</option>
<option value="11">11H00</option>
<option value="12">12H00</option>
<option value="13">13H00</option>
<option value="14">14H00</option>
<option value="15">15H00</option>
<option value="16">16H00</option>
<option value="17">17H00</option>
<option value="18" selected>18H00</option>
<option value="19">19H00</option>
<option value="20">20H00</option>
<option value="21">21H00</option>
<option value="22">22H00</option>
<option value="23">23H00</option>
</select>
<br><br><br>
<input type="submit" name="S_Graphe"                          value="Graphe de la vitesse du vent">
<input type="submit" formaction="/windrose" name="S_Graphe"   value="   Rose des vents   ">
<input type="submit" formaction="/allhistory" name="S_Graphe" value="Graphes des données météo"><br><br>
<input type="submit" formaction="/windtable" name="S_Graphe"  value="Tableau des données météo">
<input type="submit" formaction="/faq" name="S_Graphe"        value="Foire aux questions">
<input type="submit" formaction="/shorttermforecast" name="S_Graphe"  value="Prévision du vent dans l'heure"><br><br>
<!--<input type="submit" formaction="/winddump" name="S_Graphe"       value="Dump"><br><br>-->
<select name="S_Unit" id="Unit">
<option value="km/h">km/h</option>
<option value="noeud" selected>noeud</option>
</select>
</form>
<br><br><pre>Questions, commentaires ou bugs: <a href="mailto:myWindStats@gmail.com">myWindStats@gmail.com</a></pre>
<pre>Les données météorologiques de Léry-Poses sont issues de la sonde de "troislacs - base de loisirs"</pre>
</body>
</html>
"""


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
