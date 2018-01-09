create table mscans (
  id int primary key not null auto_increment,
  user_id int default null,
  name varchar(255) default null,
  raw text,
  check_date varchar(32) default null,
  fit_times bigint default 100
);

create table esi_locations(
  id bigint primary key not null,
  name varchar(255)
);

create table mscan_locations(
  mscan_id int not null,
  esi_location_id bigint not null,
  esi_char_id bigint not null
);

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