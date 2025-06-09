import mysql.connector
from db_config import config
from db_operations import utils


def create_school(name):
    if utils.check_existance("schools", utils.find_id("schools", (name,))):
        print(f"school {name} already exists")
        return False

    query = "INSERT INTO schools (name) VALUES (%s)"

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name,))  # needs to be a tuple
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def create_course(name, hours_weekly, level):
    if utils.check_existance(
        "courses", utils.find_id("courses", (name, hours_weekly, level))
    ):
        print(f"course {name} {hours_weekly} {level} already exists")
        return False

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

    if utils.check_existance(
        "teachers", utils.find_id("teachers", (name, surname, school_id))
    ):
        print(f"teacher {name} {surname} {school_id} already exists")
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

    if utils.check_existance(
        "groups", utils.find_id("groups", (name, level, school_id))
    ):
        print(f"group {name} {level} {school_id} already exists")
        return False

    query = "INSERT INTO groups (name, level, id_school) VALUES (%s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (name, level, school_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def create_classroom(location, school_id):
    if not utils.check_existance("schools", school_id):
        print(f"There is no such school: {school_id}. Could not create group")
        return False

    if utils.check_existance(
        "classrooms", utils.find_id("classrooms", (location, school_id))
    ):
        print(f"classroom {location} {school_id} already exists")
        return False

    query = "INSERT INTO classrooms (location, id_school) VALUES (%s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, (location, school_id))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def grant_privilege_to_course(
    who_gets_privilege: str, privileged_id: int, course_id: int
):
    if not utils.check_existance(who_gets_privilege + "s", privileged_id):
        print(
            f"There is no such entry: {who_gets_privilege}s - {privileged_id}. Could not grant privilege"
        )
        return False

    if not utils.check_existance("courses", course_id):
        print(f"There is no such course: {course_id}. Could not grant privilege")
        return False

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"INSERT INTO privileges_{who_gets_privilege}s (id_{who_gets_privilege}, id_course) VALUES (%s, %s)"

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

    if not utils.check_existance("groups", group_id):
        print(f"There is no such group: {group_id}. Could not create a set")
        return False

    if utils.check_existance(
        "assigned_sets",
        utils.find_id("assigned_sets", (teacher_id, course_id, group_id)),
    ):
        print(f"assigned_set {teacher_id} {course_id} {group_id} already exists")
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

    if utils.check_existance(
        "schedule",
        utils.find_id(
            "schedule",
            (year, school_id, version, timeframe, assigned_set_id, classroom_id),
        ),
    ):
        print(
            f"schedule {year} {school_id} {version} {timeframe} {assigned_set_id} {classroom_id} already exists"
        )
        return False

    query = "INSERT INTO schedule (year, id_school, schedule_version, timeframe, id_assigned_set, id_classroom) VALUES (%s, %s, %s, %s, %s, %s)"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(
        query, (year, school_id, version, timeframe, assigned_set_id, classroom_id)
    )
    cnx.commit()
    cursor.close()
    cnx.close()
    return True
