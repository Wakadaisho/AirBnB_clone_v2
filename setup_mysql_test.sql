-- Prepares a MySQL server db, user and their privileges
-- Database: hbnb_test_db
-- User: hbnb_test
-- Password: hbnb_test_pwd
-- Host: localhost
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
