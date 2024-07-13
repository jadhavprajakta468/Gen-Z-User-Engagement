create database myntra;
use myntra;
CREATE TABLE participant (
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    `Outfit Description` TEXT,
    PRIMARY KEY (Email)
);

CREATE TABLE Challenge (
    ChallengeID INT AUTO_INCREMENT PRIMARY KEY,
    ChallengeTitle VARCHAR(255) NOT NULL,
    Theme VARCHAR(100) NOT NULL,
    StartDate DATE NOT NULL
);

