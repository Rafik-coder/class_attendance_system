DROP DATABASE IF EXISTS attendance_system;
CREATE DATABASE IF NOT EXISTS attendance_system;

USE attendance_system;

DROP TABLE IF EXISTS attendance_system.students;
CREATE TABLE IF NOT EXISTS attendance_system.students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    student_id VARCHAR(20) NOT NULL,
    std_course VARCHAR(255) NOT NULL,
    image BLOB NOT NULL
);

DROP TABLE IF EXISTS attendance_system.attendance;
CREATE TABLE IF NOT EXISTS attendance_system.attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    attendance_date DATETIME
);
