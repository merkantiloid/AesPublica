create table build_items(
    id           bigint not null auto_increment primary key,
    ore_calc_id  bigint not null,
    blueprint_id bigint not null,
    runs         bigint not null,
    me           int not null,
    te           int not null
);

alter table ore_calcs add column build_items_text text;
alter table eve_blueprints add column blueprint_id bigint not null;