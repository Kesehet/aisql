import sqlite3
import difflib
import yaml
import pandas as pd
import os

class SqlConn:
    base_path = './databases/'  # Set your desired base path
    def __init__(self, db_name="user001.starter.db" ):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        print("------Database path:", self.base_path , db_name)
        self.db_path = self.base_path + db_name

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # So we can get column names easily

    def execute(self, query, params=None):
        cur = self.conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        headers = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall()

        # Convert sqlite3.Row to list
        result_rows = [list(row) for row in rows]

        cur.close()
        return headers, result_rows


    def get_database_structure(self):
        cur = self.conn.cursor()

        # Get list of tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cur.fetchall()

        db_structure = {"database": self.db_path, "tables": {}}

        for table_row in tables:
            table_name = table_row[0]
            cur.execute(f"PRAGMA table_info('{table_name}')")
            columns = cur.fetchall()

            db_structure["tables"][table_name] = []
            for column in columns:
                column_info = {
                    "Field": column["name"],
                    "Type": column["type"],
                    "Null": "YES" if column["notnull"] == 0 else "NO",
                    "Key": "PRI" if column["pk"] else "",
                    "Default": column["dflt_value"],
                    "Extra": ""
                }
                db_structure["tables"][table_name].append(column_info)

        cur.close()
        return db_structure

    def find_table_and_column_by_keywords(self, keyword, sensitivity=0.8):
        if isinstance(keyword, str):
            keywords = [keyword]
        else:
            keywords = keyword

        sensitivity = max(0.0, min(1.0, float(sensitivity)))
        db_struct = self.get_database_structure()
        tables = db_struct['tables']

        matched_tables = {}

        for table_name, columns in tables.items():
            for column in columns:
                column_name = column['Field']
                for kw in keywords:
                    ratio = difflib.SequenceMatcher(None, kw.lower(), column_name.lower()).ratio()
                    if ratio >= sensitivity:
                        matched_tables[table_name] = [
                            col['Field'] + " (" + col['Type'] + ")" for col in columns
                        ]
                        break
                if table_name in matched_tables:
                    break

        return yaml.dump(matched_tables, sort_keys=False)



    def get_columns_for_table(self, table_name):
        db_struct = self.get_database_structure()
        tables = db_struct['tables']
        return tables.get(table_name, [])

    @classmethod
    def create_new_database(cls, csv_title, csv_string, db_name='user001.starter.db'):

        csv_title = csv_title.split('.')[0].lower().replace(' ', '_')

        # Ensure the base directory exists
        if not os.path.exists(cls.base_path):
            os.makedirs(cls.base_path)

        # Write the CSV to a temporary file
        csv_path = os.path.join(cls.base_path, csv_title + '.csv')
        with open(csv_path, 'w') as f:
            f.write(csv_string)

        # Read the CSV
        df = pd.read_csv(csv_path)

        # Create database and write table
        db_path = os.path.join(cls.base_path, db_name)
        conn = sqlite3.connect(db_path)
        df.to_sql(csv_title, conn, index=False, if_exists='replace')
        conn.close()

        # Remove the temporary CSV file
        os.remove(csv_path)

        # Return SqlConn object
        return cls(db_name=db_name)

