import sqlite3


def createDb():
    conn = sqlite3.connect("urlshorted.db")

    sql_create_table_types = '''CREATE TABLE IF NOT EXISTS "Types" (
	"id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
'''

    sql_create_table_users = '''CREATE TABLE IF NOT EXISTS "Users" (
	"id"	INTEGER,
	"login"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''

    sql_create_table_links = '''CREATE TABLE IF NOT EXISTS "Links" (
	"id"	INTEGER,
	"url"	TEXT NOT NULL,
	"short_url"	TEXT NOT NULL,
	"alias_url"	TEXT,
	"type_id"	INTEGER,
	"user_id"	INTEGER,
	FOREIGN KEY("type_id") REFERENCES "Types"("id"),
	FOREIGN KEY("user_id") REFERENCES "Users"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
)
'''

    c = conn.cursor()

    try:
        c.execute(sql_create_table_types)
        c.execute(sql_create_table_users)
        c.execute(sql_create_table_links)
    except Exception as e:
        print(e)
