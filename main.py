import mysql.connector
from db_config import config
from db_operations import inserts, utils
from schedule import populate, schedule, cost_functions


def main():
    # Uruchom pełne populate po wyczyszczeniu bazy
    print("Uzupełnianie bazy danych...")
    populate.populate()
    print("Baza danych uzupełniona!")

    print("Sprawdzanie danych w bazie...")

    # Sprawdź co mamy w bazie
    schools = utils.fetch_table("schools")
    teachers = utils.fetch_table("teachers")
    groups = utils.fetch_table("groups")

    print(f"Szkoły w bazie: {len(schools)}")
    print(f"Nauczyciele w bazie: {len(teachers)}")
    print(f"Grupy w bazie: {len(groups)}")

    if len(schools) > 0 and len(teachers) > 0:
        # Użyj rzeczywistych ID z bazy
        school_id = schools[0][0]  # ID pierwszej szkoły
        teacher_id = teachers[0][0]  # ID pierwszego nauczyciela

        print(f"Używam szkoły ID: {school_id}, nauczyciela ID: {teacher_id}")

        print("Analizowanie danych...")
        try:
            cost_functions.worst_day(
                year=2002, version=1, id_school=school_id, id_teacher=teacher_id
            )
            cost_functions.mean_week(
                year=2002, version=1, id_school=school_id, id_teacher=teacher_id
            )
        except Exception as e:
            print(f"Błąd w analizie: {e}")

        # Generowanie planów (opcjonalnie)
        print("Generowanie planu zajęć...")
        try:
            schedule.simple_reasoning(year=2002, school_id=school_id)
        except Exception as e:
            print(f"Błąd w generowaniu planu: {e}")
    else:
        print("❌ Brak danych do analizy")


if __name__ == "__main__":
    main()

