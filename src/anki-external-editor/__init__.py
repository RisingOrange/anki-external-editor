import io
import subprocess
import sys
import tempfile

from aqt import mw
from aqt.gui_hooks import editor_did_init_shortcuts, profile_did_open

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
    config = mw.addonManager.getConfig(__name__)
    editor = get_editor()
    filename = tempfile.mktemp(suffix=f".{config.get('file_extension', 'html')}")

    with io.open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    proc = subprocess.Popen(f"{editor} {filename}", close_fds=True,
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"Error while trying to edit {filename} with {editor}:\nstdout\n{stdout.decode()}\nstderr\n{stderr.decode()}")

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
    shortcut = config["shortcut"]

    # On Mac Anki sees pressing the Cmd key as pressing Ctrl
    if sys.platform == "darwin":
        shortcut = shortcut.lower().replace("cmd", "ctrl")

    shortcuts.append((shortcut, lambda: edit_with_external_editor(editor)))


editor_did_init_shortcuts.append(add_shortcut)


def replace_ctrl_with_cmd_for_mac():

    # the shortcut needs to be changed back to ctrl later because
    # on Mac Anki sees pressing the Cmd key as pressing Ctrl

    config = mw.addonManager.getConfig(__name__)
    shortcut = config["shortcut"]

    if not (sys.platform == "darwin" and "ctrl" in shortcut.lower()):
        return

    config["shortcut"] = shortcut.lower().replace("ctrl", "cmd")
    mw.addonManager.writeConfig(__name__, config)


profile_did_open.append(replace_ctrl_with_cmd_for_mac)
