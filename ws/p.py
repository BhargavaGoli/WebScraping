import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

custom_headers={
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
    'accept_language':'en-US,en;q=0.5'
}

def get_html(url):
    res=requests.get(url,headers=custom_headers)
    return res.content

def get_product_info(soup):
    price_data = soup.select_one('span.a-price-whole')
    if price_data:
        price = price_data.text.strip()
    else:
        price = None
    return price


def get_name(soup):
    name = soup.select_one('#productTitle')
    if name:
        name_data = name.text.strip()
    else:
        name_data = None
    return name_data

def scrap_data(url):
    product_info={}
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    product_info['price']=get_product_info(soup)
    product_info['name']=get_name(soup)
    return product_info
    

if __name__ == "__main__":
    f=[]
    with open('links.csv') as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        for row in reader:
            url=row[0]
            product_info=scrap_data(url)
            f.append(product_info)
        

    df=pd.DataFrame(f)
    df.to_excel("fridge.xlsx",index=False)


    