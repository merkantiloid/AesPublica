create table eve_type_attributes(
    type_id bigint not null,
    attribute_id bigint not null,
    value double not null
);

create index eve_type_attributes_type_id_idx on eve_type_attributes(type_id);
create index eve_type_attributes_attribute_id_idx on eve_type_attributes(attribute_id);

create table eve_attributes(
    id           int not null primary key,
    code         varchar(255) not  null,
    name         varchar(255) not  null,
    category_id  bigint,
    icon_id      bigint,
    unit_id      bigint,
    description  varchar(1024) not null,
    published    bool not null,
    stackable    bool not null,
    high_is_good bool not null,
    default_value double not null
);



