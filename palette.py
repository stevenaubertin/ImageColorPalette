# -*- coding: utf-8 -*-

import sys
import getopt
from PIL import Image, ImageDraw
import urllib2
from cStringIO import StringIO


def about():
    print """
            Author      : Steven Aubertin
            File        : {0}
            Description : Create the color palette of an image
            Dependency  : PIL (http://www.pythonware.com/products/pil/)

            Copyright Steven Aubertin 2015
        """.format(sys.argv[0])


def load_image(filename, url=None):
    """Load the image from file or url"""
    img = None

    if url:
        img = Image.open(StringIO(urllib2.urlopen(url).read()))

    if filename:
        img = Image.open(filename)

    return img


def rescale_image(img, w=None, h=None, fw=None, fh=None):
    """Rescale the image
    w  : the new width
    h  : the new height
    fw : a scale factor for width
    fh : scale factor for height
    *** apply all these parameters in order"""

    if img:
        if w or h:
            img = img.resize((int(w), int(h)), Image.BILINEAR)
        if fw or fh:
            width, height = img.size
            img = img.resize((int(float(fw) * width), int(float(fh) * height)), Image.BILINEAR)
    return img


def rescaleImage(img, w=None, h=None, fw=None, fh=None):
    """Rescale the image
    w  : the new width
    h  : the new height
    fw : a scale factor for width
    fh : scale factor for height
    *** apply all these parameters in order"""

    if img:
        if w or h:
            img = img.resize((int(w), int(h)), Image.BILINEAR)
        if fw or fh:
            width, height = img.size
            img = img.resize((int(float(fw) * width), int(float(fh) * height)), Image.BILINEAR)
    return img


def print_usage():
    print """usage : {0}
            [-i <inputfile>]
            [-u <url>]
            [-o <outputfile>]
            [-c <outputconsole>]
            [-x <resize Width>]
            [-y <resize Height>]
            [-r <rescale>]
            [-a <about>]
            [-h <help>]""".format(sys.argv[0])


def create_band(inputfile, u, outputfile):
    img = load_image(inputfile, u)
    if not img:
        print "Error : Unable to load image."
        return -1

    pixels = list(set(list(img.getdata())))
    pixels = sorted(pixels, key=lambda x:-abs(pow(x[0] + x[1] + x[2], 2)))

    #create the image
    imgX = 20
    imgY = len(pixels)
    im = Image.new('RGB', (imgX, imgY), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    count = 0
    for i in pixels:
        draw.line((0, count, imgX, count), fill=i)
        count += 1
    del draw

    im.save(outputfile)


def main(argv):
    inputfile = None
    outputfile = None
    w = None
    h = None
    r = None
    c = None
    u = None

    try:
        opts, args = getopt.getopt(
            argv,
            "cahi:o:x:y:r:u:", ["ifile=", "ofile=", "width=", "height=", "rescale=", "console=", "url="]
        )
    except getopt.GetoptError:
        print_usage()
        return 2

    if len(opts) == 0:
        print_usage()
        return 0

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            return 0
        elif opt == '-a':
            about()
            return 0
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-u", "--url"):
            u = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-x", "--width"):
            w = arg
        elif opt in ("-y", "--height"):
            h = arg
        elif opt in ("-r", "--rescale"):
            r = arg
        elif opt in ("-c", "--console"):
            c = True

    create_band(inputfile, u, outputfile)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
