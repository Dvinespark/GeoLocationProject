import pandas as pd

# sentence matching library
from sentence_transformers import SentenceTransformer

# sklearn library
from sklearn.metrics.pairwise import cosine_similarity
from helper import *

model = SentenceTransformer('bert-base-nli-mean-tokens')
# Job Directory Path
job_dir_path = "C:\\Users\\longe\\Documents\\Projects\\CollegeProject\\JsonProject\\joborder"


def flat_job_category_file():
    job_category = pd.read_json('output.json')
    job_category['sub_jobs'] = None
    job_category['jobs'] = None
    for index, row in job_category.iterrows():
        sub_jobs = []
        jobs = []
        for element in row.sub_category:
            sub_jobs.append(element['title'])
            jobs.append(element['jobs'])
        row['sub_jobs'] = sub_jobs
        row['jobs'] = jobs

    return job_category


def text_matched_cvs(applicant_data, job_data):
    # Algorithm
    # Step 1: first get category in a list
    # Step 2: Sub category
    # Step 3: Jobs

    # Loop through each applicant and see if it falls on those 3
    # mark a flag if applicant falls under a same row i.e category sub-category and jobs in one row
    category_list = job_data.category.tolist()
    sub_category_list = [item for sublist in job_data.sub_jobs.tolist() for item in sublist]
    job_list = [item for sublist in job_data.jobs.tolist() for sub_sub_list in sublist for item in sub_sub_list]
    category_flag = False
    replace_flag = False  # flag for replacing first element of sentences of a job

    # looping through applicant
    for applicant in applicant_info:
        sentence = applicant['qualification_summary'] if applicant['qualification_summary'] else \
            applicant['professional_summary'] if applicant['professional_summary'] else applicant['plain_text'][0:100]
        if replace_flag:
            category_list.pop(0)
            sub_category_list.pop(0)
            job_list.pop(0)
        category_list.insert(0, sentence)
        sub_category_list.insert(0, sentence)
        job_list.insert(0, sentence)
        sentence_embeddings1 = model.encode(category_list)
        sentence_embeddings2 = model.encode(sub_category_list)
        sentence_embeddings3 = model.encode(job_list)

        # for category
        result = cosine_similarity(
            [sentence_embeddings1[0]],
            sentence_embeddings1[1:]
        )
        max_value = result
        for index, value in enumerate(result.tolist()[0]):
            if value == max_value:
                applicant['best_category'] = sentence_embeddings1[index+1]
                applicant['best_category_score'] = max_value
                break

        # for sub_category
        result = cosine_similarity(
            [sentence_embeddings2[0]],
            sentence_embeddings2[1:]
        )
        max_value = result
        for index, value in enumerate(result.tolist()[0]):
            if value == max_value:
                applicant['best_sub_category'] = sentence_embeddings2[index+1]
                applicant['best_sub_category_score'] = max_value
                break
        # for jobs
        result = cosine_similarity(
            [sentence_embeddings3[0]],
            sentence_embeddings3[1:]
        )
        max_value = result
        for index, value in enumerate(result.tolist()[0]):
            if value == max_value:
                applicant['best_job'] = sentence_embeddings3[index+1]
                applicant['best_job_score'] = max_value
                break

        replace_flag = True

    return job_data


if __name__ == '__main__':
    job_data = flat_job_category_file()

    # config.json this file should look where to look for job/cv files
    print("Process started...")
    applicants_filename = "applicant_info.json"

    # check if file exists or not before proceeding
    applicant_abs_path = os.path.join(os.path.abspath(os.curdir), applicants_filename)
    if path_exists(applicant_abs_path):
        applicant_info = read_json_file(applicant_abs_path)

        if applicant_info is not None:
            updated_output = text_matched_cvs(applicant_info, job_data)
            write_in_files(updated_output)
            print("job completed")
