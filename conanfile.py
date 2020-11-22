#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
from conans import tools

class CnlConan(ConanFile):
    name = "cnl"
    license = "Boost Software License 1.0"
    author = "John McFarlane <cnl@john.mcfarlane.name>"
    url = "https://github.com/johnmcfarlane/cnl"
    homepage = "https://johnmcfarlane.github.io/cnl/"
    description = "A Compositional Numeric Library for C++"
    topics = ("fixed-point", "value-types")
    settings = "os", "compiler", "build_type", "arch"
    options = {"enable_exceptions": [False, True],
               "int128": [False, True],
               "sanitize": [False, True],
               "target": ["test-all", "test-benchmark", "test-unit"]}
    default_options = {"enable_exceptions": True,
                       "int128": True,
                       "sanitize": False,
                       "target": "test-unit"}
    generators = "cmake_paths"
    no_copy_source = True
    requires = "gtest/1.10.0", "benchmark/1.5.0@johnmcfarlane/stable"

    scm = {
        "revision": "main",
        "type": "git",
        "url": "https://github.com/johnmcfarlane/cnl.git",
    }

    def build(self):
        cmake = CMake(self)

        if self.should_configure:
            def conan_option_to_cmake_boolean(conan_option: bool):
                return {
                    True: "ON",
                    False: "OFF"
                }[bool(conan_option)]

            self.run('''cmake \
{} \
-DCMAKE_PROJECT_cnl_INCLUDE:FILEPATH={}/conan_paths.cmake \
-DCNL_EXCEPTIONS={} \
-DCNL_INT128={} \
-DCNL_SANITIZE={} \
{}'''.format(
                cmake.command_line,
                self.build_folder,
                conan_option_to_cmake_boolean(self.options.enable_exceptions),
                conan_option_to_cmake_boolean(self.options.int128),
                conan_option_to_cmake_boolean(self.options.sanitize),
                self.source_folder))

        if self.should_build:
            self.run("cmake --build {} --target {} {}".format(
                self.build_folder,
                self.options.target,
                cmake.build_config))

        cmake.install()

        if self.should_test:
            target_to_test_pattern = {
                "test-all": "^test-",
                "test-benchmark": "test-benchmark",
                "test-unit": "^test-unit-"
            }
            self.run("ctest --output-on-failure --parallel {} --tests-regex {}".format(
                tools.cpu_count(),
                target_to_test_pattern[str(self.options.target)]
            ))

    def package(self):
        self.copy("include/*.h")
        self.copy("LICENSE_1_0.txt", "licenses")

    def package_id(self):
        self.info.header_only()
