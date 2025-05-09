README file for EN.605.202 Lab 3

# Summary 
Code to sort data using shell sort (with four different gap sequences) and heap sort. 

# Usage 
To sort the data contained in the input files, run the main.py script. 
This driver script will read the data contained in the input files, sort the data using four different shell sorts and one heap sort, and write out the sorted data to an output file: output/output.txt. 


# How to Run   
1. EDITOR   
   Open the lab_4 directory in VSCode editor (or editor of choice).   
   Open main.py and run the file.    

2. COMMAND LINE    
   cd to repo root directory   
   Run command: python main.py    


# File/Directory Descriptions 
input/   
    - Contains input files with numbers to sort. 
    - main.py writes several new input files to this directory. 

output/
    - output_example.txt: Example output text file that I generated by running main.py. When user runs main.py, the script will generate output.txt that will be saved in this directory. 
    - output.txt: Not initially included in this directory. This file will be generated once the user runs main.py. Each time user runs main.py, this file will be overwritten. 

src.py 
    - Contains source code functions for the shell sort and heap sort. 

utils.py 
    - Contains helper functions to set directories/filepaths, generate input files, and format the way output is written to output text file.

main.py 
    - Contains main driver function that reads input strings from input text files, and sorts them using 4 different shell sorts and heap sort. 

# Notes
- I developed this code using Python version 3.11.9. 
- I wrote and tested this code using the VSCode editor. 
- Code developed on MacOS Sequoia 15.3.2
- Code is on GitHub at this link: https://github.com/slomuscio/EN.605.202_lab_4