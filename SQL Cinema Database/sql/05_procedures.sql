-- Selling the tickets

CREATE PROCEDURE sp_SellTicket
(
    @ScreeningId INT,
    @SeatId INT,
    @CustomerId INT,
    @PriceListId INT
)
AS
BEGIN

SET NOCOUNT ON;

DECLARE @available INT

SELECT @available = dbo.fn_AvailableSeats(@ScreeningId)

IF @available <= 0
BEGIN
    RAISERROR('No seats available',16,1)
    RETURN
END

IF EXISTS (
    SELECT 1
    FROM Tickets
    WHERE IdScreening=@ScreeningId
    AND IdPlace=@SeatId
)
BEGIN
    RAISERROR('Seat already sold',16,1)
    RETURN
END

INSERT INTO Tickets
(
    IdPriceList,
    IdScreening,
    IdCustomer,
    TicketPrice,
    IdPlace
)
SELECT
    IdPriceList,
    @ScreeningId,
    @CustomerId,
    TicketPrice,
    @SeatId
FROM PriceList
WHERE IdPriceList=@PriceListId

END

-- Daily Revenue

CREATE PROCEDURE sp_DailyRevenue
(
    @Date DATE
)
AS
BEGIN

SELECT
    SUM(Value) AS TotalRevenue,
    COUNT(IdTransaction) AS Transactions
FROM Income
WHERE CAST(DateTransaction AS DATE) = @Date

END

-- Top Movies

CREATE PROCEDURE sp_TopMovies
AS
BEGIN

SELECT TOP 10
    F.Title,
    COUNT(T.IdTicket) AS TicketsSold
FROM Tickets T
JOIN Screening S ON T.IdScreening=S.IdScreening
JOIN Film F ON S.IdFilm=F.IdFilm
GROUP BY F.Title
ORDER BY TicketsSold DESC

END


