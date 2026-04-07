-- GENRES
INSERT INTO Genre (Name) VALUES
('Action'),
('Comedy'),
('Drama'),
('Sci-Fi'),
('Horror'),
('Animation'),
('Fantasy'),
('Thriller');

-- DIMENTIONS
INSERT INTO Dimention (ValueDimention) VALUES
('2D'),
('3D'),
('4D');

-- SCREENS
INSERT INTO Screen (NameScreen, NumberSeats, AC) VALUES
('Main Hall',120,1),
('Screen 2',80,1),
('VIP Hall',40,1),
('Classic Hall',60,0);

-- PLACES

DECLARE @screen INT = 1

WHILE @screen <= 4
BEGIN

DECLARE @row INT = 1

WHILE @row <= 8
BEGIN

DECLARE @seat INT = 1

WHILE @seat <= 10
BEGIN

INSERT INTO Place(IdScreen,RowNumber,SeatNumber)
VALUES(@screen,@row,@seat)

SET @seat = @seat + 1

END

SET @row = @row + 1

END

SET @screen = @screen + 1

END

-- FILMS

INSERT INTO Film
(Title,Director,ProductionYear,Duration,CastMembers,AgeRestriction,IdGenre,Description,AvailableTo)
VALUES

('Avengers','Joss Whedon',2012,143,'Robert Downey Jr., Chris Evans',13,1,'Marvel superhero team saves Earth','2030-01-01'),

('Interstellar','Christopher Nolan',2014,169,'Matthew McConaughey, Anne Hathaway',12,4,'Space exploration to save humanity','2030-01-01'),

('The Dark Knight','Christopher Nolan',2008,152,'Christian Bale, Heath Ledger',16,1,'Batman fights Joker','2030-01-01'),

('Frozen','Chris Buck',2013,102,'Kristen Bell, Idina Menzel',0,6,'Animated Disney musical','2030-01-01'),

('The Conjuring','James Wan',2013,112,'Patrick Wilson',18,5,'Paranormal investigators','2030-01-01'),

('Dune','Denis Villeneuve',2021,155,'Timothee Chalamet',13,7,'Sci-fi desert planet politics','2030-01-01'),

('The Matrix','Wachowski Sisters',1999,136,'Keanu Reeves',16,4,'Reality is a simulation','2030-01-01'),

('Shrek','Andrew Adamson',2001,90,'Mike Myers',0,6,'Animated ogre adventure','2030-01-01');

-- SCREENINGS

INSERT INTO Screening (IdFilm,IdScreen,IdDimention,DateTime)
VALUES
(1,1,1,'2026-05-10 18:00'),
(2,1,1,'2026-05-10 21:00'),
(3,2,1,'2026-05-10 20:00'),
(4,3,1,'2026-05-10 16:00'),
(5,2,1,'2026-05-10 23:00'),
(6,1,2,'2026-05-11 19:00'),
(7,2,1,'2026-05-11 21:00'),
(8,3,1,'2026-05-11 14:00');

-- TICKET TYPES
INSERT INTO TypeOfTicket(Type)
VALUES
('Normal'),
('Student'),
('Child'),
('Senior'),
('Family');

-- PRICE LIST
INSERT INTO PriceList(TicketPrice,Description,IdTypeOfTicket)
VALUES
(12,'Normal',1),
(9,'Student',2),
(8,'Child',3),
(8,'Senior',4),
(35,'Family Pack',5);

-- CUSTOMERS
INSERT INTO Customer(FirstName,LastName,Email,OneTime,PhoneNumber)
VALUES

('Jan','Nowak','jan.nowak@email.com',0,'500100200'),
('Anna','Kowalska','anna@email.com',0,'500100201'),
('Piotr','Zielinski','piotr@email.com',1,'500100202'),
('Maria','Wisniewska','maria@email.com',0,'500100203'),
('Adam','Lewandowski','adam@email.com',1,'500100204'),
('Julia','Kaczmarek','julia@email.com',0,'500100205'),
('Tomasz','Mazur','tomasz@email.com',1,'500100206'),
('Karolina','Piotrowska','karolina@email.com',0,'500100207');

-- GASTRONOMY
INSERT INTO Gastronomy(NameProduct,PriceProduct)
VALUES
('Popcorn Small',5),
('Popcorn Large',8),
('Nachos',7),
('Cola',4),
('Water',3),
('Hot Dog',6),
('Candy',4);

-- POSITIONS
INSERT INTO Positions(DescPositions,MinSalary,MaxSalary)
VALUES
('Cashier',3000,4000),
('Manager',6000,9000),
('Cleaner',2500,3200),
('Technician',4000,6000);

-- EMPLOYEES
INSERT INTO Employees(FirstName,LastName,Pesel,IdPositions)
VALUES
('Piotr','Kowalski','90010112345',1),
('Anna','Nowak','92030554321',1),
('Marcin','Lewandowski','88021233333',2),
('Katarzyna','Mazur','91010144444',3),
('Tomasz','Adamski','87010122222',4);

-- USERS
INSERT INTO Users(Login,PasswordHash,IdEmployees,Leader)
VALUES
('pkowalski','hashedpass',1,0),
('anowak','hashedpass',2,0),
('mlewandowski','hashedpass',3,1);

-- SHIFT PLAN
INSERT INTO ShiftPlan(IdEmployees,WorkDate,StartTime,EndTime)
VALUES
(1,'2026-05-10','08:00','16:00'),
(2,'2026-05-10','16:00','23:00'),
(3,'2026-05-10','10:00','18:00'),
(4,'2026-05-10','06:00','14:00'),
(5,'2026-05-10','12:00','20:00');

-- TICKETS
INSERT INTO Tickets(IdPriceList,IdScreening,IdCustomer,TicketPrice,IdPlace)
VALUES
(1,1,1,12,1),
(2,1,2,9,2),
(1,2,3,12,3),
(3,4,4,8,4),
(2,3,5,9,5),
(1,6,6,12,6),
(4,7,7,8,7),
(2,8,8,9,8);

-- INCOME
INSERT INTO Income
(IdTickets,IdProduct,DateTransaction,Price,Count,Value,IdCustomer,IdLogin)
VALUES
(1,NULL,'2026-05-10 17:55',12,1,12,1,1),
(2,NULL,'2026-05-10 17:56',9,1,9,2,1),
(NULL,1,'2026-05-10 18:05',5,2,10,1,1),
(NULL,4,'2026-05-10 18:07',4,2,8,2,2),
(3,NULL,'2026-05-10 20:50',12,1,12,3,2),
(4,NULL,'2026-05-10 15:45',8,1,8,4,1);

-- WORK TEAM
INSERT INTO WorkTeam(IdEmployees,NameWorkTeam)
VALUES
(1,'Ticket Service'),
(2,'Ticket Service'),
(3,'Management'),
(4,'Cleaning'),
(5,'Technical Support');
