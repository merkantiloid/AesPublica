alter table mscan_locations add column kind varchar(32);
update  mscan_locations set kind='audit';

alter table mscan_locations add column id int primary key auto_increment;