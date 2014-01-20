CREATE DATABASE IF NOT EXISTS `firefly_helloworld`;

USE `firefly_helloworld`;

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL COMMENT 'user name',
  `password` varchar(255) NOT NULL COMMENT 'user password',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

