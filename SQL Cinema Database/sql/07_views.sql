-- Screenings for a given day
CREATE OR ALTER VIEW [ScreeningsForAGivenDay] AS
SELECT IdScreening FROM Screening
WHERE DateTime = getdate(); SELECT Title,Dimention.ValueDimention, Duration,convert(date,DateTime)
’Data’ ,convert(time,DateTime)’Godzina’ FROM Screening
JOIN Film ON Screening.IdFilm=Film.IdFilm
JOIN Dimention ON Dimention.IdDimention=Screening.IdDimention
JOIN Screen ON Screen.IdScreen=Screening.IdScreen
WHERE DateTime>getdate()-30 AND DateTime<=getdate()+30
ORDER BY convert(date,DateTime),convert(time,DateTime)


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
SELECT Title, Director, Genre
FROM Film
WHERE ProductionYear = 2021;

-- Available Seats
CREATE OR ALTER VIEW [AvailableSeats]
AS
SELECT Screening.IdScreening, Title, Dimention.ValueDimention, Duration, convert(date,DateTime) ’Data’,
convert(time,DateTime)’Godzina’, CASE WHEN dbo.fnSeatForScreening(IdScreening)=0 THEN ’Brak miejsc’ ELSE
’Sprzedaz dostepna’ END
’Status’,dbo.fnSeatForScreening(IdScreening) ’Kod’ FROM Screening
JOIN Film ON Screening.IdFilm=Film.IdFilm
JOIN Dimention ON Dimention.IdDimention=Screening.IdDimention
JOIN Screen ON Screen.IdScreen=Screening.IdScreen
GO

-- One time customer
CREATE OF ALTER VIEW [OneTimeCustomer]
AS
SELECT IdCustomer, FirstName, LastName FROM Customer
WHERE OneTime=1
GO

-- Regular Customer
CREATE OF ALTER VIEW [RegularCustomer]
AS
SELECT IdCustomer, FirstName, LastName FROM Customer
WHERE OneTime=0
GO
