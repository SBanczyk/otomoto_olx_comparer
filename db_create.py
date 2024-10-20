import sqlite3

db_name = "sql.db"
sqliteConnection = sqlite3.connect(db_name)
table = """ CREATE TABLE if not exists test (
            manufacturer char(255),
            model char(255),
            production_year char(4)
            engine_type char(10)
        ); """
sqliteConnection.cursor().execute(table)
