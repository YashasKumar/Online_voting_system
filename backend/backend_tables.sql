create database it_project;
use it_project;
create table voter_details(roll_no varchar(15) primary key,full_name varchar(30) not null,email varchar(30) not null,passwd varchar(30) not null);
create table admin_details(full_name varchar(30),email varchar(30) primary key,passwd varchar(30));
create table candidate_details(roll_no varchar(15) primary key,full_name varchar(30),email varchar(30),phone_number int(10),about varchar(500),votes int(5) default 0);
select * from voter_details;
select * from admin_details;
select * from candidate_details;
insert into admin_details values("Ram","ram123","ram123");
alter table candidate_details drop column about;
alter table candidate_details add column about longtext after phone_number;