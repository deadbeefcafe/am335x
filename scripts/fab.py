#!/usr/bin/env python

import sys

#FILENAME = 'BeagleBone_Black_RevB4.CAD'
FILENAME = 'cds2f_BeagleBone_Black_RevB4.txt'


## 1 components             'REFDES', 'COMP_CLASS', 'COMP_PART_NUMBER', 'COMP_HEIGHT', 'COMP_DEVICE_LABEL',
##                          'COMP_INSERTION_CODE', 'SYM_TYPE', 'SYM_NAME', 'SYM_MIRROR', 'SYM_ROTATE',
##                          'SYM_X', 'SYM_Y', 'COMP_VALUE', 'COMP_TOL', 'COMP_VOLTAGE'

components = dict()
footprint_refs = dict()

def read_components(a):
    sym = a['SYM_NAME']
    ref = a['REFDES']

    components[ref] = a
    if footprint_refs.has_key(sym):
        footprint_refs[sym].append(ref)
    else:
        footprint_refs[sym] = [ref]

## 2 component_pin          'NET_NAME', 'REFDES', 'PIN_NUMBER', 'PIN_NAME', 'PIN_GROUND', 'PIN_POWER'

signals = dict()

def read_component_pin(a):
    net = a['NET_NAME']
    #ref = a['REFDES']
    #pnum = a['PIN_NUMBER']
    #pnam = a['PIN_NAME']

    if signals.has_key(net):
        signals[net].append(a)
    else:
        signals[net] = [a]

    #print "COMPPIN: %s" % (a)
    pass

## 3 geomentry_classes      'CLASS', 'SUBCLASS'

geom_classes = dict()
def read_geomentry_classes(a):
    cls = a['CLASS']
    sub = a['SUBCLASS']
    key = cls + '/' + sub
    if geom_classes.has_key(key):
        geom_classes[key] += 1
    else:
        geom_classes[key] = 1


## 4 pad_definition         'PAD_NAME', 'REC_NUMBER', 'LAYER', 'FIXFLAG', 'VIAFLAG', 'PADSHAPE1', 'PADWIDTH',
##                          'PADHGHT', 'PADXOFF', 'PADYOFF', 'PADFLASH', 'PADSHAPENAME', 'TRELSHAPE1',
##                          'TRELWIDTH', 'TRELHGHT', 'TRELXOFF', 'TRELYOFF', 'TRELFLASH', 'TRELSHAPENAME',
##                          'APADSHAPE1', 'APADWIDTH', 'APADHGHT', 'APADXOFF', 'APADYOFF', 'APADFLASH',
##                          'APADSHAPENAME'

pad_definitions = dict()

def read_pad_definition(a):
    padname = a['PAD_NAME']
    if pad_definitions.has_key(padname):
        pad_definitions[padname].append(a)
    else:
        pad_definitions[padname] = [ a ]
    #print "PADDEF:", a

## 5 package_geometry       'GRAPHIC_DATA_NAME', 'GRAPHIC_DATA_NUMBER', 'RECORD_TAG', 'GRAPHIC_DATA_1',
##                          'GRAPHIC_DATA_2', 'GRAPHIC_DATA_3', 'GRAPHIC_DATA_4', 'GRAPHIC_DATA_5',
##                          'GRAPHIC_DATA_6', 'GRAPHIC_DATA_7', 'GRAPHIC_DATA_8', 'GRAPHIC_DATA_9',
##                          'SUBCLASS', 'SYM_NAME', 'REFDES'

pkg_geometry = dict()

def read_package_geometry(a):
    sym = a['SYM_NAME']
    ref = a['REFDES']
    key = sym + '/' + ref

    if pkg_geometry.has_key(key):
        pkg_geometry[key].append(a)
    else:
        pkg_geometry[key] = [a]
    #print "PKGGEO: <%s>" % (a)
    pass

## 6  package_pins          'SYM_NAME', 'SYM_MIRROR', 'PIN_NAME', 'PIN_NUMBER', 'PIN_X', 'PIN_Y',
##                          'PAD_STACK_NAME', 'REFDES', 'PIN_ROTATION', 'TEST_POINT'


pkg_ref_pins = dict()

def read_package_pins(a):
    sym = a['SYM_NAME']
    ref = a['REFDES']
    key = sym + '/' + ref

    if pkg_ref_pins.has_key(key):
        pkg_ref_pins[key].append(a)
    else:
        pkg_ref_pins[key] = [a]

## 7  vias                  'VIA_X', 'VIA_Y', 'PAD_STACK_NAME', 'NET_NAME', 'TEST_POINT', 'VIA_MIRROR',
##                          'VIA_ROTATION'

vias = list()

def read_vias(a):
    vias.append(a)
    #print "VIAS: <%s>" % (a)
    pass

## 8 copper_etch            'CLASS', 'SUBCLASS', 'GRAPHIC_DATA_NAME', 'GRAPHIC_DATA_NUMBER', 'RECORD_TAG',
##                          'GRAPHIC_DATA_1', 'GRAPHIC_DATA_2', 'GRAPHIC_DATA_3', 'GRAPHIC_DATA_4',
##                          'GRAPHIC_DATA_5', 'GRAPHIC_DATA_6', 'GRAPHIC_DATA_7', 'GRAPHIC_DATA_8',
##                          'GRAPHIC_DATA_9', 'NET_NAME'

etch = list()

def read_copper_etch(a):
    #cls = a['CLASS']
    #sub = a['SUBCLASS']
    #gdn = a['GRAPHIC_DATA_NAME']
    #gdm = a['GRAPHIC_DATA_NUMBER']
    #rt  = a['RECORD_TAG']
    #gd1 = a['GRAPHIC_DATA_1']
    #gd2 = a['GRAPHIC_DATA_2']
    #gd3 = a['GRAPHIC_DATA_3']
    #gd4 = a['GRAPHIC_DATA_4']
    #gd5 = a['GRAPHIC_DATA_5']
    #gd6 = a['GRAPHIC_DATA_6']
    #gd7 = a['GRAPHIC_DATA_7']
    #gd8 = a['GRAPHIC_DATA_8']
    #gd9 = a['GRAPHIC_DATA_9']
    #net = a['NET_NAME']

    #gd = "%s:%s:%s:%s:%s:%s:%s:%s:%s" % (gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9)

    etch.append(a)

    #print "ETCH: %-30s %10s %10s %s" % ("%s:%s"%(cls,sub),net,gdn,gd)


