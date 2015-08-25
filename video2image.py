# -*- coding: utf-8 -*-

import sys
import re
import subprocess
import getopt
from decimal import Decimal
import time

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

def get_video_length(path):
    process = subprocess.Popen(['ffmpeg', '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?)", stdout, re.DOTALL).groupdict()
    return (Decimal(matches['hours']), Decimal(matches['minutes']), Decimal(matches['seconds']))


def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


def get_frames(length, step=1):
    frames = []
    if length[0]:
        for h in drange(0, length[0]+1, step):
            for m in drange(0, length[1]+1, step):
                for s in drange(0, length[2]+1, step):
                    frames.append('{0}:{1}:{2}'.format(h,m,s))
    else:
        for m in drange(0, length[1]+1, step):
            for s in drange(0, length[2]+1, step):
                frames.append('{0}:{1}:{2}'.format(0,m,s))
    return frames


def convert(path, outputfile, step=1):
    length =  get_video_length(path)
    print 'Video lenght {0}:{1}:{2}'.format(length[0], length[1], length[2])

    frames = get_frames(length,step)
    print 'Number of frames {0}'.format(len(frames))

    print
    print 'Processing...'
    i = 0
    for frame in frames:
        process = subprocess.Popen(['ffmpeg',
                                    '-i', path,
                                    '-vcodec', 'png',
                                    '-ss', frame,
                                    '-vframes', '1',
                                    '-an',
                                    '-f',
                                    'rawvideo',
                                    outputfile.format(i)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        try:
            process.wait()
        except:
            pass
        sys.stdout.write("\r%f%%" % ((float(i) / float(len(frames)))*100.0))
        sys.stdout.flush()
        i += 1


def main(argv):
    inputfile = None
    outputfile = None

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
            #about()
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

    convert(inputfile, outputfile if outputfile else '/Users/xor/Desktop/out/test{0}.png')

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))