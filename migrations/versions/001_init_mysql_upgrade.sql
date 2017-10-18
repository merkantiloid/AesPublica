create table users(
  id int not null auto_increment primary key,
  name varchar(255) not null,
  hash varchar(255),
  lang varchar(255)
);

create unique index users_name_idx on users(name);