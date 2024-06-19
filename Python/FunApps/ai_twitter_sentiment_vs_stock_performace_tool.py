#Twitter + OpenAI + Yahoo Finance

import tweepy
import csv
import openai
import yfinance as yf
import pytz
from datetime import datetime, time
import time as t
openai.api_key = "key here"


search_ticker = "SPX"
positive_ticker = "TQQQ"
negative_ticker = "SQQQ"
direction = ""
track_ticker = ""
tweets_returned = []

# Get the current date and time
now = datetime.now()
current_day = now.weekday()
date_to_check = datetime.now().date()

def get_tweets(term):
#Create an API client
    client = tweepy.Client(
        consumer_key="key here",
        consumer_secret="key here",
        access_token="key here",
        access_token_secret="key here")
    # Set the search term
    SEARCH_TERM = term
    # Set the number of tweets to return
    MAX_TWEETS = 10
    # Search for tweets containing the search term
    results = client.search_recent_tweets(SEARCH_TERM, max_results=MAX_TWEETS,
    user_auth=True)

    #Parse results from API
    #Convert results into string
    results_string = str(results)
    #Remove trailing metadata from string
    results_string = results_string[:-191]
    # Split string into list
    split_results = results_string.split(">, ")
    # iterate over the list of strings
    for i, tweet in enumerate(split_results):
    # find the index of "<Tweet id="
        start_index = tweet.index("<Tweet id=")
    # insert "https://twitter.com/i/status/" at the start index
        split_results[i] = tweet[:start_index] + "https://twitter.com/i/status/" + tweet[start_index:]
    # delete "<Tweet id=" from the string
        split_results[i] = split_results[i].replace("<Tweet id=", "")
    # delete "Response(data=[" from the string
        split_results[i] = split_results[i].replace("Response(data=[", "")
    # delete "text=" from the string
        split_results[i] = split_results[i].replace("text=", "")

    global tweets_returned

    tweets_returned = split_results
    print(tweets_returned)

#AI parser function
def ai_parse(tweets):
    global direction
    question = f"The following is a collection of 100 random tweets from today about the stock market. Based on these tweets, is the market sentiment more positive or negative?. Please only return the word positive or the word negative, followed by a comma, and give a score from 0 to 100 of your confidence in the sentiment. Please don't include a space between the comma and the score. {tweets}"
    completion = openai.Completion.create(engine="text-davinci-003",prompt=question,temperature=1,max_tokens=1024,n=1, )
    response = completion.choices[0].text

    response = response.replace('\n', '')
    to_write = f"{now},{response}"
    print(to_write)

    response_lower = response.lower()

    if "positive" in response_lower:
        direction = "positive"
    if "negative" in response_lower:
        direction = "negative"

    with open('stock_predictor.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        # Format the string as a CSV row
        row = [to_write]

        # Write the row to the file
        writer.writerow(row)

def stock_change(track_ticker,hour2,minute2):
    # Specify the desired time zone
    timezone = pytz.timezone('America/New_York')
    date = datetime.now(timezone).date()

    # Set the start and end times for the specified date and time range (9:30 AM to 3 PM)
    start_time = datetime.combine(date, time(13, 30)).astimezone(timezone)
    end_time = datetime.combine(date, time(hour2, minute2)).astimezone(timezone)

    time_elapsed = ((hour2-13)*60 + minute2-30)/60

    # Fetch the historical stock price data
    ticker_data = yf.download(track_ticker, start=start_time, end=end_time, interval='1m')

    # Calculate the percentage change
    start_price = ticker_data['Close'].iloc[0]
    end_price = ticker_data['Close'].iloc[-1]
    percentage_change = round(((end_price - start_price) / start_price) * 100, 2)

    # Print the percentage change
    results_string = f"Gain for {track_ticker} on {date} {time_elapsed} hours after the open: {percentage_change}%"
    print(results_string)

    with open('stock_predictor.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        row = [results_string]
        writer.writerow(row)

#Driver code
if current_day <5:
    tweets = get_tweets(search_ticker)
    ai_parse(tweets_returned)
    t.sleep(23400)
    if direction == "positive":
        track_ticker = positive_ticker
    if direction == "negative":
        track_ticker = negative_ticker
    stock_change(track_ticker,14,0)
    stock_change(track_ticker,15,0)
    stock_change(track_ticker,16,0)
    stock_change(track_ticker,17,0)
    stock_change(track_ticker,18,0)
    stock_change(track_ticker,19,0)






