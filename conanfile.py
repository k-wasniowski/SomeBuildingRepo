from conan import ConanFile
from conan.tools.files import chdir, mkdir, save, load
import pathlib
import os
import platform

class SomeBuildingRepo(ConanFile):
    name = 'SomeBuildingRepo'
    version = '0.1'
    settings = 'os', 'build_type', 'arch'

    depot_tools_repository = 'https://chromium.googlesource.com/chromium/tools/depot_tools.git'
    depot_tools_release = 'a104c01252f54997e672490e7ab6cb7e15295a98'
    depot_tools_dir = 'depot_tools'
    
    webrtc_release = 'refs/remotes/branch-heads/5414' # M109
    webrtc_dir = 'src'

    def gn_args(self):
        args = ''

        args += 'use_rtti=true'
        args += ' is_debug=false'
        args += ' rtc_include_tests=false'

        if platform.system() == 'Windows':
            args += ' use_lld=false'

        return args

    def setup_depot_tools(self):
        try:
            with chdir(self, self.depot_tools_dir):
                print('-- Depot tools directory already exists')
        except:
            print('-- Setting up depot tools')

            self.run(f'git clone {self.depot_tools_repository} {self.depot_tools_dir}')

            with chdir(self, self.depot_tools_dir):
                self.run(f'git checkout {self.depot_tools_release}')

        self.set_depot_tools_environment_variables()

    def set_depot_tools_environment_variables(self):
        with chdir(self, self.depot_tools_dir):
            current_path = pathlib.Path(__file__).parent.resolve()
            depot_tools_path = os.path.join(os.path.sep, str(current_path), 'externals', self.depot_tools_dir)
            os.environ['PATH'] += os.pathsep + depot_tools_path
            os.environ['DEPOT_TOOLS_WIN_TOOLCHAIN'] = '0'

            print(os.environ['PATH'])

    def setup_webrtc(self):
        try:
           with chdir(self, self.webrtc_dir):
               print('-- WebRTC directory already exists')
               return
        except:
           print('-- Setting up WebRTC')
    
        self.run('fetch --nohooks webrtc')

        with chdir(self, self.webrtc_dir):
            self.run(f'git checkout {self.webrtc_release}')

            self.run('gclient sync')

    def source(self):
        print('-- Setting up sources')

        mkdir(self, "externals")
        with chdir(self, 'externals'):
            self.setup_depot_tools()

            self.setup_webrtc()

    def setup_webrtc_on_linux(self):
        print('-- Setting up WebRTC for Linux')

        self.run('sed -i "s/} snapcraft/} /gi" build/install-build-deps.sh')
        self.run('build/install-build-deps.sh --no-prompt')

        if self.settings.arch == 'x86_64':
            self.run('python3 build/linux/sysroot_scripts/install-sysroot.py --arch=amd64')
        elif self.settings.arch == 'armv8':
            self.run('python3 build/linux/sysroot_scripts/install-sysroot.py --arch=arm64')
        else:
            raise 'Unsupported Linux distribution'
    
    def configure_webrtc(self):
        try:
            load(self, 'webrtc_configuration_lock')
            print('-- WebRTC is already configured')
            return
        except:
           print('-- Configure WebRTC')

        with chdir(self, 'src'):
            if self.settings.os == 'Linux':
                self.setup_webrtc_on_linux()
        save(self, 'webrtc_configuration_lock', '')
    
    def build(self):
        with chdir(self, 'externals'):
            self.set_depot_tools_environment_variables()

            self.configure_webrtc()

            with chdir(self, 'src'):
                self.run(f'gn gen out --args="{self.gn_args()}"')

                self.run("ninja -C out")

    def package(self):
        pass