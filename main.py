import mysql.connector
from db_config import config
from db_operations import inserts


# TODO: data creation
# TODO: basic schedule


def main():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "show columns from privileges_classrooms"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)
    inserts.grant_privilege_to_course("privileges_teachers", "teachers", 1, 1)

    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
