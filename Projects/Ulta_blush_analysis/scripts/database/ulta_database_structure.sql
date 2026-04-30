USE master;
GO

-- === CREATE DATABASE ===
DROP DATABASE IF EXISTS ulta_blushes; -- drop database if it's already exist
CREATE DATABASE ulta_blushes; -- create a new database
GO
USE ulta_blushes; -- use the newly created database
GO

-- === CREATE TABLE ===
CREATE TABLE blushes(
   shade_url         VARCHAR(104) NOT NULL PRIMARY KEY
  ,brand             VARCHAR(23) NOT NULL
  ,product_name      VARCHAR(57) NOT NULL
  ,shade             VARCHAR(65) NOT NULL
  ,swatch_img_url    VARCHAR(74) NOT NULL
  ,swatch_alt        VARCHAR(78) NOT NULL
  ,description       VARCHAR(82)
  ,price             NUMERIC(5,2) NOT NULL
  ,standard_value    NUMERIC(5,2) NOT NULL
  ,standard_unit     VARCHAR(2) NOT NULL
  ,product_id        INTEGER  NOT NULL
  ,shade_id          INTEGER  NOT NULL
  ,product_image_url VARCHAR(61) NOT NULL
);
GO

-- SELECT * FROM blushes;