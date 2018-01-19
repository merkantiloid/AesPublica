create table user_actions(
  id int primary key not null auto_increment,
  user_id int not null,
  path varchar(255),
  created_at varchar(31)
);

create index user_actions_user_id on user_actions(user_id);