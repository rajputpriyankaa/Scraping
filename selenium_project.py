import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd

############### project starts ##########

def crwler(DMKT,RMKT):
    website = "https://www.airindia.in/"
    path = "c:\\Users\\Admin\\Downloads\\chromedriver"
    driver = webdriver.Chrome(path)
    driver.get(website)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//ins[@class="iCheck-helper"]').click()

    ################ enter origin

    dest = driver.find_element_by_xpath('//input[@name="from"]')
    dest.send_keys(DMKT)
    # driver.find_element_by_xpath('//a[@id="ui-id-31"]').click()
    driver.find_element_by_xpath('//a[@class="ui-corner-all"][1]').click()

    ############### enter destination

    org = driver.find_element_by_xpath('//input[@name="to"]')
    org.send_keys(RMKT)
    driver.find_element_by_xpath("//*[contains(text(),'"+RMKT+"')]").click()
    driver.find_element_by_xpath('//input[@value="Departing"]').click()
    driver.find_element_by_xpath('//td[@data-month="3" and @data-year="2023"]/a[text()="7"]').click()
    time.sleep(5)
    for reply in driver.find_elements_by_xpath('//input[@value="Search" and @id="btnbooking"]'):
        # driver.execute_script('arguments[0].scrollIntoView();', reply)
        # reply.send_keys(Keys.DOWN)
        # reply.click()

        #or

        driver.execute_script('arguments[0].click();',reply)
    time.sleep(10)
    driver.find_element_by_xpath('//span[contains(text(),"Click to verify") or contains(text(),"Retry")]').click()

    ############### extraction
    try:
        slider_container = driver.find_element(By.XPATH, value='//div[@class="geetest_slider geetest_ready"]')
        slider = driver.find_element(By.XPATH, value='//div[@class="geetest_slider_button"]')
        actions = ActionChains(driver)

    # Perform sliding action
        for x in range(10000):
            actions.move_to_element(slider).click_and_hold().move_by_offset(x, 500).release().perform()
            time.sleep(0.1)

    except:
        print("Captcha didn't appear!")

    time.sleep(10)
    DTIME = driver.find_elements_by_xpath('//div[@class="refx-display-1 bound-departure-datetime"]')
    DATIME = driver.find_elements_by_xpath('//div[@class="refx-display-1 bound-arrival-datetime"]')
    STOPS = driver.find_elements_by_xpath('//div[@class="bound-stop-text ng-star-inserted"]')
    DURATION = driver.find_elements_by_xpath('//span[@class="duration-value"]')
    FARE = driver.find_elements_by_xpath('//refx-price[@class="no-mcp-price refx-display-1 flight-price ng-star-inserted"]/span/span[@class="price-amount price-1-6-digits-display"]')
    CURRENCY = driver.find_elements_by_xpath('//refx-price[@class="no-mcp-price refx-display-1 flight-price ng-star-inserted"]/span/abbr[@class="price-currency-code before currency-1-6-digits-display ng-star-inserted"]')
    dtime = []
    datime = []
    stops = []
    duration = []
    fare = []
    currency = []
    for (DTIME,DATIME,STOPS,DURATION,FARE,CURRENCY) in zip(DTIME,DATIME,STOPS,DURATION,FARE,CURRENCY):
        dtime.append(DTIME.text)
        datime.append(DATIME.text)
        stops.append(STOPS.text)
        duration.append(DURATION.text)
        fare.append(FARE.text)
        currency.append(CURRENCY.text)
    print(dtime,datime,stops,duration,fare)
    driver.quit()
    pd.DataFrame({'Departure Time':dtime,
                  'Arrival Time':datime,
                  'Stops':stops,
                  'Duration':duration,
                  'Fare':fare,
                  'Currency':currency}).to_csv('flight_data.csv',index=False)

crwler('DEL','HYD')




