-- Checking if movie is still available

CREATE FUNCTION fn_IsFilmAvailable(@FilmId INT)
RETURNS BIT
AS
BEGIN
    DECLARE @result BIT

    SELECT @result =
        CASE
            WHEN AvailableTo >= GETDATE() THEN 1
            ELSE 0
        END
    FROM Film
    WHERE IdFilm = @FilmId

    RETURN @result
END

-- Checking available seats

CREATE FUNCTION fn_AvailableSeats(@ScreeningId INT)
RETURNS INT
AS
BEGIN

    DECLARE @TotalSeats INT
    DECLARE @SoldSeats INT

    SELECT @TotalSeats = COUNT(*)
    FROM Place P
    JOIN Screening S ON P.IdScreen = S.IdScreen
    WHERE S.IdScreening = @ScreeningId

    SELECT @SoldSeats = COUNT(*)
    FROM Tickets
    WHERE IdScreening = @ScreeningId

    RETURN (@TotalSeats - @SoldSeats)

END

