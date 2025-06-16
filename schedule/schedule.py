import mysql.connector
import random
from db_config import config
from db_operations import utils, inserts


def simple_reasoning(year, school_id):
    cnx = mysql.connector.connect(**config)

    version = 1  # default
    version_cursor = cnx.cursor()
    version_query = f"SELECT schedule_version FROM schedule WHERE id_school = {school_id} ORDER BY schedule_version LIMIT 1"
    version_cursor.execute(version_query)
    current_version = version_cursor.fetchone()
    version_cursor.close()
    if current_version:
        version = current_version[0] + 1

    # fetch assigned_sets table from choosen school
    # sorted by coures.hours_weekly in descending order
    set_cursor = cnx.cursor()
    fetch_assigned_sets_query = f"SELECT a.id, a.id_teacher, a.id_course, a.id_group, c.hours_weekly FROM assigned_sets a INNER JOIN teachers t ON a.id_teacher = t.id AND t.id_school={school_id} INNER JOIN courses c ON a.id_course = c.id ORDER BY c.hours_weekly DESC"
    set_cursor.execute(fetch_assigned_sets_query)
    sets = set_cursor.fetchall()
    set_cursor.close()

    classroom_cursor = cnx.cursor()
    classroom_query = (
        f"SELECT id, location FROM classrooms WHERE id_school = {school_id}"
    )
    classroom_cursor.execute(classroom_query)
    classrooms = classroom_cursor.fetchall()
    classroom_cursor.close()

    # timeframes are in range between 1 and 50
    # 10 per each day
    # ex. Monday has 1st, 6th, 11th, 16th, 21st, ... 46th timeframes
    # timeframe % 5 = day of the week. Friday is 0th day
    for assigned_set in sets:
        for timeframe in range(1, 51):
            for classroom in classrooms:
                # ignore error, if all of the weekly hours are disposed, proceed
                if assigned_set[4] <= 0:
                    print("course's weekly requirements are filled", assigned_set)
                    continue

                if not utils.check_privilege(
                    "classroom", classroom[0], assigned_set[2]
                ):
                    print(
                        "Classroom does not have this privilige",
                        classroom,
                        assigned_set,
                    )
                    continue
                if utils.check_booked_classroom(
                    (year, school_id, version, timeframe, classroom[0])
                ):
                    print(
                        "Classroom already booked in this timeframe",
                        classroom,
                        timeframe,
                    )
                    continue
                if utils.check_booked_set(
                    (year, school_id, version, timeframe, assigned_set[0])
                ):
                    print(
                        "Classroom already booked in this set",
                        assigned_set,
                        timeframe,
                    )
                    continue

                if utils.check_group(
                    (year, school_id, version, timeframe, assigned_set[3])
                ):
                    print(
                        "Group already booked in this timeframe",
                        assigned_set,
                        timeframe,
                    )
                    continue

                if utils.check_teacher(
                    (year, school_id, version, timeframe, assigned_set[1])
                ):
                    print(
                        "Teacher already booked in this timeframe",
                        assigned_set,
                        timeframe,
                    )
                    continue

                if inserts.create_timeframe(
                    year=year,
                    school_id=school_id,
                    version=version,
                    timeframe=timeframe,
                    assigned_set_id=assigned_set[0],
                    classroom_id=classroom[0],
                ):
                    print(
                        "sucessfully inserted a timeframe",
                        year,
                        school_id,
                        version,
                        timeframe,
                        assigned_set[0],
                        classroom[0],
                    )
                    list_set = list(assigned_set)
                    list_set[4] -= 1
                    assigned_set = tuple(list_set)

    cnx.close()


def random_sets(year, school_id):
    cnx = mysql.connector.connect(**config)

    version = 1  # default
    version_cursor = cnx.cursor()
    version_query = f"SELECT schedule_version FROM schedule WHERE id_school = {school_id} ORDER BY schedule_version LIMIT 1"
    version_cursor.execute(version_query)
    current_version = version_cursor.fetchone()
    version_cursor.close()
    if current_version:
        version = current_version[0] + 1

    set_cursor = cnx.cursor()
    fetch_assigned_sets_query = f"SELECT a.id, a.id_teacher, a.id_course, a.id_group, c.hours_weekly FROM assigned_sets a INNER JOIN teachers t ON a.id_teacher = t.id AND t.id_school={school_id} INNER JOIN courses c ON a.id_course = c.id"
    set_cursor.execute(fetch_assigned_sets_query)
    sets = set_cursor.fetchall()
    set_cursor.close()

    classroom_cursor = cnx.cursor()
    classroom_query = (
        f"SELECT id, location FROM classrooms WHERE id_school = {school_id}"
    )
    classroom_cursor.execute(classroom_query)
    classrooms = classroom_cursor.fetchall()
    classroom_cursor.close()

    while sets:
        for timeframe in range(1, 51):
            for classroom in classrooms:
                assigned_set = sets[random.randint(0, len(sets) - 1)]
                # ignore error, if all of the weekly hours are disposed, proceed
                if assigned_set[4] <= 0:
                    print("course's weekly requirements are filled", assigned_set)
                    sets.remove(assigned_set)
                    continue

                if not utils.check_privilege(
                    "classroom", classroom[0], assigned_set[2]
                ):
                    print(
                        "Classroom does not have this privilige",
                        classroom,
                        assigned_set,
                    )
                    continue
                if utils.check_booked_classroom(
                    (year, school_id, version, timeframe, classroom[0])
                ):
                    print(
                        "Classroom already booked in this timeframe",
                        classroom,
                        timeframe,
                    )
                    continue
                if utils.check_booked_set(
                    (year, school_id, version, timeframe, assigned_set[0])
                ):
                    print(
                        "Classroom already booked in this set",
                        assigned_set,
                        timeframe,
                    )
                    continue

                if utils.check_group(
                    (year, school_id, version, timeframe, assigned_set[3])
                ):
                    print(
                        "Group already booked in this timeframe",
                        assigned_set,
                        timeframe,
                    )
                    continue

                if utils.check_teacher(
                    (year, school_id, version, timeframe, assigned_set[1])
                ):
                    print(
                        "Teacher already booked in this timeframe",
                        assigned_set,
                        timeframe,
                    )
                    continue

                if inserts.create_timeframe(
                    year=year,
                    school_id=school_id,
                    version=version,
                    timeframe=timeframe,
                    assigned_set_id=assigned_set[0],
                    classroom_id=classroom[0],
                ):
                    print(
                        "sucessfully inserted a timeframe",
                        year,
                        school_id,
                        version,
                        timeframe,
                        assigned_set[0],
                        classroom[0],
                    )
                    list_set = list(assigned_set)
                    list_set[4] -= 1
                    assigned_set = tuple(list_set)
    cnx.close()


# or something else
def genetic(year, school_id, version):
    pass
