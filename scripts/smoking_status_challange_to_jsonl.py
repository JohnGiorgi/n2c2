"""A simple script which converts the n2n2 2006 Smoking Status Challange dataset into a JSON lines
format. For more info on the format, see here: http://jsonlines.org/.

Depenencies:
    - defusedxml (`pip install defusedxml`)

Usage:
    ```python
    python smoking_status_challange_to_jsonl.py -i path/to/xml/file -o path/to/output/folder
    ```
"""
import argparse
import json
from pathlib import Path

from defusedxml.ElementTree import parse


def main(**kwargs):
    """Converts the XML data from the n2n2 2006 Smoking Status Challange dataset at
    `kwargs['input']` into JSON lines format, and saves it to disk as a .jsonl file at
    `kwargs['output']`.
    """
    records = parse(kwargs['input']).getroot().findall('RECORD')

    jsonl_formatted_records = extract_text_labels_ids_from_records(records)

    # Create output file with same name as input file but with a .jsonl extension
    output_filepath = Path(kwargs['output']) / Path(kwargs['input']).with_suffix('.jsonl').name

    with open(output_filepath, 'w') as f:
        f.write(jsonl_formatted_records)


def extract_text_labels_ids_from_records(records):
    """Returns a JSON lines formatted string, containing all text, labels and ids from `records`.

    Args:
        records (list): A list of Element objects parsed from an XML file. Expects each object to
            have three child nodes, 'SMOKING' and 'TEXT'. Additionally expects each object to have
            the attribute 'ID'.

    Returns:
        A JSON lines formatted string, containing all text, labels and ids from `records`.
    """
    jsonl_formatted_records = ''

    for record in records:
        json_record = json.dumps({
            "text": record.findall('TEXT')[0].text,
            "label": record.findall('SMOKING')[0].get('STATUS'),
            "id": record.get('ID')
        })
        jsonl_formatted_records += f'{json_record}\n'

    return jsonl_formatted_records


if __name__ == '__main__':
    description = ("A simple script which converts the n2n2 2006 Smoking Status Challange dataset"
                   " into a JSON lines format. For more info on the format, see here:"
                   " http://jsonlines.org/.")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--input", default=None, type=str, required=True,
                        help="Filepath to n2n2 2006 Smoking Status Challange XML file to convert.")
    parser.add_argument("-o", "--output", default='./', type=str,
                        help=("Optional, directory to save the jsonl file. Defaults to the"
                              " current directory."))

    args = vars(parser.parse_args())

    main(**args)
