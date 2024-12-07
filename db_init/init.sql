-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `cloud_data_2.0`;

-- Switch to the cloud_data database
USE `cloud_data_2.0`;

-- Create the camera table if it doesn't exist
CREATE TABLE IF NOT EXISTS camera (
  Id int(11) NOT NULL AUTO_INCREMENT,
  CameraId varchar(50) NOT NULL,
  DetectionTime datetime NOT NULL DEFAULT current_timestamp(),
  Detections int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (Id)
);

-- Grant all privileges to the specified user
GRANT ALL PRIVILEGES ON `cloud_data_2.0`.* TO '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}' WITH GRANT OPTION;

-- Flush privileges to ensure changes are applied
FLUSH PRIVILEGES;
