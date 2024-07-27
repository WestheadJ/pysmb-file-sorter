# pysmb-file-sorter
A script to organize files by year, month, and date on a smb server.

# Table of Contents
- [How To Run](#how-to-run)
    - 
    -

# How To Run


## Installing Required Modules
Use to install required modules:

```pip install -r requirements.txt```
> when cloning the repository, ```requirements.txt``` should be in the base directory of the project, if this does not work you may need to reference the path to the requirements file i.e ```/downloads/pysmb-file-sorter/requirements.txt```

If you don't have pip or your system cannot run the command try, you will need to use pip3 instead if this is not an option then you will need to install either pip or pip3:

```pip3 install -r requirements.txt```
> when cloning the repository, ```requirements.txt``` should be in the base directory of the project, if this does not work you may need to reference the path to the requirements file i.e ```/downloads/pysmb-file-sorter/requirements.txt```

# Config File
I purposefully have not added the configs file I use. However I will explain how to set it up to start with.

### Steps To Create Config File
1. Create a new configs file in the same folder as the script file and name it ```smb-configs.json```.
2. The layout should consist of this

``` json
{
    "profiles":[],
    "ignored-directories":[],
    "output-directory":"",
    "test-directory":"",
    "valid-extensions":[]
}
```
3. Add your credentials to the config for example:

``` json
{
    "profiles":[],
    "ignored-directories":[],
    "output-directory":"/path/to/move/files/to",
    "test-directory":"/path/to/look at the test-directory",
    "valid-extensions":[".jpg",".JPG",".png",".PNG"]
}
```
> leave ```"test-directory"``` empty if you don't want to test moving your files as it's for 
