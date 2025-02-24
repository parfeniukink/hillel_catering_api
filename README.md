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

# HASH FUNCTIONS

## ATTRIBUTES

1. fixed size (string)
2. fast
3. avalanche (лавиноподібність)
   3.1 john -> 527bd5b5d689e2c32ae974c6229ff785
   3.1 john1 -> e06ce282ec5c0f9701ec03d10690b2af
   3.1 johna -> aa8e7e8c8894f55dceb668662106bc7a
4. collision-free
5. determined (john hash always the same)

## LIST

1. MD5
2. SHA1
3. SHA2
4. SHA3

# ViewSets

```python
class UserViewSet(viewsets.ViewSet):
    def list(self, request):  # HTTP GET /users
        pass

    def create(self, request): # HTTP POST /users
        pass

    def retrieve(self, request, pk=None): # HTTP GET /users/pk
        pass

    def update(self, request, pk=None): # HTTP PUT /users/pk
        pass

    def partial_update(self, request, pk=None):  # HTTP PATCH /users/pk
        pass

    def destroy(self, request, pk=None): # HTTP DELETE /users/pk
        pass
```

# Old Code

## create user FBV

```python
import json
def create_user(request):
    if request.method != "POST":
        raise NotImplementedError
    data = json.loads(request.body)
    uesr = User.objects.create_user(**data)
    results = {
        "id": user.id,
        "email": user.email,
    }
    return JsonResponse(results)


1 - bad idea
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistratrionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

    def save(self):
        self.model.save()
```



# PROJECT INFRASTRUCTURE

1. application (Python, Django (FastAPI))
2. database (SQLite3, PosgreSQL)
3. cache (Redis, Memcached, Valkey)
4. worker (Python, RQ, Celery)
5. queue (broker, RabbitMQ, SQS, Redis)

