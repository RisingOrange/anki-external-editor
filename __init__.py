from distutils.spawn import find_executable
import tempfile
import subprocess

import aqt
from aqt import mw


def edit(text, cmd):
    filename = tempfile.mktemp(suffix=".html")

    with open(filename, "wt") as file:
        file.write(text)

    cmd_list = cmd.split() + [filename]
    cmd_list[0] = find_executable(cmd_list[0])
    proc = subprocess.Popen(cmd_list, close_fds=True)
    proc.communicate()

    with open(filename, "rt") as file:
        return file.read()


def edit_with_external_editor(self, field):
    config = mw.addonManager.getConfig(__name__)
    cmd = config.get("editor", "vim -gf")
    text = self.note.fields[field]
    text = edit(text, cmd)
    self.note.fields[field] = text
    self.note.flush()
    self.loadNote(focusTo=field)


aqt.editor.Editor._onHtmlEdit = edit_with_external_editor

