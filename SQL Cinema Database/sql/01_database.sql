USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'Cinema')
DROP DATABASE Cinema;
GO

CREATE DATABASE Cinema;
GO

USE Cinema;
GO
