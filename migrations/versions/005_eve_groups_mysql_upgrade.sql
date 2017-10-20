create table eve_groups(
    id          bigint       not null primary key,
    name        varchar(255) not null,
    category_id bigint,
    icon_id     bigint,
    published   bool         not null
);

create index eve_groups_category_id_idx on eve_groups(category_id);

create table eve_categories(
    id          bigint       not null primary key,
    name        varchar(255) not null,
    icon_id     bigint,
    published   bool         not null
);