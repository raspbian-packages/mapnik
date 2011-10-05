
import re
import os
import sys
from copy import copy

Import('env')

config_env = env.Clone()

# TODO
# major/minor versions
# git hash

config_variables = '''#!/bin/sh

## variables

CONFIG_PREFIX=%(prefix)s
CONFIG_MAPNIK_LIBNAME=%(mapnik_libname)s
CONFIG_MAPNIK_INCLUDE=${CONFIG_PREFIX}/include
CONFIG_MAPNIK_LIB=${CONFIG_PREFIX}/%(libdir_schema)s
CONFIG_MAPNIK_VERSION='%(version)s'
CONFIG_MAPNIK_LDFLAGS='%(ldflags)s'
CONFIG_DEP_LIBS='%(dep_libs)s'
CONFIG_OTHER_INCLUDES='%(other_includes)s'
CONFIG_FONTS='%(fonts)s'
CONFIG_INPUT_PLUGINS='%(input_plugins)s'
CONFIG_SVN_REVISION='%(svn_revision)s'

CONFIG_JSON="{
  \\"prefix\\": \\"${CONFIG_PREFIX}\\",
  \\"mapnik_libname\\": \\"${CONFIG_MAPNIK_LIBNAME}\\",
  \\"mapnik_include\\": \\"${CONFIG_MAPNIK_INCLUDE}\\",
  \\"mapnik_lib\\": \\"${CONFIG_MAPNIK_LIB}\\",
  \\"version\\": \\"${CONFIG_MAPNIK_VERSION}\\",
  \\"ldflags\\": \\"${CONFIG_MAPNIK_LDFLAGS}\\",
  \\"dep_libs\\": \\"${CONFIG_DEP_LIBS}\\",
  \\"other_includes\\": \\"${CONFIG_OTHER_INCLUDES}\\",
  \\"fonts\\": \\"${CONFIG_FONTS}\\",
  \\"input_plugins\\": \\"${CONFIG_INPUT_PLUGINS}\\",
  \\"svn_revision\\": ${CONFIG_SVN_REVISION}
}"

'''

def write_config(configuration,template,config_file):
    template = open(template,'r').read()
    open(config_file,'w').write(config_variables  % configuration + template)
    try:
        os.chmod(config_file,0755)
    except: pass


# todo - refine this list

other_includes = ''.join([' -I%s' % i for i in config_env['CPPPATH'] if not i.startswith('#')])

other_includes += ' '

other_includes += ' '.join(config_env['LIBMAPNIK_CXXFLAGS'])

other_includes += ' '

if config_env['HAS_CAIRO']:
    other_includes += ''.join([' -I%s' % i for i in env['CAIROMM_CPPPATHS'] if not i.startswith('#')])    


ldflags = config_env['CUSTOM_LDFLAGS'] + ''.join([' -L%s' % i for i in config_env['LIBPATH'] if not i.startswith('#')])

dep_libs = ''.join([' -l%s' % i for i in env['LIBMAPNIK_LIBS']])

if env['INTERNAL_LIBAGG']:
    dep_libs = dep_libs.replace('-lagg','')

configuration = {
    "prefix": config_env['PREFIX'],
    "mapnik_libname": 'mapnik2',
    "libdir_schema": config_env['LIBDIR_SCHEMA'],
    "ldflags": ldflags,
    "dep_libs": dep_libs,
    "other_includes": other_includes,
    "fonts": config_env['MAPNIK_FONTS'],
    "input_plugins": config_env['MAPNIK_INPUT_PLUGINS'],
    "svn_revision": config_env['SVN_REVISION'],
    "version": config_env['MAPNIK_VERSION_STRING'],
}


template = 'mapnik-config.template.sh'
config_file = 'mapnik-config'
source = config_file
write_config(configuration,template,config_file)
target_path = os.path.normpath(os.path.join(config_env['INSTALL_PREFIX'],'bin'))
full_target = os.path.join(target_path,config_file)

Depends(full_target, env.subst('../../src/%s' % env['MAPNIK_LIB_NAME']))

if 'install' in COMMAND_LINE_TARGETS:
    # we must add 'install' catch here because otherwise
    # custom command will be run when not installing
    env.Alias('install',full_target)
    
    env.Command(full_target, config_file,
       [
       Copy("$TARGET","$SOURCE"),
       Chmod("$TARGET", 0755),
       ])

config_env['create_uninstall_target'](env,os.path.join(target_path,config_file))
