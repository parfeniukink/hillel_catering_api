# PEOPLE

1. Dima - developer (implementor)
2. Carl - client (ADMIN)
3. Martin - Melange
4. Bob - Bueno
5. John - user1 (USER)
6. Marry - user2 (USER)

# PROJECT MANAGEMENT

1. Waterfall
2. Scrum - sprint

MEETINGS

1. daily
2. refinement
3. grooming (BIG BUSINESS PROBLEM -> small technical features)
4. task

# INPUT DATA

we already have the frontend application. only the backend API is left...

# BACKLOG

- User Management (CRUD for `/users`)

  - Entdpoints to implement:

    - `HTTP POST /users` - create user -> `201 User[USER]`
    - `HTTP PUT /users/ID` - update user -> `200 User[USER,ADMIN]`
    - `HTTP GET /users` - get user -> `200 User[USER,ADMIN]`
    - `HTTP DELETE /users/ID` - delete user -> `204 [USER]`

    - `HTTP POST /users/passowrd/forgot` -> `KEY[UUID]`
    - `HTTP POST /users/passowrd/change?key=UUID&creds={}` -> 200

  - Roles:
    - ADMIN
    - USER
    - SUPPORT

- Authentication & Authorization

  - `HTTP POST /token [USER,ADMIN]`

- Dishes Management

  - `HTTP POST /dishes` - create a new dish `[ADMIN]`
  - `HTTP GET /dishes` - list all dishes `[ADMIN,USER]`
  - `HTTP GET /dishes/ID` - retrieve dish `[ADMIN,USER]`
  - `HTTP PUT /dishes/ID` - update dish `[ADMIN]`
  - `HTTP DELETE /dishes/ID` - delete dish `[ADMIN]`

  - Refresh the data from restaurants

    - as a `Thread(daemon=True)`

  - Display of recommended dishes for events (_v2_)

- Orders Management

  - `HTTP POST /orders` - create a new order `[USER]`
    - `{dishes: list[OrderDish]}`
  - `HTTP GET /orders` - list all orders `[ADMIN,SUP]`
  - `HTTP GET /orders/ID` - retrieve dish `[ADMIN,USER]`
  - `HTTP PUT /orders/ID` - update dish `[ADMIN]`
  - `HTTP DELETE /orders/ID` - delete dish `[ADMIN]`
  - `HTTP POST /orders/ID/reorder` - reorder failed order `[ADMIN,SUP]`
    - check if status is `failed`

- Delivery Management
- Payment Processing

- Communication and Support
  - `HTTP POST /support/issues/orders/ID` - issue the order question...
    - `{message: str, photos: list[bytes]}`
    - `[USER]`
