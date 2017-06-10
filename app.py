from flask import Flask, abort, request, jsonify, g, url_for
from lda import Yelp, return_words

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def index():
    docs = {
        'name':'Pepper🌶',
        'description':'Tell Pepper what kind of restaurant you are looking for!',
        'endpoints': {
            'match':{
                'name':'/match',
                'description':'Checks your input and matches you with the best restaurants!',
                'method':'GET',
                'sample-input':'http://api.askpepperapp.com/match?phrase=I like italian food, and want a good date spot',
                'sample-output':'<sample>' #TODO: this.
            }
        }
    }
    return jsonify(docs)

@app.route('/match', methods=['GET'])
def match():
    phrase = request.args.get('phrase')
    yelp_api = Yelp()
    return jsonify(yelp_api.get_results(return_words(phrase)))

if __name__ == '__main__':
    app.run(debug=True)
