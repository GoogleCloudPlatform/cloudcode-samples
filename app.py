from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)
engine = create_engine('sqlite:///my_database.db')

@app.route('/query', methods=['GET'])
def query_database():
    query = request.args.get('q')
    df = pd.read_sql('documents', engine)
    results = df[df['content'].str.contains(query, na=False)]
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)