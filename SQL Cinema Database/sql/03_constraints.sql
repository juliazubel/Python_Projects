ALTER TABLE Film
ADD CONSTRAINT FK_Film_Genre
FOREIGN KEY (IdGenre) REFERENCES Genre(IdGenre);

ALTER TABLE Screening
ADD CONSTRAINT FK_Screening_Film
FOREIGN KEY (IdFilm) REFERENCES Film(IdFilm);

ALTER TABLE Screening
ADD CONSTRAINT FK_Screening_Screen
FOREIGN KEY (IdScreen) REFERENCES Screen(IdScreen);

ALTER TABLE Screening
ADD CONSTRAINT FK_Screening_Dimention
FOREIGN KEY (IdDimention) REFERENCES Dimention(IdDimention);

ALTER TABLE Place
ADD CONSTRAINT FK_Place_Screen
FOREIGN KEY (IdScreen) REFERENCES Screen(IdScreen);

ALTER TABLE Tickets
ADD CONSTRAINT FK_Tickets_Screening
FOREIGN KEY (IdScreening) REFERENCES Screening(IdScreening);

ALTER TABLE Tickets
ADD CONSTRAINT FK_Tickets_Place
FOREIGN KEY (IdPlace) REFERENCES Place(IdPlace);

ALTER TABLE Tickets
ADD CONSTRAINT FK_Tickets_Customer
FOREIGN KEY (IdCustomer) REFERENCES Customer(IdCustomer);

ALTER TABLE Employees
ADD CONSTRAINT FK_Employees_Positions
FOREIGN KEY (IdPositions) REFERENCES Positions(IdPositions);
