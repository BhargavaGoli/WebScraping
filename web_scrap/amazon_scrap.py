import requests
from datetime import datetime
import csv
import bs4

USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

REQUEST_HEADERS={
    'User-Agent':USER_AGENT,
    'Accept-Language':"en-US, en;q=0.5"
}

def get_page_html(url):
    res=requests.get(url=url, headers=REQUEST_HEADERS)
    return res.content

def get_product_price(soup):
    price_span = soup.find('span',class_="a-price-whole")
    if price_span:
        price = price_span.text.strip().replace(',', '').replace('₹', '')
        try:
            return float(price)
        except ValueError:
            print("Value obtained could not be parsed")
            return None
    else:
        print("Price span not found")
        return None



def extract_product_info(url):
    product_info={}
    print(f"Scrapping url:{url}")
    html=get_page_html(url=url)
    soup=bs4.BeautifulSoup(html,'lxml')
    product_info['price']=get_product_price(soup)
    return product_info

if __name__ == "__main__":
    with open('web_scrap/amz_ulrs.csv',newline='') as csvfile:
        reader=csv.reader(csvfile,delimiter=',')
        for row in reader:
            url=row[0]
            print(extract_product_info(url))