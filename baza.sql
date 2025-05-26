CREATE TABLE `teachers` (
    `id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    `surname` VARCHAR(255),
    `id_school` INTEGER,
    PRIMARY KEY(`id`)
);

CREATE TABLE `privileges_teachers` (
    `id_teacher` INTEGER NOT NULL,
    `id_course` INTEGER NOT NULL,
    PRIMARY KEY(`id_teacher`, `id_course`)
);

CREATE TABLE `courses` (
    `id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    `hours_weekly` INTEGER,
    `level` INTEGER,
    PRIMARY KEY(`id`)
);

CREATE TABLE `classrooms` (
    `id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    `location` VARCHAR(50),  -- Fix: Changed from INTEGER to VARCHAR
    `id_school` INTEGER,
    PRIMARY KEY(`id`)
);

CREATE TABLE `privileges_classrooms` (
    `id_classroom` INTEGER NOT NULL,
    `id_course` INTEGER NOT NULL,
    PRIMARY KEY(`id_classroom`, `id_course`)
);

CREATE TABLE `groups` (
    `id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    `level` INTEGER,
    `id_school` INTEGER,
    PRIMARY KEY(`id`)
);

CREATE TABLE `group_courses` (
    `id_group` INTEGER NOT NULL,
    `id_course` INTEGER NOT NULL,
    PRIMARY KEY(`id_group`, `id_course`)
);

CREATE TABLE `assigned_sets` (
    `id_teacher` INTEGER NOT NULL,
    `id_course` INTEGER NOT NULL,
    `id_group` INTEGER NOT NULL,
    PRIMARY KEY(`id_teacher`, `id_course`, `id_group`)
);

CREATE TABLE `schedule` (
    `id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    `year` INTEGER,
    `id_school` INTEGER,
    `timeframe` INTEGER,
    `id_assigned_set` INTEGER,
    `id_classroom` INTEGER,
    PRIMARY KEY(`id`)
);

CREATE TABLE `school` (
    `id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    PRIMARY KEY(`id`)
);

-- Foreign key constraints
-- Original constraints for tables other than assigned_sets are unchanged

-- Change 2: Enforce teacher/course/group consistency in assigned_sets
-- Replace individual FKs with composite FKs (ensure privileges exist)
ALTER TABLE `assigned_sets`
ADD FOREIGN KEY (id_teacher, id_course)
REFERENCES privileges_teachers(id_teacher, id_course);

ALTER TABLE `assigned_sets`
ADD FOREIGN KEY (id_group, id_course)
REFERENCES group_courses(id_group, id_course);

-- Change 5: Add indexes for foreign key performance
CREATE INDEX idx_teachers_school ON teachers(id_school);
CREATE INDEX idx_classrooms_school ON classrooms(id_school);
CREATE INDEX idx_groups_school ON groups(id_school);
CREATE INDEX idx_schedule_classroom ON schedule(id_classroom);

-- Change 7: Restrict deletions where orphaning is dangerous
-- Teachers: Restrict school deletion if teachers exist
ALTER TABLE `teachers`
ADD FOREIGN KEY (id_school)
REFERENCES school(id)
ON DELETE RESTRICT;

-- Classrooms: Restrict school deletion if classrooms exist
ALTER TABLE `classrooms`
ADD FOREIGN KEY (id_school)
REFERENCES school(id)
ON DELETE RESTRICT;

-- Schedule: Restrict classroom deletion if scheduled
ALTER TABLE `schedule`
ADD FOREIGN KEY (id_classroom)
REFERENCES classrooms(id)
ON DELETE RESTRICT;

-- Change 9: Add missing foreign key for assigned_sets in schedule
ALTER TABLE `schedule`
ADD FOREIGN KEY (id_assigned_set)
REFERENCES assigned_sets(id);
