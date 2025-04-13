import random
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

session = requests.Session()

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

page = 'https://www.scrapingcourse.com/ecommerce/'
productsdata = []

while page:
    print(f'hitting page.... : {page}')
    response = session.get(url=page, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    chunks = soup.findAll('li', attrs={'data-products': 'item'})
    for chunk in chunks:
        title = chunk.find('h2', class_='product-name woocommerce-loop-product__title').text
        product_url = chunk.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
        image_url = chunk.find('img', class_='attachment-woocommerce_thumbnail product-image size-woocommerce_thumbnail product-image')['src']
        price = chunk.find('span', class_='product-price woocommerce-Price-amount amount').text
        product_dict = dict(Product_Name=title, Product_url=product_url, Image_url=image_url, Price=price)
        print(product_dict)
        productsdata.append(product_dict)

    time.sleep(random.uniform(3, 7))
    # page = None
    page = soup.find('a', class_='next page-numbers')['href'] if 'next page-numbers' in str(soup) else None
    # print(soup)

    # print('next page-numbers' in str(soup))

# -----------------------with pandas--------------------------------

df = pd.DataFrame(productsdata)
df.to_csv('products_data.csv', index=False)

# ----------------------with csv DictWriter--------------------------------
# with open('products_data.csv', 'w', newline='', encoding='utf-8') as w:
#     fieldnames = ['Product_Name', 'Product_url', 'Image_url', 'Price']
#     writer = csv.DictWriter(w, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for product in productsdata:
#         writer.writerow(product)
