import mysql.connector
from db_config import config
from db_operations import utils, inserts


def simple_reasoning(year, school_id, version):
    courses = utils.fetch_table("courses")
    teachers = utils.fetch_table("teachers")
    groups = utils.fetch_table("groups")
    classrooms = utils.fetch_table("classrooms")
    print(courses, teachers, groups, classrooms)
    pass


def random(year, school_id, version):
    pass


# or something else
def genetic(year, school_id, version):
    pass
