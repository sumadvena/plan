from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import traceback

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"
CORS(app)

# Prosta konfiguracja bazy danych
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "plan",
    "password": "lekcji",
    "database": "plan_lekcji",
    "raise_on_warnings": True,
    "charset": "utf8mb4",
}


def get_db_connection():
    """Utwórz połączenie z bazą danych"""
    try:
        return mysql.connector.connect(**DATABASE_CONFIG)
    except Exception as e:
        print(f"Błąd połączenia z bazą: {e}")
        return None


@app.route("/")
def index():
    """Strona główna"""
    return render_template("index.html")


@app.route("/api/schools")
def get_schools():
    """Pobierz listę szkół"""
    try:
        cnx = get_db_connection()
        if not cnx:
            return jsonify({"error": "Błąd połączenia z bazą danych"}), 500

        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM schools ORDER BY name")
        schools = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify(schools)
    except Exception as e:
        print(f"Błąd pobierania szkół: {e}")
        return jsonify({"error": "Błąd pobierania szkół"}), 500


@app.route("/api/groups")
@app.route("/api/groups/<int:school_id>")
def get_groups(school_id=None):
    """Pobierz listę grup/klas"""
    try:
        cnx = get_db_connection()
        if not cnx:
            return jsonify({"error": "Błąd połączenia z bazą danych"}), 500

        cursor = cnx.cursor(dictionary=True)

        if school_id:
            cursor.execute(
                """
                SELECT g.id, g.name, g.level, g.id_school, s.name as school_name
                FROM groups g 
                JOIN schools s ON g.id_school = s.id
                WHERE g.id_school = %s 
                ORDER BY g.level, g.name
            """,
                (school_id,),
            )
        else:
            cursor.execute("""
                SELECT g.id, g.name, g.level, g.id_school, s.name as school_name
                FROM groups g 
                JOIN schools s ON g.id_school = s.id
                ORDER BY s.name, g.level, g.name
            """)

        groups = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify(groups)
    except Exception as e:
        print(f"Błąd pobierania grup: {e}")
        return jsonify({"error": "Błąd pobierania grup"}), 500


@app.route("/api/teachers")
@app.route("/api/teachers/<int:school_id>")
def get_teachers(school_id=None):
    """Pobierz listę nauczycieli"""
    try:
        cnx = get_db_connection()
        if not cnx:
            return jsonify({"error": "Błąd połączenia z bazą danych"}), 500

        cursor = cnx.cursor(dictionary=True)

        if school_id:
            cursor.execute(
                """
                SELECT t.id, t.name, t.surname, t.id_school, s.name as school_name
                FROM teachers t 
                JOIN schools s ON t.id_school = s.id
                WHERE t.id_school = %s 
                ORDER BY t.surname, t.name
            """,
                (school_id,),
            )
        else:
            cursor.execute("""
                SELECT t.id, t.name, t.surname, t.id_school, s.name as school_name
                FROM teachers t 
                JOIN schools s ON t.id_school = s.id
                ORDER BY s.name, t.surname, t.name
            """)

        teachers = cursor.fetchall()
        cursor.close()
        cnx.close()

        return jsonify(teachers)
    except Exception as e:
        print(f"Błąd pobierania nauczycieli: {e}")
        return jsonify({"error": "Błąd pobierania nauczycieli"}), 500


@app.route("/api/years")
def get_years():
    """Pobierz dostępne lata"""
    try:
        cnx = get_db_connection()
        if not cnx:
            return jsonify({"error": "Błąd połączenia z bazą danych"}), 500

        cursor = cnx.cursor()
        cursor.execute("SELECT DISTINCT year FROM schedule ORDER BY year DESC")
        years = [row[0] for row in cursor.fetchall()]
        cursor.close()
        cnx.close()

        # Jeśli brak lat w bazie, dodaj domyślne lata
        if not years:
            years = [2024, 2025]

        return jsonify(years)
    except Exception as e:
        print(f"Błąd pobierania lat: {e}")
        return jsonify([2024, 2025])  # Fallback


