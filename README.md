1. System Architecture
The system follows a simple 3-layer architecture:


Copy
Edit
Frontend (HTML/CSS/JS)
       ->
Django Backend (REST APIs)
       ->
SQLite Database (or PostgreSQL)
Frontend: Allows teachers and students to interact with the system

Backend: Django-based APIs handle business logic and data processing

Database: Stores users, assignments, and submissions

2. Entities and Relationships
-> User
Field	Type
id	AutoField
username	CharField
password	CharField (hashed)
role	CharField (student or teacher)

-> Assignment
Field	Type
id	AutoField
title	CharField
description	TextField
due_date	DateField
created_by	ForeignKey to User (Teacher)

-> Submission
Field	Type
id	AutoField
assignment	ForeignKey to Assignment
submitted_by	ForeignKey to User (Student)
content	TextField
file	FileField (optional)
submitted_at	DateTimeField

Relationships
A Teacher can create many Assignments

A Student can submit to many Assignments

An Assignment can have many Submissions

3. API Endpoint Definitions
Endpoint	Method	Description	Role
/api/signup/	POST	Register a new user (student or teacher)	All
/api/login/	POST	Login user and return session/token	All
/api/assignments/	POST	Create assignment	Teacher
/api/assignments/	GET	View assignments to submit	Student
/api/submit/<id>/	POST	Submit assignment content and optional file	Student
/api/submissions/<id>/	GET	View all submissions for an assignment	Teacher

All APIs return JSON responses.

4. Authentication Strategy
Django authentication system is used with a custom role field to separate students and teachers.

Role-based access is enforced in views:

Students can't create assignments

Teachers can't submit assignments

CSRF tokens are used for form submissions (or JWT if using API clients)
