# Cinema Database – SQL Project

A relational database project designed to simulate the core operations of a cinema management system.

The database allows storing and managing information about:

* movies
* screenings
* customers
* tickets
etc.

The project demonstrates fundamental **SQL database design principles**, including normalization, primary and foreign keys, and relational queries.

---

# ER Diagram

![ER Diagram](https://github.com/juliazubel/Projects/blob/main/SQL%20Cinema%20Database/cinemaER.png)

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
SQL Cinema Database/
│
├── sql
  ├───-- 01_database.sql
  ├───-- 02_tables.sql
  ├───-- 03_constraints.sql
  ├───-- 04_functions.sql
  ├───-- 05_views.sql
  ├───-- 06_procedures.sql
  ├───-- 07_triggers.sql
  └───-- 08_sample_data.sql
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

# Key Learning Goals

This project demonstrates:

* relational database modeling
* entity-relationship design
* SQL joins
* data integrity using constraints
* querying relational data
* complex triggers and procedures


---

# Author

SQL database project created as part of early database learning and practice with relational schema design.
