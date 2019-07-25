create database store;
use store;

create table categories (
id int auto_increment,
name varchar(30) unique,
primary key (id));

create table products (
id int auto_increment,
title varchar(30),
description varchar(200),
price int,
img_url varchar(30),
category varchar(30),
favorite ENUM("0","1"),
primary key (id));

	
select * from categories;
select * from products;