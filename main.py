import praw
import datetime
import json
from nltk.corpus import stopwords
import string
import collections


class Reddit:
    def __init__(self):
        self.file = open('reddit_info.json')
        self.info = json.load(self.file)
        self.reddit = praw.Reddit(client_id = self.info[0]['client_id'],
                        client_secret = self.info[0]['client_secret'],
                        user_agent = self.info[0]['user_agent'],
                        username = self.info[0]['username'],
                        password = self.info[0]['password'])
        self.wordcounts = {}
        self.datecounts = {}

    # 1000 posts may not be enough, so compile 1000 posts from each subreddit of choosing.
    def compile_subreddits(self, subreddits):
        headlines = set()

        for i in range(len(subreddits)):
            subreddit = self.reddit.subreddit(subreddits[i])
            top_headlines_in_year = subreddit.top("year", limit=5)

            for submission in top_headlines_in_year:
                headlines.add(submission)

        return headlines

    ''' Remove punctuation and digits from a string. '''

    def _process_string(self, s):
        no_digits = []

        # Convert string to lowercase, remove punctuation.
        raw_string = s.lower()
        clean_string = raw_string.translate(str.maketrans('', '', string.punctuation))

        # Remove all digits from string.
        for letter in clean_string:
            if not letter.isdigit():
                no_digits.append(letter)

        # Create the final string.
        result = ''.join(no_digits)

        return result

    '''Find the most common word'''

    def get_common_words(self, all_headlines):
        # Loop through the set with submission titles, remove stop words, and get a dictionary of word counts
        for submission in all_headlines:
            for word in self._process_string(submission.title).split():
                if word not in stopwords.words('english'):
                    if len(word) > 2:
                        if word not in self.wordcounts:
                            self.wordcounts[word] = 1
                        else:
                            self.wordcounts[word] += 1
        word_counter = dict()
        word_tuple = collections.Counter(self.wordcounts)
        for word, count in word_tuple.most_common(100):
            word_counter[word] = count

        return word_counter

    def get_common_dates(self, all_headlines):

        for submission in all_headlines:
            date = datetime.datetime.fromtimestamp(submission.created).strftime('%m/%d/%Y')

            if date not in self.datecounts:
                self.datecounts[date] = 1
            else:
                self.datecounts[date] += 1

        date_counter = dict()
        date_tuple = collections.Counter(self.datecounts)
        for date, count in date_tuple.most_common(100):
            date_counter[date] = count

        return date_counter


reddit = Reddit()

# Here I am compiling all posts from popular, news, all, politics, and worldnews subreddits.
all_headlines = reddit.compile_subreddits(["popular", "news", "politics", "worldnews", "science"])

word_list = reddit.get_common_words(all_headlines)
date_list = reddit.get_common_dates(all_headlines)

print(word_list)
print(date_list)


from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

#Used for the search extension
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Search')

#initialize Flask and config with secret key(needed for forms)
app = Flask(__name__)
app.config['SECRET_KEY'] = '62c04aebd965c494be687413770b91cc'


@app.route('/')
@app.route('/word_display')
def word_display():
    return render_template('home.html', title='Reddit Scraper', words=word_list)


@app.route('/popular_dates')
def popular_dates():
    return render_template('date_display.html', title='Date Display', dates=date_list)

global data

@app.route('/search_words', methods=["GET", "POST"])
def search_words():
    global data
    form = SearchForm()
    if form.validate_on_submit():
        print(form.search.data)
        form.search.data = form.search.data.lower()
        if form.search.data in word_list:
            data = form.search.data
            return redirect(url_for('search_words_results'))
        else:
            flash('Not found', 'danger')
    return render_template('search_words.html', title='Word Search', words=word_list, form=form)

@app.route("/search_words_results", methods=["GET", "POST"])
def search_words_results():
    return render_template('search_words_results.html', title='Search Results', words=word_list, data=data)

global data

@app.route('/search_dates', methods=["GET", "POST"])
def search_dates():
    global data
    form = SearchForm()
    if form.validate_on_submit():
        print(form.search.data)
        form.search.data = form.search.data.lower()
        if form.search.data in date_list:
            data = form.search.data
            return redirect(url_for('search_dates_results'))
        else:
            flash('Not found', 'danger')
    return render_template('search_dates.html', title='Date Search', dates=date_list, form=form)

@app.route("/search_dates_results", methods=["GET", "POST"])
def search_dates_results():
    return render_template('search_dates_results.html', title='Search Results', dates=date_list, data=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


