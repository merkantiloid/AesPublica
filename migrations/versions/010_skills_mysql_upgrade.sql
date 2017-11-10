create table esi_skills(
    id                   bigint not null auto_increment primary key,
    skill_id             bigint not null,
    skillpoints_in_skill bigint not null,
    current_skill_level  int not null,
    esi_char_id          bigint not null
);