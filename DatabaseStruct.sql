CREATE SCHEMA `books` ;

CREATE TABLE `books`.`books` (
  `title` VARCHAR(512) NOT NULL,
  `author` VARCHAR(512) NULL,
  `rating` FLOAT NULL,
  `complete_link` VARCHAR(512) NULL);
  
CREATE TABLE `books`.`query_statistic` (
  `query` TEXT NULL DEFAULT NULL,
  `count` BIGINT NULL DEFAULT NULL);
  
CREATE TABLE `books`.`contact_message` (
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP FIRST;
  `fullname` VARCHAR(512) NOT NULL,
  `email` VARCHAR(512) NULL,
  `message` VARCHAR(2048) NULL);
