# Standard imports
import ollama
from typing import Dict, Any, Callable
import json
import os
import random
import google.generativeai as genai

# internal imports
from functions.database import get_database_structure_as_context
from functions.database import get_sql_query, get_sql_query_tool
from functions.database import extract_keywords, extract_keywords_tool, validate_keywords, get_table_list_in_database
from functions.database import find_table_and_column_by_keywords, find_table_and_column_by_keywords_tool
from functions.database import get_questions_tool, get_questions
context = []
tools = [get_sql_query_tool]
available_functions: Dict[str, Callable] = {
    'extract_keywords': extract_keywords,
    'find_table_and_column_by_keywords': find_table_and_column_by_keywords,
    'get_sql_query': get_sql_query,
    'get_questions': get_questions
    }
def tool_call_to_dict(tool_call):
    """
    Convert a ToolCall object to a dictionary.
    """
    return {
        "function": {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments
        }
    }

def convert_ollama_tool_to_gemini(ollama_tool: dict) -> dict:
    if os.environ.get('USE_OLLAMA', 'False') == 'True':
        return ollama_tool
    if ollama_tool['type'] != 'function':
        raise ValueError("Only 'function' tools are supported.")
    
    gemini_tool = {
        "function_declarations": [
            {
                "name": ollama_tool['function']['name'],
                "description": ollama_tool['function']['description'],
                "parameters": ollama_tool['function']['parameters'],
            }
        ]
    }
    return gemini_tool


def get_response(prompt: str, use_tools: bool = True) -> Any:
    global context
    global tools
    global available_functions
    set_context(get_database_structure_as_context())
    context.append({'role': 'user', 'content': prompt})

    response = ollama.chat(
        'llama3.3:70b-instruct-q2_K',
        messages=context,
        tools=tools if use_tools else None,
    )

    returner = {
        "message": {
            "content": response.message.content,
        },
        "function": []
    }

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            try:
                if function_to_call := available_functions.get(tool.function.name):
                    print('Calling function:', tool.function.name)
                    print('Arguments:', tool.function.arguments)
                    output = function_to_call(**tool.function.arguments)
                    print('Function output:', output)
                    context.append({'role': 'tool', 'name': tool.function.name, 'content': str(output)})

                    returner["function"].append({
                        "name": tool.function.name,
                        "arguments": tool.function.arguments,
                        "output": output
                    })
                    print(response['message']['tool_calls'])
                else:
                   print('Function', tool.function.name, 'not found')
            except Exception as e:
                print('Error calling function:', e)
                context.append({'role': 'tool', 'name': tool.function.name, 'content': str(e)})
    else:
        context.append({'role': 'assistant', 'content': response.message.content})

    update_context()
    # returner["context"] = context

    return returner

def ask(context: list, tools: list, db_name: str = 'user001.starter.db') -> str:
    # Configure Gemini API
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

    # Prepare tools and context
    converted_tools = [convert_ollama_tool_to_gemini(tool) for tool in tools]
    gemini_context = convert_ollama_context_to_gemini(context)

    # Initialize model with tools
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        tools=converted_tools,
    )

    # Start chat session
    chat = model.start_chat(history=gemini_context)

    # Send latest user message
    user_message = gemini_context[-1]['parts'][0]['text']
    response = chat.send_message(user_message)

    # Handle tool calls if any
    if hasattr(response, 'candidates') and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call'):
                        function_call = part.function_call
                        func_name = function_call.name
                        if function_call.args:
                            args = dict(function_call.args)
                        else:
                            args = {}


                        function_to_call = available_functions.get(func_name)
                        if function_to_call:
                            if 'db_name' in function_to_call.__code__.co_varnames and 'db_name' not in args:
                                args['db_name'] = db_name
                            return function_to_call(**args)

    # No tool call was made; return normal model text
    return response.text

def add_to_context(context: list, role: str, content: str = '', file_name: str = 'context') -> list:
    context.append({'role': role, 'content': content})
    if not os.path.exists("context"):
        os.makedirs("context")
    with open( "context/"+file_name + '.json', 'w') as f:
        json.dump(context, f, indent=4)
    return context


def convert_ollama_context_to_gemini(context: list) -> list:
    role_mapping = {
        "user": "user",
        "assistant": "model",
        "tool": "model"
    }

    gemini_context = []
    for message in context:
        original_role = message.get("role", "user")
        mapped_role = role_mapping.get(original_role)

        if not mapped_role:
            print(f"Skipping unsupported role: {original_role}")
            continue
        
        content = message.get("content", "")
        if not content.strip():
            print(f"Skipping empty content for role: {original_role}")
            continue

        gemini_message = {
            "role": mapped_role,
            "parts": [{"text": content}]
        }
        gemini_context.append(gemini_message)

    return gemini_context





