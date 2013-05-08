
# Still to code.
#
# imexam
# preserve
# wcs
# get/set header cards
# lock
# match
# raise
# rotate
# orient
# scale
# shm/update
# single
# tile
# blink
# version
# wcs

# NB: Regions parsing is very crude.

import string
import sys,os

class ds9(object) :
    """	ds9 interactive
	#
	#
	# Create a ds9 object named display.  Set xpa debugging mode 1 to 
	# test the generation of xpa command text.  The file "anImage.fits"
	# is loaded in to the current ds9 frame.
	#
	>>> display = ds9("ds9mmirs", xpadbg=1)
	>>> display.file("anImage.fits")
	xpaset -p ds9mmirs file anImage.fits

	# Switch to frame 3
	#
	>>> display.frame(3)
	xpaset -p ds9mmirs frame 3

	# Pan the ds9 display to a particular image pixel.
	#
	>>> display.panto(1024, 1024)
	xpaset -p ds9mmirs pan to 1024.000000 1024.000000

	# Pan the ds9 display to a particular physical pixel.  These
	# coordinate systems are supported by ds9:
	#
	# All images support:	image
	#			physical
	#
	# IRAF mosaic image:	detector
	#			amplifier
	#
	# Image with WCS:	fk5
	#			...
	#
	>>> display.panto(1024, 1024, csys="physical")
	xpaset -p ds9mmirs pan to 1024.000000 1024.000000 physical

	# Set the frame's zoom factor
	#
	>>> display.zoom(2)
	xpaset -p ds9mmirs zoom to 2.000000

	# Regions can be sent to and returned from ds9.  The user can provide
	# a preformatted ds9 region string or lists of coordinates to as regions
	# for display.
	#
	# Send a preformatted string as a region.
	#
	>>> display.regions("circle 10 10 10")
	xpaset ds9mmirs regions
	circle 10 10 10
	
	# Display a list of x, y coordinates using the default "circle" shape
	# and 10 pixel width (5 pixel radius).
	#
	>>> display.regions([[10, 10], [15, 15], [20, 20]])
	xpaset ds9mmirs regions
	circle 10.000000 10.000000 5.000000
	circle 15.000000 15.000000 5.000000
	circle 20.000000 20.000000 5.000000
	<BLANKLINE>

	# The width can be provided as a third element in the list.
	#
	>>> display.regions([[10, 10, 4], [15, 15, 5], [20, 20, 6]])
	xpaset ds9mmirs regions
	circle 10.000000 10.000000 2.000000
	circle 15.000000 15.000000 2.500000
	circle 20.000000 20.000000 3.000000
	<BLANKLINE>

	# For circles the conversion from width to radius can be overridden
	# with the "radius" flag.
	#
	>>> display.regions([[10, 10, 4], [15, 15, 5], [20, 20, 6]], { "radius": True })
	xpaset ds9mmirs regions
	circle 10.000000 10.000000 4.000000
	circle 15.000000 15.000000 5.000000
	circle 20.000000 20.000000 6.000000
	<BLANKLINE>

	# A dict can be passed as the second argumant to provide extra formatting 
	# parameters.  Here the shape is set to "box".  Since the coordinate list
	# contains only 3 elements, the final value will be used as both the width
	# and height. Squares will be drawn.
	#
	>>> display.regions([[10, 10, 4], [15, 15, 5], [20, 20, 6]], { 'shape':'box' })
	xpaset ds9mmirs regions
	box 10.000000 10.000000 4.000000 4.000000 0.000000
	box 15.000000 15.000000 5.000000 5.000000 0.000000
	box 20.000000 20.000000 6.000000 6.000000 0.000000
	<BLANKLINE>

	# A fourth element can be used to specify both width and height.  Similarly
	# if 5 values are included the box rotation can be specified for each region.
	#
	>>> display.regions([[10, 10, 4, 14], [15, 15, 5, 14], [20, 20, 6, 14]], { 'shape':'box' })
	xpaset ds9mmirs regions
	box 10.000000 10.000000 4.000000 14.000000 0.000000
	box 15.000000 15.000000 5.000000 14.000000 0.000000
	box 20.000000 20.000000 6.000000 14.000000 0.000000
	<BLANKLINE>

	# Lines regions can be drawn, 4 values are required.  
	#
	>>> display.regions([[10, 10, 4, 14], [15, 15, 5, 14], [20, 20, 6, 14]], { 'shape':'line' })
	xpaset ds9mmirs regions
	line 10.000000 10.000000 4.000000 14.000000
	line 15.000000 15.000000 5.000000 14.000000
	line 20.000000 20.000000 6.000000 14.000000
	<BLANKLINE>

	# Ellipses and points are also supported, ellipse regions require 4 columns
	# an optional rotation column.  Point regions may take an additional "point"
	# column or parameter to specify the type of point to be drawn
	#
	>>> display.regions([[10, 10], [15, 15], [20, 20]], { 'shape':"point", 'point':"box" })
	xpaset ds9mmirs regions
	point 10.000000 10.000000 # point = {box}
	point 15.000000 15.000000 # point = {box}
	point 20.000000 20.000000 # point = {box}
	<BLANKLINE>


	# Values passed in can be transformed by passing an lambda for the desired column.
	# Here a numeric column in the data is converted to colors for display.
	#
	#
	>>> colors = ["red", "green", "blue"]
	>>> display.regions([[10, 10, 4, 14, 0], [15, 15, 5, 14, 1], [20, 20, 6, 14, 2]], \
		{ 'columns': "x y width height color", 'shape':'box', 'color':lambda c: colors[c]})
	xpaset ds9mmirs regions
	box 10.000000 10.000000 4.000000 14.000000 0.000000 # color = {red}
	box 15.000000 15.000000 5.000000 14.000000 0.000000 # color = {green}
	box 20.000000 20.000000 6.000000 14.000000 0.000000 # color = {blue}
	<BLANKLINE>
	
	#>>> display = ds9("ds9")
	#>>> display.frame()
    	#1
	#>>> display.file()
	#''
	#>>> display.zoom()
    	#1.0
	#>>> display.panto()
    	#[0.0, 0.0]
	#
	#
	#>>> display.file('test_25.fits')
	#
	#
	#>>> display.regions(delete=True)
	#
	#>>> display.panto(10, 10)
	#
    	#>>> display.zoom(4)
	#
	#>>> display.regions([[10, 10, 4], [15, 15, 5], [20, 20, 6]], { 'shape':'box' })
	#
	#>>> display.regions()
    	# Region file format: DS9 version 4.1
    	# Filename: /Users/john/src/python/test_25.fits
    	#global color=green dashlist=8 3 width=1 font="helvetica 10 normal" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1
    	#physical
    	#box(10,10,4,4,0)
    	#box(15,15,5,5,0)
	#box(20,20,6,6,0)
	#
	#>>> display.regions(parse='coords')
	#[[10.0, 10.0], [15.0, 15.0], [20.0, 20.0]]
    """

    def __init__(self, target="ds9", xpadbg=0) :
	self.xpa = xpa(target, xpadbg)

    def frame(self, frame=None) :
	if ( frame == None ) :
	    return int(self.xpa.get("frame"))
	else :
	    self.xpa.set("frame %(1)d" % { '1':frame })

    def file(self, file=None) :
	if ( file == None ) :
	    return self.xpa.get("file").strip()
	else :
	    self.xpa.set("file %(1)s" % { '1':file })

    def zoom(self, zoom=None) :
	if ( zoom == None ) :
	    return float(self.xpa.get("zoom"))
	else :
	    self.xpa.set("zoom to %(1)f" % { '1':zoom })

    def panto(self, x=None, y=None, csys=None) :
	options = ""

	if ( x == None ) :
	   x, y = self.xpa.get("pan to").split()

	   return [float(x), float(y)]
	else :
	    if ( csys != None ) :
		options = " " + csys

	    self.xpa.set("pan to %(1)f %(2)f%(3)s" % { '1':x, '2':y, '3':options })

    params = {    'shape':'circle', 'width':10, 'height':10, 'rot':0
	        , 'point':"box",

	        'shapes':["ellipse", "circle", "vector", "point", "line", "box"],
	    'attributes':["color",  "text",   "dashlist", "font"
			, "select", "dash",   "fixed",    "edit"
			, "move",   "rotate", "delete",   "tag"],

	'ellipse-coords':"%(x)f %(y)f %(a)f %(b)f %(rot)f",
	'ellipse-column':['x', 'y', 'a', 'b', 'rot'],

	 'circle-coords':"%(x)f %(y)f %(width)f",
	 'circle-column':['x', 'y', 'width'],
	 'circle-width' : lambda w: w/2.0,

	 'vector-coords':"%(x)f %(y)f %(length) %(rot)f",
	 'vector-column':['x', 'y', 'length', 'rot'],

	  'point-coords':"%(x)f %(y)f",
	  'point-column':['x', 'y'],
	  'point-attrib':" point = {%(point)s}",

	   'line-coords':"%(x1)f %(y1)f %(x2)f %(y2)f",
	   'line-column':['x1', 'y1', 'x2', 'y2'],

	    'box-coords':"%(x)f %(y)f %(width)f %(height)f %(rot)f",
	    'box-column':['x', 'y', 'width', 'height', 'rot'],
    }

    trtable = string.maketrans("(),", "   ")

    def regions(self, buffer=None, params={}, parse=False, delete=False) :
	if ( delete ) :
	    if ( buffer == None ) :
		tag=all
	    else :
	 	tag=8

	    self.xpa.set("regions delete all")
	    return

	if ( buffer == None ) :
	    regions = self.xpa.get("regions")

	    if ( parse == False ) :
		return regions

	    if ( parse == "coords" ) :
		return [[float(x) for x in row.translate(ds9.trtable).split()[1:3]]
			    for row in regions.split("\n")[4:-1]]

	    if ( parse == "shape+coords" ) :
		return [row.translate(ds9.trtabe).split()[0:2] for row in regions.split("\n")]

	    if ( parse == "all" ) :
		return


	else :
	    colattr = {}
	    coltran = {}

	    shape_col = -1

	    if ( type(buffer) == str ) :
		string = buffer

	    if ( type(buffer) == list ) :
		# Fold any provided params into defaults
		#
		params = dict(ds9.params.items() + params.items())

		if ( params.has_key("radius") ) :
		    del(params["circle-width"])

		if ( params.has_key("columns") ) :
		    columns = params["columns"]
		    if ( type(columns) == str ) :
		        columns = columns.split()


		    if ( "shape" in columns ) :
			dynamic = True
		else :
		    columns = params[params['shape'] + "-column"]

		for shape in params["shapes"] :
		    transform = {}

		    # Construct the attributes
		    #
		    if ( params.has_key(shape + "-attrib") ) :
			attribute = params[shape + "-attrib"]
		    else :
		 	attribute = ""

		    for a in params["attributes"] :
		        if ( a in columns ) :
			    attribute += " " + a + " = {%(" + a + ")s}"

		    if ( attribute != "" ) :
			attribute = " #" + attribute

		    colattr[shape] = attribute

		    # Lookup any column value transformer functions and
		    # supply the identity function as the default.  Each 
		    # shape has its own transform vector.
		    #
		    for col in columns :
		        func = None

			if ( params.has_key(col) and callable(params[col]) ) :
			    func = params[col]
			else :
			    shape_shifter = shape + "-" + col

			if (  params.has_key(shape_shifter) 
			 and callable(params[shape_shifter]) ) :
			    if ( func == None ) :
				func = params[shape_shifter]
			    else :
				func = params[shape_shifter]	# Should compose the functions

			if ( func == None ) :
			    func = lambda x: x

			transform[col] = func

		    coltran[shape] = transform
    
		string = ""
		for reg in buffer :
		    if ( type(reg) == list ) :
			if ( shape_col >= 0 ) :		# Dynamic column selection
			    shape = reg[shape_col]	#  pull out the shape early
			else :
			    shape = params["shape"]	# Or set shape to default

			if ( shape == "box" and len(reg) == 3 ) :
			    reg.append(reg[len(reg)-1])

			# Combine the default values in the params dict with 
			# the values provided in the list and named in "columns".
			#
			p = dict(params.items() + zip(columns, reg))	# Copy the parameters, overlaying
									# the defaults.
			for ( col, fun ) in coltran[shape].items() :	# Apply any transform functions
			    p[col] = fun(p[col])

    		    else :
			if ( type(reg) == dict ) :
			    p = dict(params.items() + reg.items())

		    coords = p[shape + "-coords"]

		    string += ("%(shape)s" + " " + coords + colattr[shape] + "\n") % p

	    self.xpa.set("regions", string)

class xpa(object):
    def __init__(self, target, debug=0):
	self.target = target
	self.debug  = debug

	if ( self.debug == 2 ) :
	    self.xpaset = "echo xpaset "
	    self.xpaget = "echo xpaget "
	else :
	    self.xpaset = "xpaset "
	    self.xpaget = "xpaget "

    def set(self, params, buffer=None):
	if ( buffer == None ) :
	    p = " -p"
	else :
	    p = ""

	if ( self.debug == 1 ) :
	    print "xpaset%(0)s %(1)s %(2)s" % { '0':p, '1': self.target, '2':params }
	    if ( buffer != None ) :
		print buffer
	else :

	    fp = os.popen("%(0)s%(1)s %(2)s %(3)s" % { '0':self.xpaset, '1':p, '2':self.target, '3':params }, "w")

	    if ( buffer != None ) :
		fp.write(buffer)
	    fp.close()

    def get(self, params):
	fp = os.popen("%(0)s%(1)s %(2)s" % { '0':self.xpaget, '1':self.target, '2':params }, "r")
	buffer = fp.read() 
	fp.close()

	return buffer

if __name__ == '__main__':
    import doctest
    doctest.testmod()
