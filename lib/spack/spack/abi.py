##############################################################################
# Copyright (c) 2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import os
import spack
import spack.spec
from spack.spec import CompilerSpec
from spack.util.executable import Executable, ProcessError
from llnl.util.lang import memoized

class ABI(object):
    """This class provides methods to test ABI compatibility between specs.
       The current implementation is rather rough and could be improved."""

    def architecture_compatible(self, parent, child):
        """Returns true iff the parent and child specs have ABI compatible targets."""
        return not parent.architecture or not child.architecture \
                        or parent.architecture == child.architecture


    @memoized
    def _gcc_get_libstdcxx_version(self, version):
        """Returns gcc ABI compatibility info by getting the library version of
           a compiler's libstdc++.so or libgcc_s.so"""
        spec = CompilerSpec("gcc", version)
        compilers = spack.compilers.compilers_for_spec(spec)
        if not compilers:
            return None
        compiler = compilers[0]
        rungcc = None
        libname = None
        output = None
        if compiler.cxx:
            rungcc = Executable(compiler.cxx)
            libname = "libstdc++.so"
        elif compiler.cc:
            rungcc = Executable(compiler.cc)
            libname = "libgcc_s.so"
        else:
            return None
        try:
            output = rungcc("--print-file-name=%s" % libname, return_output=True)
        except ProcessError, e:
            return None
        if not output:
            return None
        libpath = os.readlink(output.strip())
        if not libpath:
            return None
        return os.path.basename(libpath)
        
        
    @memoized
    def _gcc_compiler_compare(self, pversion, cversion):
        """Returns true iff the gcc version pversion and cversion 
          are ABI compatible."""
        plib = self._gcc_get_libstdcxx_version(pversion)
        clib = self._gcc_get_libstdcxx_version(cversion)
        if not plib or not clib:
            return False
        return plib == clib


    def _intel_compiler_compare(self, pversion, cversion):
        """Returns true iff the intel version pversion and cversion
           are ABI compatible"""

        #Test major and minor versions.  Ignore build version.
        if (len(pversion.version) < 2 or len(cversion.version) < 2):
            return False
        return (pversion.version[0] == cversion.version[0]) and \
            (pversion.version[1] == cversion.version[1])
        
    
    def compiler_compatible(self, parent, child, **kwargs):
        """Returns true iff the compilers for parent and child specs are ABI compatible"""
        if not parent.compiler or not child.compiler:
            return True
        
        if parent.compiler.name != child.compiler.name:
            #Different compiler families are assumed ABI incompatible
            return False
        
        if kwargs.get('loose', False):
            return True

        for pversion in parent.compiler.versions:
            for cversion in child.compiler.versions:
                #For a few compilers use specialized comparisons.  Otherwise
                # match on version match.
                if pversion.satisfies(cversion):
                    return True
                elif parent.compiler.name == "gcc" and \
                     self._gcc_compiler_compare(pversion, cversion):
                    return True
                elif parent.compiler.name == "intel" and \
                     self._intel_compiler_compare(pversion, cversion):
                    return True
        return False

    
    def compatible(self, parent, child, **kwargs):
        """Returns true iff a parent and child spec are ABI compatible"""
        loosematch = kwargs.get('loose', False)
        return self.architecture_compatible(parent, child) and \
               self.compiler_compatible(parent, child, loose=loosematch)
    
