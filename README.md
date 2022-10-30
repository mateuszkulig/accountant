# accountant
Tool written in python to make bot and web accounts easy to create.

The basic idea is to use main *Browser* class and its 
functions defined in *acc.py* to create bot or account maker
for any website.

### Project file tree
```
.
├── acc.py
├── recorder.py
├── decoder.py
├── accounts
|   └── __init__.py
|   └── *predefined accounts*
└── apis
    └── __init__.py
    └── *predefined apis*
```
Both *\_\_init\_\_.py* files contain only imports from predefined 
files to avoid long filenames in actual package imports.
