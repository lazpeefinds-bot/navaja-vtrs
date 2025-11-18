-- Election Database Schema
-- Drop tables if they exist
DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS voters;
DROP TABLE IF EXISTS positions;

-- Create Positions Table
CREATE TABLE positions (
    posID INTEGER PRIMARY KEY AUTOINCREMENT,
    posName VARCHAR(100) NOT NULL,
    numOfPositions INTEGER NOT NULL DEFAULT 1,
    posStat VARCHAR(10) NOT NULL DEFAULT 'open'
);

-- Create Voters Table
CREATE TABLE voters (
    voterID VARCHAR(50) PRIMARY KEY,
    voterPass VARCHAR(255) NOT NULL,
    voterFName VARCHAR(100) NOT NULL,
    voterMName VARCHAR(100),
    voterLName VARCHAR(100) NOT NULL,
    voterStat VARCHAR(10) NOT NULL DEFAULT 'active',
    voted VARCHAR(1) NOT NULL DEFAULT 'N'
);

-- Create Candidates Table
CREATE TABLE candidates (
    candID INTEGER PRIMARY KEY AUTOINCREMENT,
    candFName VARCHAR(100) NOT NULL,
    candLName VARCHAR(100) NOT NULL,
    posID INTEGER NOT NULL,
    candStat VARCHAR(10) NOT NULL DEFAULT 'active',
    FOREIGN KEY (posID) REFERENCES positions(posID)
);

-- Create Votes Table
CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posID INTEGER NOT NULL,
    voterID VARCHAR(50) NOT NULL,
    candID INTEGER NOT NULL,
    FOREIGN KEY (posID) REFERENCES positions(posID),
    FOREIGN KEY (voterID) REFERENCES voters(voterID),
    FOREIGN KEY (candID) REFERENCES candidates(candID)
);

-- Insert Sample Positions
INSERT INTO positions (posName, numOfPositions, posStat) VALUES
('President', 1, 'open'),
('Vice President', 1, 'open'),
('Secretary', 1, 'open'),
('Treasurer', 1, 'open'),
('Senator', 12, 'open'),
('Councilor', 6, 'open');

-- Insert Sample Voters
INSERT INTO voters (voterID, voterPass, voterFName, voterMName, voterLName, voterStat, voted) VALUES
('2021-0001', 'pass123', 'Juan', 'Santos', 'Dela Cruz', 'active', 'N'),
('2021-0002', 'pass123', 'Maria', 'Garcia', 'Reyes', 'active', 'N'),
('2021-0003', 'pass123', 'Jose', 'Miguel', 'Gonzales', 'active', 'N'),
('2021-0004', 'pass123', 'Ana', 'Isabel', 'Santos', 'active', 'N'),
('2021-0005', 'pass123', 'Pedro', 'Luis', 'Cruz', 'active', 'N'),
('2021-0006', 'pass123', 'Elena', 'Marie', 'Torres', 'active', 'N'),
('2021-0007', 'pass123', 'Miguel', 'Angel', 'Flores', 'active', 'N'),
('2021-0008', 'pass123', 'Sofia', 'Grace', 'Rivera', 'active', 'N'),
('2021-0009', 'pass123', 'Carlos', 'Rey', 'Mendoza', 'active', 'N'),
('2021-0010', 'pass123', 'Isabel', 'Joy', 'Ramos', 'active', 'N'),
('2021-0011', 'pass123', 'Diego', 'Paul', 'Sanchez', 'inactive', 'N'),
('2021-0012', 'pass123', 'Carmen', 'Rose', 'Morales', 'active', 'N');

-- Set sample voters to inactive
UPDATE voters
SET voterStat = 'active'
WHERE voterID IN (
    '2021-0001','2021-0002','2021-0003','2021-0004','2021-0005','2021-0006',
    '2021-0007','2021-0008','2021-0009','2021-0010','2021-0011','2021-0012'
);

-- Insert Sample Candidates for President
INSERT INTO candidates (candFName, candLName, posID, candStat) VALUES
('Roberto', 'Martinez', 1, 'active'),
('Linda', 'Aquino', 1, 'active'),
('Fernando', 'Castro', 1, 'active');

-- Insert Sample Candidates for Vice President
INSERT INTO candidates (candFName, candLName, posID, candStat) VALUES
('Gloria', 'Bautista', 2, 'active'),
('Ricardo', 'Villanueva', 2, 'active'),
('Patricia', 'Fernandez', 2, 'active');

-- Insert Sample Candidates for Secretary
INSERT INTO candidates (candFName, candLName, posID, candStat) VALUES
('Antonio', 'Lopez', 3, 'active'),
('Marissa', 'Garcia', 3, 'active');

-- Insert Sample Candidates for Treasurer
INSERT INTO candidates (candFName, candLName, posID, candStat) VALUES
('Manuel', 'Santiago', 4, 'active'),
('Teresa', 'Domingo', 4, 'active');

-- Insert Sample Candidates for Senator (12 positions)
INSERT INTO candidates (candFName, candLName, posID, candStat) VALUES
('Alberto', 'Navarro', 5, 'active'),
('Beatriz', 'Herrera', 5, 'active'),
('Carlos', 'Jimenez', 5, 'active'),
('Diana', 'Ortiz', 5, 'active'),
('Eduardo', 'Romero', 5, 'active'),
('Francisca', 'Guerrero', 5, 'active'),
('Gabriel', 'Medina', 5, 'active'),
('Helena', 'Vargas', 5, 'active'),
('Ignacio', 'Silva', 5, 'active'),
('Julia', 'Ruiz', 5, 'active'),
('Lorenzo', 'Moreno', 5, 'active'),
('Magdalena', 'Gutierrez', 5, 'active'),
('Nicolas', 'Campos', 5, 'active'),
('Olivia', 'Delgado', 5, 'active'),
('Pablo', 'Castillo', 5, 'active');

-- Insert Sample Candidates for Councilor (6 positions)
INSERT INTO candidates (candFName, candLName, posID, candStat) VALUES
('Rafael', 'Alvarez', 6, 'active'),
('Silvia', 'Ramirez', 6, 'active'),
('Tomas', 'Mendez', 6, 'active'),
('Valentina', 'Perez', 6, 'active'),
('Xavier', 'Nunez', 6, 'active'),
('Yolanda', 'Salazar', 6, 'active'),
('Zachary', 'Velasco', 6, 'active'),
('Andrea', 'Suarez', 6, 'active');
