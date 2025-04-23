import json
import pandas as pd
from functions.sql import SqlConn
import logging
from difflib import SequenceMatcher
import re


def get_sql_database_structure(db_name='user001.starter.db'):
    sql = SqlConn(db_name)
    columns = sql.get_database_structure()

    return columns

def get_table_list_in_database(db_name='user001.starter.db'):
    sql = SqlConn(db_name)
    columns = sql.get_database_structure()

    return list(columns['tables'].keys())

def extract_keywords(text):
    '''
    Takes comma-separated values and returns a list of values after splitting by comma 
    and removing the trailing 's'.
    '''
    # sanitize input
    words = re.split(r'[^a-zA-Z0-9]+', text)

    # Remove any empty strings
    words = [word for word in words if word]
    text = ",".join(words)
    print("Input for extract_keywords:", text)
    if not text:
        return []
    text = text.lower().strip()
    if not text:
        return []
    # Normalize and split input text
    keywords = [word.strip().rstrip('s').lower() for word in text.split(',') if word.strip()]
    
    return keywords

def validate_keywords(keywords, sensitivity=0.8, db_name='user001.starter.db'):
    """
    Validates a list of keywords by checking if they roughly match table or column names.
    Filters out generic/common keywords and those that match too many tables.

    :param keywords: List of keywords to validate.
    :param sensitivity: Sensitivity threshold for fuzzy matching (0 to 1).
    :return: List of useful, valid keywords.
    """

    def is_match(keyword, target):
        return SequenceMatcher(None, keyword.lower(), target.lower()).ratio() >= sensitivity

    COMMON_WORDS = {
        "id", "name", "created_at", "updated_at", "deleted_at",
        "timestamp", "status", "type", "date", "user_id",
        "is_active", "enabled", "flag", "description"
    }

    db_structure = get_sql_database_structure(db_name)
    tables = db_structure.get("tables", {})

    valid_keywords = []

    for keyword in keywords:
        if keyword.lower() in COMMON_WORDS:
            continue  # Skip common/generic words

        match_count = 0
        for table_name, columns in tables.items():
            if is_match(keyword, table_name):
                match_count += 1
                continue
            for column in columns:
                if is_match(keyword, column["Field"]):
                    match_count += 1
                    break

            if match_count > int(len(tables) / 2):
                break  # Too many matches — likely a generic word

        if 0 < match_count <= 3:
            valid_keywords.append(keyword)

    return list(set(valid_keywords))


    
    

def find_table_and_column_by_keywords(keywords, sensitivity=0.8, db_name='user001.starter.db'):
    sql = SqlConn(db_name)
    return sql.find_table_and_column_by_keywords(keywords, sensitivity)


def get_sql_query(query, db_name='user001.starter.db'):
    print("Executing SQL Query: " + str(query))
    sql = SqlConn(db_name)
    return {"query": query, "result": sql.execute(query)}

def get_database_structure_as_context():
    db_structure = get_sql_database_structure()

    db_name = db_structure['database']
    tables_info = db_structure['tables']

    context_lines = [f"Database Name: {db_name}", "Tables and Columns:"]

    for table_name, columns in tables_info.items():
        context_lines.append(f"\nTable: {table_name}")
        for col in columns:
            field = col['Field']
            col_type = col['Type']
            nullable = col.get('Null', 'YES')
            key = col.get('Key', '')
            default = col.get('Default', 'None')
            extra = col.get('Extra', '')

            attributes = []

            if key == 'PRI':
                attributes.append('Primary Key')
            if key == 'UNI':
                attributes.append('Unique')
            if key == 'MUL':
                attributes.append('Foreign Key / Indexed')

            if nullable == 'NO':
                attributes.append('Not Null')

            if default != 'None':
                attributes.append(f"Default: {default}")

            if extra:
                attributes.append(extra)

            attributes_str = ", ".join(attributes)
            column_line = f"  - {field} ({col_type}) [{attributes_str}]" if attributes_str else f"  - {field} ({col_type})"

            context_lines.append(column_line)

    relationship_note = (
        "\nNote:\n"
        "- Tables containing columns marked 'Indexed' often reference primary keys of other tables.\n"
        "- Use indexed and primary key columns to join related tables appropriately in queries."
    )

    context_lines.append(relationship_note)

    prompt = "\n".join(context_lines)

    return [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "Understood."}
    ]