def random_string(length: int) -> str:
    import string
    import random
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_sql_query(prompt: str, context: list = None, db_name: str = 'user001.starter.db') -> str:
    '''
    Step 1: Extract keywords from the user's request.
    '''
    context = add_to_context([], 'user', f"""
    I need you to extract as many relevant keywords as possible from the following request:
    
    {prompt}
    
    Be very creative and thorough — don't just copy words directly. Think about synonyms, related terms, and different ways the same idea might be expressed. 
    Imagine all possible column names, table names, and SQL functions that could be relevant to this request.
    Return a comma-separated list of single-word keywords (no spaces), capturing the full scope of the request's meaning.
    """, file_name=random_string(10))

    context_file_name = ".".join([db_name, "sql", random_string(10),'json'])

    
    tables = get_table_list_in_database(db_name=db_name)
    sub_keywords = extract_keywords(prompt)

    if len(tables) <= 2:
        print('Tables were less than or equal to 2:', tables)
        raw_keywords = list(tables)
    else:
        raw_keywords = ask(context, [extract_keywords_tool], db_name=db_name)

    if type(raw_keywords) == str:
        raw_keywords = extract_keywords(raw_keywords)

    keywords = validate_keywords(sub_keywords + raw_keywords, db_name=db_name)
    context = add_to_context(context, 'assistant', f'Are these valid keywords? {", ".join(keywords)}.', file_name=context_file_name)

    # Step 2: Validate keywords with the user
    max_attempts = 3
    attempts = 0
    sensitivity = 0.8
    while len(keywords) == 0 and attempts < max_attempts:
        context = add_to_context(context, 'user', f'''
        None of the keywords were found in the database.
        Please confirm or provide the correct keywords for the prompt: 
        ```{prompt}```''', file_name=context_file_name)

        raw_keywords = ask(context, [extract_keywords_tool], db_name=db_name)
        keywords = validate_keywords(sub_keywords + raw_keywords,sensitivity=sensitivity/(attempts+1), db_name=db_name)
        print("Keywords finalized are ", keywords)
        context = add_to_context(context, 'assistant', f'Are these valid keywords? {", ".join(keywords)}.', file_name=context_file_name)
        attempts += 1

    if len(keywords) == 0:
        raise Exception('No valid keywords found.')

    print('Keywords:', keywords, sensitivity)
    context = add_to_context(context, 'user', f'Yes, {", ".join(keywords)} are valid.', file_name=context_file_name)


    

    '''
    Step 3: Identify relevant tables and columns using the confirmed keywords.
    '''
    table_and_column = find_table_and_column_by_keywords(keywords, sensitivity=sensitivity, db_name=db_name)
    print('Table and Column:', table_and_column, sensitivity)
    context = add_to_context(context, 'assistant', f'Table and Column: {table_and_column}', file_name=context_file_name)

    '''
    Step 4: Request generation and execution of the SQL query based on the original prompt.
    '''
    add_to_context(context, 'user', f'''
    Thanks. Can you prepare and run the SQL query for my original request?
    {prompt}
    ''', file_name=context_file_name)

    attempts = 0
    max_attempts = 3
    sql_query = None

    while attempts < max_attempts:
        try:
            sql_query = ask(context, [get_sql_query_tool], db_name=db_name)
            if sql_query and sql_query.get("query"):
                print('SQL Query:', sql_query.get("query"))
                context = add_to_context(context, 'assistant', f'SQL Query: {sql_query.get("query")}')
                break
        except Exception as e:
            print(f'Attempt {attempts + 1} failed with error: {e}')
            context = add_to_context(context, 'tool', f'Error: {e}', file_name=context_file_name)
            context = add_to_context(context, 'user', f'''
            Just a reminder of the original request: {prompt}
            Keywords: {keywords}
            Table and Column: {table_and_column}
            ''', file_name=context_file_name)
        attempts += 1

    if not sql_query or not sql_query.get("query"):
        raise Exception('Failed to generate SQL query after multiple attempts.')

    if os.path.exists("context/"+context_file_name):
        os.remove("context/"+context_file_name)
    return sql_query




def generate_questions(db_name):
    """
    Generate creative question ideas by combining tables two at a time.
    """
    context_file_name = ".".join([db_name, "question", random_string(19), "json"])
    print('Generating questions...', db_name)

    tables = get_table_list_in_database(db_name=db_name)
    if len(tables) < 2:
        print('Not enough tables to generate questions.')
        return []

    context = add_to_context([], 'user', '''
    Hey there, can you help me generate some ideas for questions I can ask about my database?
    ''', file_name=context_file_name)

    context = add_to_context(context, 'assistant', '''
    Sure! Share the tables and columns, and I’ll create some questions for you.
    ''', file_name=context_file_name)

    questions = []

    table_pairs = [(tables[i], tables[j]) for i in range(len(tables)) for j in range(i + 1, len(tables))]
    random.shuffle(table_pairs)

    for str_1, str_2 in table_pairs:
        keywords = extract_keywords(str_1) + extract_keywords(str_2)
        table_info = find_table_and_column_by_keywords(keywords, db_name=db_name, sensitivity=0.3)

        if not table_info:
            print(f'No relevant data for: {str_1}, {str_2}')
            continue

        context = add_to_context(context, 'user', f'''
        Please generate creative and insightful questions involving the following tables and columns:
        {table_info}
        Think of real-world scenarios where these tables might interact.
        ''', file_name=context_file_name)

        new_questions = ask(context, [get_questions_tool], db_name=db_name)

        if new_questions:
            questions.extend(new_questions)
            context = add_to_context(context, 'assistant', f'''
            Here are some generated questions:
            {new_questions}
            ''', file_name=context_file_name)
        break
    questions = list(set(questions))  # Remove duplicates
    questions = [question for question in questions if question.strip()]  # Remove empty strings

    return questions

def update_context():
    global context
    with open('context.json', 'w') as f:
        json.dump(context, f, indent=4)

def set_context(new_context):
    global context
    context = new_context



