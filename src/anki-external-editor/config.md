### External editor: Advanced Configuration

**editor** [string]: The text editor to use, some common values are:

- **vim -gf** ideal for old-school users
- **open -t** leaves MacOS make the decision
- **code -w** common handler for [VSCode](https://code.visualstudio.com/Download)
- **atom** for lightweight editor [atom](https://atom.io/)
- **notepad++.exe** Windows' popular [Notepad++](https://notepad-plus-plus.org/downloads/)

If the specified editor could not be found, it'll try to make an educated guess. (If no editor is found an error message will show up.)
You can provide the full path to the editor executable if it doesn't work without it.
Some keyboard shortcuts are reserved by Anki and won't work.
On Mac it is not possible to use the Ctrl key as part of the shortcut (Cmd works).

In Windows remember to escape backslashes, write them twice:

```
{
    "editor": "C:\\Windows\\sol.exe"
}
```
