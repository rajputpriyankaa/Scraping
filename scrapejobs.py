import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

def scrape_timesjobs(job_designation, job_location, job_experience):
    base_url = "https://www.timesjobs.com/candidate/job-search.html"
    query_params = {
        'searchType': 'personalizedSearch',
        'from': 'submit',
        'searchTextSrc': 'as',
        'searchTextText': f'"{job_designation}, {job_location}"',
        'txtKeywords': f'"{job_designation}"',
        'txtLocation': job_location,
        'cboWorkExp1': job_experience
    }
    url = base_url + '?' + '&'.join([f'{key}={quote(value)}' for key, value in query_params.items()])
    # print(url)

    # Fetch the page
    response = requests.get(url)
    # print(response.content)
    if response.status_code == 200:

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # print('soup.prettify()', soup.prettify())

        job_elements = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        job_listings = []
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
            location = location_elem.text.strip().replace('/', '').replace('\n', '').replace('location_on','') if location_elem else ''
            experience = experience_elem.text.strip().replace('/', '').replace('\n', '').replace('card_travel','') if experience_elem else ''
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
            # print(job_listing)

        return job_listings
    else:
        print("Failed to retrieve the webpage")
        return None


# User input for fetching jobs
job_designation = input("Enter job designation: ")
job_location = input("Enter job location: ")
job_experience = input("Enter job experience: ")

# calling function scrape_timesjobs
job_listings = scrape_timesjobs(job_designation, job_location, job_experience)

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
    print("No job listings found for the given criteria.")
