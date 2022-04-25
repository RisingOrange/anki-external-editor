import io
import subprocess
import sys
import tempfile

from aqt import mw
from aqt.gui_hooks import editor_did_init_shortcuts

from .utils import find_executable, is_executable


def get_editor():
    config = mw.addonManager.getConfig(__name__)
    user_choice = config.get("editor")
    if isinstance(user_choice, list):
        command = find_executable(user_choice[0])
        if command:
            return f"{command} {' '.join(user_choice[1:])}"
    elif is_executable(user_choice):
        return user_choice
    else:
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

    with io.open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    proc = subprocess.Popen(f"{editor} {filename}", close_fds=True, shell=True)
    proc.communicate()

    with io.open(filename, "r", encoding="utf-8") as file:
        return file.read()


def edit_with_external_editor(editor):
    text = editor.note.fields[editor.currentField]
    text = edit(text)
    editor.note.fields[editor.currentField] = text
    if not editor.addMode:
        editor.note.flush()
    editor.loadNote(focusTo=editor.currentField)


def add_shortcut(shortcuts, editor):
    config = mw.addonManager.getConfig(__name__)
    shortcut = config.get("shortcut")
    shortcuts.append((shortcut, lambda: edit_with_external_editor(editor)))


editor_did_init_shortcuts.append(add_shortcut)
