# selenium imports
from asyncio import wait_for

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# headless configuration
options = Options()
options.headless = True


def get_job_list(link):
    print("Navigating to :" + str(link))
    jobs = []
    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    driver.get(link)
    jobs_elements = driver.find_elements(By.XPATH, ".//a[@class='pb0']")
    for job in jobs_elements:
        jobs.append(job.text)
    driver.close()
    return jobs


def pull_data(site_url):
    category = []
    sub_category = []
    jobs = []
    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(site_url)

    # getting divs with category
    # category = driver.find_elements(By.CLASS_NAME, 'col-2')
    bloc_class_elements = driver.find_elements(By.XPATH, ".//div[@class='col col-mobile-full bloc']")
    # category = bloc_class_elements.
    for element in bloc_class_elements:
        category_text = element.find_elements(By.TAG_NAME, 'h3')
        category.append(category_text[0].text)
        category_li_elements = element.find_elements(By.TAG_NAME, 'li')
        temp_sub_category = []
        temp_jobs = []
        for each_li in category_li_elements:
            temp_sub_category.append(each_li.text)
            print("Navigating to .... " + each_li.text)
            temp_jobs = get_job_list(each_li.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))
            # driver.execute_script("window.history.go(-1)")
        sub_category.append(temp_sub_category)
        jobs.append(temp_jobs)

    print(category)
    print(sub_category)
    print(jobs)

    driver.close()

    # do some logic here to make a flat lists and then write it in xl file


if __name__ == "__main__":
    url = "https://www.careerbuilder.com/browse"
    print("Starting to fetch data from " + url)
    pull_data(url)
