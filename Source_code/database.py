import sqlite3

class Dbase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connecter = None
        self.cursor = None

    def connect(self):
        self.connecter = sqlite3.connect(self.db_name)
        self.cursor = self.connecter.cursor()

    def close(self):
        if self.connecter:
            self.connecter.close()

    def commit(self):
        if self.connecter:
            self.connecter.commit()

    def get_tables(self):
        if self.connecter:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        else:
            print("## get_table Error: \n please connect with data base")

    def get_columns(self, table_name):
        if self.cursor:
            self.cursor.execute(f"PRAGMA table_info ({table_name})")
            columns = [column[1] for column in self.cursor.fetchall()]
            return columns
        else:
            print("## get_columns Error: \n please connect with data base")
    def get_columns_without_id(self, table_name):
        #geting tables spacily without ID column
        self.cursor.execute(f"PRAGMA table_info ({table_name})")
        cols = [c[1] for c in self.cursor.fetchall()]
        columns = []
        for col in cols:
            if col is not cols[0]:
                columns.append(col)
        return columns
    def get_data(self, table_name):
        if self.cursor:
            self.cursor.execute(f"SELECT * FROM {table_name};")
            data = self.cursor.fetchall()
            return data
        else:
            print("## get_data Error: \n please connect with data base")

    def create_table(self, table_name, columns):
        if self.connecter:
            values_text = "id INTEGER PRIMARY KEY AUTOINCREMENT "
            for key in columns:
                values_text += f", {key} {columns[key]}"
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({values_text});")
            self.commit()
        else:
             print("## create_table Error: \n please connect with data base")
            
    def inser(self, table_name, columns, data=[]):
        str_values = ""
        for d in data:
            str_values += "?, "
        str_values = str_values.rstrip(", ")

        str_columns = ""
        for column in columns:
            str_columns += f"{column}, "
        str_columns = str_columns.rstrip(", ")
        try:
            self.cursor.execute(f"INSERT INTO {table_name} ({str_columns}) VALUES ({str_values})", data)
            self.commit()
        except:
            print("error inserting data: ")
    def edit(self,table_name, id, new_data):
        columns = self.get_columns_without_id(table_name)
        set_clause = ", ".join([f"{col} = ?" for col in columns])
        pramter = new_data + [id]
        self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?",
                            pramter)
        self.commit()

    def delete(self,table_name, row_id):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (row_id,))
        self.commit()