## 9 misc_pkg_lines         'SUBCLASS', 'PAD_SHAPE_NAME', 'GRAPHIC_DATA_NAME', 'GRAPHIC_DATA_NUMBER', 
##                          'RECORD_TAG', 'GRAPHIC_DATA_1', 'GRAPHIC_DATA_2', 'GRAPHIC_DATA_3', 'GRAPHIC_DATA_4',
##                          'GRAPHIC_DATA_5', 'GRAPHIC_DATA_6', 'GRAPHIC_DATA_7', 'GRAPHIC_DATA_8', 
##                          'GRAPHIC_DATA_9', 'PAD_STACK_NAME', 'REFDES', 'PIN_NUMBER'

def read_misc_pkg_lines(a):
    #print "MISC1: <%s>" % (a)
    pass


## 10 misc_pkg_lines2       'SUBCLASS', 'PAD_SHAPE_NAME', 'GRAPHIC_DATA_NAME', 'GRAPHIC_DATA_NUMBER',
##                          'RECORD_TAG', 'GRAPHIC_DATA_1', 'GRAPHIC_DATA_2', 'GRAPHIC_DATA_3', 'GRAPHIC_DATA_4',
##                          'GRAPHIC_DATA_5', 'GRAPHIC_DATA_6', 'GRAPHIC_DATA_7', 'GRAPHIC_DATA_8', 'GRAPHIC_DATA_9',
##                          'PAD_STACK_NAME'

def read_misc_pkg_lines2(a):
    #print "MISC2: <%s>" % (a)
    pass



sections = [

    [ 'components',        read_components ],
    [ 'component_pin',     read_component_pin ],
    [ 'geomentry_classes', read_geomentry_classes ],
    [ 'pad_definition',    read_pad_definition ],
    [ 'package_geometry',  read_package_geometry ],
    [ 'package_pins',      read_package_pins ],
    [ 'vias',              read_vias ],
    [ 'copper_etch',       read_copper_etch ],
    [ 'misc_pkg_lines',    read_misc_pkg_lines ],
    [ 'misc_pkg_lines2',   read_misc_pkg_lines2 ],
]


line_num = 1
sec_index = 0

for line in open(FILENAME,'rb'):
    a = line.split('!')
    a.pop()
    #print "LINE: <<%s>>" % (a)
    if a[0] == 'R':
        pass
    elif a[0] == 'J':
        pass
    elif a[0] == 'A':
        if sec_index < len(sections):
            section_name = sections[sec_index][0]
            section_func = sections[sec_index][1]
            section_fields = a[1:]
            #print "SECTION %2d %s <%s>" % (sec_index+1,section_name,section_fields)
        else:
            section_name = None
            section_func = None
            section_fields = a[1:]
            print "Unexpected section #%d at line %d" % (sec_index+1,line_num)
        sec_index += 1
    elif a[0] == 'S':
        if section_func:
            d = dict(zip(section_fields, a[1:]))
            #section_func(a[1:])
            section_func(d)
    else:
        print "Unknown record type on line %d" % (line_num)
        sys.exit(2)
    line_num += 1



#REC_NUMBER!LAYER!FIXFLAG!VIAFLAG!PADSHAPE1!PADWIDTH!PADHGHT!PADXOFF!PADYOFF!PADFLASH!PADSHAPENAME


def get_padstack(name, verbose=True, fd=sys.stdout):
    pad = pad_definitions[name]
    if verbose: fd.write("## PAD: %s\n" % (name))
    rc = dict()
    rc['roundness'] = 0
    for x in pad:
        recno = x['REC_NUMBER']
        layer = x['LAYER']
        psh = x['PADSHAPE1']
        pdx = x['PADWIDTH']
        pdy = x['PADHGHT']
        pxo = x['PADXOFF']
        pyo = x['PADYOFF']
        pfl = x['PADFLASH']
        psn = x['PADSHAPENAME']

        if layer == "TOP":
            if verbose: fd.write("## %s %6s %6s %s %s %s %s %s %s\n" % (recno,layer,psh,pdx,pdy,pxo,pyo,pfl,psn))
            if psh == 'CIRCLE':
                rc['shape'] = 'Round'
                rc['roundness'] = 100
            elif psh == 'RECTANGLE':
                rc['shape'] = 'Rectangle'
            elif psh == 'SQUARE':
                rc['shape'] = 'Square'
            elif psh == 'OBLONG_Y':
                #rc['shape'] = 'Oblong'
                rc['shape'] = 'Round'
                rc['roundness'] = 100
            elif psh == 'OBLONG_X':
                #rc['shape'] = 'OblongX'
                rc['shape'] = 'Round'
                rc['roundness'] = 100
            else:
                rc['shape'] = 'Unknown'
            rc['dx'] = pdx
            rc['dy'] = pdy
        elif layer == "~DRILL":
            if verbose: fd.write("## %s %6s %6s %s %s %s %s %s %s\n" % (recno,layer,psh,pdx,pdy,pxo,pyo,pfl,psn))
            drill = float(psh)
            rc['drill'] = drill
        else:
            pass

    if not drill:
        rc['type'] = 'Smd'
        if psh == "CIRCLE":
            rc['roundness'] = 100
        if psh == "OBLONG_X" or psh == "OBLONG_Y":
            rc['roundness'] = 100
    else:
        rc['type'] = "Pad"
    #if verbose: print "\n"
    return rc


import math

def deg2rad(deg):
    return(deg * math.pi / 180.0)

