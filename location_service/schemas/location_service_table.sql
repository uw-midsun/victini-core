CREATE TABLE coordinates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  coordinates POINT SRID 4326 NOT NULL,
  latitude DECIMAL(9, 6) NOT NULL,
  longitude DECIMAL(9, 6) NOT NULL,
  SPATIAL INDEX (coordinates)
);
