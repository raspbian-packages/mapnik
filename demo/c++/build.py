#
# This file is part of Mapnik (c++ mapping toolkit)
#
# Copyright (C) 2009 Artem Pavlenko, Dane Springmeyer
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

import os
from copy import copy

Import ('env')

source = Split(
    """
    rundemo.cpp
    """
    )

demo_env = env.Clone()


demo_env['CXXFLAGS'] = copy(env['LIBMAPNIK_CXXFLAGS'])

if env['HAS_CAIRO']:
    demo_env.PrependUnique(CPPPATH=env['CAIROMM_CPPPATHS'])
    demo_env.Append(CXXFLAGS = '-DHAVE_CAIRO')

libraries =  copy(env['LIBMAPNIK_LIBS'])
boost_program_options = 'boost_program_options%s' % env['BOOST_APPEND']
libraries.extend([boost_program_options,'mapnik2'])

rundemo = demo_env.Program('rundemo', source, LIBS=libraries, LINKFLAGS=env["CUSTOM_LDFLAGS"])

Depends(rundemo, env.subst('../../src/%s' % env['MAPNIK_LIB_NAME']))

# we don't install this app because the datasource paths are relative
# and we're not going to install the sample data.
#env.Install(install_prefix + '/bin', rundemo)
#env.Alias('install', install_prefix + '/bin')