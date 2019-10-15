# Interactive marking tool for University of Alberta CMPUT 291 Assignment 2

Developed by Mohammad-Reza Daliri (daliri@ualberta.ca). It is a not-for-profit personal project and is not affiliated with UAlberta officials.


> Copyright (C) 2019 Mohammad-Reza Daliri
>
> This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
>
> This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public
> License   along with this program.  If not, see
> <https://www.gnu.org/licenses/>.

# Getting Started

It is a python program which has some package dependencies. Required packages are listed in `requirements.txt`. You may install them by `pip` in your environment:

```
pip install -r requirements.txt
```
Then run program with following arguments:
```
 python interactive_marker.py [-h] [--version] -q QUESTION -s SUBMISSIONS -m MARKSHEETS
```

## Sample run
```
 python interactive_marker.py -q 15 -s ~/submissions -m ~/marksheets
```

# Options
Following guide is available with `--help` argument:

    usage: interactive_marker.py [-h] [--version] -q QUESTION -s SUBMISSIONS -m MARKSHEETS

    Interactive marking tool for University of Alberta CMPUT 201 Assignment 2.
    Developed by Mohammad-Reza Daliri (daliri@ualberta.ca). IT COMES WITHOUT ANY
    WARRANTY under GNU GPL-3.0 License.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -q QUESTION, --question QUESTION
                            Question number.
      -s SUBMISSIONS, --submissions SUBMISSIONS
                            Submissions directory path.
      -m MARKSHEETS, --marksheets MARKSHEETS
                            Marksheets directory path.


# Version
Current version is **1.0.1**.