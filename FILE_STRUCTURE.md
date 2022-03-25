# File Structure
Refer to this file for explanations on the file layout, as well as where to locate certain files.


## Source Directory
You can find the source code in the source directory.
```
src/ozone
```
Here, you will find the executable code files and classes. These include files like `__init__.py` (the executable file), `ozone.py` and `urls.py` (refer to **Classes** for more information).

## Classes
In this repo, there are two main files where the classes are written. `ozone.py`, and `urls.py`. It is important to know the difference between them.

### `urls.py`
In this file, the classes stored provide the URL for the other files to use.

### `ozone.py`
In this file, the classes are stored with the purpose of creating data for the end user. The classes in this file depend on the classes in `urls.py`.

This file processes the required token to access the data, makes a request to the API, retrieves the data, and parses it.

## Dependency Management
### `setup.py`
This file is used to set up the project and install the required dependencies.
### `setup.cfg`
This file contains the configuration specification. 
### `requirements.txt`
The third-party dependencies are specified in this file.

## `src/media`
If you come across `src/media`, you will find that it contains gifs. These are the files for the showcase gifs in the README.md.
