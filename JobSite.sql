--Faculty Table
DROP TABLE IF EXISTS Faculty;
CREATE TABLE Faculty (
  facultyId INTEGER PRIMARY KEY,
  facultyEmail TEXT NOT NULL,
  facultyPosition TEXT NOT NULL UNIQUE CHECK (facultyPosition IN ("Department Dean, Professor, Assoicate Professor"),
  facultyDepartment TEXT NOT NULL
);


--Student Table
DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
	StudentID* INTEGER PRIMARY KEY,
	studentName TEXT NOT NULL,
	studentEmail TEXT NOT NULL,
	FieldsOfStudy TEXT NOT NULL,
	level TEXT NOT NULL,
	year DATE NOT NULL
);

--Posting Table
DROP TABLE IF EXISTS JobPostings;
CREATE TABLE JobPosting (
	postingID* INTEGER PRIMARY KEY,
	facutlyID INTEGER FOREIGN KEY,
	startDate DATE NOT NULL
	endDate DATE NOT NULL
	description TEXT NOT NULL
);
