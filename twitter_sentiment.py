import tweepy
import re
import pickle
import matplotlib.pyplot as plt
import numpy as np

from tweepy import OAuthHandler

#Initializing the keys
consumer_key='yLDLZ3TSII2IBCDdHzMMdeVwL'
consumer_secret='905XreDvJa9zEJnD9HL0aOo6nEj16RbETeZdQWQ6mMBv0Qpazz'
access_token='135756299-JOVABteZBygT5eqhdk4SeJkGdSypX7MJhbqcHYud'
access_secret='X6eD9BWo8X6uUVJVTVsfrigaLT56wK81wwUtata4yUUiX'


auth=OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

args=['google']
api=tweepy.API(auth,timeout=10)


#Fetching tweets
list_tweets=[]
query=args[0]
if len(args)==1:
    for status in tweepy.Cursor(api.search,q=query+" -filter:retweets",lang='en',result_type='recent').items(100):
        list_tweets.append(status.text)
        

#Loading classifier and vectorizer
with open('tfidfmodel.pickle','rb') as f:
    vectorizer=pickle.load(f)
    
with open('classifier.pickle','rb') as f:
    clf=pickle.load(f) 
    
    
total_pos=0
total_neg=0

#Preprocessing tweets
for tweet in list_tweets:
    tweet=re.sub(r'^http://t.co/[a-zA-Z0-9]*\s',' ',tweet)
    tweet=re.sub(r'\s+http://t.co/[a-zA-Z0-9]*\s',' ',tweet)
    tweet=re.sub(r'\s+http://t.co/[a-zA-Z0-9]*$',' ',tweet)
    tweet=tweet.lower()
    tweet = re.sub(r"that's","that is",tweet)
    tweet = re.sub(r"there's","there is",tweet)
    tweet = re.sub(r"what's","what is",tweet)
    tweet = re.sub(r"where's","where is",tweet)
    tweet = re.sub(r"it's","it is",tweet)
    tweet = re.sub(r"who's","who is",tweet)
    tweet = re.sub(r"i'm","i am",tweet)
    tweet = re.sub(r"she's","she is",tweet)
    tweet = re.sub(r"he's","he is",tweet)
    tweet = re.sub(r"they're","they are",tweet)
    tweet = re.sub(r"who're","who are",tweet)
    tweet = re.sub(r"ain't","am not",tweet)
    tweet = re.sub(r"wouldn't","would not",tweet)
    tweet = re.sub(r"shouldn't","should not",tweet)
    tweet = re.sub(r"can't","can not",tweet)
    tweet = re.sub(r"couldn't","could not",tweet)
    tweet = re.sub(r"won't","will not",tweet)
    tweet = re.sub(r"\W"," ",tweet)
    tweet = re.sub(r"\d"," ",tweet)
    tweet = re.sub(r"s+[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+[a-z]$"," ",tweet)
    tweet = re.sub(r"^[a-z]\s+"," ",tweet)
    tweet = re.sub(r"^[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+"," ",tweet) 
    
    #Predicting the sentiments of tweets
    sent=clf.predict(vectorizer.transform([tweet]).toarray())
    if sent[0]==1:
        total_pos+=1
    else:
        total_neg+=1
    

#Plotting the bar chart    
objects=['Positive','Negative'] 
y_pos=np.arange(len(objects))

plt.bar(y_pos,[total_pos,total_neg],alpha=0.5) 
plt.xticks(y_pos,objects)
plt.ylabel('Number')
plt.title('Number of Postive and Negative Tweets')
plt.show()  
    
    
    
    
        








