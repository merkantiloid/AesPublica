create table mscans (
  id int primary key not null auto_increment,
  user_id int not null,
  name varchar(255) default null,
  raw text,
  check_date varchar(32) default null,
  fit_times bigint default 100
);
create index mscans_user_id_idx on mscans(user_id);

create table esi_locations(
  id bigint primary key not null,
  name varchar(255)
);

create table mscan_locations(
  mscan_id int not null,
  esi_location_id bigint not null,
  esi_char_id bigint not null
);
create index mscan_locations_mscan_id_idx on mscan_locations(mscan_id);

create table mscan_items (
  id int primary key not null auto_increment,
  mscan_id int not null,
  type_id int not null,
  qty bigint,
  store_qty bigint,
  market_qty bigint,
  min_price double,
  avg_price double
);
create index mscan_items_mscan_id_idx on mscan_items(mscan_id);
create index mscan_items_type_id_idx on mscan_items(type_id);