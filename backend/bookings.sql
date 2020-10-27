use tbanerji_db;
 
drop table if exists parents;
drop table if exists pets;
drop table if exists bookings;
-- uses referential integrity to ensure every pet belongs to a parent

-- parents is a table with data on parents

create table parents (
    person_id int unsigned auto_increment,
    p_name varchar (50),
    pnum  varchar (10),
    primary key (person_id)
)

Engine = InnoDB;
 
--pets is a table with data on all pets 
-- contains basic biographic details as well as care instructions

create table pets (
   p_id int unsigned auto_increment,
   person_id int unsigned,
   pet_name varchar (50),
   species enum('cat', 'dog', 'rabbit','hamster','turtle','guinea pig'),
   sex enum('male', 'female'),
   neutered enum('yes','no'),
   foreign key (person_id) references parents(person_id),
   primary key (p_id)
)
Engine = InnoDB;
-- bookings contains details on previous and upcoming pet-sitting bookings 
-- references person and pet table
create table bookings (

    num_days int,
    person_id int unsigned,
    p_id int unsigned,
    allergies varchar(50),
    extra_care varchar(160),
    foreign key (p_id) references pets(p_id),
    foreign key (person_id) references parents(person_id)


)

Engine = InnoDB;
 
