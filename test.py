import requests
import json
import pandas as pd
from functions.sql import SqlConn
import os

def make_request(url, data, database="database.db"):
    headers = {
        'Content-Type': 'application/json'
    }
    data["databaseName"] = database
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


BASE_URL = "http://127.0.0.1:5000/"
DATABASE_NAME = "amazonDb"
sql = SqlConn(db_name=DATABASE_NAME)
print(json.dumps(sql.get_database_structure(), indent=4))
print("Number of tables:", len(sql.get_database_structure()["tables"]))
print("Tables:", sql.get_database_structure()["tables"].keys())


# questions = make_request(BASE_URL + "get-questions", {}, database=DATABASE_NAME)
# print("Questions:", questions)
# print("Number of questions:", len(questions))

# for i, question in enumerate(questions):
#     print(f"Question {i+1}: {question}")
#     query_response = make_request(BASE_URL + "request", {"query": questions[i]}, database=DATABASE_NAME)
#     print("Query Response:", query_response)
#     print("Number of rows:", len(query_response["result"]))

# print(make_request(BASE_URL + "request", {"query": "What degree causes the most depression?"}, database=DATABASE_NAME))