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

- User Management (CRUD for `/users`). EPIC (from Jira)

  - Entdpoints to implement:

    - USER STORY (from Jira)

      - `HTTP POST /users` - create user -> `201 Use[USER]`
      - `HTTP PUT /users/ID` - update user -> `200 User[USER,ADMIN]`
      - `HTTP GET /users` - get user -> `200 User[USER,ADMIN]`
      - `HTTP DELETE /users/ID` - delete user -> `204 [USER]`

      - `HTTP POST /users/passowrd/forgot` -> `KEY[UUID]`
      - `HTTP POST /users/passowrd/change?key=UUID&creds={}` -> 200

  - Roles:
    - ADMIN
    - SUPPORT
    - CLIENT
    - DRIVER

- Authentication & Authorization

  - `HTTP POST /token [USER,ADMIN]`

- Dishes Management

  - `HTTP POST /dishes` - create a new dish `[ADMIN]`
  - `HTTP GET /dishes` - list all dishes `[ADMIN,USER,SUPPORT]`
  - `HTTP GET /dishes/ID` - retrieve dish `[ADMIN,USER,SUPPORT]`
  - `HTTP PUT /dishes/ID` - update dish `[ADMIN]`
  - `HTTP DELETE /dishes/ID` - delete dish `[ADMIN]`

  - Refresh the data from restaurants

    - as a `Thread(daemon=True)`

  - Display of recommended dishes for events (_v2_)

- Orders Management (includes delivery management in a background)

  - `HTTP POST /orders` - create a new order `[USER]`
    - `{dishes: list[OrderDish]}`
  - `HTTP GET /orders` - list all orders `[ADMIN,SUP]`
  - `HTTP GET /orders/ID` - retrieve dish `[ADMIN,USER,SUP]`
  - `HTTP PUT /orders/ID` - update dish `[ADMIN,SUP]`
  - `HTTP DELETE /orders/ID` - delete dish `[ADMIN,SUP]`
  - `HTTP POST /orders/ID/reorder` - reorder failed order `[ADMIN,SUP]`
    - check if status is `failed`

Order Public Contract

```python
enum Provider:
    UKLON
    UBER


class Delivery:
    provider: Provider
    coordinates: list[float, float]


class Cooking:
    comments: str

enum State:
    WAITING
    COOKING
    DELIVERY
    DELIVERED
    FAILED
    CANCELED_BY_CLIENT
    CANCELED_BY_DELIVERY
    CANCELED_BY_REST
    WAITING_ADMIN_APPROVE


class Order:
    id: UUID
    state: State
    total: int
    cooking: CookingInfo | None = None
    delivery: DeliveryInfo | None = None
```

```
# INVALID APPROACH
# HTTP POST order(dishes) -> DB_SAVE -> ORDER REST (ORDER) -> CALLBACK -> ORDER DELIVERY (REST, CLIENT) -> RESULT
```

- Payment Processing

  - TODO...

- Communication and Support
  - `HTTP POST /support/issues/orders/ID` - issue the order question...
    - `{message: str, photos: list[bytes]}`
    - `[USER]`
