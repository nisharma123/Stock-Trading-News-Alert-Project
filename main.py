import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "your STOCK_API_KEY"
NEWS_API_KEY = "your NEWS_API_KEY"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
SID = "your sid"
AUTH_TOKEN = "your AUTH_TOKEN"
PHONE = "twillo phone no."

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday.

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
# print(data)
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']
#print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
#print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
#print(difference)

difference_percentage = (difference / float(yesterday_closing_price)) * 100
# print(difference_percentage)

if difference_percentage < 5 or difference_percentage > 5:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }

# Get relevant news about the stock

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()

    news_data = news_response.json()["articles"]
    #print(news_data)
    three_articles = news_data[:3]

    formatted_article = [f"Yesterday's Closing Price: {yesterday_closing_price}\nDay Before Yesterday Closing Price: " \
                         f"{day_before_yesterday_closing_price}\nAuthor: {article['author']}.\nHeadline: " \
                         f"{article['title']}.\nNews: {article['url']}." for article in three_articles]


# Send a separate message with the percentage change and each article's title and description to your phone number.
    client = Client(SID, AUTH_TOKEN)

    for article in formatted_article:
        message = client.messages.create(
            to="+917792850876",
            from_=PHONE,
            body=article
        )
        print(message.status)
