import io
import os
import tempfile
import subprocess
import sys

from .utils import is_executable, find_executable
try:
    import aqt
    from aqt import mw
    BUILTIN_EDITOR = aqt.editor.Editor._onHtmlEdit
except ImportError:
    BUILTIN_EDITOR = None


def get_editor():
    config = mw.addonManager.getConfig(__name__)
    user_choice = config.get("editor")
    if is_executable(user_choice):
        return user_choice
    editors = [
        user_choice,
        user_choice + ".exe",
        "notepad++.exe",
        "notepad.exe",
        "code --wait",
        "gvim -f",
        "vim -gf",
        "atom",
        "atom.exe",
        "gedit",
    ]
    if sys.platform == "darwin":
        editors.append("open -t")
    for editor in editors:
        command = find_executable(editor)
        if command:
            return command

    raise RuntimeError("Could not find external editor")


def edit(text):
    editor = get_editor()
    filename = tempfile.mktemp(suffix=".html")

    with io.open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

    cmd_list = editor.split() + [filename]
    proc = subprocess.Popen(cmd_list, close_fds=True)
    proc.communicate()

    with io.open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def edit_with_external_editor(self, field):
    text = self.note.fields[field]
    try:
        text = edit(text)
        self.note.fields[field] = text
        if not self.addMode:
            self.note.flush()
        self.loadNote(focusTo=field)
    except RuntimeError:
        return BUILTIN_EDITOR(self, field)


if BUILTIN_EDITOR:
    aqt.editor.Editor._onHtmlEdit = edit_with_external_editor
