import os
import sys
import re

RE_ESCAPED_END = re.compile(r".*?(\\*)$")


def is_executable(cmd):
    return os.path.exists(cmd) and os.access(cmd, os.X_OK)


def escaping_end(word):
    if not word:
        return 0
    match = RE_ESCAPED_END.match(word)
    return len(match.group(1))


def split_exec_options(cmd):

    executable = ""
    options = ""

    escape = False
    for char in cmd:
        if options:
            options += char
        elif escape:
            escape = False
            executable += char
        elif char == "\\":
            escape = True
        elif char == " ":
            options += char
        else:
            executable += char

    return executable, options


def find_executable(cmd):

    executable, options = split_exec_options(cmd)

    # shortcicuit is already a valid abs or rel path
    if os.path.dirname(executable):
        if is_executable(executable):
            return cmd
        return None

    path = os.environ.get("PATH", None)
    if path is None:
        try:
            path = os.confstr("CS_PATH")
        except (AttributeError, ValueError):
            path = os.defpath
    if not path:
        return None
    path = os.fsdecode(path)
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        curdir = os.curdir
        if curdir not in path:
            path.insert(0, curdir)

        # Windows uses file extensions to determine excecutables
        pathext = os.environ.get("PATHEXT", "").lower().split(os.pathsep)
        if any(executable.lower().endswith(ext) for ext in pathext):
            filenames = [executable]
        else:
            filenames = [executable + ext for ext in pathext]
    else:
        filenames = [executable]

    seen = set()
    for dir in path:
        if not dir in seen:
            seen.add(dir)
            for filename in filenames:
                filepath = os.path.join(dir, filename)
                if is_executable(filepath):
                    return filepath + options
    return None

