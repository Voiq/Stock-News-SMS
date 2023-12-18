import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY="OO0S21UNXBQD25JW"
news_api_key = "0d91ece351a543948f91d40fc78f9701"

TWILIO_SID=""
TWILIO_AUTH=""
TWILIO_PHONE_NUMBER=""
stock_params ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_KEY
}

response =requests.get(STOCK_ENDPOINT,params= stock_params)
data=response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price =yesterday_data["4. close"]
print (yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print (day_before_yesterday_closing_price)

differnece = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print (differnece)

diff_percent = (differnece/float(yesterday_closing_price))*100
print (diff_percent)

if diff_percent > 0.5:
    print("Get News")


    
    if diff_percent > 5:
        news_params={
            "apiKey":news_api_key,
            "qInTitle":COMPANY_NAME
        }
        news_response=requests.get(NEWS_ENDPOINT,params=news_params)
        articles = news_response.json()["articles"]
        print(articles)

three_articles = articles[:3]
print (three_articles)

formated_article = [f"Headline:{articles['title']} \n Description:{articles['description']}" for articles in three_articles.items()]

client = Client(TWILIO_SID,TWILIO_AUTH)
for articles in formated_article:
    message = client.message.create(
        body=articles,
        from_=TWILIO_SID,
        to=TWILIO_PHONE_NUMBER
    )
