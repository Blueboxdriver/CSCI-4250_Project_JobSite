--Faculty Table
DROP TABLE IF EXISTS Faculty;
CREATE TABLE Faculty (
  facultyId INTEGER PRIMARY KEY,
  facultyEmail TEXT NOT NULL,
  facultyPosition TEXT NOT NULL UNIQUE CHECK (facultyPosition IN ("Department Dean, Professor, Assoicate Professor"),
  facultyDepartment TEXT NOT NULL
);


--Student Table

--Posting Table
