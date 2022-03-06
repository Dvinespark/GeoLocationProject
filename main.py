import json
import os
from pathlib import Path
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim



# CV config

# {
#     "dir_path": "C:\\Users\\longe\\Documents\\Projects\\CollegeProject\\JsonProject\\CVs",
#     "dir_path": "C:\\Users\\longe\\Documents\\Projects\\CollegeProject\\JsonProject\\CVs",
#     "files": [],
#     "file_extension": "json",
#     "output_directory": "",
#     "output_file": "applicant_info.json"
# }

# job order

# {
#     "dir_path": "C:\\Users\\longe\\Documents\\Projects\\CollegeProject\\JsonProject\\joborder",
#     "files": [],
#     "file_extension": "json",
#     "output_directory": "",
#     "output_file": "joborder_info.json"
# }


# initializing geoapi
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geo_locator = Nominatim(user_agent='http')


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


def get_files(config):
    """
    returns files from a directory path
    :param config:
    :return:
    """
    file_list = []
    if config['dir_path'] is not None:
        if path_exists(config['dir_path']):
            files = os.listdir(config['dir_path'])
            if config['files'] is not None:
                for f in config['files']:
                    if f in files:
                        file_list.append(construct_filepath(config['dir_path'], f))
            file_list = [construct_filepath(config['dir_path'], f) for f in files]
    return file_list


def get_country(geo_coordinate):
    """
    timeout errors might come over here
    :param geo_coordinate:
    :return:
    """
    location = geo_locator.reverse(str(geo_coordinate['Latitude']) + ", " + str(geo_coordinate['Longitude']), timeout=10)
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


def write_in_files(config, output_data):
    """

    :param config:
    :param output_data:
    :return:
    """
    if config['output_directory'] is not None:
        file_path = os.path.join(config['output_directory'], config['output_file'])
    else:
        file_path = os.path.join(os.path.abspath(os.curdir), config['output_file'])

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f)


if __name__ == '__main__':
    # config.json this file should look where to look for job/cv files
    print("Process started...")
    output = []
    config_filepath = "config.json"
    setting_info = None
    json_data = None
    files = []

    # check if file exists or not before proceeding
    config_abs_path = os.path.join(os.path.abspath(os.curdir), config_filepath)
    if path_exists(config_abs_path):
        setting_info = read_json_file(config_abs_path)
        if setting_info is None:
            print("File information required to proceed...")
        else:
            files = get_files(setting_info)

            # this can be achieved by using async
            for file in files:
                print("Accessing country for a file: " + file)
                temp = {}
                json_data = read_json_file(file)
                file_name = os.path.basename(file)
                #geoCoordinates = json_data['ContactInformation']['Location']['GeoCoordinates']
                # write in output file
                temp['filename'] = file_name
                #temp['geoCoordinates'] = geoCoordinates
                #temp['country'] = get_country(geoCoordinates)

                ##################### CV

                # temp['plain_text'] = json_data['ResumeMetadata']['PlainText']
                # temp['professional_summary'] = json_data.get('ProfessionalSummary', None)
                # temp['qualification_summary'] = json_data.get('QualificationSummary', None)

                ############################ Job order

                temp['plain_text'] = json_data['JobMetadata']['PlainText']
                temp['job_title'] = json_data.get('JobTitles', None)
                output.append(temp)

            if len(output) > 0:
                write_in_files(setting_info, output)
                print("job completed")