def translate(point, rotate_deg, mirror=False, flip=True):
    x1=point[0]
    y1=point[1]
    tf = type(float())
    if (type(x1) != tf): x1 = float(x1)
    if (type(y1) != tf): y1 = float(y1)
    if (type(rotate_deg) != tf): rotate_deg = float(rotate_deg)

    #print "#### XLATE (%f %f) rot=%f mir=%s " % (x1,y1,rotate_deg,mirror),

    if mirror and flip:
        y1 = y1*-1.0
        #rotate_deg += 180
    rad = deg2rad(rotate_deg) * -1.0
    x2 = x1*math.cos(rad) - y1*math.sin(rad) 
    y2 = x1*math.sin(rad) + y1*math.cos(rad)

#    if mirror:
#        y1 = y1*-1.0

    #print "--> (%f %f)" % (x2,y2)
    return(x2,y2)



def graphica_data_text(a):
    sub = a['SUBCLASS']
    gdn = a['GRAPHIC_DATA_NAME']
    gdm = a['GRAPHIC_DATA_NUMBER']
    rt  = a['RECORD_TAG']
    gd1 = a['GRAPHIC_DATA_1']
    gd2 = a['GRAPHIC_DATA_2']
    gd3 = a['GRAPHIC_DATA_3']
    gd4 = a['GRAPHIC_DATA_4']
    gd5 = a['GRAPHIC_DATA_5']
    gd6 = a['GRAPHIC_DATA_6']
    gd7 = a['GRAPHIC_DATA_7']
    gd8 = a['GRAPHIC_DATA_8']
    gd9 = a['GRAPHIC_DATA_9']

    gd = "%s %s %s %s %s:%s:%s:%s:%s:%s:%s:%s:%s" % (sub,gdn,gdm,rt,gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9)
    return(gd)


junk = """
    'BOUNDARY/TOP',
    'BOUNDARY/LYR2_GND',
    'BOUNDARY/LYR3',
    'BOUNDARY/LYR4',
    'BOUNDARY/LYR5_PWR',
    'BOUNDARY/BOTTOM',
    'ETCH/TOP',
    'ETCH/LYR2_GND',
    'ETCH/LYR3',
    'ETCH/LYR4',
    'ETCH/LYR5_PWR',
    'ETCH/BOTTOM',
    'TOLERANCE/ASSEMBLY_BOTTOM',
    'TOLERANCE/ASSEMBLY_TOP',
    'BOARD GEOMETRY/SYMB_DIM',
    'BOARD GEOMETRY/SC_DNREV_1',
    'BOARD GEOMETRY/SOLDERMASK_BOTTOM',
    'BOARD GEOMETRY/SILKSCREEN_BOTTOM',
    'BOARD GEOMETRY/DIMENSION',
    'BOARD GEOMETRY/ASSEMBLY_DETAIL',
    'BOARD GEOMETRY/TOOLING_CORNERS',
    'BOARD GEOMETRY/OUTLINE',
    'BOARD GEOMETRY/ASSEMBLY_NOTES',
    'BOARD GEOMETRY/SOLDERMASK_TOP',
    'BOARD GEOMETRY/SILKSCREEN_TOP',
    'DRAWING FORMAT/OUTLINE', 
    'DRAWING FORMAT/TITLE_BLOCK',
    'DRAWING FORMAT/FAB',
    'DRAWING FORMAT/ASSY2',
    'DRAWING FORMAT/FAB2',
    'DRAWING FORMAT/ASSY',
    'DRAWING FORMAT/DRAWING_ORIGIN',
    'USER PART NUMBER/SILKSCREEN_BOTTOM',
    'PACKAGE KEEPOUT/TOP',
    'VIA KEEPOUT/BOTTOM',
    'VIA KEEPOUT/TOP',
    'COMPONENT VALUE/ASSEMBLY_BOTTOM',
    'COMPONENT VALUE/ASSEMBLY_TOP',
    'DEVICE TYPE/ASSEMBLY_TOP', 
    'DEVICE TYPE/SILKSCREEN_TOP',
    'DEVICE TYPE/SILKSCREEN_BOTTOM',
    'DEVICE TYPE/ASSEMBLY_BOTTOM',
    'USER PART NUMBER/SILKSCREEN_TOP',
    'USER PART NUMBER/ASSEMBLY_BOTTOM', 
    'USER PART NUMBER/DISPLAY_TOP',
    'USER PART NUMBER/ASSEMBLY_TOP',
    'USER PART NUMBER/DISPLAY_BOTTOM',
    'MANUFACTURING/AUTOSILK_TOP',
    'MANUFACTURING/NCLEGEND-1-6',
    'MANUFACTURING/AUTOSILK_BOTTOM',
    'MANUFACTURING/PHOTOPLOT_OUTLINE',
    'CONSTRAINT REGION/ALL',
    'CONSTRAINT REGION/TOP',
    'REF DES/ASSEMBLY_BOTTOM', 
    'REF DES/ASSEMBLY_TOP',
    'REF DES/SILKSCREEN_BOTTOM',
    'REF DES/SILKSCREEN_TOP',
    'ROUTE KEEPOUT/TOP',
    'ROUTE KEEPOUT/BOTTOM',
    'ROUTE KEEPOUT/ALL']
    """


layer_translate = [
    ('ASSEMBLY_','51'),
    ('SILKSCREEN_','21'),
    ('PLACE_BOUND_','39'),
    ('BODY_CENTER', '23'),
    ('BOTTOM','16'),
    ('TOP','1'),
    ('LYR2','2'),
    ('LYR3','3'),
    ('LYR4','4'),
    ('LYR5','5'),

    ]



def eagle_layer(name):
    for x in layer_translate:
        if name.startswith(x[0]):
            return x[1]
    return None


