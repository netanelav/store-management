create database store;
use store;

create table category (
id int auto_increment,
name varchar(30) unique,
primary key (id));

select * from category;