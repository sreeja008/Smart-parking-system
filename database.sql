CREATE DATABASE Smart_Parking;

USE Smart_Parking;

-- Table to store user details
CREATE TABLE user_details (
    User_id INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(15) NULL
);

-- Table to store uploaded video files
CREATE TABLE upload_video (
    Video_Id INT AUTO_INCREMENT PRIMARY KEY,
    Video VARCHAR(255) NOT NULL
);
