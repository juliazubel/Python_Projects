CREATE TABLE Genre (
    IdGenre INT IDENTITY PRIMARY KEY,
    Name VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE Dimention (
    IdDimention INT IDENTITY PRIMARY KEY,
    ValueDimention VARCHAR(10) NOT NULL
);

CREATE TABLE Film (
    IdFilm INT IDENTITY PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    Director VARCHAR(100) NOT NULL,
    ProductionYear INT NOT NULL,
    Duration INT NOT NULL,
    CastMembers VARCHAR(MAX),
    AgeRestriction INT,
    IdGenre INT NOT NULL,
    Description VARCHAR(MAX),
    AvailableTo DATE NOT NULL
);

CREATE TABLE Screen (
    IdScreen INT IDENTITY PRIMARY KEY,
    NameScreen VARCHAR(50),
    NumberSeats INT NOT NULL,
    AC BIT
);

CREATE TABLE Place (
    IdPlace INT IDENTITY PRIMARY KEY,
    IdScreen INT NOT NULL,
    RowNumber INT NOT NULL,
    SeatNumber INT NOT NULL
);

CREATE TABLE Screening (
    IdScreening INT IDENTITY PRIMARY KEY,
    IdFilm INT NOT NULL,
    IdScreen INT NOT NULL,
    IdDimention INT,
    DateTime DATETIME NOT NULL
);

CREATE TABLE TypeOfTicket (
    IdTypeOfTicket INT IDENTITY PRIMARY KEY,
    Type VARCHAR(200) NOT NULL
);

CREATE TABLE PriceList (
    IdPriceList INT IDENTITY PRIMARY KEY,
    TicketPrice MONEY NOT NULL,
    Description VARCHAR(50),
    IdTypeOfTicket INT
);

CREATE TABLE Customer (
    IdCustomer INT IDENTITY PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(100),
    Email VARCHAR(100),
    OneTime BIT,
    PhoneNumber VARCHAR(20)
);

CREATE TABLE Tickets (
    IdTicket INT IDENTITY PRIMARY KEY,
    IdPriceList INT,
    IdScreening INT,
    IdCustomer INT,
    TicketPrice MONEY,
    IdPlace INT
);

CREATE TABLE Gastronomy (
    IdProduct INT IDENTITY PRIMARY KEY,
    NameProduct VARCHAR(200),
    PriceProduct MONEY
);

CREATE TABLE Positions (
    IdPositions INT IDENTITY PRIMARY KEY,
    DescPositions VARCHAR(50),
    MinSalary MONEY,
    MaxSalary MONEY
);

CREATE TABLE Employees (
    IdEmployees INT IDENTITY PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(100),
    Pesel VARCHAR(11),
    IdPositions INT
);

CREATE TABLE Users (
    IdLogin INT IDENTITY PRIMARY KEY,
    Login VARCHAR(50),
    PasswordHash VARCHAR(200),
    IdEmployees INT,
    Leader BIT
);

CREATE TABLE ShiftPlan (
    IdShiftPlan INT IDENTITY PRIMARY KEY,
    IdEmployees INT,
    WorkDate DATE,
    StartTime TIME,
    EndTime TIME
);

CREATE TABLE Income (
    IdTransaction INT IDENTITY PRIMARY KEY,
    IdTickets INT,
    IdProduct INT,
    DateTransaction DATETIME,
    Price MONEY,
    Count INT,
    Value MONEY,
    IdCustomer INT,
    IdLogin INT
);

CREATE TABLE WorkTeam (
    IdWorkTeam INT IDENTITY PRIMARY KEY,
    IdEmployees INT,
    NameWorkTeam VARCHAR(50)
);
