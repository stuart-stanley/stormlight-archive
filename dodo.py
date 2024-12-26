from pathlib import Path
import platform
import shutil
import os
import urllib.request
# import fixture_info
import distutils.spawn
from doit import tools
from doit.exceptions import TaskError
DOIT_CONFIG = {
    'cleanforget': True,
    'verbosity': 2,
}


_REPO_ROOT = Path(__file__).parent.resolve()


def is_docker():
    # TODO: turn this into a command-line argument based value
    return True   # HACK so I can get moving. sheesh.
    return 'DOCKER_BUILD_DESCRIPTION' in os.environ


class _TaskPreconditions(object):
    def __init__(self):
        self.__errors = []

    def __make_missing(self, trigger, problem, fix, osx, lnx):
        error = [trigger, problem, fix, osx, lnx]
        self.__errors.append(error)

    def __scan_preconditions(self):
        # we will probe all the things here, but SCREAM about
        # them in the actual action...
        self.__errors = []
        if is_docker():
            return self.__errors  # HACK for docker

        if "DIRENV_DIR" not in os.environ:
            self.__make_missing(
                '"DIRENV_DIR" not in os.environ',
                "direnv MUST be active",
                "Install direnv for your OS",
                "brew install direnv",
                "apt install direnv"
            )
        # TODO: add version checks to these.
        self.__exe_check(
            'docker',
            'https://www.docker.com/products/docker-desktop',
            'https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04')

        return self.__errors

    def __exe_check(self, cmd, osx, lnx):
        """
        checks for the given cmd in our path and adds an error to self.__errors if not there.
        """
        if distutils.spawn.find_executable(cmd) is None:
            self.__make_missing(
                '"{}" not in path'.format(cmd),
                '{} MUST be installed to run tests'.format(cmd),
                'install {} for your OS'.format(cmd), osx, lnx)

    def check_uptodate(self):
        errors = self.__scan_preconditions()
        return len(errors) == 0

    def python_check_preconditions(self):
        errors = self.__scan_preconditions()
        if len(errors) == 0:
            return True
        print("-----there are missing required packages----")
        system = platform.system()
        if system not in ['Darwin', 'Linux']:
            print("WARNING: unknown platform.system {}. Showing all 'howto install' instructions".format(
                  system))
        for trigger, problem, fix, osx, lnx in errors:
            if system == 'Darwin':
                how_to = osx
            elif system == 'Linux':
                how_to = lnx
            else:
                how_to = "mac: '{}', linux: '{}'".format(osx, lnx)
            print("trigger: {}, problem: {}, fix-by: {}. On this system::::::: '{}'".format(
                trigger, problem, fix, how_to))

        return TaskError(errors)


def task_check_preconditions():
    """determine if envirnoment has all required preconditions"""
    _preconditioner = _TaskPreconditions()
    return {
        'basename': 'check-preconditions',
        'actions': [_preconditioner.python_check_preconditions],
        'uptodate': [_preconditioner.check_uptodate]
    }


def _find_file_from_path_list(list_of_paths, file_part):
    for path in list_of_paths:
        check_path = Path(path).resolve()
        check_file = check_path / file_part
        if check_file.exists():
            return check_file
    return None


def task_create_deploy_dockerfile():
    """take template Dockerfile and make the one used for balena deployment"""

    def _docker_to_balena_docker_xlate(src_path, dst_path):
        # TODO: build this info
        docker_data = src_path.read_text()
        docker_data = docker_data.replace("${build_commit_id}", "mfd.build_commit_id")
        docker_data = docker_data.replace("${build_commit_timestamp}", "mfd.build_commit_timestamp")
        docker_data = docker_data.replace("${build_branch}", "mfd.build_branch")
        docker_data = docker_data.replace("${build_tag}", "mfd.build_tag")
        docker_data = docker_data.replace("${build_firmware_loader_commit_id}",
                                          "mfd.build_firmware_loader_commit_id")
        dst_path.write_text(docker_data)

    _base_dockerfile_path = _REPO_ROOT / 'stormlight_archive/' / 'ci' / 'templates' / 'Dockerfile.pre_build_info'
    _balena_dockerfile_path = _REPO_ROOT / 'Dockerfile'
    return {
        'basename': 'create-deploy-dockerfile',
        'actions': [(_docker_to_balena_docker_xlate, [_base_dockerfile_path, _balena_dockerfile_path])],
        'targets': [_balena_dockerfile_path]
    }


def task_deploy_production():
    """deploy to balena production"""
    # _build_data = fixture_info.get_software_info()
    # btag = _build_data.build_tag
    btag = "todo-from-poetry"
    atxt = "DEBUG=%(bebug)s balena push stormlight --release-tag build {}".format(
        btag)
    return {
        'basename': 'deploy-production',
        'actions': [atxt],
        'params': [
            {
                'name': 'bebug',
                'short': 'b',
                'long': 'bebug',
                'default': 0,
                'help': 'set to 1 to add DEBUG=1 in front of balena command'
            }
        ],
        'file_dep': [
            _REPO_ROOT / 'Dockerfile'
        ],
        'uptodate': [False],   # never remember we built this w/o someway to _check_ for real
    }


def task_get_balena_cli():
    """get the specific version of the balena-cli"""
    version = "v20.0.7"
    system = platform.system()
    if system == 'Darwin':
        os_field = 'macOS'
    elif system == 'Linux':
        os_field = 'linux'
    else:
        raise Exception("WARNING: unknown platform.system {}. Showing all 'howto install' instructions".format(
            system))
    arch = platform.machine()
    if arch in ['arm64', 'aarch64']:
        arch_field = 'arm64'
    elif arch in ['x86_64']:
        arch_field = 'x64'
    else:
        raise Exception("WARNING: unknown platform.machine {}. Showing all 'howto install' instructions".format(
            arch))


    dl_file_name = "balena-cli-{}-{}-{}-standalone.zip".format(version, os_field, arch_field)
    dl_file_dir_path = _REPO_ROOT / '.venv'
    dl_file_dir_path.mkdir(exist_ok=True)
    dl_file_path = dl_file_dir_path / dl_file_name

    url = "https://github.com/balena-io/balena-cli/releases/download/{}/{}".format(version, dl_file_name)

    def _is_downloaded(dl_file_path):
        if dl_file_path.exists():
            return True
        return False

    def _download_version(dl_url, dl_file_path):
        urllib.request.urlretrieve(dl_url, dl_file_path.as_posix())

    yield {
        'basename': 'get-balena-cli',
        'name': 'download',
        'uptodate': [(_is_downloaded, [dl_file_path])],
        'actions': [(_download_version, [url, dl_file_path])],
        'clean': [dl_file_path.unlink]
    }

    unpack_dir_name = _REPO_ROOT / '.venv' / 'balena-cli'

    extract_cmd = "unzip -q {} -d .venv".format(dl_file_path)

    yield {
        'basename': 'get-balena-cli',
        'name': 'unpack',
        'uptodate': [unpack_dir_name.exists],
        'actions': [tools.CmdAction(extract_cmd)],
        'clean': [(shutil.rmtree, [unpack_dir_name, True])]
    }



def task_prepareproduction_deploy_group():
    """group of all steps to prepapre and deploy to production via balena"""
    return {
        'basename': 'production-deploy-group',
        'actions': None,
        'task_dep': ['check-preconditions', 'get-balena-cli']
    }


