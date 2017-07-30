import os

from conans import ConanFile, CMake, tools


class MsgpackConan(ConanFile):
    name = "msgpack"
    version = "2.1.3"
    license = "Boost Software License"
    url = "https://github.com/msgpack/msgpack-c/"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        tools.download("https://github.com/msgpack/msgpack-c/archive/master.zip", "master.zip")
        tools.unzip("master.zip")
        os.unlink("master.zip")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("msgpack-c-master/CMakeLists.txt", "PROJECT (msgpack)", '''PROJECT(msgpack)
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        options = {
            "CMAKE_INSTALL_BINDIR": "./bin",
            "CMAKE_INSTALL_LIBDIR": "./lib",
        }
        cmake.configure(source_dir="../msgpack-c-master", defs=options, build_dir='_build')
        cmake.build(target='install')

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["msgpackc"]
