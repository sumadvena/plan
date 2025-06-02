import mysql.connector
from db_config import config


def check_existance(table: str, index: int):
    """
    Table is groups/teachers in plural form
    """

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


def find_id(table: str, fields: tuple):
    """
    Table is groups/teachers in plural form
    """

    query = "SELECT id FROM "
    match table:
        case "assigned_sets":
            query += "assigned_sets WHERE id_teacher = %s AND id_course = %s AND id_group = %s"
        case "classrooms":
            query += "classrooms WHERE location = %s AND id_school = %s"
        case "groups":
            query += "groups WHERE name = %s AND level = %s AND id_school = %s"
        case "schools":
            query += "schools WHERE name = %s"
        case "teachers":
            query += "teachers WHERE name = %s AND surname = %s AND id_school = %s"
        case "courses":
            query += "courses WHERE name = %s AND hours_weekly = %s AND level = %s"
        case "schedule":
            query += "schedule WHERE year = %s AND id_school = %s AND version = %s AND timeframe = %s AND id_assigned_set = %s AND id_classroom = %s"

    query += " LIMIT 1"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, fields)
    id = cursor.fetchone()
    cursor.close()
    cnx.close()
    return id[0] if id else False


def fetch_table(table):
    query = f"SELECT * FROM {table}"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query)
    table = cursor.fetchall()
    cursor.close()
    cnx.close()
    return table


def check_privilege(who_check: str, id_check: int, course_id: int):
    """
    who_check is group/teacher in singular form
    """
    if not check_existance(who_check + "s", id_check):
        print(
            f"There is no such entry: {who_check}s - {id_check}. Could not check for privilege"
        )
        return
    if not check_existance("courses", course_id):
        print(f"There is no such course: {course_id}. Could not check fot privilege")
        return

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"SELECT * FROM {who_check}s WHERE id_{who_check} = %s AND id_course = %s"
    cursor.execute(query, (id_check, course_id))
    privilege = cursor.fetchone()

    cursor.close()
    cnx.close()
    return True if privilege else False
