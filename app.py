from flask import Flask, abort, request, jsonify, g, url_for
from flask_cors import CORS
import lda

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)

@app.before_request
def before_request():
    if 'status' in request.endpoint:
        response = jsonify({'It works!':'Nothing to see here.'})
        response.status_code = 200
        return response
    #Kite app.py has mashape stuff here

@app.route('/')
def index():
    docs = {
        'name':'Pepper🌶',
        'description':'Tell Pepper what kind of restaurant you are looking for!'
        'endpoints': {
            'match':{
                'name':'/match',
                'description':'Checks your input and matches you with the best restaurants!'
                'method':'GET',
                'sample-input':'http://api.askpepperapp.com/match?phrase=I like italian food, and want a good date spot'
                'sample-output':'<sample>' #TODO: this.
            }
        }
    }
    return jsonify(docs)

@app.route('/status')
def status():
    return 'It works! Nothing to see here'

@app.route('/match', methods=['GET'])
def match():
    phrase = request.args.get('phrase')
    yelp_api = Yelp()
    return yelp_api.get_results(phrase)

if __name__ == '__main':
    app.run()
