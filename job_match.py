import json
import os
from pathlib import Path
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim


# Job Directory Path
job_dir_path = "C:\\Users\\longe\\Documents\\Projects\\CollegeProject\\JsonProject\\joborder"


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


def location_match_cvs(applicant_info, job_infos):
    for job in job_infos:
        matched_applicants = [a for a in applicant_info if a['country'] == job['country']]
        job['location_matched_applicants'] = matched_applicants
    return job_infos


def write_in_files(output_data):
    """

    :param output_data:
    :return:
    """
    file_path = os.path.join(os.path.abspath(os.curdir), 'location_matched_applicant_job_info.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f)


if __name__ == '__main__':
    # config.json this file should look where to look for job/cv files
    print("Process started...")
    output = []
    applicant_country_filepath = "applicant_info.json"
    setting_info = None
    json_data = None
    files = []

    # check if file exists or not before proceeding
    applicant_abs_path = os.path.join(os.path.abspath(os.curdir), applicant_country_filepath)
    if path_exists(applicant_abs_path):
        applicant_info = read_json_file(applicant_abs_path)
        if applicant_info is None:
            print("File information required to proceed...")
        else:
            files = get_files()
            # this can be achieved by using async
            for file in files:
                print("Getting Best Match Applicant for a file: " + file)
                temp = {}
                json_data = read_json_file(file)
                file_name = os.path.basename(file)
                geoCoordinates = None
                try:
                    geoCoordinates = json_data['CurrentLocation']['GeoCoordinates']
                except KeyError:
                    pass
                # write in output file
                temp['filename'] = file_name
                temp['geoCoordinates'] = geoCoordinates
                temp['country'] = None if geoCoordinates is None else get_country(geoCoordinates)
                output.append(temp)

            if len(output) > 0:
                updated_output = location_match_cvs(applicant_info, output)
                write_in_files(updated_output)
                print("job completed")
