# Render Class

This class is here to help make pdf's of the various *markdown* files that are contained in this repository. The render 
class takes a path to the top level that it should search through and then goes through the sub directories in that directory
and determines if they have a subdirectory "pdf". If it does it looks through the contents of that directory and looks for ".md" 
files and then opens those files up and looks for [comment]: lines. If after the comment it says '''render''' then the 
program will use pandoc to create a pdf of that file in the pdf directory. 

## Commands

Currently this program supports the following commands:

* ```[comment]: render``` - this makes the file be turned into a pdf
* ```[comment]: landscape``` - when the file is processed to pdf it will do so in a landscape orientation.