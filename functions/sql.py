import mariadb
import difflib
import yaml

class SqlConn:
    def __init__(self, host='localhost', user='root', password='', database='archisty'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )

    def execute(self, query, params=None):
        cur = self.conn.cursor()
        cur.execute(query, params)
        headers = [desc[0] for desc in cur.description] if cur.description else []
        res = cur.fetchall()
        cur.close()
        return headers, res

    def get_database_structure(self):
        cur = self.conn.cursor()
        
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        
        db_structure = {"database": self.database, "tables": {}}
        
        for table in tables:
            table_name = table[0]
            cur.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cur.fetchall()
            
            db_structure["tables"][table_name] = []
            for column in columns:
                column_info = {
                    "Field": column[0],
                    "Type": column[1],
                    "Null": column[2],
                    "Key": column[3],
                    "Default": column[4],
                    "Extra": column[5]
                }
                db_structure["tables"][table_name].append(column_info)
        
        cur.close()
        return db_structure




    def find_table_and_column_by_keywords(self, keyword, sensitivity=0.8):
        """
        Finds and returns YAML of tables containing columns that match any of the keywords
        based on sensitivity. All columns of matched tables are returned with types.

        :param keyword: String or list of strings to search for.
        :param sensitivity: Float between 0 and 1; higher means stricter match.
        :return: YAML string of tables and their columns with types.
        """
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
                        break  # One match is enough for this table
                if table_name in matched_tables:
                    break  # Stop checking columns if table is already matched

        return yaml.dump(matched_tables, sort_keys=False)
    
    def get_columns_for_table(self, table_name):
        db_struct = self.get_database_structure()
        tables = db_struct['tables']
        columns = tables.get(table_name, [])
        return columns
