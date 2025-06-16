import mysql.connector
from db_config import config
from db_operations import inserts, utils
from schedule import populate, schedule, cost_functions


def main():
    schedule.simple_reasoning(year=2002, school_id=1)
    schedule.simple_reasoning(year=2002, school_id=2)
    schedule.random_sets(year=2004, school_id=1)
    schedule.random_sets(year=2004, school_id=2)
    cost_functions.worst_day(year=2002, version=1, id_school=1, id_teacher=66)
    cost_functions.mean_week(year=2002, version=1, id_school=1, id_teacher=66)


if __name__ == "__main__":
    main()
