import pandas as pd


def main():
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

    job_category.to_json('flat_jobs.json')


if __name__ == '__main__':
    main()