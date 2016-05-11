
DEBUG = 3

if(DEBUG == 1):
    from matplotlib.pyplot import figure, show
    import numpy as npy
    from numpy.random import rand


    if 1: # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)

        x, y, c, s = rand(4, 100)
        def onpick3(event):
            ind = event.ind
            print 'onpick3 scatter:', ind, npy.take(x, ind), npy.take(y, ind)

        fig = figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(x, y, 100*s, c, picker=True)
        #fig.savefig('pscoll.eps')
        fig.canvas.mpl_connect('pick_event', onpick3)

    show()

elif(DEBUG == 2):
    #!/usr/bin/python
    # -*- coding: utf-8 -*-



    import sys
    from PyQt4 import QtGui


    class Example(QtGui.QWidget):
        
        def __init__(self):
            super(Example, self).__init__()
            
            self.initUI()
            
        def initUI(self):
            
            QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
            
            self.setToolTip('This is a <b>QWidget</b> widget')
            
            btn = QtGui.QPushButton('Button', self)
            btn.setToolTip('This is a <b>QPushButton</b> widget')
            btn.resize(btn.sizeHint())
            btn.move(50, 50)       
            
            self.setGeometry(300, 300, 250, 150)
            self.setWindowTitle('Tooltips')    
            self.show()
            
    def main():
        
        app = QtGui.QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())


    if __name__ == '__main__':
        main()

