import pymongo
from sqlalchemy import create_engine,text # use a version prior to 2.0.0 or adjust creating the engine and df.to_sql()
import psycopg2
import time
import logging
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


# mongo db definitions
client = pymongo.MongoClient('mongodb', port=27017)  # my_mongo is the hostname (= service in yml file)
cgt = client.my_cgt #change this to what your mongodb database is called
cgt_coll = cgt.my_collection #change this to whatever your collection in that db is called


# postgres db definitions. HEADS UP: outsource these credentials and don't push to github.
USERNAME_PG = 'postgres'
PASSWORD_PG = 'postgres'
HOST_PG = 'my_postgres'  # my_postgres is the hostname (= service in yml file)
PORT_PG = 5432
DATABASE_NAME_PG = 'reddits_pgdb'

conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"
time.sleep(3)  # safety margine to ensure running postgres server
pg = create_engine(conn_string_pg)


# Create the table
create_table_string = text("""CREATE TABLE IF NOT EXISTS reddits (
                                         time TEXT,
                                         reddit TEXT,
                                         sentiment NUMERIC
                                         );
                                      """)

with pg.connect() as conn:
     conn.execute(create_table_string)
#pg.execute(create_table_string)

def extract(limit=5):
    # We are loading only the last 5 entries for speed/debugging
    extracted_reddits = list(cgt_coll.find(limit = limit))
    logging.critical(f"\n---- {limit} reddits extracted ----\n")
    return extracted_reddits

def regex_clean(reddit):
    # Remove links from the reddit
#    reddit = re.sub(r'http\S+', '', reddit)
#    reddit = re.sub(r'www\S+', '', reddit)
#    return reddit
     pass


def sentiment_analysis(text):
#    s = SentimentIntensityAnalyzer()
#    sentiment_score = s.polarity_scores(text)
#    compound_score = sentiment_score['compound']
#    return compound_score
    return 1

#def sentiment_analysis(posts):
#    s  = SentimentIntensityAnalyzer()
#    for reddit in posts:
#            text =reddit['text']
#            # calculate sentiment
#            score = s.polarity_scores(text)
#            sentiment=score['compound']
#            #reddit.update({'sentiment': sentiment})
 #   return posts

    
def transform(extracted_reddits):
    transformed_reddits = []
    for post in extracted_reddits:
        #post=post['found_reddit']
        # optional just to see what is going on:
        #logging.critical(f"{post}")

        #here we select the 'text' key from the dictoinary
        text = post['text']

        #... clean it using the regex cleaning function (which currently does nothing)
        text = regex_clean(text)

        #...perform sentiment analysis (currently returns 1 for all text - yours will be different)
        sentiment = sentiment_analysis(text)

        #... add a field to the post dictionary called "sentiment" that contains this value
        post['sentiment'] = sentiment

        # ... and finally append the post to our list of transformed reddits
        transformed_reddits.append(post)

        # can also optionally add a logging statement
        #(-think about if you want this inside or outside the for-loop)
        logging.critical("\n---- new reddit post successfully transformed ----\n")

    return transformed_reddits
    

def load(transformed_reddits):
    for i in transformed_reddits:
        insert_query = "INSERT INTO reddits (time, reddit, sentiment) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
        pg.execute(insert_query, (i['time'], i['text'], i['sentiment']))
        logging.critical(f"New reddit post incoming: {i['text']} with sentiment score {i['sentiment']}")
        logging.critical("\n---- new reddit post loaded to postgres db ----\n")
    return None

if __name__ == '__main__':
    while True:
        extracted_reddits = extract()
        transformed_reddits = transform(extracted_reddits)
        load(transformed_reddits)
        logging.critical("ETL job finished")
        time.sleep(120)

