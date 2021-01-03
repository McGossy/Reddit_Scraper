import praw
import datetime
import json
from nltk.corpus import stopwords
import string
import pandas as pd
import collections

class Reddit:
    def __init__(self):
        self.file = open('reddit_info.json')
        self.info = json.load(self.file)
        self.reddit = praw.Reddit(client_id = self.info['client_id'],
                        client_secret = self.info['client_secret'],
                        user_agent = self.info['user_agent'],
                        username = self.info['username'],
                        password = self.info['password'])
        

    # 1000 posts may not be enough, so compile 1000 posts from each subreddit of choosing.
    def compile_subreddits(self, subreddits):
        headlines = set()

        for i in range(len(subreddits)):
            subreddit = self.reddit.subreddit(subreddits[i])
            top_headlines_in_year = subreddit.top("year", limit=None)

            for submission in top_headlines_in_year:
                headlines.add(submission)
        
        return headlines

    ''' Remove punctuation and digits from a string. '''
    def _process_string(self, s):
        no_digits = []

        # Convert string to lowercase, remove punctuation.
        raw_string = s.lower()
        clean_string = raw_string.translate(str.maketrans('','', string.punctuation))

        # Remove all digits from string.
        for letter in clean_string:
            if not letter.isdigit():
                no_digits.append(letter)

        # Create the final string.
        result = ''.join(no_digits)

        return result

    '''Find the most common word'''
    def get_common_words(self, all_headlines):

        wordcounts = {}

        # Loop through the set with submission titles, remove stop words, and get a dictionary of word counts
        for submission in all_headlines:
            for word in self._process_string(submission.title).split():
                if word not in stopwords.words('english'):
                    if len(word) > 2:
                        if word not in wordcounts:
                            wordcounts[word] = 1
                        else:
                            wordcounts[word] += 1
        
        return wordcounts

    def find_common_words(self, wordcounts):
        word_counter = collections.Counter(wordcounts)
        for word, count in word_counter.most_common(100):
            print(word, ":", count)


    def get_common_dates(self, all_headlines):
        datecounts = {}

        for submission in all_headlines:
            date = datetime.datetime.fromtimestamp(submission.created).strftime('%m/%d/%Y')

            if date not in datecounts:
                datecounts[date] = 1
            else:
                datecounts[date] += 1
        
        return datecounts
    
    def find_common_dates(self, datecounts):
        date_counter = collections.Counter(datecounts)
        for date, count in date_counter.most_common(100):
            print(date, ":", count)

    
reddit = Reddit()

all_headlines = reddit.compile_subreddits(["all", "news", "politics", "worldnews", "science"])
wordcounts = reddit.get_common_words(all_headlines)
datecounts = reddit.get_common_dates(all_headlines)

reddit.find_common_words(wordcounts)
reddit.find_common_dates(datecounts)

