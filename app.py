import ast, json, datetime, random
from bson.objectid import ObjectId
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'university'
app.config['MONGO_URI'] = 'mongodb://<username>:<password>@ds117858.mlab.com:17858/university'

mongo = PyMongo(app)

app.json_encoder = JSONEncoder

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = ast.literal_eval(request.data.decode('utf-8'))
        new_quote = {}
        if data.get('quote'):
            new_quote['quote'] = data['quote']
            new_quote['quotee'] = data.get('quotee', '')
            new_quote['contributor'] = data.get('contributor', '')
            mongo.db.quotes.insert(new_quote)
            return jsonify({'status': 'Quote posted successfully!'})
        return jsonify({'status': 'Provide quote parameter!'})

    elif request.method == 'GET':
        quotes_cursor = mongo.db.quotes.find()
        quotes = []
        for quote in quotes_cursor:
            quotes.append(quote)
        quote = random.choice(quotes)
        del quote['_id']
        return jsonify(quote)
    
    else:
        return jsonify({'status': 'Method not allowed!'})

if __name__ == '__main__':
    app.run()