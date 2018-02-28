#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibgcryptConan(ConanFile):
    name = "libgcrypt"
    version = "1.7.3"
    url = "http://github.com/DEGoodmanWilson/conan-libgcrypt"
    description = "The GNU bignum library"
    license = "https://www.gnupg.org/software/libgcrypt/index.html"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "enable_m_guard": [True, False],
               "disable_asm": [True, False],
               "enable_ld_version_script": [True, False],
               "disable_endian_check": [True, False],
               "enable_random_daemon": [True, False],
               "enable_hmac_binary_check": [True, False],
               "disable_padlock_support": [True, False],
               "disable_aesni_support": [True, False],
               "disable_O_flag_munging": [True, False]}
               #TODO add in non-binary flags

    default_options = "shared=False", "enable_m_guard=False", "disable_asm=False", \
                      "enable_ld_version_script=False", "disable_endian_check=False", \
                      "enable_random_daemon=False", "disable_aesni_support=False", \
                      "enable_hmac_binary_check=False", "disable_padlock_support=False", \
                      "disable_O_flag_munging=False"

    requires = 'libgpg-error/1.24@DEGoodmanWilson/stable'


    def source(self):
        source_url = "https://gnupg.org/ftp/gcrypt/libgcrypt"
        tools.get("{0}/libgcrypt-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            # self.build_vs()
            self.output.fatal("No windows support yet. Sorry. Help a fellow out and contribute back?")

        with tools.chdir("sources"):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True

            config_args = []
            for option_name in self.options.values.fields:
                if(option_name == "shared"):
                    if(getattr(self.options, "shared")):
                        config_args.append("--enable-shared")
                        config_args.append("--disable-static")
                    else:
                        config_args.append("--enable-static")
                        config_args.append("--disable-shared")
                else:
                    activated = getattr(self.options, option_name)
                    if activated:
                        self.output.info("Activated option! {0}".format(option_name))
                        config_args.append("--{0}".format(option_name))

            # find the libgpg-error folder, so we can set the binary path for configuring it
            gpg_error_path = ""
            for path in self.deps_cpp_info.lib_paths:
                if "libgpg-error" in path:
                    gpg_error_path = '/lib'.join(path.split("/lib")[0:-1]) #remove the final /lib. There are probably better ways to do this.
                    config_args.append("--with-libgpg-error-prefix={0}".format(gpg_error_path))
                    break

            # This is a terrible hack to make cross-compiling on Travis work
            if (self.settings.arch=='x86' and self.settings.os=='Linux'):
                env_build.configure(args=config_args, host="i686-linux-gnu") #because Conan insists on setting this to i686-linux-gnueabi, which smashes gpg-error hard
            else:
                env_build.configure(args=config_args)


            env_build.configure(args=config_args)
            env_build.make()
       
    def package(self):
        self.copy(pattern="COPYING*", src="sources")
        self.copy("*.h", dst="include", src="sources/src", keep_path=True)
        # self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="sources", keep_path=False)
        
        self.copy("libgcrypt-config", dst="bin", src="sources/src", keep_path=False)
        self.copy("hmac256", dst="bin", src="sources/src", keep_path=False)
        self.copy("dumpsexp", dst="bin", src="sources/src", keep_path=False)
        self.copy("mpicalc", dst="bin", src="sources/src", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)


