create table eve_types(
    id              bigint       not null primary key,
    group_id        bigint,
    market_group_id bigint,
    volume          double,
    name            varchar(255) not null,
    portion_size    bigint       not null,
    published       bool
);

create index eve_types_names_idx on eve_types(name);