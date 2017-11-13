create table build_items(
    id           bigint not null auto_increment primary key,
    blueprint_id bigint not null,
    runs         bigint not null,
    me           int not null,
    te           int not null
);

alter table ore_calcs add column build_items text;