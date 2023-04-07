import sqlite3
import pandas as pd

class SqliteDb():
    def __init__(self):
        super().__init__()

    def connect(self, name):
        self.con = sqlite3.connect(name)
        self.cursor = self.con.cursor()
        return self.cursor

    def make_table(self, table):
        self.cursor.execute("CREATE TABLE "+ table + "(idx INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)")
    
    def drop_table(self, table):
        self.cursor.execute("DROP TABLE "+ table)

    def to_sql(self, table, df):
        df.to_sql(table, self.con)

    def exists_table(self, table):
        try :
            self.cursor.execute("SELECT * FROM " + table)
            return True
        except :
            return False

    def exists_table_column(self, table, coulumn) :
        try :
            self.cursor.execute("SELECT %s FROM %s "%(coulumn, table))
            return True
        except :
            return False

    def add_column(self, table, column_name_type) :
        # add_column(TABLE_NAME,'column_name float')
        sql = "ALTER TABLE %s ADD COLUMN %s" % (table, column_name_type)
        self.cursor.execute(sql)

    def insert_data(self, table, values):
        #insert_data(TABLE_NAME,"'2018-01-01',1000")
        sql = "INSERT INTO %s VALUES%s" % (table, values)
        self.cursor.execute(sql)

    def insert_data_with_cols(self, table, cols, values):
        #insert_data_with_cols("table_name","column_name1,column_name2","value1,value2")
        sql = "INSERT INTO %s%s VALUES%s" % (table, cols, values)
        self.cursor.execute(sql)

    def get_value(self, table, cols, condition):
        #value = get_value("table_name","colname","idx=value")
        sql = "SELECT %s FROM %s WHERE %s" % (cols, table, condition)
        cursor = self.cursor.execute(sql)
        row = cursor.fetchone()
        if row==None : return None
        if len(row)==0 : return None
        return row[0]
    
    def update_value(self, table, setvalue, condition):
        #update_value("table_name","colname=value","idx=value")
        sql = "UPDATE %s SET %s WHERE %s" % (table, setvalue, condition)
        self.cursor.execute(sql)

    def get_dataframe(self, table):
        df = pd.read_sql_query("SELECT * FROM %s" % table, self.con)
        return df

    def comm(self):
        self.con.commit()

    def close(self):
        self.con.commit()
        self.con.close()