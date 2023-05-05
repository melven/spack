# Copyright (C) 2023 DLR (Karsten Bock, Melven Roehrig-Zoellner)
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vast(CMakePackage):
    """VAST (Versatile Aeromechanic Simulation Tool) is developed by the Rotorcraft
    department of the Institute of Flight Systems of the German Aerospace Agency (DLR)."""

    homepage = "https://gitlab.dlr.de/vast/unrestricted/VAST"
    url = "https://gitlab.dlr.de/vast/unrestricted/VAST/-/archive/v1.0/VAST-v1.0.tar.gz"
    git = "https://gitlab.dlr.de/vast/unrestricted/VAST.git"
    maintainers = ["Melven.Roehrig-Zoellner@DLR.de"]

    version("1.2", tag="v1.2")
    version("1.1", tag="v1.1")
    version("1.0", tag="v1.0")
    version("develop", branch="master")

    variant("python", description="Build python module/interface", default=True)
    variant("doc", description="Build and install documentation", default=False)
    variant("mpi", description="Build with MPI parallelization", default=True)
    variant("gui", description="Add dependencies to run the GUI", default=False)

    depends_on("git", type="build")

    depends_on("tixi+fortran+shared", type=("build", "link", "run"))
    depends_on("tixi@3.3:", when="@1.2:")
    depends_on("tixi@2.2.4", when="@:1.1")

    depends_on("eigen@3.3:")
    depends_on("lapack")
    depends_on("mpi@2:", when="+mpi")

    # python binding
    depends_on("python@2.6.8:", type="build", when="~python")
    depends_on("python@3.8:", type=("build", "link", "run"), when="+python")
    depends_on("py-pybind11", type="build", when="+python")
    depends_on("py-numpy", type="run", when="+python")

    # documentation
    depends_on("texlive", type="build", when="+doc")

    # GUI
    depends_on("python@3.8:", type="run", when="+gui")
    depends_on("py-pyside2@5.12:", type="run", when="+gui")
    depends_on("py-matplotlib@3.1:", type="run", when="+gui")
    depends_on("opencv@4.1:+python3", type="run", when="+gui")
    depends_on("py-pyopengl", type="run", when="+gui")

    def cmake_args(self):
        return [
            self.define_from_variant("VAST_BUILD_PYTHON_MODULE", "python"),
            self.define_from_variant("VAST_BUILD_DOC", "doc"),
            self.define_from_variant("VAST_USE_MPI", "mpi"),
        ]

    def setup_build_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["tixi"].prefix.lib)

    def setup_run_environment(self, env):
        if "+python" in self.spec:
            env.prepend_path("PYTHONPATH", self.prefix.lib)
