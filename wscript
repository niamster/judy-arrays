# -*- python -*-

import os

APPNAME = 'judy'
VERSION = '1.0'

top = '.'
out = 'build'

def configure(conf):
    conf.load('compiler_c')
    conf.load('compiler_cxx')

def options(opt):
    opt.load('compiler_c')
    opt.load('compiler_cxx')
    opt.add_option('--mode', action='store', default='release', help='Compile mode: release or debug')

def build(bld):
    cflags = {
        'cflags'        : ['-O2', '-Wall', '-Wextra', '-std=c11', '-Wpedantic'],
    }
    cxxflags = {
        'cxxflags'        : ['-O2', '-Wall', '-Wextra', '-std=c++14', '-Wpedantic'],
    }
    if bld.options.mode == 'debug':
        cflags['cflags'] += ['-g', '-O0']
    source = bld.path.ant_glob('src/*.c', excl=['**/%s_*.c' % x for x in ['test', 'bench']])

    features = {
        'source'        : source,
        'target'        : 'sh-judy',
    }
    features.update(cflags)
    bld.shlib(**features)

    features = {
        'source'        : source,
        'target'        : 'st-judy',
    }
    features.update(cflags)
    bld.stlib(**features)

    for test in bld.path.ant_glob('src/test_*.c'):
        features = {
            'source'        : [test],
            'target'        : os.path.splitext(str(test))[0],
            'use'           : 'st-judy',
            'lib'           : ['cunit', 'crypto', 'dl'],
        }
        features.update(cflags)
        bld.program(**features)

    for bench in bld.path.ant_glob('src/bench_*.cc'):
        features = {
            'source'        : [bench],
            'target'        : os.path.splitext(str(bench))[0],
            'use'           : 'st-judy',
            'lib'           : ['crypto', 'dl'],
            'stlib'         : ['hayai_main'],
        }
        features.update(cxxflags)
        bld.program(**features)
