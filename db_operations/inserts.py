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
