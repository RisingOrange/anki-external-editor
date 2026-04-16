import os
import sys

from pytest import fixture

import importlib.util
from pathlib import Path

_utils_path = Path(__file__).parent.parent / "src" / "anki-external-editor" / "utils.py"
_spec = importlib.util.spec_from_file_location("anki_external_editor_utils", _utils_path)
_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_utils)

find_executable = _utils.find_executable
is_executable = _utils.is_executable
split_exec_options = _utils.split_exec_options
escaping_end = _utils.escaping_end


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

WINDOWS_OPTIONS = [
    {
        "cmd": r"C:\Editor\foo.exe --wait",
        "executable": r"C:\Editor\foo.exe",
        "options": " --wait",
    },
    {
        "cmd": r'"C:\Program Files\Editor\foo.exe" --wait',
        "executable": r"C:\Program Files\Editor\foo.exe",
        "options": " --wait",
    },
    {
        "cmd": "editpadpro8.exe",
        "executable": "editpadpro8.exe",
        "options": "",
    },
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


@fixture(params=WINDOWS_OPTIONS)
def windows_options(request, mocker):
    mocker.patch.object(_utils.sys, "platform", "win32")
    return request.param


def test__split_exec_options__windows(windows_options):
    cmd = windows_options["cmd"]
    good_executable = windows_options["executable"]
    good_options = windows_options["options"]

    executable, options = split_exec_options(cmd)

    assert good_executable == executable
    assert good_options == options


def test__find_executable__with_arguments(env_case):
    cmd = env_case["cmd"]
    answer = env_case["result_end"]

    result = find_executable(cmd)

    assert result.endswith(answer)