def eagle_primitive(a,offset=(0.0,0.0),mirror=False,rotation=0.0):
    sub = a['SUBCLASS']
    gdn = a['GRAPHIC_DATA_NAME']
    gdm = a['GRAPHIC_DATA_NUMBER']
    rt  = a['RECORD_TAG']
    gd1 = a['GRAPHIC_DATA_1']
    gd2 = a['GRAPHIC_DATA_2']
    gd3 = a['GRAPHIC_DATA_3']
    gd4 = a['GRAPHIC_DATA_4']
    gd5 = a['GRAPHIC_DATA_5']
    gd6 = a['GRAPHIC_DATA_6']
    gd7 = a['GRAPHIC_DATA_7']
    gd8 = a['GRAPHIC_DATA_8']
    gd9 = a['GRAPHIC_DATA_9']
    if a.has_key('NET_NAME'):
        net = a['NET_NAME']
    else:
        net = None

## GEOM: BODY_CENTER ARC 175.00:625.00:175.00:625.00:150.00:625.00:25.00:0.00:COUNTERCLOCKWISE
## GEOM: BODY_CENTER LINE 125.00:625.00:175.00:625.00:0.00::::
## GEOM: BODY_CENTER LINE 150.00:600.00:150.00:650.00:0.00::::
## GEOM: ASSEMBLY_TOP RECTANGLE 110.00:600.00:190.00:650.00:0::::
## unknown graphic primitive RECTANGLE
## GEOM: SILKSCREEN_TOP LINE 90.00:590.00:210.00:590.00:0.00::::
## GEOM: SILKSCREEN_TOP LINE 210.00:590.00:210.00:660.00:0.00::::
## GEOM: SILKSCREEN_TOP LINE 210.00:660.00:90.00:660.00:0.00::::
## GEOM: SILKSCREEN_TOP LINE 90.00:660.00:90.00:590.00:0.00::::
## GEOM: PLACE_BOUND_TOP RECTANGLE 90.00:590.00:210.00:660.00:1::::
## unknown graphic primitive RECTANGLE
## GEOM: SILKSCREEN_TOP RECTANGLE 80.00:590.00:90.00:660.00:1:::: 
## unknown graphic primitive RECTANGLE

    layer = eagle_layer(sub)
    if not layer:
        layer = '48'

    if gdn == 'LINE':
        ## GEOM: BODY_CENTER LINE 125.00:625.00:175.00:625.00:0.00::::
        x1 = float(gd1) - offset[0]
        y1 = float(gd2) - offset[1]
        x2 = float(gd3) - offset[0]
        y2 = float(gd4) - offset[1]
        width = float(gd5)

        (x1,y1) = translate((x1,y1),rotation,mirror)
        (x2,y2) = translate((x2,y2),rotation,mirror)

        if net:
            return "Change Layer %s; Wire '%s' %s (%f %f) (%f %f);" % (layer,net,width,x1,y1,x2,y2)
        else:
            return "Change Layer %s; Wire %s (%f %f) (%f %f);" % (layer,width,x1,y1,x2,y2)
        pass
    elif gdn == 'ARC':
        x1 = float(gd1) - offset[0] # start
        y1 = float(gd2) - offset[1]
        x2 = float(gd3) - offset[0] # end
        y2 = float(gd4) - offset[1]
        x3 = float(gd5) - offset[0] # center
        y3 = float(gd6) - offset[1]

        (x1,y1) = translate((x1,y1),rotation,mirror)
        (x2,y2) = translate((x2,y2),rotation,mirror)
        (x3,y3) = translate((x3,y3),rotation,mirror)

        rad = float(gd7)    # radius
        width = float(gd8)
        ccw = True if gd9 == 'COUNTERCLOCKWISE' else False

        if (x1 == x2 and y1 == y2):
            if width == 0.0: width = 0.1
            return "Change Layer %s; Circle %f (%f %f) (%f %f);" % (layer,width,x3,y3,x1,y1)
        x4 = x3 - (x1 - x3)
        y4 = y3 - (y1 - y3)
        if net:
            return "Change Layer %s; Arc '%s' %s %f (%f %f) (%f %f) (%f %f);" % (layer,net ,'CCW' if ccw else 'CW',width,x1,y1,x4,y4,x2,y2)
        else:
            return "Change Layer %s; Arc %s %f (%f %f) (%f %f) (%f %f);" % (layer,'CCW' if ccw else 'CW',width,x1,y1,x4,y4,x2,y2)

        ## GEOM: BODY_CENTER ARC 175.00:625.00:175.00:625.00:150.00:625.00:25.00:0.00:COUNTERCLOCKWISE
        pass
    elif gdn == 'RECTANGLE':
        ## GEOM: SILKSCREEN_TOP RECTANGLE 80.00:590.00:90.00:660.00:1:::: 
        x1 = float(gd1) - offset[0] # start
        y1 = float(gd2) - offset[1]
        x2 = float(gd3) - offset[0] # end
        y2 = float(gd4) - offset[1]
        width = float(gd5)
        (x1,y1) = translate((x1,y1),rotation,mirror)
        (x2,y2) = translate((x2,y2),rotation,mirror)
        rc = "Change Layer %s;" % (layer)
        rc += "Wire %s (%f %f) (%f %f);" % (width,x1,y1,x1,y2)
        rc += "Wire %s (%f %f) (%f %f);" % (width,x1,y2,x2,y2)
        rc += "Wire %s (%f %f) (%f %f);" % (width,x2,y2,x2,y1)
        rc += "Wire %s (%f %f) (%f %f);" % (width,x2,y1,x1,y1)
        return rc
        pass
    elif gdn == 'TEXT':
        pass
    else:
        return "## unknown graphic primitive %s" % (gdn)



# Change Drill <size>; Pad '<name>' round <size> R0 (x y);
# Smd 'name' dx dy -round R0 (x y);

