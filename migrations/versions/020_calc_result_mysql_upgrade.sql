create table calc_results(
    id          bigint not null auto_increment primary key,
    ore_calc_id bigint not null,
    type_id     bigint not null,
    qty         bigint not null
);

create index calc_results_ore_calc_id_idx on calc_results(ore_calc_id);