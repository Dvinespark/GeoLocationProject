import json
import os
from pathlib import Path


def path_exists(path):
    """

    :param path:
    :return:
    """
    if Path(path).exists():
        return True
    return False


def construct_filepath(dir_path, filename):
    """

    :param dir_path:
    :param filename:
    :return:
    """
    return os.path.join(dir_path, filename)


def get_files():
    """
    returns files from a directory path
    :param config:
    :return:
    """
    file_list = []
    if path_exists(job_dir_path):
        file_names = os.listdir(job_dir_path)
        file_list = [construct_filepath(job_dir_path, f) for f in file_names]
    return file_list


def get_country(geo_coordinate):
    """
    timeout errors might come over here
    :param geo_coordinate:
    :return:
    """
    location = geo_locator.reverse(str(geo_coordinate['Latitude']) + ", " + str(geo_coordinate['Longitude']),
                                   timeout=10)
    address = location.raw['address']
    return address.get('country', 'Unknown')


def read_json_file(path=None):
    """
    :param path:
    :return: json data
    """
    if path_exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            return data
    return None


def write_in_files(output_data):
    """

    :param output_data:
    :return:
    """
    file_path = os.path.join(os.path.abspath(os.curdir), 'text_matched.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f)
