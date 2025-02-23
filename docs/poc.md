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
      - `HTTP GET /users` - get user -> `200 User[USER,ADMIN]`

      - `HTTP PUT /users/ID` - update user -> `200 User[USER,ADMIN]`
      - `HTTP DELETE /users/ID` - delete user -> `204 [USER]`
      - `HTTP POST /users/passowrd/forgot` -> `KEY[UUID]`
      - `HTTP POST /users/passowrd/change?key=UUID&creds={}` -> 200

  - Roles:
    - ADMIN
    - SUPPORT
    - CLIENT
    - DRIVER

- Authentication & Authorization
  - `HTTP POST /auth/token [USER,ADMIN]`

- Food tier
  - Endpoints
    - `HTTP GET /food/restaurants` - list of restaurants with dishes
    - `HTTP GET /food/dishes` - list of dishes
    - `HTTP GET /food/dishes/ID` - retrieve dish
    - `HTTP POST /food/orders` - create the order
    - `HTTP GET /food/orders/ID` - retrieve the order
    - `HTTP POST /food/orders/ID/reorder` - reorder failed order `[ADMIN,SUP]`
  - Refresh the data from restaurants
    - as a `Thread(daemon=True)`
  - Display of recommended dishes for events (_v2_)

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
