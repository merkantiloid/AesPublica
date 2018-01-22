alter table mscan_locations add column kind varchar(32);
update  mscan_locations set kind='audit';

alter table mscan_locations add column id int primary key auto_increment;
alter table esi_locations add column system_id bigint;
alter table esi_locations add column region_id bigint;