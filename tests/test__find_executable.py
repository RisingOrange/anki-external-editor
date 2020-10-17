import os
import sys

from pytest import fixture

from src.utils import (
    find_executable,
    is_executable,
    split_exec_options,
    escaping_end,
)


WINDOWS_PATHEXT = ".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH"
FAKE_PATH = os.path.join("tests", "fake_path")


ENVS = [
    {
        "os": "Windows",
        "cmd": "code --wait",
        "patch": {
            "sys.platform": "win32",
            "os.environ": {"PATHEXT": WINDOWS_PATHEXT, "PATH": FAKE_PATH},
            "os.pathsep": ";",
        },
        "result_end": "code.exe --wait",
    },
    {
        "os": "Linux",
        "cmd": "code --wait",
        "patch": {
            "sys.platform": "linux",
            "os.environ": {"PATH": FAKE_PATH},
            "os.pathsep": ":",
        },
        "result_end": "code --wait",
    },
]

OPTIONS = [
    {"cmd": "code --wait", "executable": "code", "options": " --wait"},
    {"cmd": "vim -gf", "executable": "vim", "options": " -gf"},
    {"cmd": "vim -g -f", "executable": "vim", "options": " -g -f"},
    {"cmd": r"code\ editor -f", "executable": "code editor", "options": " -f"},
]


@fixture(params=ENVS)
def env_case(request, mocker):
    for key, value in request.param["patch"].items():
        mocker.patch(key, value)
    return request.param


def test__find_executable__find_python():
    # We know python is installed
    python_path = find_executable("python")
    assert python_path
    assert python_path != "python"


def test__find_executable__find_extensions(env_case):
    answer = env_case["result_end"]
    cmd = env_case["cmd"]

    result = find_executable(cmd)

    assert result.endswith(answer)


@fixture(params=OPTIONS)
def with_options(request):
    return request.param


def test__escaping_end__examples():
    assert 1 == escaping_end("command\\")
    assert 2 == escaping_end("command\\\\")
    assert 3 == escaping_end("command\\\\\\")


def test__split_exec_options(with_options):
    cmd = with_options["cmd"]
    good_executable = with_options["executable"]
    good_options = with_options["options"]

    executable, options = split_exec_options(cmd)

    assert good_executable == executable
    assert good_options == options


def test__find_executable__with_arguments(env_case):
    cmd = env_case["cmd"]
    answer = env_case["result_end"]

    result = find_executable(cmd)

    assert result.endswith(answer)
