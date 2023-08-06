# fix-winpath
If you are sure python is installed on your windows machine, but still encounter the following problem while trying to run `python` from your windows `cmd` terminal:

```
C:\Users\Joe> python
'python' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\Joe> pip install requests
'pip' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\Joe> jupyter notebook
'jupyter' is not recognized as an internal or external command,
operable program or batch file.
```
`fix-winpath` might help you to fix your windows' PATH environment variable.

## Instructions
Check if you can launch python using the `py` launcher first:

```
C:\Users\Guest>py --version
Python 3.7.0
```

Assuming the line above works, install `fix-winpath` with: 

    py -3 -m pip install --upgrade fix-winpath 
    
After installing the package successfully fix your `PATH` with:

    py -3 -m fix_winpath -i 
