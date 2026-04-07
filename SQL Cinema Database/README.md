# Cinema Database – SQL Project

A relational database project designed to simulate the core operations of a cinema management system.

The database allows storing and managing information about:

* movies
* cinema halls
* screenings
* customers
* tickets

The project demonstrates fundamental **SQL database design principles**, including normalization, primary and foreign keys, and relational queries.

---

# Project Overview

Cinema management systems rely on relational databases to organize information about movies, showtimes, tickets, and customers.

This project implements a simplified **cinema database schema** and demonstrates how SQL can be used to:

* manage movie screenings
* store ticket information
* track customer reservations
* query cinema schedules

---

# Database Schema

The database consists of several interconnected tables.

Example entities:

* **Movies** – information about films shown in the cinema
* **Cinema_Halls** – rooms where screenings take place
* **Screenings** – specific movie showtimes
* **Customers** – people purchasing tickets
* **Tickets** – purchased seats for a screening

Relationships include:

* One movie → many screenings
* One hall → many screenings
* One screening → many tickets
* One customer → many tickets

---

# Database Structure

Example structure:

```
cinema-database/
│
├── schema.sql
├── sample_data.sql
├── queries.sql
└── README.md
```

---

# Technologies Used

* SQL
* Relational database design
* Database normalization
* Query optimization

Compatible with:

* MySQL
* PostgreSQL
* SQLite

---

# Example SQL Queries

Example operations implemented in this project:

### List all movies currently scheduled

```sql
SELECT title, duration
FROM Movies;
```

### Show all screenings for a specific movie

```sql
SELECT m.title, s.screening_time
FROM Screenings s
JOIN Movies m ON s.movie_id = m.id
WHERE m.title = 'Inception';
```

### List purchased tickets with customer names

```sql
SELECT c.name, m.title, s.screening_time
FROM Tickets t
JOIN Customers c ON t.customer_id = c.id
JOIN Screenings s ON t.screening_id = s.id
JOIN Movies m ON s.movie_id = m.id;
```

---

# Key Learning Goals

This project demonstrates:

* relational database modeling
* entity-relationship design
* SQL joins
* data integrity using constraints
* querying relational data

---

# How to Run the Project

1. Create a new database:

```sql
CREATE DATABASE cinema_db;
```

2. Run schema file:

```bash
mysql -u username -p cinema_db < schema.sql
```

3. Insert sample data:

```bash
mysql -u username -p cinema_db < sample_data.sql
```

4. Run example queries.

---

# Author

SQL database project created as part of early database learning and practice with relational schema design.
