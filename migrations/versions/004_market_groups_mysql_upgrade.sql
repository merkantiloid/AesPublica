create table eve_market_groups(
    id          bigint        not null primary key,
    name        varchar(255) not null,
    description varchar(1024) not null,
    has_types   bool not null,
    icon_id     bigint,
    parent_id   bigint
);

create index eve_market_groups_parent_id_idx on eve_market_groups(parent_id);


