# CATERING API

# TECH STACK

- Python - programming language
- Django -web framework
- DRF (Django REST Framework) - data validation
- PostgreSQL - Database (RDBMS)
  - tables
- Redis/MongoDB - Key-value Storage
  - json {"any-key": value}
- Manage dependencies...

# SETUP

```shell
# activate virtual environment
pipenv shell --python python3.12


# generate `Pipfile.lock` file after adding dependencies
pipenv lock

# install dependencies form `Pipfile.lock` file
pipenv sync
```

# ABOUT Django & DRF

## Django concepts

1. View - endpoint (`HTTP POST /users`, create user, `UserView`, SSR (using Django Templates), MVT, Return HTML document)
2. Forms - HTML (`<input>`, SSR (using Django Templates), MVT)
3. Models - ORM (`Data Access Layer`, database tables, migrations, admin)
4. Admin - battery (SSR (using Django Templates))

## DRF concepts

1. APIViews (inherited from `View`s, implement `JsonResponse`, `Content-Type: application-json`)
2. Serializers (data validations, aka `@dataclass`)

```python
class User(models.Model):
    email = models.EmailField(...)
    password = models.CharField(...)

# http request body
class UserInputStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# public stucture
class UserOutputStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserAPIView(generics.EverythingAPIView):
    model = User
    serializer_class = UserSerializser
    pk = "id"


urlpatterns = [
    path("users/", UserAPIView.as_view())
]

# HTTP POST /users
#   RequestBody: __all__
# HTTP GET /users
#   list[User]
# HTTP GET /users/7
#   User
# HTTP PUT /users/7
#   RequestBody: first_name, last_name
#   User
# HTTP DELETE /users/7
#   204
```
