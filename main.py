import mysql.connector
from db_config import config
from db_operations import inserts


# TODO: data creation
# TODO: basic schedule


def main():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "select id from schools"
    cursor.execute(query)
    rows = cursor.fetchall()
    inserts.create_teacher("a", "b", 123)
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
