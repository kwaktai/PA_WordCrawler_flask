import os
import csv
from typing import List


def csv_to_html_string(filename: str) -> str:
    file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '..', 'data', filename)

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = [row for row in reader]

    return generate_html_table(header, rows)


def generate_html_table(header: List[str], rows: List[List[str]]) -> str:
    table = '<table>\n'
    table += '  <tr>\n'

    for column_name in header:
        table += f'    <th>{column_name}</th>\n'

    table += '  </tr>\n'

    for row in rows:
        table += '  <tr>\n'
        for cell in row:
            table += f'    <td>{cell}</td>\n'
        table += '  </tr>\n'

    table += '</table>'
    return table


if __name__ == '__main__':
    print(csv_to_html_string('word_list.csv'))
