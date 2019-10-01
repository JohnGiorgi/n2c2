import argparse
import json
from pathlib import Path

from defusedxml.ElementTree import parse


def main(**kwargs):
    """Parses the XML data from the n2n2 2006 Smoking Status Challange dataset.
    """
    records = parse(kwargs['input']).getroot().findall('RECORD')

    json_formatted_content = extract_text_labels_ids__from_records(records)

    # Create output file with same path as input file but with a .json extension
    output_filepath = Path(kwargs['output']) / Path(kwargs['input']).with_suffix('.json').name

    write_json_to_disk(output_filepath, json_formatted_content)


def extract_text_labels_ids__from_records(records):
    """Returns a dictionary containing all text, labels and ids from the n2n2 2006 Smoking Status
    Challange.

    Args:
        records (list): A list of Element objects parsed from an XML file. Expects each object to
            have three child nodes, 'SMOKING' and 'TEXT'. Additionally expects each object to have
            the attribute 'ID'.

    Returns:
        A dictionary, with keys 'text' and 'labels' which point to paired lists containing texts and
        labels from `records`.
    """
    json_formatted_contents = {'text': [], 'label': [], 'id': []}
    for record in records:
        json_formatted_contents['text'].append(record.findall('TEXT')[0].text)
        json_formatted_contents['label'].append(record.findall('SMOKING')[0].get('STATUS'))
        json_formatted_contents['id'].append(record.get('ID'))

    return json_formatted_contents


def write_json_to_disk(filepath, dictionary):
    """Writes `dictionary` to `filepath` as a json file.

    Args:
        filepath (str): Filepath to write a json formatted `dictionary` file.
        dictionary (dict): A python dictionary which will be written to `filepath` as a json file.

    Returns:
        Returns `filepath`.
    """
    with open(filepath, 'w') as f:
        json.dump(dictionary, f)

    return filepath


if __name__ == '__main__':
    description = ("A simple script for converting the n2n2 2006 Smoking Status Challange dataset"
                   " into a simpler json format for easier downstream processing. The output json"
                   " contains three fields, 'text', 'labels', 'ids', containing the raw text,"
                   " document labels and ids for each example in the input file.")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--input", default=None, type=str, required=True,
                        help="Filepath to n2n2 2006 Smoking Status Challange xml file to parse.")
    parser.add_argument("-o", "--output", default='./', type=str,
                        help=("Optional, directory to save the parsed contents. Defaults to the"
                              " current directory"))

    args = vars(parser.parse_args())

    main(**args)
