[![PyPI version](https://badge.fury.io/py/haran-utils.svg)](https://badge.fury.io/py/haran-utils) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Utils
A collection of utility functions and scripts I use.  

## Image scripts
These are a set of cli scripts related to image housekeeping. The syntax is - 
```
utils image <command> <args>
```
You can use the `-h` arg to get help on the specific command
### List of available commands
1. `crop` - Crops images given in one folder and outputs to the target folder
2. `filter` - 
Checks the resolution of all the files in the specified directory and moves them to the target directory if they are of a larger resolution
1. `summarise` - Checks the resolutions of images in all the sub-directories of the given directory and tells how many of images of a given resolution are there in a sub-directory

