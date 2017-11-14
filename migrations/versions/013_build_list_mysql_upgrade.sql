create table build_items(
    id           bigint not null auto_increment primary key,
    ore_calc_id  bigint not null,
    type_id      bigint not null,
    runs         bigint not null,
    me           int not null,
    te           int not null
);

alter table ore_calcs add column build_items_text text;

CREATE FULLTEXT INDEX eve_types_name_idx ON eve_types(name);