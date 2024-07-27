# pysmb-file-sorter
A script to organize files by year, month, and date on a smb server.

# Table of Contents
1. [How To Setup & Run](#how-to-setup--run)
- [Installing Required Modules](#installing-required-modules)
- [Creating & Setting Up The Config File](#creating--setting-up-the-config-file)
- [Path Information For Config](#path-information-for-config)
- [Server Profiles](#server-profiles)

# How To Setup & Run


## Installing Required Modules
Use to install required modules:

```pip install -r requirements.txt```
> when cloning the repository, ```requirements.txt``` should be in the base directory of the project, if this does not work you may need to reference the path to the requirements file i.e ```/downloads/pysmb-file-sorter/requirements.txt```

If you don't have pip or your system cannot run the command try, you will need to use pip3 instead if this is not an option then you will need to install either pip or pip3:

```pip3 install -r requirements.txt```
> when cloning the repository, ```requirements.txt``` should be in the base directory of the project, if this does not work you may need to reference the path to the requirements file i.e ```/downloads/pysmb-file-sorter/requirements.txt```

## Creating & Setting Up The Config File
I purposefully have not added the configs file I use. However I will explain how to set it up to start with.

### Steps To Create Config File
1. Create a new configs file in the same folder as the script file and name it ```smb-configs.json```.
2. The layout should consist of this

``` json
{
    "profiles":[],
    "ignored-directories":[],
    "output-directory":"",
    "valid-extensions":[]
}
```
3. Add your credentials to the config for example:

``` json
{
    "profiles":[],
    "ignored-directories":[],
    "output-directory":"/path/to/move/files/to",
    "valid-extensions":[".jpg",".JPG",".png",".PNG"]
}
```

## Path Information For Config
This script needs a folder to move the files to. This needs to be the exact path on the drive, it also needs the parent directory to be the same as your indicated ```"SHARE_NAME"```.
### Example 1
Take this as the config file example:
``` json
{
         "profiles":
         [
            {
            "SERVER_NAME": "smbserver",
            "USERNAME": "user1",
            "PASSWORD": "password",
            "DOMAIN": "smbserver",
            "SHARE_NAME": "main/smbserver"
            }
        ],
        "output-directory":"Sorted"
}
```

The ```SHARE_NAME``` is the SHARE folder, and the ```output-directory``` is a folder called "Sorted" in the share path so this would look like : ```smb://smbserver/main/smbserver/Sorted``` as a file link.

## Server Profiles
A profile consists of a:
- ```SERVER_NAME```
- ```USERNAME```
- ```PASSWORD```
- ```DOMAIN```
- ```SHARE_NAME```

 ### - ```SERVER_NAME```
The server name is dictated as what the machine name or network name of the machine is. 

For example my raspberry pi comes under it's IP which also is linked to the [```DOMAIN```](#--domain). But my truenas server it's ```SHARE_NAME``` is ```truenas``` but it can be accessed by it's IP or the term truenas in it's [```DOMAIN```](#--domain) so you may have to play about with the different options.

### - ```USERNAME```
This has to be a user to the machine, this could be a root user or if it's a user specific to the share.

### - ```PASSWORD``` 
This is the password that you will use with the [```USERNAME```](#--username) to login to that Share.

### - ```DOMAIN```
This is the server address that it will need to connect to it, wether this is the IP of the machine or the actual smb address like I mentioned in [```SERVER_NAME```](#--server_name)

### - ```SHARE_NAME```
This is the name/display name of the Share folder. 

For example in ```smbd.config``` you may have a share called ```James``` but it could be linked to a folder called ```smbserver/James-Share``` the ```SHARE_NAME``` may look like this ```"SHARE_NAME":"James:"```
