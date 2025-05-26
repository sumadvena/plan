import mysql.connector
from db_config import config


def check_existance(table, index):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"select id from {table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for (id,) in rows:
        if index == id:
            cursor.close()
            cnx.close()
            return True
    cursor.close()
    cnx.close()
    return False
