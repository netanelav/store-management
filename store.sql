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

insert into categories 
values ("1","Business"), ("2","Finance"),("3","Cooking"),("4","History"),
("5","Medical"),("6","Sports"),("7","Travel"),("8","Romance");	

insert into products (title,description,price,img_url,category,favorite)
values ("Nickel and Dimed","by Barbara Ehrenreich",5,"images/business1.jpg",1,"0"),
("The Two Towers","by Peter S. Beagle and J.R.R. Tolkien",4,"images/business2.jpg",1,"1"),
("The Wealthy Barber","by David Chilton",5,"images/finance1.jpg",2,"0"),
("Financial Freedom","by Suze Orman",5,"images/finance2.jpg",2,"0"),
("Eat to Live","by Joel Fuhrman",5,"images/cooking1.jpg",3,"0"),
("Fast Food Nation","by Eric Schlosser",4,"images/cooking2.jpg",3,"0"),
("Into the Wild","by Jon Krakauer",4,"images/history1.jpg",4,"0"),
("Number the Stars","by Lois Lowry",4,"images/history2.jpg",4,"1"),
("Body for Life","by Bill Phillips",6,"images/medical1.jpg",5,"0"),
("Healthy Sleep Habits","by Marc Weissbluth",5,"images/medical2.jpg",5,"0"),
("Silent Spring","by Rachel Carson",6,"images/sports1.jpg",6,"0"),
("Harvey Penick Little Red Book","by Bud Shrake and Harvey Penick",6,"images/sports2.jpg",6,"1"),
("Herat of Darkness","by Joseph Conrad",5,"images/travel1.jpg",7,"0"),
("The Pilgrimage","by Paulo Coelho",3,"images/travel2.jpg",7,"0"),
("The Great Gatsby","by Scott Fichgerald",6,"images/romance1.jpg",8,"1"),
("The House on Mango Street","by Sandra Cinros",4,"images/romance2.jpg",8,"0");

select * from categories;
select * from products;
