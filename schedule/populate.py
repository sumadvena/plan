from db_operations import utils, inserts


def populate():
    # SCHOOLS
    inserts.create_school("SP Pcim Dolny")  # ID = 1
    inserts.create_school("SP Pcim Górny")  # ID = 2

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

    # GROUPS
    for i in range(1, 3):
        inserts.create_group("4A", 4, i)
        inserts.create_group("4B", 4, i)
        inserts.create_group("5A", 5, i)
        inserts.create_group("5B", 5, i)
        inserts.create_group("6A", 6, i)
        inserts.create_group("6B", 6, i)

    # TEACHERS

    inserts.create_teacher("Adam", "Polski", 1)
    inserts.create_teacher("Adrianna", "Polski", 1)
    inserts.create_teacher("Agnieszka", "Polski", 1)
    inserts.create_teacher("Antoni", "Matematyka", 1)
    inserts.create_teacher("Antonina", "Matematyka", 1)
    inserts.create_teacher("Adam", "Matematyka", 1)
    inserts.create_teacher("Amadeusz", "Muzyka", 1)
    inserts.create_teacher("Adrianna", "Plastyka-Technika", 1)
    inserts.create_teacher("Albert", "WF-Technika", 1)
    inserts.create_teacher("Aldona", "WF", 1)
    inserts.create_teacher("Aleksandra", "WF", 1)
    inserts.create_teacher("Ambroży", "WF", 1)
    inserts.create_teacher("Antoni", "Religia", 1)
    inserts.create_teacher("Alan", "Przyroda-Geografia", 1)
    inserts.create_teacher("Alina", "Przyroda-Biologia", 1)
    inserts.create_teacher("Amanda", "Historia", 1)
    inserts.create_teacher("Aleksy", "Historia", 1)

    inserts.create_teacher("Barbara", "Polski", 2)
    inserts.create_teacher("Bartłomiej", "Polski", 2)
    inserts.create_teacher("Bartosz", "Polski", 2)
    inserts.create_teacher("Beata", "Matematyka", 2)
    inserts.create_teacher("Beniamin", "Matematyka", 2)
    inserts.create_teacher("Berenika", "Matematyka", 2)
    inserts.create_teacher("Bernadeta", "Muzyka", 2)
    inserts.create_teacher("Błażej", "Plastyka-Technika", 2)
    inserts.create_teacher("Blanka", "WF-Technika", 2)
    inserts.create_teacher("Bogdan", "WF", 2)
    inserts.create_teacher("Bogumiła", "WF", 2)
    inserts.create_teacher("Borys", "WF", 2)
    inserts.create_teacher("Bożena", "Religia", 2)
    inserts.create_teacher("Bronisław", "Przyroda-Geografia", 2)
    inserts.create_teacher("Beatrycze", "Przyroda-Biologia", 2)
    inserts.create_teacher("Bolesław", "Historia", 2)
    inserts.create_teacher("Bandyta", "Historia", 2)

    # CLASSROOMS
    for i in range(1, 3):
        inserts.create_classroom("1", i)
        inserts.create_classroom("2", i)
        inserts.create_classroom("3", i)
        inserts.create_classroom("4", i)
        inserts.create_classroom("5", i)
        inserts.create_classroom("Gimnastyczna", i)

    # PRIVILEGES

    ## Teachers
    for i in range(4, 7):
        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adam", "Polski", 1)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adrianna", "Polski", 1)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Agnieszka", "Polski", 1)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Antoni", "Matematyka", 1)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Antonina", "Matematyka", 1)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adam", "Matematyka", 1)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Amadeusz", "Muzyka", 1)),
                utils.find_id("courses", ("MUZ", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adrianna", "Plastyka-Technika", 1)),
                utils.find_id("courses", ("PLAST", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Adrianna", "Plastyka-Technika", 1)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Albert", "WF-Technika", 1)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Albert", "WF-Technika", 1)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aldona", "WF", 1)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aleksandra", "WF", 1)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Ambroży", "WF", 1)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Antoni", "Religia", 1)),
                utils.find_id("courses", ("REL", 2, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alan", "Przyroda-Geografia", 1)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alan", "Przyroda-Geografia", 1)),
                utils.find_id("courses", ("GEO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alina", "Przyroda-Biologia", 1)),
                utils.find_id("courses", ("BIO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Alina", "Przyroda-Biologia", 1)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Amanda", "Historia", 1)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Amanda", "Historia", 1)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aleksy", "Historia", 1)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Aleksy", "Historia", 1)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

    ### 2nd school
    for i in range(4, 7):
        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Barbara", "Polski", 2)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bartłomiej", "Polski", 2)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bartosz", "Polski", 2)),
                utils.find_id("courses", ("PL", 5, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beata", "Matematyka", 2)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beniamin", "Matematyka", 2)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Berenika", "Matematyka", 2)),
                utils.find_id("courses", ("MAT", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bernadeta", "Muzyka", 2)),
                utils.find_id("courses", ("MUZ", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Błażej", "Plastyka-Technika", 2)),
                utils.find_id("courses", ("PLAST", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Błażej", "Plastyka-Technika", 2)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Blanka", "WF-Technika", 2)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Blanka", "WF-Technika", 2)),
                utils.find_id("courses", ("TECH", 1, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bogdan", "WF", 2)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bogumiła", "WF", 2)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Borys", "WF", 2)),
                utils.find_id("courses", ("WF", 4, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bożena", "Religia", 2)),
                utils.find_id("courses", ("REL", 2, i)),
            )
        except:
            print("duplicate privilege")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bronisław", "Przyroda-Geografia", 2)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bronisław", "Przyroda-Geografia", 2)),
                utils.find_id("courses", ("GEO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beatrycze", "Przyroda-Biologia", 2)),
                utils.find_id("courses", ("BIO", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Beatrycze", "Przyroda-Biologia", 2)),
                utils.find_id("courses", ("PRZ", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bronisław", "Historia", 2)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bronisław", "Historia", 2)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bandyta", "Historia", 2)),
                utils.find_id("courses", ("HIST", 1, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

        try:
            inserts.grant_privilege_to_course(
                "teacher",
                utils.find_id("teachers", ("Bandyta", "Historia", 2)),
                utils.find_id("courses", ("HIST", 2, i)),
            )
        except:
            print("duplicate privilege or course does not exist")

    ## Groups
    for school in range(1, 3):
        for level in range(4, 7):
            for group in "AB":
                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("PL", 5, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("ANG", 3, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("MUZ", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("PLAST", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("HIST", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("HIST", 2, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("MAT", 4, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("INF", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("TECH", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("WYCH", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("PRZ", 2, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("REL", 2, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("BIO", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "group",
                        utils.find_id("groups", (f"{level}{group}", level, school)),
                        utils.find_id("courses", ("GEO", 1, level)),
                    )
                except:
                    print("duplicate group privilege or course does not exist")

            try:
                inserts.grant_privilege_to_course(
                    "group",
                    utils.find_id("groups", (f"{level}{group}", level, school)),
                    utils.find_id("courses", ("WF", 4, level)),
                )
            except:
                print("duplicate group privilege or course does not exist")

    # Classrooms

    classrooms = ["1", "2", "3", "4", "5"]
    for school in range(1, 3):
        for level in range(4, 7):
            for cr in classrooms:
                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("PL", 5, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("ANG", 3, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("MUZ", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("PLAST", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("HIST", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("HIST", 2, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("MAT", 4, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("INF", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("TECH", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("WYCH", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("PRZ", 2, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("REL", 2, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("BIO", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

                try:
                    inserts.grant_privilege_to_course(
                        "classroom",
                        utils.find_id("classrooms", (cr, school)),
                        utils.find_id("courses", ("GEO", 1, level)),
                    )
                except:
                    print("duplicate classroom privilege or course does not exist")

            try:
                inserts.grant_privilege_to_course(
                    "classroom",
                    utils.find_id("classrooms", ("Gimnastyczna", school)),
                    utils.find_id("courses", ("WF", 4, level)),
                )
            except:
                print("duplicate classroom privilege or course does not exist")
