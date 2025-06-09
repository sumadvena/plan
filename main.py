import mysql.connector
from db_config import config
from db_operations import inserts, utils
from schedule import populate, schedule


# TODO: data creation
# TODO: basic schedule
# select t.name, t. surname, c.name, c.level from teachers t join privileges_teachers pt on (t.id=pt.id_teacher) join courses c on (pt.id_course=c.id);


def main():
    schedule.simple_reasoning(year=2002, school_id=1)
    schedule.simple_reasoning(year=2002, school_id=2)

    # populate.populate()


if __name__ == "__main__":
    main()
