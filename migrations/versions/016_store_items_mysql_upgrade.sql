alter table ore_calcs add column store_items_text text;

create table store_items(
     id          bigint not null auto_increment primary key,
     ore_calc_id bigint not null,
     type_id     bigint not null,
     qty         bigint not null
);