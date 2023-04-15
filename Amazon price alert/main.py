from bs4 import BeautifulSoup
import lxml
import requests
import smtplib

my_email = "vashtaputre246@gmail.com"
my_password="wbunlkjnzmmhltbt"
URL="https://www.amazon.in/dp/0063266911/?coliid=IW1MDN47LXY0H&colid=1812W597E777B&psc=1&ref_=lv_ov_lig_dp_it"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9"
}
response=requests.get(URL,headers=headers)
website_html=response.text
website_url=response.url
# print(website_html)

soup=BeautifulSoup(website_html,"lxml")
price=soup.find(id="price").getText()
price_without_currency=price.split("₹")[1]
price_as_float=float(price_without_currency)
if price_as_float < 400:
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(user=my_email,password=my_password)
        connection.sendmail(from_addr=my_email,to_addrs=my_email,msg=f"Subject:Price Drop!\n\n price of your fav item is: {price_as_float}\n{website_url}".encode('utf-8'))


