# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyside2(PythonPackage):
    """Python bindings for Qt."""

    homepage = "https://www.pyside.org/"
    git = "https://code.qt.io/pyside/pyside-setup.git"
    url = "https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-5.15.14-src/pyside-setup-opensource-src-5.15.14.tar.xz"

    # More recent versions of PySide2 (for Qt5) have been taken under
    # the offical Qt umbrella.  For more information, see:
    # https://wiki.qt.io/Qt_for_Python_Development_Getting_Started

    license("LGPL-3.0-or-later")

    version("develop", tag="dev")
    version("5.15.14", sha256="32651194f6a6b7bce42f04e68b1401ad2087e4789a4c8f3fb8649e86189c6372")
    # untested
    # version("5.15.13", sha256="7a57797b20268d6ebcb39deba48c754a69abf9221aee03e1f3dca6f6565b7da9")
    # version("5.15.12", sha256="9c53a111ca5779064593e690db0da43ce0d5dad25369931b7a4f593886259ff4")
    # version("5.15.11", sha256="da567cd3b7854d27a0b4afe3e89de8b2f98b7a6d57393be56f1fc13f770faf29")
    # version("5.15.10", sha256="2af691d3613a41f83a60439b46568fc2c696dbfae42f7cd7b07152d115ead33a")
    # version("5.15.8", sha256="23436302c8deb5b4cbc769b205d09604e38ba83b40708efccb7bd8c9af6f6b5d")
    # version("5.15.7", sha256="f61210ae24e6882d5d0ca0059229e5dc4f35e2bca92dd6caf96c0f41943a8294")
    # version("5.15.6", sha256="171ee058d056599b8e9e8605fe3dae5dabdab7764285b21b28f64760a0f6779d")
    # version("5.15.5", sha256="3920a4fb353300260c9bc46ff70f1fb975c5e7efa22e9d51222588928ce19b33")
    # version("5.15.4", sha256="3c68ed0def4111ef5d0641370306338d277ae8983a77eaf22f223ddd3a14450b")
    # version("5.15.3", sha256="7ff5f1cc4291fffb6d5a3098b3090abe4d415da2adec740b4e901893d95d7137")
    version(
        "5.15.2.1",
        tag="v5.15.2.1",
        commit="9282e03de471bb3772c8d3997159e49c113d7678",
        submodules=True,
    )
    version(
        "5.14.2.1",
        tag="v5.14.2.1",
        commit="6341c063dea6022c1e40cca28d3bbf0f52350dcb",
        submodules=True,
    )
    version(
        "5.13.2", tag="v5.13.2", commit="a1a94b43c5b277fd4e65c1389e24c4fbbb1c5641", submodules=True
    )
    version(
        "5.13.1", tag="v5.13.1", commit="de1e75b55f6f59bba4bae5cd036d6c355c62986a", submodules=True
    )
    version(
        "5.13.0", tag="v5.13.0", commit="208d0c8bc8595aebc2191dafd9d0e3ec719e2550", submodules=True
    )
    version(
        "5.12.5", tag="v5.12.5", commit="af0953e0d261ab9b1fc498d63e8d790a329dd285", submodules=True
    )

    variant(
        "doc",
        default=False,
        description="Enables the generation of html and man page documentation",
    )

    # see https://wiki.qt.io/Qt_for_Python#Python_compatibility_matrix
    depends_on("python@2.7.0:2.7,3.5.0:3.5,3.6.1:3.8", when="@:5.15.0", type=("build", "run"))
    depends_on(
        "python@2.7.0:2.7,3.5.0:3.5,3.6.1:3.9", when="@5.15.1:5.15.7", type=("build", "run")
    )
    depends_on("python@2.7:3.10", when="@5.15.8", type=("build", "run"))
    depends_on("python@3.5:3.10", when="@5.15.9:5.15.10", type=("build", "run"))
    depends_on("python@3.6:3.11", when="@5.15.11:5.15.15", type=("build", "run"))

    depends_on("cmake@3.1:", type="build")
    # libclang versioning from sources/shiboken2/doc/gettingstarted.rst
    depends_on("llvm@6", type="build", when="@5.12:5.13")
    # clang >= 16 doesn't work, see https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=270715#c6
    depends_on("llvm@10:15 +clang", type="build", when="@5.15")
    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-wheel", type="build")
    # https://bugreports.qt.io/browse/PYSIDE-1385
    depends_on("py-wheel@:0.34", when="@:5.14", type="build")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")
    depends_on("qt@5.11:+opengl")

    depends_on("graphviz", when="+doc", type="build")
    depends_on("libxml2@2.6.32:", when="+doc", type="build")
    depends_on("libxslt@1.1.19:", when="+doc", type="build")
    depends_on("py-sphinx", when="+doc", type="build")

    def patch(self):
        filter_file(
            "=${shiboken_include_dirs}",
            ":".join(
                [
                    "=${shiboken_include_dirs}",
                    self.spec["qt"]["glx"]["libglx"].prefix.include,
                    self.spec["qt"]["libxcb"].prefix.include,
                ]
            ),
            "sources/pyside2/cmake/Macros/PySideModules.cmake",
            string=True,
        )

    def setup_build_environment(self, env):
        env.set("LLVM_INSTALL_DIR", self.spec["llvm"].prefix)

    def install_options(self, spec, prefix):
        args = [
            "--parallel={0}".format(make_jobs),
            "--ignore-git",
            # if you want to debug build problems, uncomment this
            # "--verbose-build",
            "--qmake={0}".format(spec["qt"].prefix.bin.qmake),
        ]
        # older versions allow some limited api for @3.10:
        # (prevented currently by dependency matrix above!)
        if spec.satisfies("@:5.15.2 ^python@3.10:"):
            args.append("--limited-api=yes")

        # fix rpaths
        args.append("--rpath={0}".format(":".join(self.rpath)))

        if self.run_tests:
            args.append("--build-tests")
        return args

    def install(self, spec, prefix):
        python("setup.py", "install", "--prefix=" + prefix, *self.install_options(spec, prefix))

    @run_after("install")
    def install_docs(self):
        if "+doc" in self.spec:
            make("apidoc")
