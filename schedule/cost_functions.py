import mysql.connector
from db_config import config
from db_operations import utils, inserts


def worst_day(
    year=None,
    version=None,
    id_school=None,
    id_teacher=None,
    id_group=None,
    id_classroom=None,
):
    """year and version and id_school are obligatory"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"SELECT sch.timeframe FROM schedule AS sch INNER JOIN assigned_sets AS a ON a.id = sch.id_assigned_set WHERE sch.year = {year} AND sch.id_school = {id_school} AND sch.schedule_version = {version} "

    if id_teacher:
        query += f"AND a.id_teacher = {id_teacher} "
    if id_group:
        query += f"AND a.id_group = {id_group} "
    if id_classroom:
        query += f"AND a.id_classroom = {id_classroom} "

    cursor.execute(query)
    timeframes = cursor.fetchall()

    week = dict(Monday=0, Tuesday=0, Wednesday=0, Thursday=0, Friday=0)
    for t in timeframes:
        day = t[0] % 5
        match day:
            case 1:
                week["Monday"] += 1
            case 2:
                week["Tuesday"] += 1
            case 3:
                week["Wednesday"] += 1
            case 4:
                week["Thursday"] += 1
            case 0:
                week["Friday"] += 1
    worse_day = max(week, key=week.get)
    print("The most overwhelming day is", worse_day, week[worse_day])
    return week[worse_day]


def mean_week(
    year=None,
    version=None,
    id_school=None,
    id_teacher=None,
    id_group=None,
    id_classroom=None,
):
    """year and version and id_school are obligatory"""
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = f"SELECT sch.timeframe FROM schedule AS sch INNER JOIN assigned_sets AS a ON a.id = sch.id_assigned_set WHERE sch.year = {year} AND sch.id_school = {id_school} AND sch.schedule_version = {version} "

    if id_teacher:
        query += f"AND a.id_teacher = {id_teacher} "
    if id_group:
        query += f"AND a.id_group = {id_group} "
    if id_classroom:
        query += f"AND a.id_classroom = {id_classroom} "

    cursor.execute(query)
    timeframes = cursor.fetchall()

    week = dict(Monday=0, Tuesday=0, Wednesday=0, Thursday=0, Friday=0)
    for t in timeframes:
        day = t[0] % 5
        match day:
            case 1:
                week["Monday"] += 1
            case 2:
                week["Tuesday"] += 1
            case 3:
                week["Wednesday"] += 1
            case 4:
                week["Thursday"] += 1
            case 0:
                week["Friday"] += 1
    mean = sum(week.values()) / 5
    print("The mean of the ends of classes is", mean)
    return mean
