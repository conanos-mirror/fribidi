from conans import ConanFile, CMake, tools, Meson
from shutil import copyfile
import os
from conanos.build import config_scheme

class FribidiConan(ConanFile):
    name = "fribidi"
    version = "1.0.5"
    description = "GNU FriBidi is an implementation of the Unicode Bidirectional Algorithm"
    url = "https://github.com/conan-multimedia/fribidi"
    homepage = "http://fribidi.org/"
    license = "LGPLv2_1Plus"
    generators = "visual_studio", "gcc"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = { 'shared': True, 'fPIC': True }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    
    def build_requirements(self):
        self.build_requires("glib/2.58.1@conanos/stable")
        self.build_requires("libffi/3.299999@conanos/stable")
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def configure(self):
        del self.settings.compiler.libcxx


    def source(self):
        url_ = 'https://github.com/fribidi/fribidi/archive/v{version}.tar.gz'.format(version=self.version)
        tools.get(url_)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        pkg_config_paths=[ os.path.join(self.deps_cpp_info[i].rootpath, "lib", "pkgconfig") for i in ["glib","libffi"] ]
        prefix = os.path.join(self.build_folder, self._build_subfolder, "install")
        meson = Meson(self)

        meson.configure(defs={'prefix' : prefix,'docs':'false','libdir':'lib'},
                        source_dir=self._source_subfolder, build_dir=self._build_subfolder,
                        pkg_config_paths=pkg_config_paths)
        meson.build()
        self.run('ninja -C {0} install'.format(meson.build_dir))

    def package(self):
        self.copy("*", dst=self.package_folder, src=os.path.join(self.build_folder,self._build_subfolder, "install"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

