#!/usr/bin/env python

import os, sys
from glob import glob
from scipy_distutils.core import Extension
from scipy_distutils.misc_util import get_path, default_config_dict, dot_join

def _copyfile(src, dest, paths):
    file_src = os.path.join(paths, src)
    file_dest = os.path.join(paths, dest)
    destid = open(file_dest,'w')
    srcid = open(file_src,'r')
    destid.write(srcid.read())
    destid.close()
    srcid.close()
    return

def configuration(parent_package=''):
    config = default_config_dict('special',parent_package)
    local_path = get_path(__name__)

    c_misc = glob(os.path.join(local_path,'c_misc','*.c'))
    cephes = glob(os.path.join(local_path,'cephes','*.c'))
    mach = glob(os.path.join(local_path,'mach','*.f'))
    amos = glob(os.path.join(local_path,'amos','*.f'))
    toms = glob(os.path.join(local_path,'toms','*.f'))
    cdf = glob(os.path.join(local_path,'cdflib','*.f'))
    specfun = glob(os.path.join(local_path, 'specfun','*.f'))
    
    # C libraries
    config['libraries'].append(('c_misc',{'sources':c_misc}))
    config['libraries'].append(('cephes',{'sources':cephes}))
    
    # Fortran libraries
    config['fortran_libraries'].append(('mach',{'sources':mach}))
    config['fortran_libraries'].append(('amos',{'sources':amos}))
    config['fortran_libraries'].append(('toms',{'sources':toms}))
    config['fortran_libraries'].append(('cdf',{'sources':cdf}))
    config['fortran_libraries'].append(('specfun',{'sources':specfun}))
    
    # Extension
    sources = ['cephesmodule.c', 'amos_wrappers.c', 'specfun_wrappers.c',
               'toms_wrappers.c','cdf_wrappers.c','ufunc_extras.c']
    sources = [os.path.join(local_path,x) for x in sources]
    ext = Extension(dot_join(parent_package,'special.cephes'),sources,
                    libraries = ['amos','toms','c_misc','cephes','mach', 'cdf', 'specfun']
                    )
    config['ext_modules'].append(ext)

    # Test to see if big or little-endian machine and get correct default
    #   mconf.h module.
    cephes_path = os.path.join(local_path, 'cephes')
    if sys.byteorder == "little":
        print "### Little Endian detected ####"
        _copyfile('mconf_LE.h','mconf.h',cephes_path)
    else:
        print "### Big Endian detected ####"
        _copyfile('mconf_BE.h','mconf.h',cephes_path)

        
    return config

if __name__ == '__main__':
    from scipy_distutils.core import setup
    setup(**configuration())
