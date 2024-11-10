import sqlite3

con = sqlite3.connect('database.db')

with open('database.sql','r') as file:
    dbsetup = file.read()

con.executescript(dbsetup)

con.close()