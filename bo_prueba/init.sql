CREATE DATABASE PortalTest;
GO
USE PortalTest;
GO
CREATE TABLE usuarios (
    id INT IDENTITY PRIMARY KEY,
    username NVARCHAR(50) NOT NULL,
    password NVARCHAR(100) NOT NULL
);
GO
INSERT INTO usuarios (username, password) VALUES ('admin', 'admin');
