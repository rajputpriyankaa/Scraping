import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv
def extraction(driver):
    print('entered in extraction')
    try:
        html_content = driver.find_element(By.XPATH, '//div[@class="css-1dbjc4n r-1xdf14d"]').get_attribute('innerHTML')
        response = BeautifulSoup(html_content, 'html.parser')
        all_content = response.find_all("div", {"class": "css-76zvg2 r-homxoj r-1i10wst r-1kfrs79"})
        dep_time = all_content[0].text
        arr_time = all_content[1].text
        duration = response.find("div", {"class": "css-76zvg2 r-14lw9ot r-cqee49 r-ubezar r-1e081e0 r-7xmw5f r-136ojw6"}).text
        fare = all_content[2].text.replace(',','')+'- '+all_content[3].text.replace(',','')
        info = []
        info_html = response.find_all("div", {"class": "css-1dbjc4n r-13awgt0"})
        for i in info_html:
            info.append(i.text)
        info = ''.join(info).replace(',','')
        print('date : ', [dep_time,arr_time,duration,fare,info])
        with open('spicejet.csv','w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([['Departure time','Arrival time','Duration','Fare','Info'],
                             [dep_time, arr_time, duration, fare, info]])
    except:
        print('exception in extraction')


def navigate(dep_code, arr_code, dep_date, passengers, trip_settings, return_date):
    retry = 1
    data = True
    while retry < 3 and data:
        try:
            retry = retry+1
            driver = webdriver.Chrome()
            driver.get('https://www.spicejet.com/')
            driver.maximize_window()

            ####### change settings to roundtrip ##########
            time.sleep(5)
            if trip_settings in ['y','Y']:
                driver.find_element(By.XPATH, '//div[text()="round trip"]').click()

            ####### enter deaprture & arrival code #########
            departure = driver.find_element(By.XPATH, '//input[@value="Delhi (DEL)"]')
            departure.send_keys(dep_code)
            time.sleep(5)
            arrival = driver.find_element(By.XPATH, "(//input[@type='text'])[2]")
            arrival.send_keys(arr_code)
            time.sleep(5)

            ############# enter departure date #######################
            dep_date_month_year = datetime.datetime.strptime(dep_date, '%d-%m-%y').strftime('%B-%Y')
            dep_date_date = datetime.datetime.strptime(dep_date, '%d-%m-%y').strftime('%d')
            date_xpath = f'//div[@data-testid="undefined-month-{dep_date_month_year}"]/div/div/div/div/div[text()="{dep_date_date}"]'
            driver.find_element(By.XPATH, date_xpath).click()
            time.sleep(5)

            ############# enter departure date #######################
            if trip_settings in ['y','Y']:
                ret_date_month_year = datetime.datetime.strptime(return_date, '%d-%m-%y').strftime('%B-%Y')
                ret_date_date = datetime.datetime.strptime(return_date, '%d-%m-%y').strftime('%d')
                date_xpath = f'//div[@data-testid="undefined-month-{ret_date_month_year}"]/div/div/div/div/div[text()="{ret_date_date}"]'
                driver.find_element(By.XPATH, date_xpath).click()
                time.sleep(5)

            ################ enter passengers ########################
            if int(passengers) > 1:
                driver.find_element(By.XPATH, '//div[@data-testid="home-page-travellers"]').click()
                for i in range(1, int(passengers)):
                    driver.find_element(By.XPATH, '//div[@data-testid="Adult-testID-plus-one-cta"]').click()

            ############# click on search flights ####################

            driver.find_element(By.XPATH, '//div[@data-testid="home-page-flight-cta"]').click()
            time.sleep(20)

            ############ Call extraction if page is loaded #############
            if driver.find_element(By.XPATH, '//div[text()="Flight Details"]').is_displayed() or \
                    driver.find_element(By.XPATH, '//div[text()="All flights"]').is_displayed():
                data = ''
                extraction(driver)
            else:
                raise Exception('page is not loaded')

        except:
            if driver.find_element(By.XPATH, '//div[text()="Unfortunately, there are no flights available."]').is_displayed():
                data = ''
                print('No Flights found..🙂')
            else:
                driver.quit()
                print('error occurred')
                if retry == 3:
                    print('error in crawling')


if __name__ == "__main__":
    departure_code = input('Enter Departure code: ')
    arrival_code = input('Enter Arrival code: ')
    dep_date = input('Enter departure date (dd-mm-yy): ')
    passengers = input('Enter number of passengers: ')
    trip_settings = input('Do you want Roundtrip (y/n) ? ')
    if trip_settings == 'Y' or trip_settings == 'y':
        return_date = input('Enter return date (dd-mm-yy): ')
    else:
        return_date = None
    navigate(departure_code, arrival_code, dep_date, passengers, trip_settings, return_date)



