--Student Table
DROP TABLE IF EXISTS Student;
CREATE TABLE Student (
  facultyId INTEGER PRIMARY KEY,
  facultyEmail TEXT NOT NULL,
  facultyPosition TEXT NOT NULL UNIQUE CHECK (facultyPosition IN ("Department Dean, Professor, Assoicate Professor"),
  facultyDepartment TEXT NOT NULL
);


--Faculty Table

--Posting Table
