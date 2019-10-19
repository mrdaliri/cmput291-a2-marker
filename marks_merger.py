# Marks merging tool for University of Alberta CMPUT 201 Assignment 2.
#
# Developed by Mohammad-Reza Daliri (daliri@ualberta.ca).
#
# Copyright (C) 2019 Mohammad-Reza Daliri
# Licensed under GNU General Public License 3 (GPL-3.0)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__version__ = '1.0.3'

import os
import re
import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Marks merging tool for University of Alberta CMPUT 201 Assignment 2. Developed by Mohammad-Reza Daliri (daliri@ualberta.ca). IT COMES WITHOUT ANY WARRANTY under GNU GPL-3.0 License.')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-m', '--marksheets', help='Marksheets directory path.', required=True)
    parser.add_argument('-o', '--csv', help='Output file name (CSV).', required=True)
    args = parser.parse_args()

    marksheets_path = args.marksheets
    csv_path = args.csv

    with os.scandir(marksheets_path) as marksheets:
        csv_file = open(csv_path, mode='w')
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['CCID', 'Score'])

        for marksheet_file in marksheets:
            if os.path.isdir(marksheet_file.path):
                continue

            ccid = marksheet_file.name.replace('.txt', '')
            sum_of_marks = 0
            marksheet_content = []
            with open(marksheet_file.path) as marksheet:
                for line in marksheet:
                    line = line.replace('_____', '0')
                    line = line.replace('_', '')
                    marksheet_content.append(line)  # used later to update the file
                    if line.lower().find('/10 total') != -1:
                        line = line.strip()
                        mark = float(re.compile(r'\d+\.?\d?/').search(line).group().replace('/', ''))
                        sum_of_marks += mark
                    elif line.lower().find('readme.txt is not submitted or is missing content') != -1 or line.find(
                            'Late penalty') != -1:
                        mark = float(re.compile(r'\d+\.?\d? ').search(line).group().strip())
                        sum_of_marks -= mark

            sum_of_marks = sum_of_marks if not sum_of_marks.is_integer() else int(sum_of_marks)
            if sum_of_marks < 0:
                sum_of_marks = 0
            csv_writer.writerow([ccid, sum_of_marks])

            with open(marksheet_file.path, 'w') as marksheet:
                for line in marksheet_content:
                    if line.find('=====/100 TOTAL') != -1:
                        marksheet.write(line.replace('=====', str(sum_of_marks)))
                    else:
                        marksheet.write(line)

        csv_file.close()
