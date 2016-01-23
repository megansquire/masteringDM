CREATE TABLE IF NOT EXISTS `book_entity_matches` (
  `rf_project_name` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `rg_project_name` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `url_levenshtein` int(11) DEFAULT NULL,
  `rf_name_soundex` varchar(5) CHARACTER SET latin1 DEFAULT NULL,
  `rg_name_soundex` varchar(5) CHARACTER SET latin1 DEFAULT NULL,
  `name_levenshtein` int(11) DEFAULT NULL,
  `rf_name_in_rg_name` tinyint(1) DEFAULT NULL,
  `rf_name_in_rg_url` tinyint(1) DEFAULT NULL,
  `rf_dev_in_rg_dev` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`rf_project_name`,`rg_project_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
