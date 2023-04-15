import requests
import smtplib
import datetime as dt
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key=os.environ["COMPANY_API_KEY"]
news_api_key=os.environ["NEWS_API_KEY"]
my_email = "vashtaputre246@gmail.com"
my_password= os.environ["PASSWORD"]

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

 # Using https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then printing("Get News").

response=requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK_NAME}&outputsize=full&apikey={api_key}")
data=response.json()["Time Series (Daily)"]


data_list=[value for (key, value) in data.items()]
yesterday_data=data_list[0]
closing_value_yesterday=[value for (key, value) in yesterday_data.items()][3]


previous_day_data=data_list[1]
closing_value_previous=[value for (key, value) in previous_day_data.items()][3]


difference = round(abs(float(closing_value_yesterday)-float(closing_value_previous)),2)



percentage_difference = round((difference/float(closing_value_yesterday))*100,2)

if percentage_difference < 5:

    ## Using https://newsapi.org/ 
    # Instead of printing ("Get News"), getting the first 3 news pieces for the COMPANY_NAME.


    news_response=requests.get(url=f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from=2023-02-17&sortBy=publishedAt&apiKey={news_api_key}")
    news_data=news_response.json()
    news_articles = news_data["articles"]


    top_news_articles=news_articles[:3]
    ## STEP 3: Using smtp to send mail
    #to send a separate message with each article's title and description to the email address. 

    formatted_article=[f"Headlines: {article['title']}.\n\nBrief: {article['description']}" for article in top_news_articles]

    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(user=my_email,password=my_password)
        message = f"Subject:Top Three news \n\n {formatted_article[0]}".encode( )
        connection.sendmail(from_addr=my_email,to_addrs=my_email,msg=message)


