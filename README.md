# Reddit_Scraper
Scrapes data from a few of Reddit's most popular subreddits. We chose the top 1000 posts over the last year from these subreddits:
              <ul>
              <li>/r/popular</li>
              <li>/r/news</li>
              <li>/r/politics</li>
              <li>/r/worldnews</li>
              <li>/r/science</li>
              </ul>
              
This site allows you to view the most common words, dates, and allows you to search through both of those categories.

# URGENT
Running this program will take roughly 5 minutes to gather all the submission data. It's going through 5000 reddit posts so it needs some time.
Look at the 'editing main.py' section to alter this time frame.

## How to use
We unfortunately were blocked from uploading this to google app engine due to the sensitive information disclosed in the .json file and couldn't find a proper solution in time.

To use this software you will need 
<ul>
  <li>PyCharm 3.8.2</li>
  <li>Reddit Account</li>
  <li>Access to the Reddit API</li>
  <li>You can install everything in requirements.txt, but tbh that's way overboard for whats needed. For some reason it shows everything I've ever downloaded. Here's the actual necessary modules you'll need to run.</li>
  <ul>
    <li>praw</li>
    <li>json</li>
    <li>nltk</li>
    <li>nltk.stopwords</li>
    <li>strings</li>
    <li>collections</li>
    <li>flask</li>
    <li>wtforms</li>
  </ul>
  <li>On getting access to the reddit API, you'll need to change the reddit_info.json file to include your own information.*
  </ul>
  
## *json file and reddit API
https://www.youtube.com/watch?v=gIZJQmX-55U
You can follow the above tutorial up the 3:00 timestamp to set up reddit API with a reddit account.
Once you get your application setup, you must change all the 'xxxxxx' options in the json file to your account information to get this program to work.

## Editing main.py
If you want to do your own sleuthing there are two key lines to change.
<ul>
  <li>top_headlines_in_year = subreddit.top("year", limit=1000) change limit to change submission's gathered number(note: 994 seems to be reddits limit on top posts)</li>
  <li>all_headlines = reddit.compile_subreddits(["popular", "news", "politics", "worldnews", "science"]) change the list to be whatever subreddits you want to gather from</li>
  
