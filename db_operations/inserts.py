import mysql.connector
from db_config import config
from db_operations import utils


def create_school(name):
    query = "INSERT INTO schools (name) VALUES (%s)"

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name,))  # needs to be a tuple
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def create_course(name, hours_weekly, level):
    query = "INSERT INTO courses (name, hours_weekly, level) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, hours_weekly, level))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def create_teacher(name, surname, school_id):
    if not utils.check_existance("schools", school_id):
        print(f"There is no such school: {school_id}. Could not create teacher")
        return False

    query = "INSERT INTO teachers (name, surname, id_school) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, surname, school_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def create_group(name, level, school_id):
    if not utils.check_existance("schools", school_id):
        print(f"There is no such school: {school_id}. Could not create group")
        return False

    query = "INSERT INTO groups (name, level, id_school) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, level, school_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def create_classrom(location, school_id):
    if not utils.check_existance("schools", school_id):
        print(f"There is no such school: {school_id}. Could not create group")
        return False

    query = "INSERT INTO groups (location, id_school) VALUES (%s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (location, school_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def grant_privilege_to_course(
    privilege_table, who_gets_privilege, privileged_id, course_id
):
    if not utils.check_existance(who_gets_privilege, privileged_id):
        print(
            f"There is no such entry: {who_gets_privilege} - {privileged_id}. Could not grant privilege"
        )
        return False
    if not utils.check_existance("courses", course_id):
        print(f"There is no such course: {course_id}. Could not grant privilege")
        return False

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
    return True


def create_assigned_set(teacher_id, course_id, group_id):
    if not utils.check_existance("teachers", teacher_id):
        print(f"There is no such teacher: {teacher_id}. Could not create a set")
        return False

    if not utils.check_existance("courses", course_id):
        print(f"There is no such course: {course_id}. Could not create a set")
        return False

    if not utils.check_existance("group", group_id):
        print(f"There is no such group: {group_id}. Could not create a set")
        return False
    if utils.check_if_duplicate_set(teacher_id, course_id, group_id):
        print(
            f"This set exists. teacher_id = {teacher_id}, course_id = {course_id}, group_id = {group_id}"
        )
        return False

    query = "INSERT INTO assigned_sets (id_teacher, id_course, id_group) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (teacher_id, course_id, group_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


# TODO:this below
def create_timeframe(
    year, school_id, version, timeframe, assigned_set_id, classroom_id
):
    if not utils.check_existance("schools", school_id):
        print(f"There is no such school: {school_id}. Could not create a timeframe")
        return False

    if not utils.check_existance("assigned_sets", assigned_set_id):
        print(f"There is no such set: {assigned_set_id}. Could not create a timeframe")
        return False

    if not utils.check_existance("classrooms", classroom_id):
        print(
            f"There is no such classroom: {classroom_id}. Could not create a timeframe"
        )
        return False

    if utils.check_if_duplicate_timeframe(
        year, school_id, version, timeframe, assigned_set_id, classroom_id
    ):
        print(
            f"This schedule already exists. year = {year}, school_id = {school_id}, version = {version}, timeframe =  {timeframe}, assigned_set_id = {assigned_set_id}, classroom_id = {classroom_id}"
        )
        return False

    query = "INSERT INTO schedule (year, school_id, version, timeframe, assigned_set_id, classroom_id) VALUES (%s, %s, %s, %s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(
        query, (year, school_id, version, timeframe, assigned_set_id, classroom_id)
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return True
