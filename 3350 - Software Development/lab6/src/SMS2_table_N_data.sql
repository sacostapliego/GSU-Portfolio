DROP DATABASE IF EXISTS SMS2;

CREATE DATABASE SMS2;
use SMS2;

CREATE TABLE department(
dept_id varchar(8) PRIMARY KEY,
dept_name varchar(132) NOT NULL UNIQUE,
chair varchar(256) NOT NULl,
building varchar(32),
room varchar(32) );

INSERT INTO department (dept_id, dept_name, chair, building, room)
VALUES ('CS','Computer Science', 'Mikler', '25 ParkPL','700'),
('Math','Mathematics', 'Carson', '25 ParkPL', '1100'),
('ITS','Information Techlonology Systems', 'Kasich', '25 ParkPL', '1200'),
('EE','Electrical Engineering', 'Costello', 'North', '100');

CREATE TABLE course(
 course_id char(4),
 course_name varchar(132),
 hours int);
 
INSERT INTO course (course_id, course_name, hours)
VALUES ('1301','CS Principles I',4),
('1302','CS Principles II',4),
('4250','Design and Analysis of Algorithms',4),
('3350','Software Development',4),
('1110','Algebra',3),
('2211','Calculus',4),
('3455','Analysis',4),
('4222','Project Management',4),
('3550','Circuits',4),
('4550','Statics',4),
('4677','Management Info Sys',3),
('4850','Intro to AI',4),
('4840','Machine Learning',3)
;

CREATE TABLE current_enrollments(
student_id int,
dept_id varchar(8),
course_id char(4)
);

INSERT INTO current_enrollments (student_id, dept_id, course_id)
VALUES (11,'CS','1301'),
	(11,'Math','2211'),
	(11,'Math','3455'),
	(12,'CS','4250'),
	(12,'EE','4550'),
	(22,'CS','3350'),
	(23,'Math','2211'),
	(23,'EE','3550'),
	(22,'Math','3455'),
	(22,'ITS','4222'),
	(22,'EE','3550'),
	(22,'CS','4250'),
    (24,'ITS','4222'),
	(24,'ITS','4677'),
	(30,'CS','4840'),
	(30,'CS','4850')
;
	

CREATE TABLE students (
  student_id INT NOT NULL,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL,
  classify VARCHAR(50) NOT NULL,
  city VARCHAR(255),
  stu_state VARCHAR(255),
  streetname VARCHAR(255),
  streetnumber VARCHAR(255),
  apartment VARCHAR(255),
  zip VARCHAR(255),
  major varchar(8), 
  PRIMARY KEY (student_id) );

INSERT INTO students (student_id, firstname, lastname, classify, city, 
		stu_state,streetname,streetnumber,apartment,zip,major)
VALUES
  (11,'Grace', 'Hopper', 'FRESHMAN','Atlanta','GA','Peachtree St.','8','A-1','30303','CS'),
  (22,'Alan', 'Turing', 'JUNIOR','Lilburn','GA','Pecantree St.','16','B-2','30304','EE'),
  (12,'Charles', 'Babbage', 'SENIOR','Hapeville','GA','Appletree St.','32','C-3','30305','Math'),
  (24,'Edgar', 'Codd', 'SOPHOMORE','Lilburn','GA','Walnuttree St.','4','A','30316','ITS'),
  (23,'Ada', 'Lovelace', 'FRESHMAN','Alpharetta','GA','Avacadotree St.','64','D-4','30306','Math'),
  (30,'Thomas', 'Kurtz', 'SENIOR','Decatur','GA','Pinetree St.','33','E','30326','CS')
;

