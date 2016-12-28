import cgi
from google.appengine.ext import ndb
import webapp2
import matplotlib
import matplotlib.pyplot
import datetime
import StringIO


import matplotlib
import matplotlib.cm as cm
import numpy as np
from matplotlib.patches import Rectangle, Polygon
from matplotlib.ticker import ScalarFormatter, AutoLocator
from matplotlib.text import Text, FontProperties
from matplotlib.projections.polar import PolarAxes
from numpy.lib.twodim_base import histogram2d
import matplotlib.pyplot as plt
from pylab import poly_between

RESOLUTION = 100
ZBASE = -1000 #The starting zorder for all drawing, negative to have the grid on

class WindroseAxes(PolarAxes):
    """

    Create a windrose axes

    """

    def __init__(self, *args, **kwargs):
        """
        See Axes base class for args and kwargs documentation
        """
        
        #Uncomment to have the possibility to change the resolution directly 
        #when the instance is created
        #self.RESOLUTION = kwargs.pop('resolution', 100)
        PolarAxes.__init__(self, *args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.radii_angle = 67.5
        self.cla()


    def cla(self):
        """
        Clear the current axes
        """
        PolarAxes.cla(self)

        self.theta_angles = np.arange(0, 360, 45)
        self.theta_labels = ['E', 'N-E', 'N', 'N-O', 'O', 'S-O', 'S', 'S-E']
        self.set_thetagrids(angles=self.theta_angles, labels=self.theta_labels)

        self._info = {'dir' : list(),
                      'bins' : list(),
                      'table' : list()}

        self.patches_list = list()


    def _colors(self, cmap, n):
        '''
        Returns a list of n colors based on the colormap cmap

        '''
        return [cmap(i) for i in np.linspace(0.0, 1.0, n)]


    def set_radii_angle(self, **kwargs):
        """
        Set the radii labels angle
        """

        null = kwargs.pop('labels', None)
        angle = kwargs.pop('angle', None)
        if angle is None:
            angle = self.radii_angle
        self.radii_angle = angle
        radii = np.linspace(0.1, self.get_rmax(), 6)
        radii_labels = [ "%.1f%%" %r for r in radii ]
        radii_labels[0] = "" #Removing label 0
        null = self.set_rgrids(radii=radii, labels=radii_labels,
                               angle=self.radii_angle, **kwargs)


    def _update(self):
        self.set_rmax(rmax=np.max(np.sum(self._info['table'], axis=0)))
        self.set_radii_angle(angle=self.radii_angle)


    def legend(self, UniteVitesse, loc='lower right', **kwargs):
        """
        Sets the legend location and her properties.
        The location codes are

          'best'         : 0,
          'upper right'  : 1,
          'upper left'   : 2,
          'lower left'   : 3,
          'lower right'  : 4,
          'right'        : 5,
          'center left'  : 6,
          'center right' : 7,
          'lower center' : 8,
          'upper center' : 9,
          'center'       : 10,

        If none of these are suitable, loc can be a 2-tuple giving x,y
        in axes coords, ie,

          loc = (0, 1) is left top
          loc = (0.5, 0.5) is center, center

        and so on.  The following kwargs are supported:

        isaxes=True           # whether this is an axes legend
        prop = FontProperties(size='smaller')  # the font property
        pad = 0.2             # the fractional whitespace inside the legend border
        shadow                # if True, draw a shadow behind legend
        labelsep = 0.005     # the vertical space between the legend entries
        handlelen = 0.05     # the length of the legend lines
        handletextsep = 0.02 # the space between the legend line and legend text
        axespad = 0.02       # the border between the axes and legend edge
        """

        def get_handles():
            handles = list()
            for p in self.patches_list:
                if isinstance(p, matplotlib.patches.Polygon) or \
                isinstance(p, matplotlib.patches.Rectangle):
                    color = p.get_facecolor()
                elif isinstance(p, matplotlib.lines.Line2D):
                    color = p.get_color()
                else:
                    raise AttributeError("Can't handle patches")
                handles.append(Rectangle((0, 0), 0.2, 0.2,
                    facecolor=color, edgecolor='black'))
            return handles

        def get_labels(UniteVitesse):
            labels = np.copy(self._info['bins'])
            jmvper = range(6) 
            for jmvrow in range(6):
                jmvper[jmvrow] = 0.0
                for jmvcol in range(16):
                    jmvper[jmvrow] = jmvper[jmvrow] + self._info['table'][jmvrow,jmvcol]

            if (UniteVitesse=="km/h"):
                labels = ["%4.0f%%    [%.1f km/h: %0.1f km/h[" %(jmvper[i], labels[i], labels[i+1]) \
                          for i in range(len(labels)-1)]
            if (UniteVitesse=="noeud"):
                labels = ["%4.0f%%    [%.1f noeud: %0.1f noeud[" %(jmvper[i], labels[i], labels[i+1]) \
                          for i in range(len(labels)-1)] 
            return labels

        null = kwargs.pop('labels', None)
        null = kwargs.pop('handles', None)
        handles = get_handles()
        labels = get_labels(UniteVitesse)
        self.legend_ = matplotlib.legend.Legend(self, handles, labels,
                                                loc, **kwargs)
        return self.legend_


    def _init_plot(self, dir, var, **kwargs):
        """
        Internal method used by all plotting commands
        """
        #self.cla()
        null = kwargs.pop('zorder', None)

        #Init of the bins array if not set
        bins = kwargs.pop('bins', None)
        if bins is None:
            bins = np.linspace(np.min(var), np.max(var), 6)
        if isinstance(bins, int):
            bins = np.linspace(np.min(var), np.max(var), bins)
        bins = np.asarray(bins)
        nbins = len(bins)

        #Number of sectors
        nsector = kwargs.pop('nsector', None)
        if nsector is None:
            nsector = 16

        #Sets the colors table based on the colormap or the "colors" argument
        colors = kwargs.pop('colors', None)
        cmap = kwargs.pop('cmap', None)
        if colors is not None:
            if isinstance(colors, str):
                colors = [colors]*nbins
            if isinstance(colors, (tuple, list)):
                if len(colors) != nbins:
                    raise ValueError("colors and bins must have same length")
        else:
            if cmap is None:
                cmap = cm.jet
            colors = self._colors(cmap, nbins)

        #Building the angles list
        angles = np.arange(0, -2*np.pi, -2*np.pi/nsector) + np.pi/2

        normed = kwargs.pop('normed', False)
        blowto = kwargs.pop('blowto', False)

        #Set the global information dictionnary
        self._info['dir'], self._info['bins'], self._info['table'] = histogram(dir, var, bins, nsector, normed, blowto)

        return bins, nbins, nsector, colors, angles, kwargs


    def contour(self, dir, var, **kwargs):
        """
        Plot a windrose in linear mode. For each var bins, a line will be
        draw on the axes, a segment between each sector (center to center).
        Each line can be formated (color, width, ...) like with standard plot
        pylab command.

        Mandatory:
        * dir : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6, then
            bins=linspace(min(var), max(var), 6)
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.

        others kwargs : see help(pylab.plot)

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(dir, var,
                                                                       **kwargs)

        #closing lines
        angles = np.hstack((angles, angles[-1]-2*np.pi/nsector))
        vals = np.hstack((self._info['table'],
                         np.reshape(self._info['table'][:,0],
                                   (self._info['table'].shape[0], 1))))
        
        offset = 0
        for i in range(nbins):
            val = vals[i,:] + offset
            offset += vals[i, :]
            zorder = ZBASE + nbins - i
            patch = self.plot(angles, val, color=colors[i], zorder=zorder,
                              **kwargs)
            self.patches_list.extend(patch)
        self._update()


    def contourf(self, dir, var, **kwargs):
        """
        Plot a windrose in filled mode. For each var bins, a line will be
        draw on the axes, a segment between each sector (center to center).
        Each line can be formated (color, width, ...) like with standard plot
        pylab command.

        Mandatory:
        * dir : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6, then
            bins=linspace(min(var), max(var), 6)
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.

        others kwargs : see help(pylab.plot)

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(dir, var,
                                                                       **kwargs)
        null = kwargs.pop('facecolor', None)
        null = kwargs.pop('edgecolor', None)
        
        #closing lines
        angles = np.hstack((angles, angles[-1]-2*np.pi/nsector))
        vals = np.hstack((self._info['table'],
                         np.reshape(self._info['table'][:,0],
                                   (self._info['table'].shape[0], 1))))
        offset = 0
        for i in range(nbins):
            val = vals[i,:] + offset
            offset += vals[i, :]
            zorder = ZBASE + nbins - i
            xs, ys = poly_between(angles, 0, val)
            patch = self.fill(xs, ys, facecolor=colors[i],
                              edgecolor=colors[i], zorder=zorder, **kwargs)
            self.patches_list.extend(patch)


    def bar(self, dir, var, **kwargs):
        """
        Plot a windrose in bar mode. For each var bins and for each sector,
        a colored bar will be draw on the axes.

        Mandatory:
        * dir : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6 between min(var) and max(var).
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.
        edgecolor : string - The string color each edge bar will be plotted.
        Default : no edgecolor
        * opening : float - between 0.0 and 1.0, to control the space between
        each sector (1.0 for no space)

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(dir, var,
                                                                       **kwargs)
        null = kwargs.pop('facecolor', None)
        edgecolor = kwargs.pop('edgecolor', None)
        if edgecolor is not None:
            if not isinstance(edgecolor, str):
                raise ValueError('edgecolor must be a string color')
        opening = kwargs.pop('opening', None)
        if opening is None:
            opening = 0.8
        dtheta = 2*np.pi/nsector
        opening = dtheta*opening

        for j in range(nsector):
            offset = 0
            for i in range(nbins):
                if i > 0:
                    offset += self._info['table'][i-1, j]
                val = self._info['table'][i, j]
                zorder = ZBASE + nbins - i
                patch = Rectangle((angles[j]-opening/2, offset), opening, val,
                    facecolor=colors[i], edgecolor=edgecolor, zorder=zorder,
                    **kwargs)
                self.add_patch(patch)
                if j == 0:
                    self.patches_list.append(patch)
        self._update()
        # added sept 6
        return bins, nbins, nsector, colors, angles, self._info['table']

    def box(self, dir, var, **kwargs):
        """
        Plot a windrose in proportional bar mode. For each var bins and for each
        sector, a colored bar will be draw on the axes.

        Mandatory:
        * dir : 1D array - directions the wind blows from, North centred
        * var : 1D array - values of the variable to compute. Typically the wind
        speeds
        Optional:
        * nsector: integer - number of sectors used to compute the windrose
        table. If not set, nsectors=16, then each sector will be 360/16=22.5°,
        and the resulting computed table will be aligned with the cardinals
        points.
        * bins : 1D array or integer- number of bins, or a sequence of
        bins variable. If not set, bins=6 between min(var) and max(var).
        * blowto : bool. If True, the windrose will be pi rotated,
        to show where the wind blow to (usefull for pollutant rose).
        * colors : string or tuple - one string color ('k' or 'black'), in this
        case all bins will be plotted in this color; a tuple of matplotlib
        color args (string, float, rgb, etc), different levels will be plotted
        in different colors in the order specified.
        * cmap : a cm Colormap instance from matplotlib.cm.
          - if cmap == None and colors == None, a default Colormap is used.
        edgecolor : string - The string color each edge bar will be plotted.
        Default : no edgecolor

        """

        bins, nbins, nsector, colors, angles, kwargs = self._init_plot(dir, var,
                                                                       **kwargs)
        null = kwargs.pop('facecolor', None)
        edgecolor = kwargs.pop('edgecolor', None)
        if edgecolor is not None:
            if not isinstance(edgecolor, str):
                raise ValueError('edgecolor must be a string color')
        opening = np.linspace(0.0, np.pi/16, nbins)

        for j in range(nsector):
            offset = 0
            for i in range(nbins):
                if i > 0:
                    offset += self._info['table'][i-1, j]
                val = self._info['table'][i, j]
                zorder = ZBASE + nbins - i
                patch = Rectangle((angles[j]-opening[i]/2, offset), opening[i],
                    val, facecolor=colors[i], edgecolor=edgecolor,
                    zorder=zorder, **kwargs)
                self.add_patch(patch)
                if j == 0:
                    self.patches_list.append(patch)
        self._update()

def histogram(dir, var, bins, nsector, normed=False, blowto=False):
    """
    Returns an array where, for each sector of wind
    (centred on the north), we have the number of time the wind comes with a
    particular var (speed, polluant concentration, ...).
    * dir : 1D array - directions the wind blows from, North centred
    * var : 1D array - values of the variable to compute. Typically the wind
        speeds
    * bins : list - list of var category against we're going to compute the table
    * nsector : integer - number of sectors
    * normed : boolean - The resulting table is normed in percent or not.
    * blowto : boolean - Normaly a windrose is computed with directions
    as wind blows from. If true, the table will be reversed (usefull for
    pollutantrose)

    """

    if len(var) != len(dir):
        raise ValueError("var and dir must have same length")

    angle = 360./nsector

    dir_bins = np.arange(-angle/2 ,360.+angle, angle, dtype=np.float)
    dir_edges = dir_bins.tolist()
    dir_edges.pop(-1)
    dir_edges[0] = dir_edges.pop(-1)
    dir_bins[0] = 0.

    var_bins = bins.tolist()
    var_bins.append(np.inf)

    if blowto:
        dir = dir + 180.
        dir[dir>=360.] = dir[dir>=360.] - 360

    table = histogram2d(x=var, y=dir, bins=[var_bins, dir_bins],
                          normed=False)[0]
    # add the last value to the first to have the table of North winds
    table[:,0] = table[:,0] + table[:,-1]
    # and remove the last col
    table = table[:, :-1]
    if normed:
        table = table*100/table.sum()

    return dir_edges, var_bins, table


def wrcontour(dir, var, **kwargs):
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect)
    fig.add_axes(ax)
    ax.contour(dir, var, **kwargs)
    l = ax.legend(axespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)
    plt.draw()
    plt.show()
    return ax

def wrcontourf(dir, var, **kwargs):
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect)
    fig.add_axes(ax)
    ax.contourf(dir, var, **kwargs)
    l = ax.legend(axespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)
    plt.draw()
    plt.show()
    return ax

def wrbox(dir, var, **kwargs):
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect)
    fig.add_axes(ax)
    ax.box(dir, var, **kwargs)
    l = ax.legend(axespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)
    plt.draw()
    plt.show()
    return ax

def wrbar(dir, var, **kwargs):
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect)
    fig.add_axes(ax)
    ax.bar(dir, var, **kwargs)
    l = ax.legend(axespad=-0.10)
    plt.setp(l.get_texts(), fontsize=8)
    plt.draw()
    plt.show()
    return ax

def clean(dir, var):
    '''
    Remove masked values in the two arrays, where if a direction data is masked,
    the var data will also be removed in the cleaning process (and vice-versa)
    '''
    dirmask = dir.mask==False
    varmask = var.mask==False
    ind = dirmask*varmask
    return dir[ind], var[ind]

if __name__=='__main__':
    from pylab import figure, show, setp, random, grid, draw
    vv=random(500)*6
    dv=random(500)*360
    fig = figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)

#    ax.contourf(dv, vv, bins=np.arange(0,8,1), cmap=cm.hot)
#    ax.contour(dv, vv, bins=np.arange(0,8,1), colors='k')
#    ax.bar(dv, vv, normed=True, opening=0.8, edgecolor='white')
    ax.box(dv, vv, normed=True)
    l = ax.legend(axespad=-0.10)
    setp(l.get_texts(), fontsize=8)
    draw()
    #print ax._info
    show()


import time
import datetime
import matplotlib.pyplot
import matplotlib.cm

def new_axes():
    fig = matplotlib.pyplot.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax, canvas

def set_legend(UniteVitesse, ax):
    l = ax.legend(UniteVitesse, borderaxespad=-3.8)
    plt.setp(l.get_texts(), fontsize=8)


# Create your views here.
def index(request,dateplagehoraire):

    rows = Releves.objects.all()
    SelectedDate = dateplagehoraire[6:10] + "-" + dateplagehoraire[3:5] + "-" + dateplagehoraire[0:2]
    SelectedHourStart = dateplagehoraire[11:13]
    SelectedHourEnd   = dateplagehoraire[14:16]
    UniteVitesse = dateplagehoraire[17:]

    # JMV - remove the 3 following lines in production
    #SelectedDate = "2015-02-28"
    #SelectedHourStart = "08"
    #SelectedHourEnd = "18"

    ListeVentDirection = []
    ListeVentVitesse = []

    CompassDict = {'N':0.0, 'NNE':22.5, 'NE':45.0, 'ENE':67.5, 'E':90.0, 'ESE':112.5, 'SE':135, 'SSE':157.5, 'S':180.0, 'SSW':202.5, 'SW':225.0, 'WSW':247.5, 'W':270.0, 'WNW':292.5, 'NW':315.0, 'NNW':337.5, '':-1}

    for row in rows:
        if row.dateupdate.startswith(SelectedDate):
            if row.dateupdate[11:13] >= SelectedHourStart and row.dateupdate[11:13] < SelectedHourEnd:
                ListeVentDirection.append(CompassDict[row.direction])
                if (UniteVitesse=="km/h"):
                    ListeVentVitesse.append(row.vitesse)
                if (UniteVitesse=="noeud"):
                    #ListeVentVitesse.append(int(str(round(row.vitesse/1.852))))
                    ListeVentVitesse.append(round(row.vitesse/1.852,1))

    if all(ijmv==-1 for ijmv in ListeVentDirection):
       return HttpResponse("""
<p>Il n'est pas possible de générer la rose des vents à la date et sur la plage horaire données:</p><br>
<p> - soit parce qu'il n'y a pas de vent sur cette période, </p><br>
<p> - soit parce que les données météorologiques provenant de la station ne sont pas valides.</p>
""")
    else:
        from numpy.random import random
        from numpy import arange, array
        ws = array(ListeVentVitesse)
        wd = array(ListeVentDirection)

        #windrose like a stacked histogram with normed (displayed in percent) results
        matplotlib.use('Agg')
     
        ax, canvas = new_axes()
        bins, nbins, nsector, colors, angles, table = ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
        set_legend(UniteVitesse, ax)
        SelectedDateFrench = SelectedDate[8:10]+ "/" + SelectedDate[5:7]+ "/" + SelectedDate[0:4] + " de " + SelectedHourStart + "H00 à " + SelectedHourEnd + "H00"
        matplotlib.pyplot.title('Rose des vents à Léry-Poses, le ' + SelectedDateFrench, y=1.075)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response


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


class WindRose(webapp2.RequestHandler):
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

        if SelectedGraph=="   Rose des vents   ":
            ListeVentDirection = []
            ListeVentVitesse = []
            CompassDict = {'N':0.0, 'NNE':22.5, 'NE':45.0, 'ENE':67.5, 'E':90.0, 'ESE':112.5, 'SE':135, 'SSE':157.5, 'S':180.0, 'SSW':202.5, 'SW':225.0, 'WSW':247.5, 'W':270.0, 'WNW':292.5, 'NW':315.0, 'NNW':337.5, '':-1}
            for ientity in qry3:
                ListeVentDirection.append(CompassDict[ientity.direction])
                if SelectedUnit=="km/h":
                    ListeVentVitesse.append(ientity.vitesse)
                if SelectedUnit=="noeud":
                    ListeVentVitesse.append(round(ientity.vitesse/1.852,1))
            
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

            if all(ijmv==-1 for ijmv in ListeVentDirection):
                self.response.write("""
                <p>Il n'est pas possible de générer la rose des vents à la date et sur la plage horaire données,
                soit parce qu'il n'y a pas de vent sur cette période, soit parce que les données météorologiques
                provenant de la station ne sont pas valides.</p>
                """)
            else:
                from numpy.random import random
                from numpy import arange, array
                ws = array(ListeVentVitesse)
                wd = array(ListeVentDirection)

                #windrose like a stacked histogram with normed (displayed in percent) results
                
     
                ax, canvas = new_axes()
                bins, nbins, nsector, colors, angles, table = ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
                set_legend(SelectedUnit, ax)
                SelectedDateFrench = SelectedDate[8:10]+ "/" + SelectedDate[5:7]+ "/" + SelectedDate[0:4] + " de " + SelectedStartHour + "H00 à ".decode('utf-8') + SelectedEndHour + "H00"
                if SelectedSpot=="Lery-Poses":
                    matplotlib.pyplot.title('Rose des vents à Léry-Poses, le '.decode('utf-8') + SelectedDateFrench, y=1.075)
                if SelectedSpot=="Le Crotoy":
                    matplotlib.pyplot.title('Rose des vents à Le Crotoy, le '.decode('utf-8') + SelectedDateFrench, y=1.075) 
                rv = StringIO.StringIO()
                matplotlib.pyplot.savefig(rv,format="png")
                matplotlib.pyplot.clf()
                self.response.write("""<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip())
                if (False): # if True, debug messages
                    self.response.write("\nDEBUG=ON\nNombre d'echantillons: %d\n" % len(ListeVentDirection))
                    NumberOfEchantillonSpeedNonNull = 0
                    for ijmv in ListeVentDirection:
                        if ijmv!=-1:
                            NumberOfEchantillonSpeedNonNull = NumberOfEchantillonSpeedNonNull + 1
                    self.response.write("Nombre d'echantillons a vitesse non nulle: %d\n" % NumberOfEchantillonSpeedNonNull)

                    self.response.write("Wind Speed Array\n")
                    self.response.write(ws)
                    self.response.write("\nWind Direction Array\n")
                    self.response.write(wd)
                    self.response.write("\nBins\n")
                    self.response.write(bins)
                    self.response.write("\nNBins\n")
                    self.response.write(nbins)
                    self.response.write("\nNSectors\n")
                    self.response.write(nsector)
                    self.response.write("\nAngles\n")
                    self.response.write(angles)
                    self.response.write("\nTable\n")
                    self.response.write(table)
                    self.response.write("\n")
                    sumall = 0.0
                    for row in range(6):
                        sum = 0.0
                        for col in range(16):
                            sum = sum + table[row,col]
                        self.response.write("Row %d > Sum = %f\n" % (row,sum))
                        sumall = sumall + sum
                    self.response.write("All rows > Sum = %f\n" % sumall)
                    
                    sumall = 0.0
                    for col in range(16):
                        sum = 0.0
                        for row in range(6):
                            sum = sum + table[row,col]
                        self.response.write("Col %d > Sum = %f\n" % (col,sum))
                        sumall = sumall + sum
                    self.response.write("All cols > Sum = %f\n" % sumall)

                    self.response.write("\nDEBUG=OFF\n")
 

            self.response.write("""\n\nQuestions, commentaires ou bugs: <a href="mailto:myWindStats@gmail.com">myWindStats@gmail.com</a>""")
            if SelectedSpot=="Lery-Poses":
                self.response.write("""\nLes données météorologiques sont issues de la sonde de "troislacs - base de loisirs" """)
            self.response.write('</pre></body></html>')


app = webapp2.WSGIApplication([('/windrose',WindRose)], debug=True)
