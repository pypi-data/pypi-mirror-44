# vtemplate

A python library to create a structured directories for different kinds of projects

This is created for structuring of projects inside virtusa
all projects are roughlt divided into 4 catogeries and a specific structure in proposed for easc. This library helps create the strcuture of one of the 4 kind as specified 

## Installation
This can be installed with pip 
``` 
pip install vtemplate
```

Or you can download the git repo and navigate to dist folder vtemplate>vtemplate>dist  and use

```
pip install vtemplate-*.*.*-py3-none-any.whl
```
change * to respective release

## Usage

you can import the package and call create with the project name
for example
```
import vtemplate as vt
vt.create('project name')
```

this starts creating the project structure
There will be some questions you need to answer

to get the full idea see example.ipynb
