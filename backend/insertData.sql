-- inserts people, dates, questions, and more into tables

--parents
load data local infile 'parents.csv'
into table parents
fields terminated by ','
lines terminated by '\n';

