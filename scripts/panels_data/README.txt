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
tilt - degree from zenith
width - width of panel in meters (based off each cell being 0.125m wide)
height - height of panel in meters (based off each cell being 0.125m wide)
area - area of panel in meters^2 (based off each cell having an area of roughly 0.0153m^2 -> from the data sheet) 
(note: the individual cells are not perfect squares and there are bond pads that do not absorb sunlight so there is a discrepancy 
between the area from multiplying width and height and the approximate area based off the data sheet.)

Fields and values can be changed, added, or deleted by editing the script
-----------------------------------------------------------------



