### External editor: Advanced Configuration

**editor** [string]: The text editor to use, some common values are:

- **vim -gf** ideal for old-school users
- **open -t** leaves MacOS make the decision
- **code** common handler for [VSCode](https://code.visualstudio.com/Download)
- **atom** for lightweight editor [atom](https://atom.io/)
- **notepad++.exe** Windows' popular [Notepad++](https://notepad-plus-plus.org/downloads/)

If the specified editor could not be found, it'll try to make an educated guess.

In Windows remember to escape backslashes, write them twice:

```
{
    "editor": "C:\\Windows\\sol.exe"
}
```