def eagle_footprint(fd, name, ref=None):
    if not ref:
        ref = footprint_refs[name][0]
    comp = components[ref]
    key = name + '/' + ref 
    pkg = pkg_ref_pins[key]

    smir = True if comp['SYM_MIRROR'] == 'YES' else False
    #srot = int(float(comp['SYM_ROTATE']))
    srot = float(comp['SYM_ROTATE'])
    sx = float(comp['SYM_X'])
    sy = float(comp['SYM_Y'])


    fd.write("#########################################\n")
    fd.write("## %s ref: %s\n" % (name,ref))
    fd.write("## comp: <%s>\n" % (comp))
    fd.write("Remove %s.pac;\n" % name)
    fd.write("Edit %s.pac;\n" % name)
    fd.write("Layer 1;\n")
    fd.write("grid mil;\n")
    for pin in pkg:
        padstkname = pin['PAD_STACK_NAME']
        ps = get_padstack(padstkname,fd=fd)
        fd.write("## pin: <%s>\n" % (pin))
        fd.write("## %s\n" % (ps))
        pinno = pin['PIN_NUMBER']

        x = float(pin['PIN_X']) - sx
        y = float(pin['PIN_Y']) - sy

        (x,y) = translate((x,y), srot,smir)
        rot = int(float(pin['PIN_ROTATION']))
        
        #y = float(pin['PIN_Y'])
        #x = float(pin['PIN_X'])
        #rot = int(float(pin['PIN_ROTATION']))
        #trot = (rot + srot).__divmod__(360)[1]
        trot = rot

        mirror = pin['SYM_MIRROR']
        pinname = pin['PIN_NAME']
        fd.write("\n\n");
        if ps['type'] == 'Smd':
            fd.write("Smd '%s' %s %s -%d R%d (%f %f)  ## %s\n" % (pinno,ps['dx'],ps['dy'],ps['roundness'],trot,x,y,pinname))
        else:
            if not pinno:
                fd.write("Hole %s (%f %f); ## %s\n" % (ps['drill'],x,y,pinname))
            else:
                fd.write("Change Drill %s; Pad '%s' %s %s R%d (%f %f)  ## %s\n" % (ps['drill'], pinno,ps['dx'],ps['shape'],trot,x,y,pinname))
        fd.write("\n\n");

    if pkg_geometry.has_key(key):
        pkg_geom = pkg_geometry[key]
        for geom in pkg_geom:
            fd.write("## GEOM: %s mir=%d rot=%s org=(%s %s)\n" % (graphica_data_text(geom),smir,srot,sx,sy))
            rc = eagle_primitive(geom,offset=(sx,sy),mirror=smir,rotation=srot)
            if rc: fd.write("%s\n" % (rc))


##add 402@bbb R777 MR23.2 (0 0);

def eagle_place_components(fd,libname):
    for ref in components.keys():
        comp = components[ref]

        x       = comp['SYM_X']
        y       = comp['SYM_Y']
        rot     = float(comp['SYM_ROTATE'])
        val     = comp['COMP_VALUE']
        pkgname = comp['SYM_NAME']
        mir     = 'M' if comp['SYM_MIRROR'] == 'YES' else ''
        if mir == 'M':
            rot = (rot + 180.0).__divmod__(360)[1]

        fd.write("Add %s@%s '%s' %sR%s (%s %s);\n" % (pkgname,libname,ref,mir,rot,x,y))
        if val:
            fd.write("Value %s '%s';\n" % (ref,val))

#>>> signals['VDD_5V']
#[{'PIN_GROUND': '', 'PIN_NUMBER': '6', 'NET_NAME': 'VDD_5V', 'PIN_NAME': '28', 'PIN_POWER': '', 'REFDES': 'P9'}, {'PIN_GROUND': '', 'PIN_NUMBER': '5', 'NET_NAME': 'VDD_5V', 'PIN_NAME': '3', 'PIN_POWER': '', 'REFDES': 'P9'}, {'PIN_GROUND': '', 'PIN_NUMBER': '10', 'NET_NAME': 'VDD_5V', 'PIN_NAME': 'AC', 'PIN_POWER': '', 'REFDES': 'U2'}, {'PIN_GROUND': '', 'PIN_NUMBER': '1', 'NET_NAME': 'VDD_5V', 'PIN_NAME': '1', 'PIN_POWER': '', 'REFDES': 'P1'}, {'PIN_GROUND': '', 'PIN_NUMBER': '2', 'NET_NAME': 'VDD_5V', 'PIN_NAME': '2', 'PIN_POWER': '', 'REFDES': 'C2'}]


def eagle_generate_signals(fd):
    for net in signals.keys():
        if net:
            fd.write("Signal %s " % (net))
            for sig in signals[net]:
                ref = sig['REFDES']
                pin = sig['PIN_NUMBER']
                fd.write("%s %s " % (ref,pin))
            fd.write(";\n")



## 7  vias                  'VIA_X', 'VIA_Y', 'PAD_STACK_NAME', 'NET_NAME', 'TEST_POINT', 'VIA_MIRROR',
##                          'VIA_ROTATION'

#vias = list()

def eagle_place_vias(fd):
    for via in vias:
        x = via['VIA_X']
        y = via['VIA_Y']
        psname = via['PAD_STACK_NAME']
        net = via['NET_NAME']
        if net:
            ps = get_padstack(psname,fd=fd)
            fd.write("Change drill %s; Via '%s' %s Round (%s %s);" % (ps['drill'],net,ps['dx'],x,y))


## LINE
## ARC
## TEXT
## RECTANGLE
## FIG_RECTANGLE
## CIRCLE
## CROSS
## OBLONG_X
## OBLONG_Y
## DIAMOND
## SQUARE
## NULL


def eagle_copper_etch(fd):
    for geom in etch:
            fd.write("## GEOM: %s\n" % (graphica_data_text(geom)))
            rc = eagle_primitive(geom,offset=(0,0),mirror=False,rotation=0.0)
            if rc: fd.write("%s\n" % (rc))


# A!CLASS!SUBCLASS!GRAPHIC_DATA_NAME!GRAPHIC_DATA_NUMBER!RECORD_TAG!GRAPHIC_DATA_1!GRAPHIC_DATA_2!GRAPHIC_DATA_3!GRAPHIC_DATA_4!GRAPHIC_DATA_5!GRAPHIC_DATA_6!GRAPHIC_DATA_7!GRAPHIC_DATA_8!GRAPHIC_DATA_9!NET_NAME!