def get_questions(questions):
    print("Questions:", questions)
    if not questions:
        return []
    return questions.split("?")
    

get_sql_query_tool = {
  'type': 'function',
  'function': {
    'name': 'get_sql_query',
    'description': (
      'Generate a single valid SQL SELECT query to retrieve the desired information.\n\n'
      'This query will be used to generate a chart.js chart.\n\n'
      'Guidelines:\n'
      '- Only generate **SELECT** statements. No INSERT, UPDATE, DELETE, etc.\n'
      # '- Avoid Select * statements and use explicit column names or aliases.\n'
      '- The query must be complete and executable on its own. Avoid multi-statement or procedural SQL.\n'
      '- If using **aggregate functions** like COUNT, SUM, AVG, etc., always use an **alias** (e.g., COUNT(*) AS total_count).\n'
      '- You can use **nested subqueries**, but the final output must be a **single query**.\n'
      '- Avoid ambiguous column references — qualify column names with table aliases where appropriate.\n'
      '- Ensure all columns in SELECT, GROUP BY, and ORDER BY are valid and correctly referenced.\n'
      '- Always write clear, clean, and readable SQL — avoid overly complex or unnecessary clauses.\n'
      '- Always include **ORDER BY** clause with **ASC** or **DESC** keyword when possible. This helps ensure that results are sorted consistently across different databases and systems.'
    ),
    'parameters': {
      'type': 'object',
      'properties': {
        'query': {
          'type': 'string',
          'description': 'The finalized SQL SELECT query to be executed.',
        },
      },
      'required': ['query'],
    },
  },
}


extract_keywords_tool = {
  "type": "function",
  "function": {
    "name": "extract_keywords",
    "description": "Extracts as many relevant keywords as possible from a comma-separated string. Each keyword must be a single word without any whitespace or special characters.",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "A comma-separated list of potential keywords. Each keyword must be a single word (no spaces, no punctuation). Example: marketing,analytics,growth,performance"
        }
      },
      "required": ["text"]
    }
  }
}


find_table_and_column_by_keywords_tool = {
    'type': 'function',
    'function': {
        'name': 'find_table_and_column_by_keywords',
        'description': (
            'Searches across all available tables and columns to identify any that may be relevant '
            'to the provided keyword. The result includes table and column names in a comma-separated format. '
            'Ensure that the keyword is descriptive enough to produce meaningful matches.'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'keyword': {
                    'type': 'string',
                    'description': (
                        'A single keyword or phrase to search for in table or column names. '
                        'Avoid using overly broad or ambiguous terms. Must be a non-empty string.'
                    ),
                },
                'sensitivity': {
                    'type': 'number',
                    'description': (
                        'A float between 0 and 1 that determines the strictness of the match. '
                        'Higher values require closer matches (e.g., 0.9 = stricter, 0.5 = looser). '
                        'Defaults to 0.8. Values outside the 0–1 range will be rejected.'
                    ),
                    'default': 0.8,
                },
            },
            'required': ['keyword'],
        },
    },
}

get_questions_tool = {
    'type': 'function',
    'function': {
        'name': 'get_questions',
        'description': (
            'Extracts a list of broad, graph-oriented questions from a given string. '
            'The questions should be separated by question marks and should focus on exploring various aspects of the data, '
            'such as trends, comparisons, distributions, or relationships, rather than specific values.'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'questions': {
                    'type': 'string',
                    'description': (
                        'A string containing multiple broad questions separated by question marks. '
                        'Use technical terms and column names where appropriate. '
                        'These questions should aim to explore data comprehensively, such as "What are the trends in sales over time? "'
                        '"How do customer demographics compare across regions? What is the distribution of product categories? Why did my sales drop last month?" '
                    ),
                },
            },
            'required': ['questions'],
        },
    },
}