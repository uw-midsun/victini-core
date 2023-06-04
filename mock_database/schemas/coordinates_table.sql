CREATE TABLE coordinates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  coordinates POINT SRID 4326 NOT NULL,
  latitude DOUBLE NOT NULL,
  longitude DOUBLE NOT NULL,
  SPATIAL INDEX (coordinates)
);
