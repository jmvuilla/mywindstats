# -*- coding: utf-8 -*-
import cgi
import webapp2

class FAQ(webapp2.RequestHandler):
    def post(self):
        SelectedGraph = cgi.escape(self.request.get('S_Graphe'))
        SelectedSpot = cgi.escape(self.request.get('S_Spot'))
        if SelectedGraph=="Foire aux questions":
            self.response.write("""
            <html><head>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65403806-1', 'auto');
  ga('send', 'pageview');

</script>
            """)
            self.response.write('<body>')
            self.response.write("""
<a name="pourquoi"></a>
<h1>Foire aux questions</h1>
<h2>Pourquoi cette foire aux questions?</h2>
<p>Cette foire aux questions recense les questions les plus fr&#233;quentes pos&#233;es par les utilisateurs du site Web myWindStats.com. Cette page est r&#233;guli&#232;rement mise &#224; jour en fonction des nouvelles questions des utilisateurs, ainsi que des nouvelles fonctions du site.</p>

<p>Vous pouvez soumettre vos questions par e-mail &#224; myWindStats@gmail.com.</p>

<p>La derni&#232;re mise &#224; jour de la foire aux questions remonte au 17/10/2015.</p>

<ul>
<li><a href="#pourquoi">Pourquoi cette foire aux questions?</a></li>
<li><a href="#objectifs">Quels sont les objectifs du site Web?</a></li>
<li><a href="#web">Pourquoi un n-ième site Web?</a></li>
<li><a href="#origine">Quelle est l'origine des données météorologiques?</a></li>
<li><a href="#donnees">Quelles sont les données météorologiques collectées?</a></li>
<li><a href="#selection">Pourquoi n’est-il pas possible de sélectionner une date avant le 13 avril 2015 ?</a></li>
<li><a href="#minuit">Comment sélectionner minuit comme heure de fin ?</a></li>
<li><a href="#noeud">A quoi sert le bouton "noeud"?</a></li>
<li><a href="#vitesse">Comment interpréter le graphe de la vitesse du vent?</a></li>
<li><a href="#rose">Comment interpréter la rose des vents?</a></li>
<li><a href="#graphes">Comment interpréter les graphes des données météorologiques?</a></li>
</ul>
<a name="objectifs"></a>
<h2>Quels sont les objectifs du site Web?</h2>
<p>Le premier objectif du site Web myWindStats.com est de fournir l'historique des donn&#233;es m&#233;t&#233;orologiques &#224; un groupuscule de v&#233;liplanchistes enthousiastes.</p>

<p>Le second objectif, encore &#224; l'&#233;tude, consiste &#224; utiliser des techniques de type r&#233;seau de neurones pour faire des pr&#233;dictions &#224; court terme, c'est &#224; dire quelques heures, bas&#233;es sur l'historique des donn&#233;es m&#233;t&#233;orologiques. Ces pr&#233;dictions peuvent compl&#233;ter avantageusement les mod&#232;les m&#233;t&#233;orologiques traditionnels. De nombreuses publications scientifiques ont montr&#233; que de telles pr&#233;dictions sont possibles et sont utilis&#233;es en production, par exemple pour pr&#233;dire la puissance &#233;lectrique des parcs &#233;oliens.</p>

<a name="web"></a>
<h2>Pourquoi un n-i&#232;me site Web?</h2>
<p>Les sites Web permettant de fournir l'historique des donn&#233;es m&#233;t&#233;orologiques sont nombreux.</p>

<p>myWindStats.com se distingue des autres sites Web par:</p>
<ul>
<li>la fr&#233;quence d'&#233;chantillonnage des donn&#233;es m&#233;t&#233;orologiques. Cette fr&#233;quence varie entre 0.75 et 1 &#233;chantillon par minute selon la station m&#233;t&#233;orologique. Les autres sites Web fournissant l'historique des donn&#233;es m&#233;t&#233;orologiques ont une fr&#233quence d'environ 0.2 échantillon par minute (soit 1 &#233;chantillon toutes les cinq &#224; six minutes).</li>
<li>l'utilisation des donn&#233;es brutes, notamment la vitesse instantan&#233;e du vent et non pas la moyenne mobile sur 10 minutes. Apr&#232;s tout, le v&#233;liplanchiste est propuls&#233; par le vent r&#233;el et non par un vent moyen...</li>
<li>la possibilit&#233; de s&#233;lectionner une plage horaire dans une journ&#233;e de son choix afin de mieux pouvoir &#233;tudier les donn&#233;es m&#233;t&#233;orologiques sur cette p&#233;riode.</li>
<li>la diversit&#233; des historiques propos&#233;s: depuis le simple graphe affichant la vitesse instantan&#233;e du vent en fonction du temps, la table ou les graphes de toutes les donn&#233;es m&#233;t&#233;orologiques en fonction du temps,  jusqu'&#224; la rose des vents.</li>
</ul>
<p></p>
<a name="origine"></a>
<h2>Quelle est l'origine des donn&#233;es m&#233;t&#233;orologiques?</h2>
Le site myWindStats.com collecte actuellement les donn&#233;es de deux stations m&#233;t&#233;orologiques bas&#233es &#224;:
<ul>
<li>Le Crotoy, et</li>
<li>L&#233;ry-Poses.</li>
</ul>

<p>Le site peut être facilement enrichi avec des nouvelles stations m&#233;t&#233;orologiques. Si vous êtes int&#233;ress&#233; pour en rajouter une, contactez myWindStats@gmail.com.</p>

<a name="donnees"></a>
<h2>Quelles sont les donn&#233;es m&#233;t&#233;orologiques collect&#233;es?</h2>
<p>Le site Web myWindStats.com collecte les donn&#233;es suivantes.</p>
<ul>
<li>La vitesse instantan&#233;e du vent</li>
<ul>
<li>Unit&#233;: noeud ou km/h</li>
<li>Pr&#233;cision: 1km/h</li>
</ul>
<li>La direction instantan&#233;e du vent</li>
<ul>
<li>Unit&#233;: points cardinaux (N, E, S, O) et intercardinaux (NNE, NE, ENE, ESE, SE, SSE, SSO, SO, OSO, ONO, NO, NNO)</li>
<li>Pr&#233;cision: 22.5°</li>
</ul>
<li>La temp&#233;rature de l'air</li>
<ul>
<li>Unit&#233;: °C</li>
<li>Pr&#233;cision: 1°C</li>
</ul>
<li>Le taux d'humidit&#233; dans l'air</li>
<ul>
<li>Unit&#233;: %</li>
<li>Pr&#233;cision: 1 %</li>
</ul>
<li>Les pr&#233;cipitations cumul&#233;es quotidiennes</li>
<ul>
<li>Unit&#233;: mm</li>
<li>Pr&#233;cision: 0.1mm</li>
<li>Commentaire : le cumul est remis à z&#233;ro &#224; minuit ou vers 2h00 du matin selon la station m&#233;t&#233;orologique
</ul>
<li>La pression atmosph&#233;rique</li>
<ul>
<li>Unit&#233;: hPa</li>
<li>Pr&#233;cision: 0.1hPa</li>
</ul>
</ul>
<p>Toutes ces donn&#233;es sont collect&#233es et enregistr&#233;es &#224; la fr&#233;quence de:</p>
<ul>
<li>1 &#233;chantillon par minute pour la sonde m&#233;t&#233;orologique du Crotoy, et</li>
<li>0.75 &#233;chantillon par minute (soit 3 &#233;chantillons toutes les 4 minutes) pour la sonde m&#233;t&#233;orologique de L&#233;ry-Poses.</li>
</ul>

<p>Durant les p&#233;riodes de panne ou de maintenance des stations m&#233;t&#233;orologiques (ou de leurs connexions Internet), certains &#233;chantillons ne sont pas collect&#233;s ou enregistr&#233s.
Ces interruptions de service sont visibles sur les graphes, et tout particuli&#232;rement le graphe de la vitesse du vent, sous la forme d'une ligne parfaitement droite reliant deux &#233;chantillons (le dernier pr&#233;lev&#233; avant la panne, et le premier pr&#233;lev&#233; apr&#232;s la panne). La figure ci-dessous illustre un exemple de panne le 5 juin 2015 entre 11h20 et 12h36.</p>
<img src="/static/panneimg.png" style="width:608px;height:456px;">

<a name="selection"></a>
<h2>Pourquoi n’est-il pas possible de s&#233;lectionner une date avant le 13 avril 2015 ?</h2>
<p>Le site myWindStats.com collecte des donn&#233;es m&#233;t&#233;orologiques depuis :
<ul>
<li>le 13 avril 2015 pour la sonde m&#233;t&#233;orologique de L&#233;ry-Poses, et</li>
<li>le 10 ao&#251;t 2015 pour la sonde m&#233;t&#233;orologique du Crotoy.</li>
</ul>
</p>

<p>Il n’est, par cons&#233;quent, pas possible de s&#233;lectionner une date ant&#233;rieure au 13 avril 2015.</p>
<p>Le site myWindStats ne dispose pas de donn&#233;e m&#233;t&#233;orologique pour Le Crotoy entre le 13 avril 2015 et le 10 ao&#251;t 2015.
<ul>
<li>Les graphes pour Le Crotoy entre le 13 avril 2015 et le 10 ao&#251;t 2015 sont vides.</li>
<li>Les roses des vents pour le Crotoy entre le 13 avril 2015 et le 10 ao&#251;t 2015 ne sont pas g&#233;n&#233;r&#233;es. Le message suivant appara&#238;t en lieu et place de la rose des vents : "Il n'est pas possible de g&#233;n&#233;rer la rose des vents &#224; la date et sur la plage horaire donn&#233;es, soit parce qu'il n'y a pas de vent sur cette p&#233;riode, soit parce que les donn&#233;es m&#233;t&#233;orologiques provenant de la station ne sont pas valides".</li>
<li>Les tableaux pour le Crotoy entre le 13 avril 2015 et le 10 ao&#251;t 2015 sont vides.</li>
</ul>
</p>

<a name="minuit"></a>
<h2>Comment s&#233;lectionner minuit comme heure de fin ?</h2>
<p>Pour s&#233;lectionner minuit comme heure de fin de la plage horaire, il faut choisir l’option "0H00".</p>
<p>Ainsi, pour sélectionner toutes les heures d’une journée, l’heure de début et l’heure de fin doivent être fix&#233;es &#224; "0H00".</p>

<a name="noeud"></a>
<h2>A quoi sert le bouton "noeud"?</h2>
<p>Le bouton "noeud" permet de s&#233;lectionner l’unit&#233; de vitesse du vent utilis&#233;e pour tous les graphes, la rose des vents, ainsi que le tableau des donn&#233;es m&#233;t&#233;orologiques.
Le site myWindStats.com permet d’afficher les vitesses du vent soit en noeud, soit en km/h.</p>
<p>Pour m&#233;moire : 1 noeud = 1.852km/h.</p>

<a name="vitesse"></a>
<h2>Comment interpr&#233;ter le graphe de la vitesse du vent?</h2>
<p>Le graphe de la vitesse du vent en fonction du temps affiche l'historique sous la forme d'une courbe reliant les &#233;chantillons de la vitesse instantan&#233;e du vent (voir la figure ci-dessous).<p>

<p>Cette repr&#233;sentation, bien qu'incorrecte, est tr&#232;s pratique.</p>
<img src="/static/plotimg.png" style="width:608px;height:456px;">
<p>Cette repr&#233;sentation est incorrecte parce qu'elle donne l'illusion de connaitre l'historique des donn&#233;es m&#233;t&#233;orologiques entre deux &#233;chantillons successifs. Par exemple, supposons que l'historique des donn&#233;es m&#233;t&#233;orologiques inclut une vitesse instantan&#233;e de 10km/h &#224; 9h00, puis 30km/h &#224; 9h01, le graphe de la vitesse du vent en fonction du temps montrera une ligne droite entre ces deux &#233;chantillons. Or, il est tout &#224; fait possible que la vitesse du vent ait chut&#233; ou augment&#233; (&#224; cause d'une molle ou d'une rafale) entre ces deux &#233;chantillons, et ce plusieurs fois!</p>
<p>Cette repr&#233;sentation est n&#233;anmoins pratique, car elle facilite la lecture du graphe. Une repr&#233;sentation plus exacte aurait consist&#233; &#224; afficher les points correspondant aux &#233;chantillons, et &#224; ne pas les relier entre eux par des lignes droites (voir la figure ci-dessous).</p>
<img src="/static/scatterimg.png" style="width:608px;height:456px;">

<a name="rose"></a>
<h2>Comment interpr&#233;ter la rose des vents?</h2>
<p>La rose des vents permet de repr&#233;senter graphiquement la distribution du vent en fonction de sa direction et de sa vitesse.</p>
<p>Prenons l'exemple de la journ&#233;e du 18 avril 2015 entre 8h00 et 18h00 (voir la figure ci-dessous). </p>
<img src="/static/roseimg.png" style="width:608px;height:621px;">

<p>Le vent a souffl&#233; principalement de l'Est (60.6 % du temps), et dans une moindre mesure de Est-Nord-Est (environ 30 % du temps).</p>
<p>Si on veut &#233;tudier la distribution du vent d'Est en fonction de la vitesse, il est n&#233;cessaire de se r&#233;f&#233;rer &#224; la l&#233;gende. Elle fournit, en effet, la correspondance entre les couleurs et les plages de vitesse. Ainsi,</p>
<ul>
<li>le vent a souffl&#233; &#224; environ 18 % du temps entre 9.6 noeud et 13.2 noeud (triangle bleu marine),</li>
<li>le vent a souffl&#233;  &#224; environ 18 % du temps entre 13.2 noeud et 16.8 noeud (trap&#232ze bleu clair), et</li>
<li>le vent a souffl&#233;  &#224; environ 24 % du temps entre 16.8 noeud et 20.4 noeud (trap&#232ze vert clair).</li>
</ul>
<p>La l&#233;gende fournit &#233;galement la distribution du vent en fonction de la vitesse, quelle que soit sa direction. Ainsi, le 18 avril 2015 entre 8h00 et 18h00 :</p>
<ul>
<li>le vent a souffl&#233; &#224; 31 % du temps entre 13.2 et 16.8 nœud, et</li>
<li>le vent a souffl&#233; &#224; 31 + 37 + 4 +1 = 73 % du temps au dessus de 13.2 nœud. Une bonne session !</li>
</ul>
<p>Il est &#224; noter que la rose des vents est construite en &#233;liminant tous les &#233;chantillons pour lesquels la vitesse instantan&#233;e du vent est nulle. En effet, ces &#233;chantillons ne trouvent pas leur place sur la rose des vents. Par cons&#233;quent, la rose des vents est un mode de repr&#233;sentation &#224; privil&#233;gier pour analyser des sessions bien ventées.</p>

<a name="graphes"></a>
<h2>Comment interpr&#233;ter les graphes des donn&#233;es m&#233;t&#233;orologiques?</h2>
<p>Les graphes des donn&#233;es m&#233;t&#233;orologiques permettent de repr&#233;senter graphiquement l'historique de:
<ul>
<li>la vitesse instantan&#233;e du vent,</li>
<li>la direction instantan&#233;e du vent, </li>
<li>la temp&#233;rature de l'air,</li>
<li>le taux d'humidit&#233; dans l'air,</li>
<li>les pr&#233;cipitations cumul&#233;es quotidiennes, et</li>
<li>la pression atmosph&#233;rique.</li>
</ul>
</p>

<p>
Les six graphes ont tous la m&#234;me origine et la m&#234;me &#233;chelle des temps sur l'axe horizontal, ce qui permet de facilement faire correspondre un &#233;v&#232;nement sur une donn&#233;e avec les autres donn&#233;es.
</p>
<p>
Prenons l'exemple de l'apr&#232;s-midi du 6 mai 2015 entre 14h00 et 18h00 (voir la figure ci-dessous).
</p>
<img src="/static/graphesimg.png" style=width:608px;height:456px;">
<p>
Il y a une forte corr&#233;lation entre la mont&#233;e brutale de la pression peu apr&#232;s 15h40, et le passage d'un grain avec une vitesse instantan&#233;e du vent maximum de 37 noeud, ainsi que des pr&#233;cipitations cumul&#233;es de 1mm. Il est &#233;galement possible d'appr&#233;cier l'impact des pr&#233;cipitations sur le taux d'humidit&#233; de l'air, ainsi que sa temp&#233;rature.
</p>
<p>
Il est &#224; noter un traitement particulier pour afficher la direction instantan&#233;e d'&#233;chantillons ayant une vitesse instantan&#233;e du vent nulle. Pour &#233;viter des "trous" sur le graphe de la direction du vent, les &#233;chantillons ayant une vitesse nulle sont repr&#233;sent&#233;s avec la m&#234;me direction du vent que l'&#233;chantillon le plus r&#233;cent le pr&#233;c&#233;dant dans le temps avec une vitesse non nulle. La figure ci-dessous illustre ce choix (un peu arbitraire) de repr&#233;sentation.
</p>
<p>
<img src="/static/vitessenulleimg.png" style=width:608px;height:456px;">
</p>
""")
            self.response.write("""\n\n\n\nQuestions, commentaires ou bugs: <a href="mailto:myWindStats@gmail.com">myWindStats@gmail.com</a>""")
            if SelectedSpot=="Lery-Poses":
                self.response.write("""\nLes donn&#233;es m&#233;t&#233;orologiques sont issues de la sonde de "troislacs - base de loisirs" """)
            self.response.write('</pre></body></html>') 

app = webapp2.WSGIApplication([('/faq',FAQ)], debug=True)
