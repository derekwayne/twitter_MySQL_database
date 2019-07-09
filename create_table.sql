/*This SQL script will create the
table necessary for storing the data from
a twitter stream:*/
CREATE TABLE `twitter` (
  -- 11 digits in a twitter ID
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `tweet_id` varchar(250) DEFAULT NULL,
 `screen_name` varchar(128) DEFAULT NULL,
 `created_at` timestamp NULL DEFAULT NULL,
 `text` text,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=UTF8MB4;
