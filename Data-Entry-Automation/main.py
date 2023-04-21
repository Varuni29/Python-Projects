from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

form_url="https://docs.google.com/forms/d/e/1FAIpQLScGrttyJCFizgUkXfWOrkUCWob9pHwNKa-2Eif1kZ0TgNmGZg/viewform?usp=sf_link"
zillow_link="https://www.zillow.com/new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Newyork%20Ny%2C%20AS%2002222%22%2C%22mapBounds%22%3A%7B%22north%22%3A40.96437679232164%2C%22east%22%3A-73.6157588808594%2C%22south%22%3A40.43025572552515%2C%22west%22%3A-74.34360311914065%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A393682%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A2000%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%7D"

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
response=requests.get(zillow_link,headers=headers)
rentals=response.text
soup=BeautifulSoup(rentals,"html.parser")

# ALL ADDRESS ELEMENTS
all_address=soup.select(".property-card-link address")
address=[location.text.split("|")[-1] for location in all_address]

# ALL PRICES
all_prices=soup.select(".bqsBln span")
prices=[]
for element in all_prices:
    if "/" in element.text:
        price=element.text.split("/")[0]
    else:
        price=element.text.split("+")[0]
    prices.append(price)

# ALL LINKS
all_links=soup.select(".juCZCh a")
links=[]
for weblink in all_links:
    href=weblink["href"]
    if "https:" not in href:
        links.append(f"https://www.zillow.com{href}")
    else:
        links.append(href)

# Converting the data to a Google spreedsheet

driver=webdriver.Chrome(executable_path="C:\development\chromedriver.exe")

for n in range(len(links)):
    driver.get(form_url)
    form_address=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_link=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(3)
    form_address.send_keys(address[n])
    time.sleep(2)
    form_price.send_keys(prices[n])
    time.sleep(2)
    form_link.send_keys(links[n])
    time.sleep(2)
    submit_button=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()

driver.quit()
