#
# This file is part of Mapnik (c++ mapping toolkit)
#
# Copyright (C) 2006 Artem Pavlenko, Jean-Francois Doyon
#
# Mapnik is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# $Id$

import os, re, sys, glob
from subprocess import Popen, PIPE


Import('env')

def call(cmd, silent=True):
    stdin, stderr = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if not stderr:
        return stdin.strip()
    elif not silent:
        print stderr

def run_2to3(*args,**kwargs):
    call('2to3 -w %s' % os.path.dirname(kwargs['target'][0].path))

def is_py3():
    return 'True' in os.popen('''%s -c "import sys as s;s.stdout.write(str(s.version_info[0] == 3))"''' % env['PYTHON']).read().strip()


prefix = env['PREFIX']
target_path = env['PYTHON_INSTALL_LOCATION'] + os.path.sep + 'mapnik2'

libraries = ['mapnik2','png']

if env['JPEG']:
    libraries.append('jpeg')

if env['BOOST_PYTHON_LIB']:
    if os.path.sep in env['BOOST_PYTHON_LIB']:
        pylib_dir = os.path.dirname(env['BOOST_PYTHON_LIB'])
        env.Prepend(LIBPATH = pylib_dir)
        pylib_name = os.path.splitext(os.path.basename(env['BOOST_PYTHON_LIB']))[0].replace('lib','',1)
        libraries.append(pylib_name)
    else:
        libraries.append(env['BOOST_PYTHON_LIB'].replace('lib','',1))
else:
    if is_py3():
        libraries.append('boost_python3%s' % env['BOOST_APPEND'])
    else:
        libraries.append('boost_python%s' % env['BOOST_APPEND'])

if env['PLATFORM'] == 'Darwin':
    libraries.append(env['ICU_LIB_NAME'])
    libraries.append('boost_regex%s' % env['BOOST_APPEND'])
    if env['THREADING'] == 'multi':
        libraries.append('boost_thread%s' % env['BOOST_APPEND'])

    ##### Python linking on OS X is tricky ### 
    # Confounding problems are:
    # 1) likelyhood of multiple python installs of the same major.minor version
    #  because apple supplies python built-in and many users may have installed 
    #  further versions using macports
    # 2) boost python directly links to a python version
    # 3) the below will directly link _mapnik.so to a python version
    # 4) _mapnik.so must link to the same python lib as boost_python.dylib otherwise
    # python will Abort with a Version Mismatch error.
    # See http://trac.mapnik.org/ticket/453 for the seeds of a better approach
    # for now we offer control over method of direct linking...
    # The default below is to link against the python dylib in the form of
    #/path/to/Python.framework/Python instead of -lpython
    
    # http://developer.apple.com/mac/library/DOCUMENTATION/Darwin/Reference/ManPages/man1/ld.1.html
    
    if env['PYTHON_DYNAMIC_LOOKUP']:
        python_link_flag = '-undefined dynamic_lookup'
    elif env['FRAMEWORK_PYTHON']:
        if env['FRAMEWORK_SEARCH_PATH']:
            # if the user has supplied a custom root path to search for 
            # a given Python framework, then use that to direct the linker
            python_link_flag = '-F%s -framework Python -Z' % env['FRAMEWORK_SEARCH_PATH']
        else:
            # otherwise be as explicit as possible for linking to the same Framework
            # as the executable we are building with (or is pointed to by the PYTHON variable)
            # otherwise we may accidentally link against either:
            # /System/Library/Frameworks/Python.framework/Python/Versions/
            # or
            # /Library/Frameworks/Python.framework/Python/Versions/
            # See: http://trac.mapnik.org/ticket/380
            link_prefix = env['PYTHON_SYS_PREFIX']
            if '.framework' in link_prefix:
                python_link_flag = '-F%s -framework Python -Z' % os.path.dirname(link_prefix.split('.')[0])
            elif '/System' in link_prefix:
                python_link_flag = '-F/System/Library/Frameworks/ -framework Python -Z'
            else:
                # should we fall back to -lpython here?
                python_link_flag = '-F/ -framework Python'
            
    # if we are not linking to a framework then use the *nix standard approach
    else:
        # TODO - do we need to pass -L/?
        python_link_flag = '-lpython%s' % env['PYTHON_VERSION']
