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

# CheatSheet

**Transaction Commands**

| Command                   | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `START TRANSACTION;`      | Begins a transaction                           |
| `COMMIT;`                 | Saves changes permanently                      |
| `ROLLBACK;`               | Undoes changes since last `START TRANSACTION;` |
| `SAVEPOINT point_name;`   | Creates a rollback point inside a transaction  |
| `ROLLBACK TO point_name;` | Rolls back to a specific savepoint             |

**Safe Order Processing**

```sql
START TRANSACTION;

-- Insert order
INSERT INTO orders (customer_id, total_price, order_status)
VALUES (5, 45.99, 'pending');

-- Reduce stock
UPDATE inventory SET stock_quantity = stock_quantity - 2
WHERE ingredient_id = 10;

-- Check for negative stock
IF (SELECT COUNT(*) FROM inventory WHERE stock_quantity < 0) > 0 THEN
    ROLLBACK; -- Undo everything if stock is insufficient
ELSE
    COMMIT; -- Finalize order
END IF;
```

**Types of Joins**

| Join Type    | Description                                     | Example                            |
| ------------ | ----------------------------------------------- | ---------------------------------- |
| `INNER JOIN` | Returns only **matching** rows                  | Orders with Customers              |
| `LEFT JOIN`  | Returns **all** from left + matching from right | All Customers, even without Orders |
| `RIGHT JOIN` | Returns **all** from right + matching from left | All Orders, even without Customers |
| `FULL JOIN`  | Returns **all** rows, even if there's no match  | Every record from both tables      |
| `CROSS JOIN` | Returns **every combination** of both tables    | All menu items + All ingredients   |

**Best Practices**

- use transactions only if multiple queries depend on each other
- test joins with `LIMIT` before using them in complex queries
- Use `EXPLAIN` to check performance on large joins
- normalize database design to avoid unnecessary joins
- denormalize database design to provide better performance
- ensure indexes exist on foreign keys for faster joins
