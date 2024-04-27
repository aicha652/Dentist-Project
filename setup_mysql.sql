CREATE DATABASE IF NOT EXISTS Dentist;
CREATE USER IF NOT EXISTS 'user_db'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON Dentist .* TO 'user_db'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'user_db'@'localhost';
FLUSH PRIVILEGES;