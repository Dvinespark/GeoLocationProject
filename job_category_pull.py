# selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def pull_data(site_url):
    category = []
    sub_category = []
    jobs = []
    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s)
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
        for each_li in category_li_elements:
            temp_sub_category.append(each_li.text)
        sub_category.append(temp_sub_category)

    print(category)
    print(sub_category)


    # loop through each li elements to get sub categories

    driver.close()


if __name__ == "__main__":
    url = "https://www.careerbuilder.com/browse"
    print("Starting to fetch data from " + url)
    pull_data(url)
