create table esi_chars(
    id                bigint not null auto_increment primary key,
    character_id      bigint not null,
    character_name    varchar(255) not null,
    scopes            varchar(4095) not null,
    token_type        varchar(31) not null,
    user_id           bigint not null,
    access_expiration double not null,
    refresh_token     varchar(255),
    access_token      varchar(255)
);