@app.route("/api/schedule")
def get_schedule():
    """Pobierz plan zajęć z opcjonalnymi filtrami (wielokrotny wybór)"""
    try:
        # Pobierz parametry jako listy (mogą być wielokrotne)
        school_ids = request.args.getlist("school_id")
        group_ids = request.args.getlist("group_id")
        teacher_ids = request.args.getlist("teacher_id")
        years = request.args.getlist("year")

        # Konwertuj na int i usuń puste wartości
        school_ids = [int(x) for x in school_ids if x and x.isdigit()]
        group_ids = [int(x) for x in group_ids if x and x.isdigit()]
        teacher_ids = [int(x) for x in teacher_ids if x and x.isdigit()]
        years = [int(x) for x in years if x and x.isdigit()]

        print(
            f"Received filters - Schools: {school_ids}, Groups: {group_ids}, Teachers: {teacher_ids}, Years: {years}"
        )

        cnx = get_db_connection()
        if not cnx:
            return jsonify({"error": "Błąd połączenia z bazą danych"}), 500

        cursor = cnx.cursor(dictionary=True)

        # Bazowe zapytanie
        query = """
            SELECT 
                sch.timeframe,
                sch.year,
                s.name as school_name,
                s.id as school_id,
                g.name as group_name,
                g.id as group_id,
                g.level as group_level,
                c.name as course_name,
                CONCAT(t.name, ' ', t.surname) as teacher_name,
                t.id as teacher_id,
                cl.location as classroom_location,
                cl.id as classroom_id
            FROM schedule sch
            JOIN schools s ON sch.id_school = s.id
            JOIN assigned_sets aset ON sch.id_assigned_set = aset.id
            JOIN groups g ON aset.id_group = g.id
            JOIN teachers t ON aset.id_teacher = t.id
            JOIN courses c ON aset.id_course = c.id
            JOIN classrooms cl ON sch.id_classroom = cl.id
            WHERE 1=1
        """

        params = []

        # Dodaj warunki dla multiple selection
        if school_ids:
            placeholders = ",".join(["%s"] * len(school_ids))
            query += f" AND s.id IN ({placeholders})"
            params.extend(school_ids)

        if group_ids:
            placeholders = ",".join(["%s"] * len(group_ids))
            query += f" AND g.id IN ({placeholders})"
            params.extend(group_ids)

        if teacher_ids:
            placeholders = ",".join(["%s"] * len(teacher_ids))
            query += f" AND t.id IN ({placeholders})"
            params.extend(teacher_ids)

        if years:
            placeholders = ",".join(["%s"] * len(years))
            query += f" AND sch.year IN ({placeholders})"
            params.extend(years)

        query += " ORDER BY s.name, g.name, sch.timeframe"

        print(f"Executing query: {query}")
        print(f"With params: {params}")

        cursor.execute(query, params)
        raw_schedule = cursor.fetchall()
        cursor.close()
        cnx.close()

        print(f"Found {len(raw_schedule)} schedule entries")

        # ZAWSZE pokazuj wspólny plan (jak widok ogólny)
        # Niezależnie od tego co jest wybrane
        formatted_schedule = format_schedule_data_unified(
            raw_schedule, school_ids, group_ids, teacher_ids, years
        )

        return jsonify(formatted_schedule)

    except Exception as e:
        print(f"Błąd pobierania planu: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Błąd pobierania planu"}), 500


