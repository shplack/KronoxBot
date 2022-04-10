drop table if exists courses_localization;

drop table if exists courses;

drop table if exists dialogue_localizations;

drop table if exists dialogue;

drop table if exists program_localization;

drop table if exists programs;

drop table if exists school_localization;

drop table if exists schools;

create table dialogue
(
    id     integer
        constraint dialogue_pk
            primary key autoincrement,
    name   text not null,
    output text not null
);

create unique index dialogue_name_uindex
    on dialogue (name);

create unique index dialogue_output_uindex
    on dialogue (output);

create table dialogue_localizations
(
    id            integer
        constraint dialogue_localizations_pk
            primary key autoincrement,
    dialogue_name text
        constraint dialogue_localizations_dialogue_name_fk
            references dialogue (name)
            on update cascade on delete cascade,
    locale        text,
    localization  text,
    constraint dialogue_localizations_pk_2
        unique (dialogue_name, locale)
);

create table schools
(
    id      integer
        constraint schools_pk
            primary key autoincrement,
    name    text not null,
    acronym text not null,
    link    text not null
);

create table courses
(
    id     integer
        constraint courses_pk
            primary key autoincrement,
    name   text not null,
    link   text not null,
    school text not null
        references schools (name)
            on update cascade on delete cascade,
    constraint courses_pk_2
        unique (school, name)
);

create unique index courses_link_uindex
    on courses (link);

create table courses_localization
(
    id           integer
        constraint courses_localization_pk
            primary key autoincrement,
    school       text    not null
        constraint courses_localization_schools_name_fk
            references schools (name)
            on update cascade on delete cascade,
    courses      text    not null
        constraint courses_localization_courses_name_fk
            references courses (name)
            on update cascade on delete cascade,
    locale       text    not null,
    localization integer not null,
    constraint courses_localization_pk_2
        unique (courses, locale)
);

create table programs
(
    id     integer
        constraint programs_pk
            primary key autoincrement,
    name   text not null,
    link   text not null,
    school text not null
        constraint programs_schools_name_fk
            references schools (name)
            on update cascade on delete cascade,
    constraint programs_pk_2
        unique (school, name)
);

create table program_localization
(
    id           integer
        constraint program_localization_pk
            primary key autoincrement,
    school       text not null
        constraint program_localization_schools_name_fk
            references schools (name)
            on update cascade on delete cascade,
    program      text not null
        constraint program_localization_programs_name_fk
            references programs (name)
            on update cascade on delete cascade,
    locale       text not null,
    localization text not null,
    constraint program_localization_pk_2
        unique (program, locale)
);

create unique index programs_link_uindex
    on programs (link);

create unique index programs_name_uindex
    on programs (name);

create table school_localization
(
    id           integer
        constraint school_localization_pk
            primary key autoincrement,
    school       text not null
        constraint school_localization_schools_name_fk
            references schools (name)
            on update cascade on delete cascade,
    locale       text not null,
    localization text not null,
    constraint school_localization_pk_2
        unique (school, locale)
);

create unique index schools_acronym_uindex
    on schools (acronym);

create unique index schools_link_uindex
    on schools (link);

create unique index schools_name_uindex
    on schools (name);

