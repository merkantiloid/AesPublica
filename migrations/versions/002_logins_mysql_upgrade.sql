create table ore_calcs(
  id      int not null auto_increment primary key,
  user_id int not null,
  space   varchar(255),
  foreign key (user_id) references users(id)
);

create unique index ore_calcs_user_id_idx on ore_calcs(user_id);