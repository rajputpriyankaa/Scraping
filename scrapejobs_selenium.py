import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def scrape_timesjobs(job_designation, job_location, experience):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()  # Provide path to your chromedriver
    driver.maximize_window()
    # Construct the URL based on user input
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=%22{job_designation}%2C%20{job_location}%22&txtKeywords=%22{job_designation}%22&txtLocation={job_location}&cboWorkExp1={experience}"

    # Load the webpage
    driver.get(url)
    time.sleep(20)
    try:
        driver.find_element(By.XPATH, '// span[ @ id = "closeSpanId"]').click()
    except:
        None
    # Parse the HTML content after the page has fully loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all elements with class 'job-bx'
    job_elements = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    job_listings = []
    # Extract job details (remaining code remains the same)
    for job_elem in job_elements:
        job_title_elem = job_elem.find('h2')
        company_name_elem = job_elem.find('h3', class_='joblist-comp-name')
        experience_elem = job_elem.find('ul', class_='top-jd-dtl clearfix').find_all('li')[0]
        location_elem = job_elem.find('ul', class_='top-jd-dtl clearfix').find_all('li')[-1]

        li_elements = job_elem.find('ul', class_='top-jd-dtl clearfix').find_all('li')
        salary_elem = li_elements[1] if len(li_elements) >= 3 else None
        posted_date_elem = job_elem.find('span', class_='sim-posted')

        job_title = job_title_elem.text.strip().replace('/', '').replace('\n', '') if job_title_elem else ''
        company_name = company_name_elem.text.strip().replace('/', '').replace('\n', '') if company_name_elem else ''
        location = location_elem.text.strip().replace('/', '').replace('\n', '').replace('location_on',
                                                                                         '') if location_elem else ''
        experience = experience_elem.text.strip().replace('/', '').replace('\n', '').replace('card_travel',
                                                                                             '') if experience_elem else ''
        salary = salary_elem.text.strip().replace('/', '').replace('\n', '') if salary_elem else ''
        posted_date = posted_date_elem.text.strip().replace('/', '').replace('\n', '') if posted_date_elem else ''

        job_listing = {
            'Title': job_title,
            'Company': company_name,
            'Location': location,
            'Experience': experience,
            'Salary': salary,
            'Posted Date': posted_date
        }
        job_listings.append(job_listing)

    # Close the WebDriver
    driver.quit()

    return job_listings

# Get user input for job designation, location, and experience
job_designation = input("Enter job designation: ")
job_location = input("Enter job location: ")
experience = input("Enter experience (in years): ")

# Scrape job listings
job_listings = scrape_timesjobs(job_designation, job_location, experience)

if job_listings:
    # Convert data into DataFrame using pandas
    df = pd.DataFrame(job_listings)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)
    print("\n Jobs for the searched criteria:")
    print(df)
    # df.to_csv('Data.csv', index=False) # for converting into csv
else:
    print("No job listings found.")