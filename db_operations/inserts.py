import mysql.connector
from db_config import config
from db_operations.utils import check_existance


def create_school(name):
    query = "INSERT INTO schools (name) VALUES (%s)"

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name,))  # needs to be a tuple
    cnx.commit()
    cursor.close()
    cnx.close()


def create_course(name, hours_weekly, level):
    query = "INSERT INTO courses (name, hours_weekly, level) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, hours_weekly, level))
    cnx.commit()
    cursor.close()
    cnx.close()


def create_teacher(name, surname, id_school):
    if not check_existance("schools", id_school):
        print(f"There is no such school: {id_school}. Could not create teacher")
        return

    query = "INSERT INTO teachers (name, surname, id_school) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, surname, id_school))
    cnx.commit()
    cursor.close()
    cnx.close()


def create_group(name, level, id_school):
    if not check_existance("schools", id_school):
        print(f"There is no such school: {id_school}. Could not create group")
        return

    query = "INSERT INTO groups (name, level, id_school) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, level, id_school))
    cnx.commit()
    cursor.close()
    cnx.close()


def grant_privilege_to_course(
    privilege_table, who_gets_privilege, privileged_id, course_id
):
    if not check_existance(who_gets_privilege, privileged_id):
        print(
            f"There is no such entry: {who_gets_privilege} - {privileged_id}. Could not grant privilege"
        )
        return
    if not check_existance("courses", course_id):
        print(f"There is no such course: {course_id}. Could not grant privilege")
        return

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    columns_query = f"SHOW COLUMNS FROM {privilege_table}"
    cursor.execute(columns_query)
    get_columns = cursor.fetchall()
    columns = []
    for Field, Type, Null, Key, Default, Extra in get_columns:
        columns.append(Field)

    query = f"INSERT INTO {privilege_table} ({columns[0]},{columns[1]}) VALUES (%s, %s)"

    cursor.execute(query, (privileged_id, course_id))

    cnx.commit()
    cursor.close()
    cnx.close()
