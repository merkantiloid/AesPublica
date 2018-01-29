create table moon_mats(
  id int primary key not null auto_increment,
  user_id int not null,
  raw text,
  space varchar(255)
);
create index moon_mats_user_id on moon_mats(user_id);

create table moon_mat_rigs(
  moon_mat_id int not null,
  rig_id int not null
);

create table moon_mat_items(
  id int primary key not null auto_increment,
  moon_mat_id int not null,
  type_id int not null,
  qty bigint not null
);
create index moon_mat_items_moon_mat_id on moon_mat_items(moon_mat_id);