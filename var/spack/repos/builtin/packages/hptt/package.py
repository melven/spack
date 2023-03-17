# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hptt(CMakePackage):
    """High-Performance Tensor Transpose library"""

    homepage = "https://github.com/springer13/hptt"
    url = "https://github.com/springer13/hptt/archive/refs/tags/v1.0.5.tar.gz"
    git = "https://github.com/springer13/hptt.git"

    # version has no CMakeLists.txt, only in master
    #version("1.0.5", sha256="29f8de960f0d8825d3ae82a1bafbcf2c03793e46abbdfac0685ee9d27e2830b1")
    version("master", branch="master")
    patch("hptt_cmake_PIC.patch")

    def cmake_args(self):
        if "avx2" in self.spec.target:
            args = ['-DENABLE_AVX=On']
        else:
            args = []
        return args
