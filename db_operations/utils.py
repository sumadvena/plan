import mysql.connector
from db_config import config


def check_existance(table, index):
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


def check_privilege(table, who_check, id_check, course_id):
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
    query = f"SELECT * FROM {table} WHERE id_{who_check} = %s AND id_course = %s"
    cursor.execute(query, (id_check, course_id))
    privilege = cursor.fetchone()

    cursor.close()
    cnx.close()
    return True if privilege else False


def check_if_duplicate_set(teacher_id, course_id, group_id):
    if not check_existance("teachers", teacher_id):
        print(f"There is no such teacher: {teacher_id}. Could not create a set")
        return

    if not check_existance("courses", course_id):
        print(f"There is no such course: {course_id}. Could not create a set")
        return

    if not check_existance("group", group_id):
        print(f"There is no such group: {group_id}. Could not create a set")
        return

    query = "SELECT * FROM assigned_sets WHERE id_teacher = %s AND id_course = %s AND id_group = %s"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (teacher_id, course_id, group_id))
    is_duplicate = cursor.fetchone()

    cursor.close()
    cnx.close()
    return True if is_duplicate else False


def check_if_duplicate_timeframe(
    year, school_id, version, timeframe, assigned_set_id, classroom_id
):
    if not check_existance("schools", school_id):
        print(f"There is no such school: {school_id}. Could not create a timeframe")
        return

    if not check_existance("assigned_sets", assigned_set_id):
        print(f"There is no such set: {assigned_set_id}. Could not create a timeframe")
        return

    if not check_existance("classrooms", classroom_id):
        print(
            f"There is no such classroom: {classroom_id}. Could not create a timeframe"
        )
        return

    query = "SELECT * FROM schedule WHERE year = %s AND id_school = %s AND version = %s AND timeframe = %s AND id_assigned_set = %s AND id_classroom = %s"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(
        query, (year, school_id, version, timeframe, assigned_set_id, classroom_id)
    )
    is_duplicate = cursor.fetchone()

    cursor.close()
    cnx.close()
    return True if is_duplicate else False
