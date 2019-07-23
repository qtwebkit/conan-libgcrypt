#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools, VisualStudioBuildEnvironment
import os
import shutil


class LibgcryptConan(ConanFile):
    name = "libgcrypt"
    version = "1.8.4"
    url = "http://github.com/DEGoodmanWilson/conan-libgcrypt"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "Libgcrypt is a general purpose cryptographic library originally based on code from GnuPG"
    license = "LGPL-2.1-or-later"
    homepage = "https://www.gnupg.org/download/index.html#libgcrypt"
    topics = ("conan", "libgcrypt", "gcrypt", "gnupg", "gpg", "crypto", "cryptography")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False]}

    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "sources"

    requires = 'libgpg-error/1.36@qtproject/stable'

    @property
    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    def build_requirements(self):
        if tools.os_info.is_windows:
            if "CONAN_BASH_PATH" not in os.environ:
                self.build_requires("cygwin_installer/2.9.0@bincrafters/stable")
        if self._is_msvc:
            self.build_requires("automake_build_aux/1.16.1@bincrafters/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://gnupg.org/ftp/gcrypt/libgcrypt"
        tools.get("{0}/libgcrypt-{1}.tar.gz".format(source_url, self.version),
                  sha256="fc3c49cc8611068e6008482c3bbee6c66b9287808bbb4e14a473f4cc347b78ce")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _apply_msvc_fixes(self):
        # FIXME : create patch
        tools.replace_in_file(os.path.join(self._source_subfolder, "src", "gcrypt.h.in"),
                              "typedef int  pid_t;", "")
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'ln -s "$ac_rel_source" "$ac_file" 2>/dev/null ||',
                              'cp -pR "$ac_rel_source" "$ac_file" 2>/dev/null ||')
        tools.replace_in_file(os.path.join(self._source_subfolder, "cipher", "Makefile.in"),
                              "cipher-gcm-armv8-aarch32-ce.lo cipher-gcm-armv8-aarch64-ce.lo", "")
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha256-ssse3-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha256-avx-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha256-avx2-bmi2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha512-ssse3-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha512-avx-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha512-avx2-bmi2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS whirlpool-sse2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha1-ssse3-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha1-avx-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS sha1-avx-bmi2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS rijndael-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS rijndael-ssse3-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS rijndael-ssse3-amd64-asm.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS poly1305-sse2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS poly1305-avx2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS chacha20-sse2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS chacha20-ssse3-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS chacha20-avx2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS salsa20-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_DIGESTS="$GCRYPT_DIGESTS crc-intel-pclmul.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS arcfour-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS blowfish-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS cast5-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS des-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS twofish-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS camellia-arm.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "configure"),
                              'GCRYPT_CIPHERS="$GCRYPT_CIPHERS serpent-sse2-amd64.lo"', '')
        tools.replace_in_file(os.path.join(self._source_subfolder, "cipher", "stribog.c"),
                              "u64 Z[8] = {};", "u64 Z[8] = {0};")
        tools.replace_in_file(os.path.join(self._source_subfolder, "cipher", "cipher-ccm.c"),
                              "unsigned char tmp[blocksize];",
                              """
#ifdef _MSC_VER
unsigned char * tmp = (unsigned char*) _alloca(sizeof(unsigned char) * blocksize);
#else
unsigned char tmp[blocksize];
#endif""")
        tools.replace_in_file(os.path.join(self._source_subfolder, "cipher", "cipher-poly1305.c"),
                              "static const byte zero_padding_buf[15] = {};",
                              "static const byte zero_padding_buf[15] = {0};")
        tools.replace_in_file(os.path.join(self._source_subfolder, "src", "hwf-x86.c"),
                              "#if !defined (__i386__) && !defined (__x86_64__)",
                              "#if !defined (__i386__) && !defined (__x86_64__) && !defined(_M_IX86) && !defined(_M_X64)")
        unistd_h = """
        #ifdef _MSC_VER
        #define access _access
        #define R_OK 4
        #define W_OK 2
        #define X_OK R_OK
        #define F_OK 0

        # define S_IRWXU    0700
        # define S_IRUSR    0400
        # define S_IWUSR    0200
        # define S_IXUSR    0100

        typedef int ssize_t;
        #else
        #include <unistd.h>
        #endif
        """
        os.makedirs(os.path.join(self._source_subfolder, "random", "sys"))
        tools.save(os.path.join(self._source_subfolder, "random", "unistd.h"), unistd_h)
        tools.save(os.path.join(self._source_subfolder, "src", "unistd.h"), unistd_h)
        tools.save(os.path.join(self._source_subfolder, "random", "sys", "time.h"), "")

    @property
    def _msvc_env(self):
        env_build = VisualStudioBuildEnvironment(self)
        libdirs = [os.path.join(self.build_folder, self._source_subfolder, "ciper"),
                   os.path.join(self.build_folder, self._source_subfolder, "compat"),
                   os.path.join(self.build_folder, self._source_subfolder, "mpi"),
                   os.path.join(self.build_folder, self._source_subfolder, "random"),
                   os.path.join(self.build_folder, self._source_subfolder, "src")]
        env_build.lib_paths.extend(libdirs)
        return env_build.vars

    def build(self):
        gpg_error_prefix = self.deps_cpp_info["libgpg-error"].rootpath
        gpg_error_prefix = tools.unix_path(gpg_error_prefix) if tools.os_info.is_windows else gpg_error_prefix
        args = ["--disable-dependency-tracking",
                "--disable-doc",
                "--with-libgpg-error-prefix=%s" % gpg_error_prefix]
        if self.options.shared:
            args.extend(["--disable-static", "--enable-shared"])
        else:
            args.extend(["--disable-shared", "--enable-static"])
        build = None
        host = None
        rc = None
        if self._is_msvc:
            self._apply_msvc_fixes()
            # INSTALL.windows: Native binaries, built using the MS Visual C/C++ tool chain.
            for filename in ["compile", "ar-lib"]:
                shutil.copy(os.path.join(self.deps_cpp_info["automake_build_aux"].rootpath, filename),
                            os.path.join(self._source_subfolder, "build-aux", filename))
            build = False
            if self.settings.arch == "x86":
                host = "i686-w64-mingw32"
                rc = "windres --target=pe-i386"
            elif self.settings.arch == "x86_64":
                host = "x86_64-w64-mingw32"
                rc = "windres --target=pe-x86-64"
            args.extend(["CC=$PWD/build-aux/compile cl -nologo",
                         "LD=link",
                         "NM=dumpbin -symbols",
                         "STRIP=:",
                         "AR=$PWD/build-aux/ar-lib lib",
                         "RANLIB=:",
                         "--disable-asm"])
            if rc:
                args.extend(['RC=%s' % rc, 'WINDRES=%s' % rc])
        with tools.chdir(self._source_subfolder):
            with tools.vcvars(self.settings) if self._is_msvc else tools.no_op():
                with tools.environment_append(self._msvc_env) if self._is_msvc else tools.no_op():
                    print(self._msvc_env)
                    env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
                    if self._is_msvc:
                        env_build.libs.remove("ws2_32")
                    env_build.configure(args=args, build=build, host=host)
                    env_build.make()
                    env_build.install()
       
    def package(self):
        self.copy(pattern="COPYING*", src="sources")
        
    def package_info(self):
        self.cpp_info.libs = ["gcrypt"]
