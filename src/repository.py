import sqlite3 as db


def create_base():
    with db.connect('db.sqlite3') as connection:
        cursor = connection.cursor()
        cursor.executescript("""CREATE TABLE IF NOT EXISTS parts (
                              id serial PRIMARY KEY,
                              part_type character varying(100),
                              mark character varying(100),
                              model character varying(100),
                              frame character varying(50),
                              engine character varying(50),
                              year character varying(4),
                              price double precision,
                              company character varying(100),
                              photo  character varying(100))""")


def add(parts):
    with db.connect('db.sqlite3') as connect:
        cursor = connect.cursor()
        cursor.executemany("""INSERT INTO parts(part_type, mark, model, frame, engine, year, price, company, photo) 
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           parts)
        connect.commit()
