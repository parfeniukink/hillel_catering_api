# Purpose of a Database

1. storing data
2. providing an ornganizational structure for data
3. providing a mechanism for querying, creating, modifying, and deleting data (CRUD)
   3.1. `CRUDService`, `DALService`, `Repository`

# from where we start thinking about the data in database?

our problem is not about HOW we store the information but actually WHAT may happen to that information.

# about Database System

1. users (actors) -> real people
   - keep track of information
   - CRUD
   - inference
   - ...
2. database application (s) - software binding for DMBS (python package, go package)
3. DBMBS - software that exposes the databse itself (postgresql, mysql)
4. database (db)
   - self-describing collection of related records
   - consist of: user data, metadata, indexes, other overhead data, application metadata

**DMBS functions:**

- create db
- create tables
- read database data
- maintain database structure
- enforce rules (to regulate the control)
- control concurrency
- backup & recovery
- security

# RELATION

- ROWS are INSTANCES
- COLUMNS are ATTRIBUTES
- CELL represent a single value
- all values in the same column has the same kind (data type)
- each column has a unique name
- the order of columns and rows is unimportant
- 2 rows CAN NOT be identical (if you have similar ids for records)

# Keys...

1. Unique Key
   1. candidate key
   2. composite key
   3. primary key
   4. surrogate key
2. Non-Unique Key
   1. FOREIGN KEY

# Normalization

1. First Normal Form -> products and orders in the same table
2. Second ... -> have their own ids
3. Third -> no transitive deps...
