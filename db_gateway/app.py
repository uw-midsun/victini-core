from flask import Flask, jsonify
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
import urllib, os
from sqlalchemy import text
from dotenv import load_dotenv
import pymysql
pymysql.install_as_MySQLdb()

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus(DATABASE_PASSWORD)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD_UPDATED +'@'+DATABASE_HOST+'/'+DATABASE_NAME
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello World!'})

@app.route('/health', methods=['GET'])
def test_db():
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({'message': 'Connection successful!'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'Connection_failed!'})

if __name__ == '__main__':
    app.run(debug=True)
