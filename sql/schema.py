SCHEMA = """
University(UniversityID, Name, City, Country, EstablishedYear, TuitionFee, Currency)
Faculty(FacultyID, FacultyName, UniversityID, MinHighSchoolGrade)
Department(DepartmentID, DepartmentName, FacultyID)
Courses(CourseID, CourseName, Credits, DepartmentID)
Doctors(DoctorID, FullName, Title, Email, DepartmentID)
DoctorCourses(DoctorID, CourseID)
Students(StudentID, FullName, Email, EnrollmentYear, DepartmentID, HighSchoolGrade)
Semesters(SemesterID, Name, Year)
Enrollments(EnrollmentID, StudentID, CourseID, Grade)
Exams(ExamID, CourseID, SemesterID, ExamType, ExamDate)
"""