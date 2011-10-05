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

prefix = env['PREFIX']

program_env = env.Clone()

source = Split(
    """
    main.cpp
    sqlite.cpp
    """
    )

headers = ['#plugins/input/postgis'] + env['CPPPATH'] 


libraries = []
boost_program_options = 'boost_program_options%s' % env['BOOST_APPEND']
libraries.extend([boost_program_options,'sqlite3','pq','mapnik2'])

pgsql2sqlite = program_env.Program('pgsql2sqlite', source, CPPPATH=headers, LIBS=libraries, LINKFLAGS=env['CUSTOM_LDFLAGS'])
Depends(pgsql2sqlite, env.subst('../../src/%s' % env['MAPNIK_LIB_NAME']))

if 'uninstall' not in COMMAND_LINE_TARGETS:
    env.Install(os.path.join(env['INSTALL_PREFIX'],'bin'), pgsql2sqlite)
    env.Alias('install', os.path.join(env['INSTALL_PREFIX'],'bin'))

env['create_uninstall_target'](env, os.path.join(env['INSTALL_PREFIX'],'bin','pgsql2sqlite'))
