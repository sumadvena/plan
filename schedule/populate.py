import mysql.connector
from db_config import config
from db_operations import utils, inserts


def clear_all_tables():
    """Czyści wszystkie tabele w odpowiedniej kolejności (respektując foreign keys)"""
    print("Czyszczenie wszystkich tabel...")
    
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        # Wyłącz sprawdzanie foreign keys
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Lista tabel w kolejności do wyczyszczenia
        tables_to_clear = [
            'schedule',           # Najpierw tabele zależne
            'assigned_sets',
            'privileges_teachers',
            'privileges_groups', 
            'privileges_classrooms',
            'teachers',          # Potem tabele główne
            'groups',
            'classrooms',
            'courses',
            'schools'            # Na końcu tabele bazowe
        ]
        
        for table in tables_to_clear:
            try:
                cursor.execute(f"TRUNCATE TABLE {table};")
                print(f"   Wyczyszczono tabelę: {table}")
            except mysql.connector.Error as e:
                print(f"   Błąd czyszczenia {table}: {e}")
        
        # Włącz z powrotem sprawdzanie foreign keys
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        print("Wszystkie tabele wyczyszczone!")
        
    except Exception as e:
        print(f"Błąd podczas czyszczenia tabel: {e}")
        raise


def populate():
    """Główna funkcja uzupełniania bazy danych"""
    
    # Test połączenia z bazą
    try:
        cnx = mysql.connector.connect(**config)
        print("Połączenie z bazą danych: OK")
        cnx.close()
    except Exception as e:
        print(f"Błąd połączenia z bazą: {e}")
        return
    
    # KROK 1: Wyczyść wszystkie tabele
    clear_all_tables()
    
    # KROK 2: Uzupełnij danymi
    print("\nRozpoczynam uzupełnianie bazy danych...")
    
    print("Tworzenie szkół...")
    # SCHOOLS
    inserts.create_school("SP Pcim Dolny")
    inserts.create_school("SP Pcim Górny")
    
    # Pobierz rzeczywiste ID szkół z bazy
    school1_id = utils.find_id("schools", ("SP Pcim Dolny",))
    school2_id = utils.find_id("schools", ("SP Pcim Górny",))
    
    if not school1_id or not school2_id:
        print("Błąd: Nie można znaleźć ID szkół!")
        return
        
    print(f"   Szkoły utworzone - ID: {school1_id}, {school2_id}")

    print("Tworzenie kursów...")
    # COURSES
    # Level 4
    inserts.create_course("PL", 5, 4)
    inserts.create_course("ANG", 3, 4)
    inserts.create_course("MUZ", 1, 4)
    inserts.create_course("PLAST", 1, 4)
    inserts.create_course("HIST", 1, 4)
    inserts.create_course("PRZ", 2, 4)
    inserts.create_course("MAT", 4, 4)
    inserts.create_course("INF", 1, 4)
    inserts.create_course("TECH", 1, 4)
    inserts.create_course("WF", 4, 4)
    inserts.create_course("WYCH", 1, 4)
    inserts.create_course("REL", 2, 4)

    # Level 5 and 6
    for i in range(5, 7):
        inserts.create_course("PL", 5, i)
        inserts.create_course("ANG", 3, i)
        inserts.create_course("MUZ", 1, i)
        inserts.create_course("PLAST", 1, i)
        inserts.create_course("HIST", 2, i)
        inserts.create_course("MAT", 4, i)
        inserts.create_course("INF", 1, i)
        inserts.create_course("TECH", 1, i)
        inserts.create_course("WF", 4, i)
        inserts.create_course("WYCH", 1, i)
        inserts.create_course("GEO", 1, i)
        inserts.create_course("BIO", 1, i)
        inserts.create_course("REL", 2, i)

    print("Tworzenie grup...")
    # GROUPS - używaj rzeczywistych ID szkół
    for school_id in [school1_id, school2_id]:
        inserts.create_group("4A", 4, school_id)
        inserts.create_group("4B", 4, school_id)
        inserts.create_group("5A", 5, school_id)
        inserts.create_group("5B", 5, school_id)
        inserts.create_group("6A", 6, school_id)
        inserts.create_group("6B", 6, school_id)

    print("Tworzenie nauczycieli...")
    # TEACHERS - używaj rzeczywistych ID szkół

    # Szkoła 1
    inserts.create_teacher("Adam", "Polski", school1_id)
    inserts.create_teacher("Adrianna", "Polski", school1_id)
    inserts.create_teacher("Agnieszka", "Polski", school1_id)
    inserts.create_teacher("Antoni", "Matematyka", school1_id)
    inserts.create_teacher("Antonina", "Matematyka", school1_id)
    inserts.create_teacher("Adam", "Matematyka", school1_id)
    inserts.create_teacher("Amadeusz", "Muzyka", school1_id)
    inserts.create_teacher("Adrianna", "Plastyka-Technika", school1_id)
    inserts.create_teacher("Albert", "WF-Technika", school1_id)
    inserts.create_teacher("Aldona", "WF", school1_id)
    inserts.create_teacher("Ambroży", "WF", school1_id)
    inserts.create_teacher("Antoni", "Religia", school1_id)
    inserts.create_teacher("Alan", "Przyroda-Geografia", school1_id)
    inserts.create_teacher("Alina", "Przyroda-Biologia", school1_id)
    inserts.create_teacher("Amanda", "Historia", school1_id)
    inserts.create_teacher("Aleksy", "Historia", school1_id)

    # Szkoła 2
    inserts.create_teacher("Barbara", "Polski", school2_id)
    inserts.create_teacher("Bartłomiej", "Polski", school2_id)
    inserts.create_teacher("Bartosz", "Polski", school2_id)
    inserts.create_teacher("Beata", "Matematyka", school2_id)
    inserts.create_teacher("Beniamin", "Matematyka", school2_id)
    inserts.create_teacher("Berenika", "Matematyka", school2_id)
    inserts.create_teacher("Bernadeta", "Muzyka", school2_id)
    inserts.create_teacher("Błażej", "Plastyka-Technika", school2_id)
    inserts.create_teacher("Blanka", "Technika", school2_id)
    inserts.create_teacher("Bogdan", "WF", school2_id)
    inserts.create_teacher("Bogumiła", "WF", school2_id)
    inserts.create_teacher("Borys", "WF", school2_id)
    inserts.create_teacher("Bożena", "Religia", school2_id)
    inserts.create_teacher("Bronisław", "Przyroda-Geografia", school2_id)
    inserts.create_teacher("Beatrycze", "Przyroda-Biologia", school2_id)
    inserts.create_teacher("Bolesław", "Historia-Religia", school2_id)
    inserts.create_teacher("Bandyta", "Historia", school2_id)

    print("Tworzenie sal...")
    # CLASSROOMS - używaj rzeczywistych ID szkół
    for school_id in [school1_id, school2_id]:
        inserts.create_classroom("1", school_id)
        inserts.create_classroom("2", school_id)
        inserts.create_classroom("3", school_id)
        inserts.create_classroom("4", school_id)
        inserts.create_classroom("5", school_id)
        inserts.create_classroom("Gimnastyczna", school_id)

    print("Tworzenie uprawnień nauczycieli...")
    # PRIVILEGES - Teachers - używaj rzeczywistych ID szkół
    for i in range(4, 7):
        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adam", "Polski", school1_id)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adrianna", "Polski", school1_id)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Agnieszka", "Polski", school1_id)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Antoni", "Matematyka", school1_id)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Antonina", "Matematyka", school1_id)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adam", "Matematyka", school1_id)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Amadeusz", "Muzyka", school1_id)),
                utils.find_id("courses", ("MUZ", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adrianna", "Plastyka-Technika", school1_id)),
                utils.find_id("courses", ("PLAST", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adrianna", "Plastyka-Technika", school1_id)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Albert", "WF-Technika", school1_id)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Albert", "WF-Technika", school1_id)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aldona", "WF", school1_id)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Ambroży", "WF", school1_id)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Antoni", "Religia", school1_id)),
                utils.find_id("courses", ("REL", 2, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alan", "Przyroda-Geografia", school1_id)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alan", "Przyroda-Geografia", school1_id)),
                utils.find_id("courses", ("GEO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alina", "Przyroda-Biologia", school1_id)),
                utils.find_id("courses", ("BIO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alina", "Przyroda-Biologia", school1_id)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Amanda", "Historia", school1_id)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Amanda", "Historia", school1_id)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aleksy", "Historia", school1_id)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aleksy", "Historia", school1_id)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

    # 2nd school
    for i in range(4, 7):
        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Barbara", "Polski", school2_id)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bartłomiej", "Polski", school2_id)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bartosz", "Polski", school2_id)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beata", "Matematyka", school2_id)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beniamin", "Matematyka", school2_id)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Berenika", "Matematyka", school2_id)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bernadeta", "Muzyka", school2_id)),
                utils.find_id("courses", ("MUZ", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Błażej", "Plastyka-Technika", school2_id)),
                utils.find_id("courses", ("PLAST", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Błażej", "Plastyka-Technika", school2_id)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Blanka", "Technika", school2_id)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bogdan", "WF", school2_id)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bogumiła", "WF", school2_id)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Borys", "WF", school2_id)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bożena", "Religia", school2_id)),
                utils.find_id("courses", ("REL", 2, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bronisław", "Przyroda-Geografia", school2_id)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bronisław", "Przyroda-Geografia", school2_id)),
                utils.find_id("courses", ("GEO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beatrycze", "Przyroda-Biologia", school2_id)),
                utils.find_id("courses", ("BIO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beatrycze", "Przyroda-Biologia", school2_id)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bolesław", "Historia-Religia", school2_id)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bolesław", "Historia-Religia", school2_id)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bolesław", "Historia-Religia", school2_id)),
                utils.find_id("courses", ("REL", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bandyta", "Historia", school2_id)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bandyta", "Historia", school2_id)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

    print("Tworzenie uprawnień grup...")
    # Groups - używaj rzeczywistych ID szkół
    for school_id in [school1_id, school2_id]:
        for level in range(4, 7):
            for group in "AB":
                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("PL", 5, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("ANG", 3, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("MUZ", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("PLAST", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("HIST", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("HIST", 2, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("MAT", 4, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("INF", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("TECH", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("WYCH", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("PRZ", 2, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("REL", 2, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("BIO", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("GEO", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school_id)),
                        utils.find_id("courses", ("WF", 4, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

    print("Tworzenie uprawnień sal...")
    # Classrooms - używaj rzeczywistych ID szkół
    classrooms = ["1", "2", "3", "4", "5"]
    for school_id in [school1_id, school2_id]:
        for level in range(4, 7):
            for cr in classrooms:
                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("HIST", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("HIST", 2, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("MAT", 4, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("INF", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("TECH", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("WYCH", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("PRZ", 2, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("REL", 2, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("BIO", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school_id)),
                        utils.find_id("courses", ("GEO", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

            try:
                inserts.grant_privilege_to_course(
                    "classroom",
                    utils.find_id("classrooms", ("Gimnastyczna", school_id)),
                    utils.find_id("courses", ("WF", 4, level)),
                )
            except:
                print("duplicate classroom privilege or course does not exist")

    print("Tworzenie zestawów przypisań...")
    # ASSIGNED SETS - używaj rzeczywistych ID szkół
    # 1st school
    for c in "AB":
        inserts.create_assigned_set(
            utils.find_id("teachers", ("Adam", "Polski", school1_id)),
            utils.find_id("courses", ("PL", 5, 4)),
            utils.find_id("groups", (f"4{c}", 4, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Adrianna", "Polski", school1_id)),
            utils.find_id("courses", ("PL", 5, 5)),
            utils.find_id("groups", (f"5{c}", 5, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Agnieszka", "Polski", school1_id)),
            utils.find_id("courses", ("PL", 5, 6)),
            utils.find_id("groups", (f"6{c}", 6, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Antoni", "Matematyka", school1_id)),
            utils.find_id("courses", ("MAT", 4, 4)),
            utils.find_id("groups", (f"4{c}", 4, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Antonina", "Matematyka", school1_id)),
            utils.find_id("courses", ("MAT", 4, 5)),
            utils.find_id("groups", (f"5{c}", 5, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Adam", "Matematyka", school1_id)),
            utils.find_id("courses", ("MAT", 4, 6)),
            utils.find_id("groups", (f"6{c}", 6, school1_id)),
        )

        for l in range(4, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Amadeusz", "Muzyka", school1_id)),
                utils.find_id("courses", ("MUZ", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school1_id)),
            )

        for l in range(4, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Adrianna", "Plastyka-Technika", school1_id)),
                utils.find_id("courses", ("PLAST", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school1_id)),
            )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Adrianna", "Plastyka-Technika", school1_id)),
                utils.find_id("courses", ("TECH", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school1_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Albert", "WF-Technika", school1_id)),
            utils.find_id("courses", ("TECH", 1, 4)),
            utils.find_id("groups", (f"4{c}", 4, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Albert", "WF-Technika", school1_id)),
            utils.find_id("courses", ("WF", 4, 4)),
            utils.find_id("groups", (f"4{c}", 4, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Aldona", "WF", school1_id)),
            utils.find_id("courses", ("WF", 4, 5)),
            utils.find_id("groups", (f"5{c}", 5, school1_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Ambroży", "WF", school1_id)),
            utils.find_id("courses", ("WF", 4, 6)),
            utils.find_id("groups", (f"6{c}", 6, school1_id)),
        )

        for l in range(4, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Antoni", "Religia", school1_id)),
                utils.find_id("courses", ("REL", 2, l)),
                utils.find_id("groups", (f"{l}{c}", l, school1_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Alan", "Przyroda-Geografia", school1_id)),
            utils.find_id("courses", ("PRZ", 2, 4)),
            utils.find_id("groups", ("4A", 4, school1_id)),
        )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Alan", "Przyroda-Geografia", school1_id)),
                utils.find_id("courses", ("GEO", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school1_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Alina", "Przyroda-Biologia", school1_id)),
            utils.find_id("courses", ("PRZ", 2, 4)),
            utils.find_id("groups", ("4B", 4, school1_id)),
        )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Alina", "Przyroda-Biologia", school1_id)),
                utils.find_id("courses", ("BIO", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school1_id)),
            )

    inserts.create_assigned_set(
        utils.find_id("teachers", ("Amanda", "Historia", school1_id)),
        utils.find_id("courses", ("HIST", 1, 4)),
        utils.find_id("groups", ("4A", 4, school1_id)),
    )

    for l in range(5, 7):
        inserts.create_assigned_set(
            utils.find_id("teachers", ("Amanda", "Historia", school1_id)),
            utils.find_id("courses", ("HIST", 2, l)),
            utils.find_id("groups", (f"{l}A", l, school1_id)),
        )

    inserts.create_assigned_set(
        utils.find_id("teachers", ("Aleksy", "Historia", school1_id)),
        utils.find_id("courses", ("HIST", 1, 4)),
        utils.find_id("groups", ("4B", 4, school1_id)),
    )

    for l in range(5, 7):
        inserts.create_assigned_set(
            utils.find_id("teachers", ("Aleksy", "Historia", school1_id)),
            utils.find_id("courses", ("HIST", 2, l)),
            utils.find_id("groups", (f"{l}B", l, school1_id)),
        )

    # 2nd school
    for c in "AB":
        inserts.create_assigned_set(
            utils.find_id("teachers", ("Barbara", "Polski", school2_id)),
            utils.find_id("courses", ("PL", 5, 4)),
            utils.find_id("groups", (f"4{c}", 4, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bartłomiej", "Polski", school2_id)),
            utils.find_id("courses", ("PL", 5, 5)),
            utils.find_id("groups", (f"5{c}", 5, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bartosz", "Polski", school2_id)),
            utils.find_id("courses", ("PL", 5, 6)),
            utils.find_id("groups", (f"6{c}", 6, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Beata", "Matematyka", school2_id)),
            utils.find_id("courses", ("MAT", 4, 4)),
            utils.find_id("groups", (f"4{c}", 4, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Beniamin", "Matematyka", school2_id)),
            utils.find_id("courses", ("MAT", 4, 5)),
            utils.find_id("groups", (f"5{c}", 5, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Berenika", "Matematyka", school2_id)),
            utils.find_id("courses", ("MAT", 4, 6)),
            utils.find_id("groups", (f"6{c}", 6, school2_id)),
        )

        for l in range(4, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Bernadeta", "Muzyka", school2_id)),
                utils.find_id("courses", ("MUZ", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

        for l in range(4, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Błażej", "Plastyka-Technika", school2_id)),
                utils.find_id("courses", ("PLAST", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Błażej", "Plastyka-Technika", school2_id)),
            utils.find_id("courses", ("TECH", 1, 4)),
            utils.find_id("groups", (f"4{c}", 4, school2_id)),
        )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Blanka", "Technika", school2_id)),
                utils.find_id("courses", ("TECH", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bogdan", "WF", school2_id)),
            utils.find_id("courses", ("WF", 4, 4)),
            utils.find_id("groups", (f"4{c}", 4, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bogumiła", "WF", school2_id)),
            utils.find_id("courses", ("WF", 4, 5)),
            utils.find_id("groups", (f"5{c}", 5, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Borys", "WF", school2_id)),
            utils.find_id("courses", ("WF", 4, 6)),
            utils.find_id("groups", (f"6{c}", 6, school2_id)),
        )

        for l in range(4, 6):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Bożena", "Religia", school2_id)),
                utils.find_id("courses", ("REL", 2, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bronisław", "Przyroda-Geografia", school2_id)),
            utils.find_id("courses", ("PRZ", 2, 4)),
            utils.find_id("groups", ("4A", 4, school2_id)),
        )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Bronisław", "Przyroda-Geografia", school2_id)),
                utils.find_id("courses", ("GEO", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Beatrycze", "Przyroda-Biologia", school2_id)),
            utils.find_id("courses", ("PRZ", 2, 4)),
            utils.find_id("groups", ("4B", 4, school2_id)),
        )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Beatrycze", "Przyroda-Biologia", school2_id)),
                utils.find_id("courses", ("BIO", 1, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bolesław", "Historia-Religia", school2_id)),
            utils.find_id("courses", ("HIST", 1, 4)),
            utils.find_id("groups", (f"4{c}", 4, school2_id)),
        )

        inserts.create_assigned_set(
            utils.find_id("teachers", ("Bolesław", "Historia-Religia", school2_id)),
            utils.find_id("courses", ("REL", 2, 6)),
            utils.find_id("groups", (f"6{c}", 6, school2_id)),
        )

        for l in range(5, 7):
            inserts.create_assigned_set(
                utils.find_id("teachers", ("Bandyta", "Historia", school2_id)),
                utils.find_id("courses", ("HIST", 2, l)),
                utils.find_id("groups", (f"{l}{c}", l, school2_id)),
            )

    print("\nSUKCES! Baza danych została w pełni uzupełniona!")
    print("Podsumowanie:")
    print("   Szkoły: 2")
    print("   Kursy: 38")
    print("   Grupy: 12") 
    print("   Nauczyciele: 33")
    print("   Sale: 12")
    print("   Uprawnienia: utworzone")
    