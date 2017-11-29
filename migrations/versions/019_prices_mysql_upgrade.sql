create table prices(
    id         bigint not null auto_increment primary key,
    type_id    bigint not null,
    source     varchar(32) not null,
    updated_at varchar(32) not null,
    value      double
)