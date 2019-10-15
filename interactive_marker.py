# git remote add origin git@github.com:mrdaliri/cmput291-a2-marker.git.
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

__version__ = '1.0.1'

import os
import re
import argparse

from PyInquirer import prompt
from prompt_toolkit.shortcuts import clear


def is_number(string):
    try:
        return int(string) or True
    except ValueError:
        return False


def sum_in_range(number_to_be_added, current_total, max_value):
    return abs(number_to_be_added) + abs(current_total) <= abs(max_value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interactive marking tool for University of Alberta CMPUT 201 Assignment 2. Developed by Mohammad-Reza Daliri (daliri@ualberta.ca). IT COMES WITHOUT ANY WARRANTY under GNU GPL-3.0 License.')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-q', '--question', help='Question number.', required=True)
    parser.add_argument('-s', '--submissions', help='Submissions directory path.', required=True)
    parser.add_argument('-m', '--marksheets', help='Marksheets directory path.', required=True)
    args = parser.parse_args()

    q_number = int(args.question)
    submissions_path = args.submissions
    marksheets_path = args.marksheets

    with os.scandir(submissions_path) as submissions:
        for submission in submissions:
            ccid = submission.name

            try:
                diff_file = open('%s/%d_diff.txt' % (submission.path, q_number))
                print('Output differences with solution:\n')
                print(diff_file.read())
            except FileNotFoundError:
                print("OUTPUT MATCHES")

            print('----------------------------------')

            with open('%s/errors.txt' % (submission.path, )) as cumulative_run_output_file:
                cumulative_run_output = cumulative_run_output_file.read()
                run_output = re.search('(Running %d)(.*)((?:\n.*)+)(Running %d)' % (q_number, q_number + 1),
                                       cumulative_run_output, re.MULTILINE).group(3)
                if len(run_output.strip()) != 0:
                    print('Runtime errors:\n')
                    print(run_output)
                else:
                    print('NO RUNTIME ERROR')

            print('----------------------------------')

            try:
                print('%d.sql contents:\n' % q_number)
                solution_file = open('%s/%d.sql' % (submission.path, q_number))
                print(solution_file.read())
            except FileNotFoundError:
                pass

            print('----------------------------------')

            print('%s/a2-script.txt related contents:\n' % (submission.path,))
            with open('%s/a2-script.txt' % (submission.path,)) as cumulative_output_file:
                cumulative_output = cumulative_output_file.read()
                try:
                    output = re.search('([qQ](.*)%d)(.*)((?:\n.+)+)' % q_number, cumulative_output, re.MULTILINE).group()
                    print(output.strip())
                except AttributeError:  # if we cannot find question 5 answer
                    print(cumulative_output.strip())

            print('----------------------------------')

            marking_items = []
            marksheet_content = []
            marksheet_path = '%s/%s.txt' % (marksheets_path, ccid)
            with open(marksheet_path) as marksheet:
                for line in marksheet:
                    marksheet_content.append(line)  # used later to update the file
                    if line.find('_____') != -1 and line.lower().find('total') == -1:
                        line = line.strip()
                        points = int(re.compile('-?[0-9]+').search(line).group())
                        description = re.compile('[^(_]+').search(line).group(0).strip()
                        marking_items.append({'max': points, 'description': description, 'points': 0})

            total = 0
            while True:
                total = sum([item['points'] for item in marking_items])
                answer = prompt([{
                    'type': 'list',
                    'name': 'item',
                    'message': 'Please select a marking criteria for "%s" (%d/-10):' % (ccid, total),
                    'choices': [{'name': 'Nothing = looks good', 'value': -1}] + [
                        {'name': '%(description)s (%(points)d/%(max)d)' % item, 'value': i} for i, item in
                        enumerate(marking_items)],
                    'default': 0
                }])
                if not answer or answer['item'] == -1:
                    break

                selected_item = marking_items[answer['item']]
                answer = prompt([{
                    'type': 'input',
                    'name': 'mark',
                    'message': '%(description)s (%(max)d):' % selected_item,
                    'default': str(selected_item['max']),
                    'validate': lambda x: is_number(x) and (
                            (selected_item['max'] < 0 and 0 >= int(x) >= selected_item['max']) or (
                             selected_item['max'] > 0 and 0 <= int(x) <= selected_item['max'])) and sum_in_range(
                        int(x), total, 10)
                }])
                if not answer:
                    continue
                selected_item['points'] = int(answer['mark'])

            confirmation = prompt([{
                'type': 'confirm',
                'message': 'Do you want to save marks for "%s"?' % ccid,
                'name': 'save',
                'default': True,
            }])
            if confirmation and confirmation['save']:
                with open(marksheet_path, 'w') as marksheet:
                    placed_marks = 0
                    for line in marksheet_content:
                        if line.find('_____') != -1:
                            try:
                                marking_item = marking_items[placed_marks]
                                marksheet.write(line.replace('_____', str(marking_item['points'])))
                                placed_marks = placed_marks + 1

                            # We reached to the end of marksheet items list, so should print the total
                            except IndexError:
                                # Student's mark = 10 - abs(total_deducted_points)
                                marksheet.write(line.replace('_____', str(total + 10)))
                        else:
                            marksheet.write(line)

            do_continue = prompt([{
                'type': 'confirm',
                'message': 'Do you want to enter another mark?',
                'name': 'continue',
                'default': True,
            }])
            if not do_continue or not do_continue['continue']:
                break

            clear()
