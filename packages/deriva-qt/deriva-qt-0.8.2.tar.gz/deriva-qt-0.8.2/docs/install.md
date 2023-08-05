# Installing Desktop Clients

## Download the packages

You can find the latest versions for Deriva-Auth and Deriva-Upload below:

## By desktop (for Windows / MacOS)
* Find downloads [here](https://github.com/informatics-isi-edu/deriva-qt/releases). (these are prebuilt bundles which include all dependencies)
* Download the appropriate file for your OS and extract the archive. 
* Windows users can run the extracted `exe` file directly, while Mac users can copy the extracted file to the Application folder and then context (right) click and select `Open`.

## Install from source (Linux)

### Fedora

1. Install dependency packages 

```
dnf install python3-qt5 python3-qt5-webengine python3-devel 
```

2. install deriva-py and deriva-qt from source

```
pip3 install --upgrade git+https://github.com/informatics-isi-edu/deriva-py.git
pip3 install --upgrade git+https://github.com/informatics-isi-edu/deriva-qt.git
```

### Windows 10 

TBD
