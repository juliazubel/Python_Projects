-- No double seats

CREATE TRIGGER trg_NoDoubleSeat
ON Tickets
AFTER INSERT
AS
BEGIN

IF EXISTS (
    SELECT IdScreening, IdPlace
    FROM Tickets
    GROUP BY IdScreening, IdPlace
    HAVING COUNT(*) > 1
)
BEGIN
    RAISERROR('Seat already taken',16,1)
    ROLLBACK TRANSACTION
END

END

-- Calculate Income

CREATE TRIGGER trg_CalculateIncome
ON Income
AFTER INSERT
AS
BEGIN

UPDATE Income
SET Value = Price * Count
WHERE IdTransaction IN (SELECT IdTransaction FROM inserted)

END

-- Age validation

CREATE TRIGGER trg_CheckAgeRestriction
ON Tickets
AFTER INSERT
AS
BEGIN

IF EXISTS (
SELECT 1
FROM inserted i
JOIN Screening s ON i.IdScreening=s.IdScreening
JOIN Film f ON s.IdFilm=f.IdFilm
JOIN Customer c ON i.IdCustomer=c.IdCustomer
WHERE f.AgeRestriction >=18
)
BEGIN
PRINT 'Warning: movie for adults'
END

END