def format_schedule_data_unified(
    raw_data, school_ids=[], group_ids=[], teacher_ids=[], years=[]
):
    """Formatuj dane planu - ZAWSZE jako wspólny plan"""
    schedule = {}

    # Mapowanie timeframe na dni i godziny
    days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
    times = [
        "8:00-8:45",
        "8:55-9:40",
        "9:50-10:35",
        "10:45-11:30",
        "11:40-12:25",
        "12:35-13:20",
        "13:30-14:15",
        "14:25-15:10",
        "15:20-16:05",
        "16:15-17:00",
    ]

    if not raw_data:
        return schedule

    # Utwórz tytuł na podstawie filtrów
    title_parts = []

    if school_ids:
        if len(school_ids) == 1:
            school_name = next(
                (
                    item["school_name"]
                    for item in raw_data
                    if item["school_id"] == school_ids[0]
                ),
                f"Szkoła {school_ids[0]}",
            )
            title_parts.append(school_name)
        else:
            title_parts.append(f"{len(school_ids)} szkół")
    else:
        title_parts.append("Wszystkie szkoły")

    if group_ids:
        if len(group_ids) == 1:
            group_name = next(
                (
                    item["group_name"]
                    for item in raw_data
                    if item["group_id"] == group_ids[0]
                ),
                f"Klasa {group_ids[0]}",
            )
            title_parts.append(f"Klasa {group_name}")
        else:
            title_parts.append(f"{len(group_ids)} klas")

    if teacher_ids:
        if len(teacher_ids) == 1:
            teacher_name = next(
                (
                    item["teacher_name"]
                    for item in raw_data
                    if item["teacher_id"] == teacher_ids[0]
                ),
                f"Nauczyciel {teacher_ids[0]}",
            )
            title_parts.append(teacher_name)
        else:
            title_parts.append(f"{len(teacher_ids)} nauczycieli")

    if years:
        if len(years) == 1:
            title_parts.append(f"Rok {years[0]}")
        else:
            title_parts.append(f"{len(years)} lat")

    # Jeśli nie ma żadnych filtrów, grupuj po latach
    if not any([school_ids, group_ids, teacher_ids, years]):
        # Grupuj po latach
        years_data = {}
        for item in raw_data:
            year = item.get("year", "Nieznany rok")
            if year not in years_data:
                years_data[year] = []
            years_data[year].append(item)

        for year, year_items in years_data.items():
            year_key = f"Rok {year} - Wszystkie zajęcia"
            schedule[year_key] = create_unified_schedule(
                year_items,
                f"Wszystkie klasy - Rok {year}",
                "Wszystkie szkoły",
                times,
                days,
            )
    else:
        # Jeden wspólny plan dla wszystkich wybranych filtrów
        main_title = " - ".join(title_parts)
        schedule[main_title] = create_unified_schedule(
            raw_data,
            main_title,
            title_parts[0] if title_parts else "Plan zajęć",
            times,
            days,
        )

    return schedule


def create_unified_schedule(items, group_name, school_name, times, days):
    """Utwórz wspólną strukturę planu"""
    unified_schedule = {
        "school_name": school_name,
        "school_id": items[0]["school_id"] if items else None,
        "group_name": group_name,
        "group_id": None,
        "year": items[0]["year"] if items else None,
        "schedule": {},
        "is_general_view": True,
    }

    for item in items:
        timeframe = item["timeframe"]

        # Oblicz dzień i godzinę z timeframe
        day_index = (timeframe - 1) % 5
        hour_index = (timeframe - 1) // 5

        if day_index >= len(days) or hour_index >= len(times):
            continue

        day = days[day_index]
        time = times[hour_index]

        # Inicjalizuj strukturę jeśli nie istnieje
        if time not in unified_schedule["schedule"]:
            unified_schedule["schedule"][time] = {}

        if day not in unified_schedule["schedule"][time]:
            unified_schedule["schedule"][time][day] = []

        # Dodaj lekcję do listy
        lesson_info = {
            "course": item["course_name"],
            "teacher": item["teacher_name"],
            "teacher_id": item["teacher_id"],
            "classroom": item["classroom_location"],
            "classroom_id": item["classroom_id"],
            "school": item["school_name"],
            "group": item["group_name"],
        }

        unified_schedule["schedule"][time][day].append(lesson_info)

    return unified_schedule


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
