from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello World!'})

if __name__ == '__main__':
    app.run(debug=True)
