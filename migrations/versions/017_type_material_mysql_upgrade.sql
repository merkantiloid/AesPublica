create table eve_type_materials(
    type_id bigint not null,
    material_id bigint not null,
    qty bigint not null
);

create index eve_type_materials_type_id_idx on eve_type_materials(type_id);