import traceback
from flask import Flask, request, jsonify, render_template, send_from_directory
from functions.run import get_sql_query, context
from functions.sql import SqlConn
from functions.database import get_sql_query as sql_run
# enable CORS
from flask_cors import CORS
import dotenv
import os
from waitress import serve

dotenv.load_dotenv()

app = Flask(__name__, static_folder='build', template_folder='build')

CORS(app)

FAKE_CHARTS = os.getenv("FAKE_CHARTS") == "true" or os.getenv("FAKE_CHARTS") == "1" or os.getenv("FAKE_CHARTS") == "True"
DEBUG = os.getenv("DEBUG") == "true" or os.getenv("DEBUG") == "1" or os.getenv("DEBUG") == "True"

# Serve static files and fallback to index.html for React-style routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')  # just serve the file


query_cache = {}

@app.route('/request', methods=['POST'])
def process_request():
    global query_cache
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        data = request.get_json()
    if FAKE_CHARTS:
        return {
            "query": "SELECT column1, column2, column3 FROM table1",
            "result": [
                    [
                        "id",
                        "rating",
                        "review",
                        "name",
                        "email",
                        "city",
                        "user_id",
                        "product_id",
                        "created_at",
                        "updated_at"
                    ],
                    [
                        [
                            1,
                            72,
                            "Consequatur quo amet sint dolor hic veniam veniam.",
                            "Earum quibusdam cupiditate culpa et ea.",
                            "Amet enim ut commodi consequuntur tempora.",
                            "Asperiores qui dignissimos quo id.",
                            1,
                            156,
                            "null",
                            "null"
                        ],
                        [
                            2,
                            61,
                            "Quis labore sit eveniet veniam natus hic.",
                            "Nemo labore sint numquam autem.",
                            "In id facilis omnis minima et.",
                            "Mollitia sint rerum sit voluptas dolore libero.",
                            1,
                            38,
                            "null",
                            "null"
                        ],
                        [
                            3,
                            25,
                            "Ut dolorem iure consequatur aut.",
                            "Quia cupiditate labore dicta et sint voluptas doloremque.",
                            "Ducimus impedit rerum nihil quo sequi numquam.",
                            "Nihil ipsum neque vero veniam nostrum consequatur.",
                            1,
                            103,
                            "null",
                            "null"
                        ],
                        [
                            4,
                            62,
                            "Mollitia nobis nam recusandae.",
                            "Facere cupiditate eius eveniet magnam ducimus qui quo rerum.",
                            "Expedita qui eos ea adipisci deleniti molestias perspiciatis et.",
                            "Aut eveniet reprehenderit harum est sit.",
                            1,
                            41,
                            "null",
                            "null"
                        ]
                    ]
                ]
        }
    query = data['query']
    if query in query_cache:
        return query_cache[query]
    else:
        print("User Query:", query)
        response = get_sql_query(query, db_name=data['databaseName'])
        query_cache[query] = response
        return response

@app.route("/run-sql", methods=['POST'])
def run_sql():
    data = request.get_json()
    return sql_run(data["query"],data["databaseName"])

@app.route('/create-database', methods=['POST'])
def create_database():
    try:
        data = request.get_json()

        if not all(k in data for k in ('csv_title', 'csv_string', 'db_name')):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        csv_title = data['csv_title']
        csv_string = data['csv_string']
        db_name = data['db_name']

        conn = SqlConn.create_new_database(csv_title, csv_string, db_name)
        columns = conn.get_database_structure()

        return jsonify({'status': 'success', 'database': conn.db_path, 'table': csv_title, 'columns': columns})

    except Exception as e:
        return jsonify({'status': 'error', 'traceback': traceback.format_exc() }), 500


print("curl -X POST -H 'Content-Type: application/json' -d '{\"csv_title\":\"test\",\"csv_string\":\"col1,col2\\nval1,val2\",\"db_name\":\"test.db\"}' http://localhost:5000/create-database")
   

@app.route('/test.html')
def test():
    with open('test_results.html', 'r') as f:
        html = f.read()
    return html



if __name__ == '__main__':
    if not DEBUG:
        serve(app, port=5000)
    else:
        app.run(debug=DEBUG, port=5000, host='0.0.0.0')

