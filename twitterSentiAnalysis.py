#Youssef Errami 

import tweepy
import sys
import csv
import matplotlib.pyplot as p
from tweepy import OAuthHandler
from collections import Counter
from aylienapiclient import textapi

#twitter
consumer_key = #insert yours here
consumer_secret = #insert yours here
access_token = #insert yours here
access_secret = #insert yours here

#aylein
application_id = #insert yours here
application_key = #insert yours here

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

## set up an instance of the AYLIEN Text API
theClient = textapi.Client(application_id, application_key)

## search Twitter for something that interests you
query = input("What topic do you want to analyze? \n")
number = input("How many Tweets do you want to analyze? \n")

results = api.search(lang="en", q=query + " -rt", count=number, result_type="recent")

print("Tweets have been collected \n")

## open a csv file to store the Tweets and their sentiment 
fName = 'SA_of_'+number+'_tweets_regarding'+query+'.csv'

with open(fName, 'w', newline='') as csvfile:
   csv_writer = csv.DictWriter(f=csvfile, fieldnames=["Tweet", "Sentiment"])
   csv_writer.writeheader()

   print("A CSV file has been made to store the results \n")

## clean up the Tweets and send them to the AYLIEN Text API
   for c, result in enumerate(results, start=1):
       tweet = result.text
       clean = tweet.strip().encode('ascii', 'ignore')

       if len(tweet) == 0:
           print('Empty Tweet')
           continue

       response = theClient.Sentiment({'text': clean})
       csv_writer.writerow({'Tweet': response['text'], 'Sentiment': response['polarity']})

       print("Analyzed Tweet "+c)

## count the data in the Sentiment column of the CSV file 
with open(fName, 'r') as data:
   itr = Counter()
   for row in csv.DictReader(data):
       itr[row['Sentiment']] += 1

   positive = itr['positive']
   negative = itr['negative']
   neutral = itr['neutral']

#variables for pie chart
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'

#plot chart
p.pie(x=sizes, shadow=True, colors=colors, labels=labels, startangle=90)

p.title("Sentiment of "+number+" Tweets about "+query)
p.show()

print(theClient.RateLimits())