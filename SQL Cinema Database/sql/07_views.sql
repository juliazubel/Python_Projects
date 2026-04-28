-- Screenings for a given day
CREATE OR ALTER VIEW [ScreeningsForAGivenDay] 
AS
SELECT Title
		,Dimention.ValueDimention
		, Duration,convert(date,DateTime) AS 'Date'
		,convert(time,DateTime) AS 'Hour' 
FROM Screening
JOIN Film ON Screening.IdFilm=Film.IdFilm
JOIN Dimention ON Dimention.IdDimention=Screening.IdDimention
JOIN Screen ON Screen.IdScreen=Screening.IdScreen
WHERE DateTime>getdate()-30 AND DateTime<=getdate()+30


-- Movies for kids
CREATE OR ALTER VIEW [FilmsForKids] AS
SELECT Title
FROM Film
WHERE AgeRestriction < 18

-- Movies for adults
CREATE OR ALTER VIEW [FilmsForAdults] AS
SELECT Title
FROM Film
WHERE AgeRestriction = 18

-- Movies from 2021
CREATE OR ALTER VIEW [Films2021] AS
SELECT f.Title, f.Director, g.Name as Genre
FROM Film f
LEFT OUTER JOIN Genre g On f.idGenre = g.idGenre
WHERE ProductionYear = 2021;

-- Available Seats
CREATE OR ALTER VIEW [AvailableSeats]
AS
SELECT Screening.IdScreening
	, Title
	, Dimention.ValueDimention
	, Duration
	, convert(date,DateTime) AS 'Date'
	, convert(time,DateTime) AS 'Hour'
	, CASE WHEN dbo.fn_AvailableSeats(IdScreening)=0 THEN 'No places' ELSE 'Seats available' END AS 'Available Seats'
	, dbo.fn_AvailableSeats(IdScreening) AS 'Kod' 
FROM Screening
JOIN Film ON Screening.IdFilm=Film.IdFilm
JOIN Dimention ON Dimention.IdDimention=Screening.IdDimention
JOIN Screen ON Screen.IdScreen=Screening.IdScreen
GO

-- One time customer
CREATE OR ALTER VIEW [OneTimeCustomer]
AS
SELECT IdCustomer, FirstName, LastName 
FROM Customer
WHERE OneTime=1
GO

-- Regular Customer
CREATE OR ALTER VIEW [RegularCustomer]
AS
SELECT IdCustomer, FirstName, LastName 
FROM Customer
WHERE OneTime=0
GO