elif env['PLATFORM'] == 'SunOS':
    # make sure to explicitly link mapnik.so against
    # libmapnik in its installed location
    python_link_flag = '-R%s' % env['MAPNIK_LIB_BASE']
else:
    # all other platforms we don't directly link python
    python_link_flag = ''

if env['CUSTOM_LDFLAGS']:
    linkflags = '%s %s' % (env['CUSTOM_LDFLAGS'], python_link_flag)
else:
    linkflags = python_link_flag

paths = '''
"""Configuration paths of Mapnik fonts and input plugins (auto-generated by SCons)."""

import os

mapniklibpath = '%s'
'''

paths += "inputpluginspath = os.path.normpath(mapniklibpath + '/input')\n"

if env['SYSTEM_FONTS']:
    paths += "fontscollectionpath = os.path.normpath('%s')" % env['SYSTEM_FONTS']
else:
    paths += "fontscollectionpath = os.path.normpath(mapniklibpath + '/fonts')"


if not os.path.exists('mapnik'):
    os.mkdir('mapnik')
file('mapnik/paths.py','w').write(paths % (env['MAPNIK_LIB_DIR']))

try:
    os.chmod('mapnik/paths.py',0666)
except: pass

# install the core mapnik python files, including '__init__.py' and 'paths.py'
if 'install' in COMMAND_LINE_TARGETS:
    init_files = glob.glob('mapnik/*.py')
    init_module = env.Install(target_path, init_files)
    env.Alias(target='install', source=init_module)

# install the ogcserver module code
if 'install' in COMMAND_LINE_TARGETS:
    ogcserver_files = glob.glob('mapnik/ogcserver/*.py')
    ogcserver_module = env.Install(target_path + '/ogcserver', ogcserver_files)
    env.Alias(target='install', source=ogcserver_module)


# install the shared object beside the module directory
sources = glob.glob('*.cpp')


py_env = env.Clone()
py_env.Append(CPPPATH = env['PYTHON_INCLUDES'])

if env['HAS_CAIRO']:
    py_env.Append(CPPPATH = env['CAIROMM_CPPPATHS'])
    py_env.Append(CXXFLAGS = '-DHAVE_CAIRO')
    if env['PLATFORM'] == 'Darwin':
        py_env.Append(LIBS=env['CAIROMM_LINKFLAGS'])

if env['HAS_PYCAIRO']:
    py_env.ParseConfig('pkg-config --cflags pycairo')
    py_env.Append(CXXFLAGS = '-DHAVE_PYCAIRO')

if env['SVN_REVISION']:
    sources.remove('mapnik_python.cpp')
    env2 = py_env.Clone()
    env2.Append(CXXFLAGS='-DSVN_REVISION=%s' % env['SVN_REVISION'])
    sources.insert(0,env2.SharedObject('mapnik_python.cpp'))

_mapnik = py_env.LoadableModule('mapnik/_mapnik2', sources, LIBS=libraries, LDMODULEPREFIX='', LDMODULESUFFIX='.so',LINKFLAGS=linkflags)

Depends(_mapnik, env.subst('../../src/%s' % env['MAPNIK_LIB_NAME']))

if env['PLATFORM'] == 'SunOS' and env['PYTHON_IS_64BIT']:
    # http://mail.python.org/pipermail/python-dev/2006-August/068528.html
    cxx_module_path = os.path.join(target_path,'64')
else:
    cxx_module_path = target_path
    
if 'uninstall' not in COMMAND_LINE_TARGETS:
    pymapniklib = env.Install(cxx_module_path,_mapnik)
    py_env.Alias(target='install',source=pymapniklib)
    if 'install' in COMMAND_LINE_TARGETS:
        if is_py3():
            env.AddPostAction(pymapniklib, run_2to3)


env['create_uninstall_target'](env, target_path)
    