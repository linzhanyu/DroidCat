# -*- coding:utf-8 -*-
#
import os, sys, getopt

__DEBUG = False

def init_path():
    curdir = os.getcwd()
    sys.path.append( curdir )
    sys.path.append( os.path.join( curdir, 'Utile' ) )
    sys.path.append( os.path.join( curdir, 'Core' ) )
    sys.path.append( os.path.join( curdir, 'UI' ) )

def init_debug():
    if __DEBUG :
        import pdb
        pdb.set_trace()

def main( argv ):
    init_debug()
    init_path()

    from Core import AndroidLogcat
    AndroidLogcat.Logcat()

if __name__ == '__main__':
    main( sys.argv[1:] )


