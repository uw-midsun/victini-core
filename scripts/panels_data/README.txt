Python script to upload solar panel data to PostgreSQL database
---------------------------------------------------------------
Based on this information: https://uwmidsun.atlassian.net/wiki/x/HgAnsQ

Fields:
id - autoincrementing integer value, do not input manually
name - name of solar panel, naming scheme goes from back --> front, imagine that you are standing in front of the car and looking at it
  *if another naming scheme is preferred, feel free to change it
stack - which stack the panel belongs to
efficiency - how efficient the panels are
  *currently set to 0.25, change if necessary
num_panels - how many panels it is made up of
title  - degree from zenith

Fields and values can be changed, added, or deleted by editing the script

CREATE TABLE documentation: https://www.postgresql.org/docs/current/sql-createtable.html
INSERT documentation: https://www.postgresql.org/docs/current/sql-insert.html
