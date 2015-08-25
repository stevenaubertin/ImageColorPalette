# -*- coding: utf-8 -*-

import os
import sys
from palette import *
from video2image import *

def about():
    print """
            Author      : Steven Aubertin
            File        : {0}
            Description : Create an band histogram of a video
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


def create_directory(d, MAX_TRY=3):
    if not os.path.isdir(d):
        for i in xrange(0, MAX_TRY):
            create = raw_input('Directory {0} does not exists, do you wish to create it ?[y\\n]\n> '.format(d)).upper()
            if create == 'Y' or create == 'YES':
                os.mkdir(d)
                print 'Directory ', d, 'created.'
                return True
            elif create == 'N' or create == 'NO':
                print 'Need a directory to perform action, program closing.'
                return False
    return True


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

    if not create_directory(d):
        return 0

    name_ext = outputfile.split('.')
    outputfile = ''.join([name_ext[0], '{0}.', name_ext[1]])
    #convert(inputfile, ''.join([d, outputfile]))

    print 'Creating bands images...'
    i = 0
    images = sorted(filter(lambda x: 'png' in x and name_ext[0] in x, os.listdir(d)), key=lambda x: int(x[len(name_ext[0]):].split('.')[0]))
    for f in images:
        out = ''.join([d, 'band{0}.png'.format(i)])
        create_band(''.join([d,f]),  u, out)
        sys.stdout.write("\r%f%%" % ((float(i) / float(len(images)))*100.0))
        sys.stdout.flush()
        i += 1
    sys.stdout.write("\r%f%%" % 100)
    sys.stdout.flush()


    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