c2e_layers = [
    ('BOARD GEOMETRY',    'ASSEMBLY_DETAIL',   None), ##    11 layer
    ('BOARD GEOMETRY',    'ASSEMBLY_NOTES',    None), ##    20 layer
    ('BOARD GEOMETRY',    'DIMENSION',         None), ##   149 layer
    ('BOARD GEOMETRY',    'OUTLINE',           20), ##     9 layer
    ('BOARD GEOMETRY',    'SC_DNREV_1',        None), ##     7 layer
    ('BOARD GEOMETRY',    'SILKSCREEN_BOTTOM', None), ##  2652 layer
    ('BOARD GEOMETRY',    'SILKSCREEN_TOP',    None), ##  2860 layer
    ('BOARD GEOMETRY',    'SOLDERMASK_BOTTOM', None), ##     1 layer
    ('BOARD GEOMETRY',    'SOLDERMASK_TOP',    None), ##   257 layer
    ('BOARD GEOMETRY',    'SYMB_DIM',          None), ##    58 layer
    ('BOARD GEOMETRY',    'TOOLING_CORNERS',   None), ##   117 layer
    ('BOUNDARY',          'BOTTOM',            None), ##   330 layer
    ('BOUNDARY',          'LYR2_GND',          None), ##   189 layer
    ('BOUNDARY',          'LYR3',              None), ##   104 layer
    ('BOUNDARY',          'LYR4',              None), ##    58 layer
    ('BOUNDARY',          'LYR5_PWR',          None), ##   480 layer
    ('BOUNDARY',          'TOP',               None), ##   239 layer
    ('COMPONENT VALUE',   'ASSEMBLY_BOTTOM',   None), ##     7 layer
    ('COMPONENT VALUE',   'ASSEMBLY_TOP',      None), ##     6 layer
    ('CONSTRAINT REGION', 'ALL',               None), ##     8 layer
    ('CONSTRAINT REGION', 'TOP',               None), ##     8 layer
    ('DEVICE TYPE',       'ASSEMBLY_BOTTOM',   None), ##   232 layer
    ('DEVICE TYPE',       'ASSEMBLY_TOP',      None), ##    96 layer
    ('DEVICE TYPE',       'SILKSCREEN_BOTTOM', None), ##   228 layer
    ('DEVICE TYPE',       'SILKSCREEN_TOP',    None), ##    88 layer
    ('DRAWING FORMAT',    'ASSY',              None), ## 11735 layer
    ('DRAWING FORMAT',    'ASSY2',             None), ##   427 layer
    ('DRAWING FORMAT',    'DRAWING_ORIGIN',    None), ##     1 layer
    ('DRAWING FORMAT',    'FAB',               None), ##   923 layer
    ('DRAWING FORMAT',    'FAB2',              None), ##   427 layer
    ('DRAWING FORMAT',    'OUTLINE',           None), ##     7 layer
    ('DRAWING FORMAT',    'TITLE_BLOCK',       None), ##    12 layer
    ('ETCH',              'TOP',               1   ), ##  5547 layer
    ('ETCH',              'LYR2_GND',          2   ), ##  1419 layer
    ('ETCH',              'LYR3',              3   ), ##  2529 layer
    ('ETCH',              'LYR4',              4   ), ##  1871 layer
    ('ETCH',              'LYR5_PWR',          5   ), ##  2257 layer
    ('ETCH',              'BOTTOM',            16  ), ##  4064 layer
    ('MANUFACTURING',     'AUTOSILK_BOTTOM',   None), ##  2250 layer
    ('MANUFACTURING',     'AUTOSILK_TOP',      None), ##  1110 layer
    ('MANUFACTURING',     'NCLEGEND-1-6',      None), ##    92 layer
    ('MANUFACTURING',     'PHOTOPLOT_OUTLINE', None), ##     1 layer
    ('PACKAGE KEEPOUT',   'TOP',               None), ##    22 layer
    ('REF DES',           'ASSEMBLY_BOTTOM',   None), ##   252 layer
    ('REF DES',           'ASSEMBLY_TOP',      None), ##   113 layer
    ('REF DES',           'SILKSCREEN_BOTTOM', 22  ), ##   252 layer
    ('REF DES',           'SILKSCREEN_TOP',    21  ), ##   129 layer
    ('ROUTE KEEPOUT',     'ALL',               None), ##     2 layer
    ('ROUTE KEEPOUT',     'BOTTOM',            None), ##   935 layer
    ('ROUTE KEEPOUT',     'TOP',               None), ##   367 layer
    ('TOLERANCE',         'ASSEMBLY_BOTTOM',   None), ##     4 layer
    ('TOLERANCE',         'ASSEMBLY_TOP',      None), ##     4 layer
    ('USER PART NUMBER',  'ASSEMBLY_BOTTOM',   None), ##     4 layer
    ('USER PART NUMBER',  'ASSEMBLY_TOP',      None), ##     5 layer
    ('USER PART NUMBER',  'DISPLAY_BOTTOM',    None), ##     1 layer
    ('USER PART NUMBER',  'DISPLAY_TOP',       None), ##     1 layer
    ('USER PART NUMBER',  'SILKSCREEN_BOTTOM', None), ##     1 layer
    ('USER PART NUMBER',  'SILKSCREEN_TOP',    None), ##     2 layer
    ('VIA KEEPOUT',       'BOTTOM',            None), ##   912 layer
    ('VIA KEEPOUT',       'TOP',               None), ##   348 layer
]

