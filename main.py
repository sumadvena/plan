import mysql.connector
from db_config import config
from db_operations import inserts, utils
from schedule import populate, schedule


# TODO: data creation
# TODO: basic schedule
# select t.name, t. surname, c.name, c.level from teachers t join privileges_teachers pt on (t.id=pt.id_teacher) join courses c on (pt.id_course=c.id);


def main():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "show columns from privileges_classrooms"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)
    schedule.simple_reasoning(2002, 1, 1)

    cursor.close()
    cnx.close()
    populate.populate()


if __name__ == "__main__":
    main()
