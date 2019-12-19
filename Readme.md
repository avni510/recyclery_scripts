### Description
This script is used for The Recyclery Profit and Loss statements. It compresses the P and L's into
specific categories which can then be used for our quarterly report

### Usage
The script works for a specific month in CSV format (not xlsx)

### Installation
* Install python3 and pip3 by either option
  - Homebrew
    * `brew install python3`
    * pip3 will automatically be installed
  - Python website
    * [Download Python Here](https://www.python.org/downloads/)
    * [Download Pip Here](https://pip.pypa.io/en/stable/installing/)
      - Please make sure to download pip3
* Verify
  - Run `python3 --version`. This should output the installed version
  - Run `pip3 --version`. This should output the installed version 

* Install pandas `pip3 install pandas` 

### Running
* Download the latest P and L
* Open the script and update the first 4 variables. 
* Run the script `python3 p_and_l_collapsing.py`
* There may be categories that exist in the script but do not exist in the 
  P and L and vice versa. The script should notify you of this
* After those discrepancies are fixed the script will output a collapsed CSV
* Please copy and paste those numbers into Recylery Quarterly sheet found on google drive