eagle_layers = [
    (20, 'Dimension',   'Board outlines (circles for holes)'),
    (21, 'tPlace',      'Silk screen, top side'),
    (22, 'bPlace',      'Silk screen, bottom side'),
    (23, 'tOrigins',    'Origins, top side'),
    (24, 'bOrigins',    'Origins, bottom side'),
    (25, 'tNames',      'Service print, top side'),
    (26, 'bNames',      'Service print, bottom side'),
    (27, 'tValues',     'Component VALUE, top side'),
    (28, 'bValues',     'Component VALUE, bottom side'),
    (29, 'tStop',       'Solder stop mask, top side'),
    (30, 'bStop',       'Solder stop mask, bottom side'),
    (31, 'tCream',      'Solder cream, top side'),
    (32, 'bCream',      'Solder cream, bottom side'),
    (33, 'tFinish',     'Finish, top side'),
    (34, 'bFinish',     'Finish, bottom side'),
    (35, 'tGlue',       'Glue mask, top side'),
    (36, 'bGlue',       'Glue mask, bottom side'),
    (37, 'tTest',       'Test and adjustment inf., top side'),
    (38, 'bTest',       'Test and adjustment inf. bottom side'),
    (39, 'tKeepout',    'Nogo areas for components, top side'),
    (40, 'bKeepout',    'Nogo areas for components, bottom side'),
    (41, 'tRestrict',   'Nogo areas for tracks, top side'),
    (42, 'bRestrict',   'Nogo areas for tracks, bottom side'),
    (43, 'vRestrict',   'Nogo areas for via-holes'),
    (44, 'Drills',      'Conducting through-holes'),
    (45, 'Holes',       'Non-conducting holes'),
    (46, 'Milling',     'Milling'),
    (47, 'Measures',    'Measures'),
    (48, 'Document',    'General documentation'),
    (49, 'Reference',   'Reference marks'),
    (51, 'tDocu Part',  'documentation, top side'),
    (52, 'bDocu Part',  'documentation, bottom side')
]


c2e = dict()
def cadence_layer_to_eagle(cls,sub):
    global c2e
    if not c2e:
        c2e = dict()
        for x in c2e_layers:
            key = "%s:%s" % (x[0],x[1])
            c2e[key] = x[2]
    key = "%s:%s" % (cls,sub)
    if c2e.has_key(key):
        return c2e[key]
    return None

def decode_cadence(geom):
    cls = geom['CLASS']
    sub = geom['SUBCLASS']
    gdn = geom['GRAPHIC_DATA_NAME']
    gnm = geom['GRAPHIC_DATA_NUMBER']
    tag = geom['RECORD_TAG']
    gd1 = geom['GRAPHIC_DATA_1']
    gd2 = geom['GRAPHIC_DATA_2']
    gd3 = geom['GRAPHIC_DATA_3']
    gd4 = geom['GRAPHIC_DATA_4']
    gd5 = geom['GRAPHIC_DATA_5']
    gd6 = geom['GRAPHIC_DATA_6']
    gd7 = geom['GRAPHIC_DATA_7']
    gd8 = geom['GRAPHIC_DATA_8']
    gd9 = geom['GRAPHIC_DATA_9']
    net = geom['NET_NAME']
    layer = cadence_layer_to_eagle(cls,sub)

    rc = dict()
    rc['layer'] = cadence_layer_to_eagle(cls,sub)
    rc['tag'] = tag.split(' ')

    if   gdn == 'LINE':
        rc['type'] = 'line'
        rc['p1'] = (float(gd1),float(gd2))
        rc['p2'] = (float(gd3),float(gd4))
        rc['width'] = float(gd5)
    elif gdn == 'ARC':
        if rc['p1'] == rc['p2']:
            rc['type'] = 'circle'
        else:
            rc['type'] = 'arc'
        rc['p1'] = (float(gd1),float(gd2))
        rc['p2'] = (float(gd3),float(gd4))
        rc['center'] = (float(gd5),float(gd6))
        rc['radius'] = float(gd7)
        rc['width'] = float(gd8)
        rc['ccw'] = True if gd9 == 'COUNTERCLOCKWISE' else False
    elif gdn == 'TEXT':
        pass
    elif gdn == 'RECTANGLE':
        rc['type'] = 'rectangle'
        rc['p1'] = (float(gd1),float(gd2))
        rc['p2'] = (float(gd3),float(gd4))
        rc['width'] = float(gd5)
    elif gdn == 'FIG_RECTANGLE':
        rc['type'] = 'rectangle'
        x = float(gd1)
        y = float(gd2)
        w = float(gd3)
        h = float(gd4)
        rc['p1'] = (x - w/2.0,y + h/2.0)
        rc['p2'] = (x + w/2.0,y - h/2.0)
        rc['width'] = float(gd5)
    elif gdn == 'CIRCLE':
        rc['type'] = 'circle'
    elif gdn == 'CROSS':
        pass
    elif gdn == 'OBLONG_X':
        pass
    elif gdn == 'OBLONG_Y':
        pass
    elif gdn == 'DIAMOND':
        pass
    elif gdn == 'SQUARE':
        pass
    elif gdn == 'NULL':
        pass

    rc = dict()
    rc['layer'] = cadence_layer_to_eagle(cls,sub)

    if layer:
        print "%-5d %-20s %-10s %-15s %s!%s!%s!%s!%s!%s!%s!%s!%s!" % (layer,net,gdn,tag,gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9)


