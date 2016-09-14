from conans import ConanFile, CMake, tools, ConfigureEnvironment
import os
import shutil


class FlatBuffersConan(ConanFile):
    name = "FlatBuffers"
    version = "1.4.0"
    url = "https://github.com/Narquadah/conan-flatbuffers.git"
    license = "https://github.com/google/flatbuffers/blob/master/LICENSE.txt"
    settings = "os", "compiler", "build_type", "arch"
    exports = "CMakeLists.txt"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        tools.download("https://github.com/google/flatbuffers/archive/v1.4.0.zip",
                       "flatbuffers.zip")
        tools.unzip("flatbuffers.zip")
        os.unlink("flatbuffers.zip")
        os.makedirs("flatbuffers-1.4.0/build")

    def build(self):
        if self.settings.os == "Windows":
            raise Exception("No windows support yet!")
        else:

            concurrency = 1
            try:
                import multiprocessing
                concurrency = multiprocessing.cpu_count()
            except (ImportError, NotImplementedError):
                pass

            self.run("cd flatbuffers-1.4.0/build && cmake ..")

            self.run("cd flatbuffers-1.4.0/build/ && make flatc flatbuffers -j %s" % concurrency)

    def package(self):
        self.copy_headers("*.h", "flatbuffers-1.4.0/include")

        if self.settings.os == "Windows":
            raise Exception("No windows support yet!")
        else:
            # Copy the libs to lib
            self.copy("*.a", "lib", "flatbuffers-1.4.0/build/", keep_path=False)
            self.copy("flatc", "bin", "flatbuffers-1.4.0/build", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            raise Exception("No windows support yet!")
        elif self.settings.os == "Macos":
            self.cpp_info.libs = ["libflatbuffers.a"] #if not self.options.shared else ["libflatbuffers.9.dylib"]
        else:
            self.cpp_info.libs = ["libflatbuffers.a"] #if not self.options.shared else ["libflatbuffers.so.9"]