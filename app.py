from flask import Flask, request, jsonify, render_template, send_from_directory
from functions.run import get_sql_query, context
# enable CORS
from flask_cors import CORS
import dotenv
import os

dotenv.load_dotenv()






app = Flask(__name__, static_folder='build', template_folder='build')

CORS(app)

# Serve static files and fallback to index.html for React-style routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template('index.html')  # React entry point

@app.route('/request', methods=['POST'])
def process_request():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        data = request.get_json()
    
    return {
        "query": data['query'],
        "result": [
            ["column1", "column2", "column3"],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        ]
    }
    print("User Query:",data['query'])
    response = get_sql_query(data['query'])
    return response

@app.route('/context-clear')
def clear_context():
    global context
    context = []
    return 'Context cleared'

@app.route('/test.html')
def test():
    with open('test_results.html', 'r') as f:
        html = f.read()
    return html


@app.route('/context/update', methods=['POST'])
def update_context():
    global context
    data = request.get_json()
    context = data['context']
    return jsonify(context)

if __name__ == '__main__':
    app.run(debug=True)
