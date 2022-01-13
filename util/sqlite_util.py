"""Collection of utility methods for more convenient access to sqlite"""

import os
import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(path):
    """Open a connection to an existing database or create a new one, if needed.
    :param path: the local path to the database
    :return: connection or None in case of error.
    """
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB %s (%s) successful" % (sqlite3.version, path))
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def read_query(connection, sql_query):
    """Execute a SQL query on the given connection.
    :param connection: the connection object
    :param sql_query: the SQL query.
    :return: a pandas dataframe.
    """
    df = pd.read_sql_query(sql_query, connection)
    return df


def execute_query(connection, query, commit = True):
    """Execute a query or other SQL-statement on the given connection.
    :param connection: the connection object
    :return: the cursor or None in case of error.
    """
    cursor = connection.cursor()    # Ein Cursor ist eine Hilfsdatenstruktur und zeigt 
                                    # auf das Resultat der Query oder des Update-Statements.
    try:
        cursor.execute(query)
        if commit:
            connection.commit()
        return cursor
    except Error as e:
        print(f"The error '{e}' occurred")
    return None


def get_connection_path(db_name):
    """Helper to create and return connection path for a given db_name in path './data'
    :param db_name: file name of the db, including the file ending, eg. '.sqlite' or '.db'"""
    directory = os.path.dirname('./data/')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, db_name)

def show_tables(connection):
    stmt = """SELECT 
        name
    FROM 
        sqlite_master 
    WHERE 
        type ='table' AND 
        name NOT LIKE 'sqlite_%';"""
    cur = execute_query(connection, stmt)
    row = cur.fetchall()
    return [r[0] for r in row]


def desc_table(connection, table_name):
    """Describe the content of a given table.
    :param table_name: name of the table to describe
    """
    stmt = f"SELECT sql FROM sqlite_master WHERE name = '{table_name}';"
    cur = execute_query(connection, stmt)
    row = cur.fetchone()
    return row[0] if row else None


def print_results(cur, max_num_of_rows=10):
    print([i[0] for i in cur.description]) # print headers
    rows = cur.fetchall()
    for i in range(min(len(rows), max_num_of_rows)):
        print(rows[i])
    