# -*- coding: utf-8 -*-


import sys
import getopt
from PIL import Image, ImageDraw

def about():
    print """
            Author      : Steven Aubertin
            File        : {0}
            Description : Merge multiple images together
            Dependency  : PIL (http://www.pythonware.com/products/pil/)

            Copyright Steven Aubertin 2015
        """.format(sys.argv[0])

def print_usage():
    print """usage : {0}
            [-i <inputfile>]
            [-o <outputfile>]
            [-c <outputconsole>]
            [-x <resize Width>]
            [-y <resize Height>]
            [-r <rescale>]
            [-a <about>]
            [-h <help>]""".format(sys.argv[0])


def concat(filename, images=[], mode='RGB'):
    j = 0
    print 'Computing size...'
    size = (0, 0)
    for i in images:
        w,h = i.size
        size  = (w if w > size[0] else size[0], h if h > size[1] else size[1])
        sys.stdout.write("\r%f%%" % ((float(j) / float(len(images)))*100.0))
        sys.stdout.flush()
        j += 1
    size = (size[0] * len(images), size[1]/10)
    sys.stdout.write("\r%f%%" % 100)
    sys.stdout.flush()

    print
    print 'Creating image of size', size
    img = Image.new(mode, size)

    print 'Processing...'
    pos = (0, 0)
    j = 0
    for i in images:
        img.paste(i, pos)
        pos = (i.size[0] + pos[0], 0)
        sys.stdout.write("\r%f%%" % ((float(j) / float(len(images)))*100.0))
        sys.stdout.flush()
        j += 1
    sys.stdout.write("\r%f%%" % 100)
    sys.stdout.flush()
    print

    return img


def main(argv):
    inputfile = None
    outputfile = None
    d = None
    w = None
    h = None
    r = None
    c = None
    u = None

    try:
        opts, args = getopt.getopt(
            argv,
            "cahi:o:x:y:r:d:", ["ifile=", "ofile=", "width=", "height=", "rescale=", "console=", "directory="]
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
        elif opt in ("-d", "--directory"):
            d = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
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

    print 'Loading source images...'
    images = []
    for i in xrange(0, 330):
        images.append(Image.open('/Users/xor/Desktop/out_main/band{0}.png'.format(i), 'r'))
        sys.stdout.write("\r%f%%" % ((float(i) / float(len(images)))*100.0))
        sys.stdout.flush()
    sys.stdout.write("\r%f%%" % 100)
    sys.stdout.flush()
    print

    img = concat(inputfile, images)
    print 'Saving file', outputfile
    img.save(outputfile)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
