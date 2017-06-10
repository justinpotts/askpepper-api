import gensim
import argparse
import json
import pprint
import requests
import sys
import urllib
import string
import config
from stop_words import get_stop_words
from gensim import corpora, models
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

def return_words(doc):
    en_stop = get_stop_words('en')
    p_stemmer = str.maketrans('','',string.punctuation)
    doc_set = doc.split('.')
    texts = []

    for i in doc_set:
        raw = i.lower()
        tokens = raw.split(' ')
        stopped_tokens = [i for i in tokens if not i in en_stop]
        stemmed_tokens = [i.translate(p_stemmer) for i in stopped_tokens]
        texts.append(stemmed_tokens)

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=len(doc_set), id2word = dictionary, passes=30)
    topics = ldamodel.print_topics(num_topics=len(doc_set), num_words=3)

    words = set()

    for topic in topics:
        for word in topic[1].split(' + '):
            words.add(word.split('*')[1].strip('"'))

    print (' '.join(words))
    return ' '.join(words)


class Yelp:
    CLIENT_ID = config.yelp['CLIENT_ID']
    CLIENT_SECRET = config.yelp['CLIENT_SECRET']
    bearer_token = config.yelp['bearer_token']
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    GRANT_TYPE = 'client_credentials'
    BUSINESS_PATH = '/v3/businesses/'

    def request(self, host, path, bearer_token, url_params=None):
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % bearer_token,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)

        return response.json()


    def search(self, bearer_token, term, location):
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': 10,
            'categories': 'food,restaurants',
            'sort': 'rating'
        }
        return self.request(self.API_HOST, self.SEARCH_PATH, self.bearer_token, url_params=url_params)

    def get_business(self, bearer_token, business_id):
        business_path = self.BUSINESS_PATH + business_id

        return self.request(self.API_HOST, business_path, self.bearer_token)

    def get_results(self, query):
        response = self.search(self.bearer_token, query, 'McKinney Texas 75070')
        businesses = response.get('businesses')

        return businesses


if __name__ == '__main__':
    doc = input('What are you looking for? ')
    yelp_api = Yelp()
    return_words = return_words(doc)
    print(yelp_api.get_results(return_words))
