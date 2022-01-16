import os
# re-using main.py components
from main import path_exists, read_json_file, get_files


def min_education(file_path, min_edu_list):

    file_name = os.path.basename(file_path)
    matched_flag = False
    data = read_json_file(file_path)
    if 'Education' in data:
        if 'HighestDegree' in data['Education']:
            if data['Education']['HighestDegree']['Type'] in min_edu_list:
                matched_flag = True
        else:
            matched_flag = False
    return file_name if matched_flag else None


if __name__ == "__main__":
    print("Filtering with minimum education in progress..")
    config_filepath = "config.json"
    setting_info = None
    json_data = None
    files = []
    output_files = []

    config_abs_path = os.path.join(os.path.abspath(os.pardir), config_filepath)
    if path_exists(config_abs_path):
        setting_info = read_json_file(config_abs_path)
        if setting_info is None:
            print("File information required to proceed...")
        else:
            files = get_files(setting_info)

            # this can be achieved by using async
            for f in files:
                print("Reading file: " + f)
                temp = {}
                json_data = read_json_file(f)
                required_matched_file = min_education(f, setting_info['minimum_education'])
                if required_matched_file:
                    output_files.append(required_matched_file)
    print("\nMatched File names:")
    print(output_files)
    print("Process completed.")

