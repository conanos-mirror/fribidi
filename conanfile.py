from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class FribidiConan(ConanFile):
    name = "fribidi"
    version = "0.19.7"
    description = "GNU FriBidi is an implementation of the Unicode Bidirectional Algorithm"
    url = "https://github.com/conan-multimedia/fribidi"
    homepage = "http://fribidi.org/"
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "libffi/3.3-rc0@conanos/dev","glib/2.58.0@conanos/dev"
    source_subfolder = "source_subfolder"

    def source(self):
        tools.get('https://github.com/fribidi/fribidi/releases/download/{version}/{name}-{version}.tar.bz2'.format(name=self.name, version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            #self.run("autoreconf -f -i")

            _args = ["--prefix=%s/builddir"%(os.getcwd())]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            
            self.run('./configure %s'%(' '.join(_args)))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

