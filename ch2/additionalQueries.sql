-- determines number of projects per tag
-- uses 5% support threshold (2325 projects)
SELECT tag_name, COUNT( project_id ) 
FROM fc_project_tags
GROUP BY 1 
HAVING COUNT( project_id ) >= 2325
ORDER BY 2 DESC;

-- creates a view for tag and count of projects
-- using that tag
CREATE ALGORITHM = UNDEFINED 
VIEW fc_freq_tags_5pct AS 
  SELECT tag_name, COUNT( project_id ) AS num_projs
  FROM fc_project_tags
  GROUP BY 1 
  HAVING COUNT( project_id ) >= 2325
  ORDER BY 2 DESC;
  
-- creates the table to hold doubletons
CREATE TABLE IF NOT EXISTS fc_project_tag_pairs (
  tag1 varchar(255) NOT NULL,
  tag2 varchar(255) NOT NULL,
  num_projs int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- creates the table to hold tripletons
CREATE TABLE IF NOT EXISTS fc_project_tag_triples (
  tag1 varchar(255) NOT NULL,
  tag2 varchar(255) NOT NULL,
  tag3 varchar(255) NOT NULL,
  num_projs int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;