def eagle_polygons(fd):
    prev_tag = None
    prev_layer = None
    prev_width = None

    for x in range(len(etch)):
        geom = etch[x]
        cls = geom['CLASS']
        sub = geom['SUBCLASS']

        lay = cadence_layer_to_eagle(cls,sub)

        #print "%-20s %-20s %s" % (cls,sub,lay)

        if lay is None:
            continue

        gdn = geom['GRAPHIC_DATA_NAME']
        gdm = geom['GRAPHIC_DATA_NUMBER']
        rt  = geom['RECORD_TAG']
        gd1 = geom['GRAPHIC_DATA_1']
        gd2 = geom['GRAPHIC_DATA_2']
        gd3 = geom['GRAPHIC_DATA_3']
        gd4 = geom['GRAPHIC_DATA_4']
        gd5 = geom['GRAPHIC_DATA_5']
        gd6 = geom['GRAPHIC_DATA_6']
        gd7 = geom['GRAPHIC_DATA_7']
        gd8 = geom['GRAPHIC_DATA_8']
        gd9 = geom['GRAPHIC_DATA_9']
        if geom.has_key('NET_NAME'):
            if not geom['NET_NAME']:
                net = ""
            else:
                net = "'%s'" % (geom['NET_NAME'])
        else:
            net = ""

        tag = rt.split(' ')

        if gdn == 'LINE':
            p1 = (float(gd1),float(gd2))
            p2 = (float(gd3),float(gd4))
            width = float(gd5)
        elif gdn == 'ARC':
            p1 = (float(gd1),float(gd2))
            p2 = (float(gd3),float(gd4))
            p3 = (float(gd5),float(gd6))
            rad = float(gd7)    # radius
            width = float(gd8)
            ccw = '+' if gd9 == 'COUNTERCLOCKWISE' else '-'
        elif gdn == 'TEXT':
            ## TEXT lay=21 !970.00!387.50!0.000!NO!LEFT!1 0 28.00 20.00 0.000 7.00 7.00 4.00!C12!!!
            p1 = (float(gd1),float(gd2))
            rot = float(gd3)
            mir = gd4
            just = gd5
            tparm = gd6.split(' ')
            block = tparm[0]
            font = tparm[1]
            height = tparm[2]
            width = tparm[3]

            pass
        else:
            pass
            #print "unhandled primitive: %s" % (gdn)



        if tag[0] != prev_tag:
            if prev_tag is not None:
                fd.write(";\n")

        if len(tag) == 3 and tag[2] != '0':
            continue

        if lay != prev_layer:
            fd.write("Change Layer %d\n" % (lay))
            prev_layer = lay

        if width != prev_width:
            #fd.write("Change Width %f\n" % (width))
            prev_width = width

        ## polygons
        if len(tag) == 3 and tag[2] == '0':
            if tag[0] != prev_tag: 
                if width == 0.0:
                    width = 0.1
                fd.write("Polygon %s %f (%s %s)" % (net,width,gd1,gd2))
            if gdn == 'LINE':
                fd.write(" (%s %s)" % (gd3,gd4))
            elif gdn == 'ARC':
                ccw = '+' if gd9 == 'COUNTERCLOCKWISE' else '-'
                fd.write(" @%c%f (%s %s)" % (ccw,rad,gd3,gd4))
        ## other entities
        else:
            if gdn == 'LINE':
                fd.write("Wire %s %f (%s %s) (%s %s);\n" % (net,width,gd1,gd2,gd3,gd4))
            elif gdn == 'ARC':
                if p1 == p2:
                    fd.write("Circle (%s %s) (%s %s);\n" %(gd5,gd6,gd1,gd2))
                else:
                    fd.write("Wire %s %f (%s %s) @%c%f (%s %s);\n" % (net,width,gd1,gd2,ccw,rad,gd3,gd4))
            elif gdn == 'TEXT':
                fd.write("## TEXT lay=%d !%s!%s!%s!%s!%s!%s!%s!%s!%s!\n" % (lay,gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9))
            else:
                fd.write("## ???? %-20s %-20s %-20s %5s width=%s %s!%s!%s!%s!%s!%s!%s!%s!%s!" % (sub,net,tag,gdn,width,gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9))


            #print "%-20s %-20s %-20s %5s width=%s %s!%s!%s!%s!%s!%s!%s!%s!%s!" % (sub,net,tag,gdn,width,gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9)
        prev_tag = tag[0]




class Polygon:
    def __init__(self):
        self.kind = "polygon"
        self.vertex = []
        self.layer = None
        self.width = 0.0
        self.rank = 0
        self.net = None
    def add_vertex(self,x,y):
        self.vertex.append((x,y))
    def area(self):
        area = 0.0
        v = self.vertex
        np = len(self.vertex)
        j = np - 1
        for i in range(np):
            area += (v[j][0] + v[i][0]) * (v[j][1] - v[i][1])
            j = i
        return area
    def perimiter(self):
        p = 0.0
        v = self.vertex
        np = len(v)
        j = np - 1
        for i in range(np):
            p += math.sqrt((v[j][0] - v[i][0])**2 + (v[j][1] - v[i][1])**2)
        return p

    def __repr__(self):
        str = "Polygon"
        if self.net: str += " '%s'" % (self.net)
        str += " %s" % (self.width)

def eagle_polygons(fd):
    for x in range(len(etch)):
        geom = etch[x]
        cls = geom['CLASS']
        sub = geom['SUBCLASS']

        lay = cadence_layer_to_eagle(cls,sub)

        #print "%-20s %-20s %s" % (cls,sub,lay)

        if lay is None:
            continue

        gdn = geom['GRAPHIC_DATA_NAME']
        gdm = geom['GRAPHIC_DATA_NUMBER']
        rt  = geom['RECORD_TAG']
        gd1 = geom['GRAPHIC_DATA_1']
        gd2 = geom['GRAPHIC_DATA_2']
        gd3 = geom['GRAPHIC_DATA_3']
        gd4 = geom['GRAPHIC_DATA_4']
        gd5 = geom['GRAPHIC_DATA_5']
        gd6 = geom['GRAPHIC_DATA_6']
        gd7 = geom['GRAPHIC_DATA_7']
        gd8 = geom['GRAPHIC_DATA_8']
        gd9 = geom['GRAPHIC_DATA_9']
        if geom.has_key('NET_NAME'):
            if not geom['NET_NAME']:
                net = ""
            else:
                net = "'%s'" % (geom['NET_NAME'])
        else:
            net = ""

        tag = rt.split(' ')

        print "%-20s %-20s %-20s %5s %s!%s!%s!%s!%s!%s!%s!%s!%s!" % (sub,net,tag,gdn,gd1,gd2,gd3,gd4,gd5,gd6,gd7,gd8,gd9)



eagle_polygons(sys.stdout)



#fd = open('foo.scr','w')
#for i in footprint_refs.keys():
#    eagle_footprint(fd,i)
#fd.close();



#fd = open('bbb.scr','w')
#fd.write("set WIRE_BEND 2;\n")
#fd.write("grid mil;\n")
#fd.write("drc load bbb_6_layer.dru;\n")
#eagle_place_components(fd,'bbb')
#eagle_generate_signals(fd)
#eagle_place_vias(fd)
#eagle_polygons(fd)
#fd.close()