elif(DEBUG == 3):

    import matplotlib.pyplot as plt
    import scipy.spatial as spatial
    import numpy as np
    pi = np.pi
    cos = np.cos

    def fmt(x, y):
        return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x=x, y=y)

    class FollowDotCursor(object):
        """Display the x,y location of the nearest data point.
        http://stackoverflow.com/a/4674445/190597 (Joe Kington)
        http://stackoverflow.com/a/13306887/190597 (unutbu)
        http://stackoverflow.com/a/15454427/190597 (unutbu)
        """
        def __init__(self, ax, x, y, tolerance=5, formatter=fmt, offsets=(-20, 20)):
            try:
                x = np.asarray(x, dtype='float')
            except (TypeError, ValueError):
                x = np.asarray(dates.date2num(x), dtype='float')
            y = np.asarray(y, dtype='float')
            mask = ~(np.isnan(x) | np.isnan(y))
            x = x[mask]
            y = y[mask]
            self._points = np.column_stack((x, y))
            self.offsets = offsets
            y = y[np.abs(y-y.mean()) <= 3*y.std()]
            self.scale = x.ptp()
            self.scale = y.ptp() / self.scale if self.scale else 1
            self.tree = spatial.cKDTree(self.scaled(self._points))
            self.formatter = formatter
            self.tolerance = tolerance
            self.ax = ax
            self.fig = ax.figure
            self.ax.xaxis.set_label_position('top')
            self.dot = ax.scatter(
                [x.min()], [y.min()], s=130, color='green', alpha=0.7)
            self.annotation = self.setup_annotation()
            plt.connect('motion_notify_event', self)

        def scaled(self, points):
            points = np.asarray(points)
            return points * (self.scale, 1)

        def __call__(self, event):
            ax = self.ax
            # event.inaxes is always the current axis. If you use twinx, ax could be
            # a different axis.
            if event.inaxes == ax:
                x, y = event.xdata, event.ydata
            elif event.inaxes is None:
                return
            else:
                inv = ax.transData.inverted()
                x, y = inv.transform([(event.x, event.y)]).ravel()
            annotation = self.annotation
            x, y = self.snap(x, y)
            annotation.xy = x, y
            annotation.set_text(self.formatter(x, y))
            self.dot.set_offsets((x, y))
            bbox = ax.viewLim
            event.canvas.draw()

        def setup_annotation(self):
            """Draw and hide the annotation box."""
            annotation = self.ax.annotate(
                '', xy=(0, 0), ha = 'right',
                xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
                bbox = dict(
                    boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
                arrowprops = dict(
                    arrowstyle='->', connectionstyle='arc3,rad=0'))
            return annotation

        def snap(self, x, y):
            """Return the value in self.tree closest to x, y."""
            dist, idx = self.tree.query(self.scaled((x, y)), k=1, p=1)
            try:
                return self._points[idx]
            except IndexError:
                # IndexError: index out of bounds
                return self._points[0]

    fig, ax = plt.subplots()
    x = np.linspace(0.1, 2*pi, 10)
    y = cos(x)
    #markerline, stemlines, baseline = ax.stem(x, y, '-.')
    ax.plot(x, y)
    #plt.setp(markerline, 'markerfacecolor', 'b')
    #plt.setp(baseline, 'color','r', 'linewidth', 2)
    cursor = FollowDotCursor(ax, x, y, tolerance=2)
    plt.show()


elif(DEBUG == 4):

    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click on points')

    line, = ax.plot(np.random.rand(100), '-', picker=5)  # 5 points tolerance

    def onpick(event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        print 'onpick points:', zip(xdata[ind], ydata[ind])

    fig.canvas.mpl_connect('pick_event', onpick)

    plt.show()

elif(DEBUG==5):
    """Example of how to use wx tooltips on a matplotlib figure window.
    Adapted from http://osdir.com/ml/python.matplotlib.devel/2006-09/msg00048.html"""

    import matplotlib as mpl
    mpl.use('WXAgg')
    mpl.interactive(False)

    import pylab as pl
    from pylab import get_current_fig_manager as gcfm
    import wx
    import numpy as np
    import random


    class wxToolTipExample(object):
        def __init__(self):
            self.figure = pl.figure()
            self.axis = self.figure.add_subplot(111)

            # create a long tooltip with newline to get around wx bug (in v2.6.3.3)
            # where newlines aren't recognized on subsequent self.tooltip.SetTip() calls
            self.tooltip = wx.ToolTip(tip='tip with a long %s line and a newline\n' % (' '*100))
            gcfm().canvas.SetToolTip(self.tooltip)
            self.tooltip.Enable(False)
            self.tooltip.SetDelay(0)
            self.figure.canvas.mpl_connect('motion_notify_event', self._onMotion)

            self.dataX = np.arange(0, 100)
            self.dataY = [random.random()*100.0 for x in xrange(len(self.dataX))]
            self.axis.plot(self.dataX, self.dataY, linestyle='-', marker='o', markersize=10, label='myplot')

        def _onMotion(self, event):
            collisionFound = False
            if event.xdata != None and event.ydata != None: # mouse is inside the axes
                for i in xrange(len(self.dataX)):
                    radius = 1
                    if abs(event.xdata - self.dataX[i]) < radius and abs(event.ydata - self.dataY[i]) < radius:
                        top = tip='x=%f\ny=%f' % (event.xdata, event.ydata)
                        self.tooltip.SetTip(tip) 
                        self.tooltip.Enable(True)
                        collisionFound = True
                        break
            if not collisionFound:
                self.tooltip.Enable(False)



    example = wxToolTipExample()
    pl.show()

elif(DEBUG==6):
    #!/usr/bin/env python

    """

    You can enable picking by setting the "picker" property of an artist
    (for example, a matplotlib Line2D, Text, Patch, Polygon, AxesImage,
    etc...)

    There are a variety of meanings of the picker property

        None -  picking is disabled for this artist (default)

        boolean - if True then picking will be enabled and the
          artist will fire a pick event if the mouse event is over
          the artist

        float - if picker is a number it is interpreted as an
          epsilon tolerance in points and the artist will fire
          off an event if it's data is within epsilon of the mouse
          event.  For some artists like lines and patch collections,
          the artist may provide additional data to the pick event
          that is generated, for example, the indices of the data within
          epsilon of the pick event

        function - if picker is callable, it is a user supplied
          function which determines whether the artist is hit by the
          mouse event.

             hit, props = picker(artist, mouseevent)

          to determine the hit test.  If the mouse event is over the
          artist, return hit=True and props is a dictionary of properties
          you want added to the PickEvent attributes


    After you have enabled an artist for picking by setting the "picker"
    property, you need to connect to the figure canvas pick_event to get
    pick callbacks on mouse press events.  For example,

      def pick_handler(event):
          mouseevent = event.mouseevent
          artist = event.artist
          # now do something with this...


    The pick event (matplotlib.backend_bases.PickEvent) which is passed to
    your callback is always fired with two attributes:

      mouseevent - the mouse event that generate the pick event.  The
        mouse event in turn has attributes like x and y (the coordinates in
        display space, such as pixels from left, bottom) and xdata, ydata (the
        coords in data space).  Additionally, you can get information about
        which buttons were pressed, which keys were pressed, which Axes
        the mouse is over, etc.  See matplotlib.backend_bases.MouseEvent
        for details.

      artist - the matplotlib.artist that generated the pick event.

    Additionally, certain artists like Line2D and PatchCollection may
    attach additional meta data like the indices into the data that meet
    the picker criteria (for example, all the points in the line that are within
    the specified epsilon tolerance)

    The examples below illustrate each of these methods.
    """

    #from __future__ import print_function
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    from matplotlib.text import Text
    from matplotlib.image import AxesImage
    import numpy as np
    from numpy.random import rand

    if 1:  # simple picking, lines, rectangles and text
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.set_title('click on points, rectangles or text', picker=True)
        ax1.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))
        line, = ax1.plot(rand(100), 'o', picker=5)  # 5 points tolerance

        # pick the rectangle
        bars = ax2.bar(range(10), rand(10), picker=True)
        for label in ax2.get_xticklabels():  # make the xtick labels pickable
            label.set_picker(True)

        def onpick1(event):
            if isinstance(event.artist, Line2D):
                thisline = event.artist
                xdata = thisline.get_xdata()
                ydata = thisline.get_ydata()
                ind = event.ind
                print('onpick1 line:', zip(np.take(xdata, ind), np.take(ydata, ind)))
            elif isinstance(event.artist, Rectangle):
                patch = event.artist
                print('onpick1 patch:', patch.get_path())
            elif isinstance(event.artist, Text):
                text = event.artist
                print('onpick1 text:', text.get_text())

        fig.canvas.mpl_connect('pick_event', onpick1)

    if 1:  # picking with a custom hit test function
        # you can define custom pickers by setting picker to a callable
        # function.  The function has the signature
        #
        #  hit, props = func(artist, mouseevent)
        #
        # to determine the hit test.  if the mouse event is over the artist,
        # return hit=True and props is a dictionary of
        # properties you want added to the PickEvent attributes

        def line_picker(line, mouseevent):
            """
            find the points within a certain distance from the mouseclick in
            data coords and attach some extra attributes, pickx and picky
            which are the data points that were picked
            """
            if mouseevent.xdata is None:
                return False, dict()
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            maxd = 0.05
            d = np.sqrt((xdata - mouseevent.xdata)**2. + (ydata - mouseevent.ydata)**2.)

            ind = np.nonzero(np.less_equal(d, maxd))
            if len(ind):
                pickx = np.take(xdata, ind)
                picky = np.take(ydata, ind)
                props = dict(ind=ind, pickx=pickx, picky=picky)
                return True, props
            else:
                return False, dict()

        def onpick2(event):
            print('onpick2 line:', event.pickx, event.picky)

        fig, ax = plt.subplots()
        ax.set_title('custom picker for line data')
        line, = ax.plot(rand(100), rand(100), 'o', picker=line_picker)
        fig.canvas.mpl_connect('pick_event', onpick2)


    if 1:  # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)

        x, y, c, s = rand(4, 100)

        def onpick3(event):
            ind = event.ind
            print('onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind))

        fig, ax = plt.subplots()
        col = ax.scatter(x, y, 100*s, c, picker=True)
        #fig.savefig('pscoll.eps')
        fig.canvas.mpl_connect('pick_event', onpick3)

    if 1:  # picking images (matplotlib.image.AxesImage)
        fig, ax = plt.subplots()
        im1 = ax.imshow(rand(10, 5), extent=(1, 2, 1, 2), picker=True)
        im2 = ax.imshow(rand(5, 10), extent=(3, 4, 1, 2), picker=True)
        im3 = ax.imshow(rand(20, 25), extent=(1, 2, 3, 4), picker=True)
        im4 = ax.imshow(rand(30, 12), extent=(3, 4, 3, 4), picker=True)
        ax.axis([0, 5, 0, 5])

        def onpick4(event):
            artist = event.artist
            if isinstance(artist, AxesImage):
                im = artist
                A = im.get_array()
                print('onpick4 image', A.shape)

        fig.canvas.mpl_connect('pick_event', onpick4)


    plt.show()

elif(DEBUG==7):
    """
    SVG tooltip example
    ===================

    This example shows how to create a tooltip that will show up when
    hovering over a matplotlib patch.

    Although it is possible to create the tooltip from CSS or javascript,
    here we create it in matplotlib and simply toggle its visibility on
    when hovering over the patch. This approach provides total control over
    the tooltip placement and appearance, at the expense of more code up
    front.

    The alternative approach would be to put the tooltip content in `title`
    atttributes of SVG objects. Then, using an existing js/CSS library, it
    would be relatively straightforward to create the tooltip in the
    browser. The content would be dictated by the `title` attribute, and
    the appearance by the CSS.


    :author: David Huard
    """


    import matplotlib.pyplot as plt
    import xml.etree.ElementTree as ET
    from io import BytesIO

    ET.register_namespace("", "http://www.w3.org/2000/svg")

    fig, ax = plt.subplots()

    # Create patches to which tooltips will be assigned.
    circle = plt.Circle((0, 0), 5, fc='blue')
    rect = plt.Rectangle((-5, 10), 10, 5, fc='green')

    ax.add_patch(circle)
    ax.add_patch(rect)

    # Create the tooltips
    circle_tip = ax.annotate(
        'This is a blue circle.',
        xy=(0, 0),
        xytext=(30, -30),
        textcoords='offset points',
        color='w',
        ha='left',
        bbox=dict(boxstyle='round,pad=.5', fc=(.1, .1, .1, .92),
                  ec=(1., 1., 1.), lw=1, zorder=1))

    rect_tip = ax.annotate(
        'This is a green rectangle.',
        xy=(-5, 10),
        xytext=(30, 40),
        textcoords='offset points',
        color='w',
        ha='left',
        bbox=dict(boxstyle='round,pad=.5', fc=(.1, .1, .1, .92),
                  ec=(1., 1., 1.), lw=1, zorder=1))

    # Set id for the patches
    for i, t in enumerate(ax.patches):
        t.set_gid('patch_%d' % i)

    # Set id for the annotations
    for i, t in enumerate(ax.texts):
        t.set_gid('tooltip_%d' % i)


    # Save the figure in a fake file object
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_aspect('equal')

    f = BytesIO()
    plt.savefig(f, format="svg")

    # --- Add interactivity ---

    # Create XML tree from the SVG file.
    tree, xmlid = ET.XMLID(f.getvalue())
    tree.set('onload', 'init(evt)')

    # Hide the tooltips
    for i, t in enumerate(ax.texts):
        el = xmlid['tooltip_%d' % i]
        el.set('visibility', 'hidden')

    # Assign onmouseover and onmouseout callbacks to patches.
    for i, t in enumerate(ax.patches):
        el = xmlid['patch_%d' % i]
        el.set('onmouseover', "ShowTooltip(this)")
        el.set('onmouseout', "HideTooltip(this)")

    # This is the script defining the ShowTooltip and HideTooltip functions.
    script = """
        <script type="text/ecmascript">
        <![CDATA[

        function init(evt) {
            if ( window.svgDocument == null ) {
                svgDocument = evt.target.ownerDocument;
                }
            }

        function ShowTooltip(obj) {
            var cur = obj.id.slice(-1);

            var tip = svgDocument.getElementById('tooltip_' + cur);
            tip.setAttribute('visibility',"visible")
            }

        function HideTooltip(obj) {
            var cur = obj.id.slice(-1);
            var tip = svgDocument.getElementById('tooltip_' + cur);
            tip.setAttribute('visibility',"hidden")
            }

        ]]>
        </script>
        """

    # Insert the script at the top of the file and save it.
    tree.insert(0, ET.XML(script))
    ET.ElementTree(tree).write('svg_tooltip.svg')
    
    plt.show()
