import time
import pandas as pd
from selenium import webdriver
def crawler():
    websiteurl = 'https://www.saucedemo.com/'
    path = "c:\\Users\\Admin\\Downloads\\chromedriver"
    driver = webdriver.Chrome(path)
    driver.get(websiteurl)
    username = driver.find_element_by_xpath('//input[@placeholder="Username"]')
    username.send_keys('standard_user')
    password = driver.find_element_by_xpath('//input[@placeholder="Password"]')
    password.send_keys('secret_sauce')
    driver.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//select[@data-test="product_sort_container"]').click()
    driver.find_element_by_xpath('//option[text()="Price (low to high)"]').click()
    extraction(driver)

def extraction(driver):
    product_name = driver.find_elements_by_xpath('//div[@class="inventory_item_name"]')
    img_url = driver.find_elements_by_xpath('//img[@class="inventory_item_img"]')
    product_desc = driver.find_elements_by_xpath('//div[@class="inventory_item_desc"]')
    prod_price = driver.find_elements_by_xpath('//div[@class="inventory_item_price"]')
    ProductName, ImageUrl, ProductDesc, ProductPrice = ([] for i in range(4))
    for productname,imgurl,desc,price in zip(product_name,img_url,product_desc,prod_price):
        print(f"ProductName : {productname.text}, image_url : {imgurl.get_attribute('src')}, product_description : {desc.text},"
              f"price : {price.text} ")
        ProductName.append(productname.text)
        ImageUrl.append(imgurl.get_attribute('src'))
        ProductDesc.append(desc.text)
        ProductPrice.append(price.text)

    driver.close()
    pd.DataFrame({'Product Name': ProductName,
                  'Image URLS': ImageUrl,
                  'Product Description': ProductDesc,
                  'Product Price': ProductPrice}).to_csv('site_data.csv', index=False)

if __name__=="__main__":
    crawler()