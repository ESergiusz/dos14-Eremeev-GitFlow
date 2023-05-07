import json
import yaml

class Permissions:
    def __init__(self, create=False, read=False, update=False, delete=False):
        self._create = create
        self._read = read
        self._update = update
        self._delete = delete

    def to_dict(self):
        return {
            'create': self._create,
            'read': self._read,
            'update': self._update,
            'delete': self._delete,
        }
    @property
    def create(self):
        return self._create

    @property
    def read(self):
        return self._read

    @property
    def update(self):
        return self._update

    @property
    def delete(self):
        return self._delete


class Role:
    def __init__(self, name, **permissions):
        self._name = name
        self._permissions = {}
        for key, values in self._permissions.items():
            self._permissions[key] = Permissions(**values)
    # print(self._permissions)

    def to_dict(self):

        perm = {}
        for key, value in self._permissions.items():
            print(key,value)
            perm[key] = value.to_dict()
            # print(perm[key])
            # print(f"value {perm[key] }")
        # print(perm)
        return {
            'name': self._name,
            'permissions': perm
        }


    @property
    def name(self):
        return self._name

    def __getitem__(self, key):
        return self._permissions[key]


class Entity:
    def __init__(self, entity_id, role):
        self._entity_id = entity_id
        self._role = role

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value


class User(Entity):
    def __init__(
        self, entity_id, first_name, last_name, fathers_name, date_of_birth, role
    ):
        super().__init__(entity_id, role)
        self._first_name = first_name
        self._last_name = last_name
        self._fathers_name = fathers_name
        self._date_of_birth = date_of_birth

    def to_dict(self):
        fields = {
            'entity_id': self._entity_id,
            'first_name': self._first_name,
            'last_name':  self._last_name,
            'fathers_name': self._fathers_name,
            'date_of_birth': self._date_of_birth,
            'role': self._role.to_dict()
        }
        return fields

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def fathers_name(self):
        return self._fathers_name

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @property
    def age(birth, year=2023):
        result = year - birth
        return result

class Organisation(Entity):
    def __init__(self, entity_id, creation_date, unp, name, role):
        super().__init__(entity_id, role)
        self._creation_date = creation_date
        self._unp = unp
        self._name = name

    def to_dict(self):
        fields = {
            'entity_id': self._entity_id,
            'role': self._role,
            'creation_date': self._creation_date,
            'unp': self._unp,
            'name': self._name,
        }
        return fields
    @property
    def creation_date(self):
        return self._creation_date

    @property
    def unp(self):
        return self._unp

    @property
    def name(self):
        return self._name

class App(Entity):
    def __init__(self, entity_id, name, role=None):
        super().__init__(entity_id, role)
        self._name = name

    @property
    def name(self):
        return self._name


# Функция по расчету возраста нашего пользователя.
def age(birth, year=2023):
    result = year - birth
    return result


def new_user():
    first_name = input("Input first_name: ")
    last_name = input("Input last_name: ")
    fathers_name = input("Input fathers_name: ")
    date_of_birth = input("Input date_of_birth: ")
    role_name = input("Input role_name: ")
    max_id = max([int(user_item.entity_id) for user_item in users])
    users.append(
        User(
            max_id + 1,
            first_name,
            last_name,
            fathers_name,
            date_of_birth,
            roles[role_name],
        )
    )


def save_to_file(users, organisations):
    DB = {"users": [], "organisations": []}
    for user in users:
        DB["users"].append(user.to_dict())
    for organisation in organisations:
        DB["organisations"].append(organisation.to_dict())
    with open("DataBase.json", "w") as convert_to_json:
        json.dump(DB, convert_to_json, ensure_ascii=False, indent=4)


# Создание объектов на основании данных
with open("users.json", "r", encoding="utf8") as filejson:
    users_data = json.loads(filejson.read())["Users"]
users = []
for user_data in users_data:
    user = User(
        int(user_data["entity_id"]),
        user_data["first_name"],
        user_data["last_name"],
        user_data["fathers_name"],
        int(user_data["date_of_birth"]),
        user_data['role'],
    )
    users.append(user)

with open("users.json", "r", encoding="utf8") as filejson:
    organisation_data = json.loads(filejson.read())["Organisations"]
organisations = []
for organisation_data in organisation_data:
    organization = Organisation(
            int(organisation_data["entity_id"]),
            organisation_data["role"],
            organisation_data["creation_date"],
            organisation_data["unp"],
            organisation_data["name"],
            )

organisations.append(organization)
with open("app.yaml", "r", encoding="utf8") as yamlfile:
    apps_data = yaml.load(yamlfile, Loader=yaml.FullLoader)["Apps"]
    apps = []
    for app_data in apps_data:
        app = App(int(app_data["entity_id"]), app_data["name"])
    apps.append(app)
with open("roles.yaml", "r", encoding="utf8") as yamlfile:
    roles_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    roles = {}
    for role_name, role_data in roles_data.items():
        permissions = {}
        for class_name, class_permissions in role_data.items():
            # print(class_name, class_permissions)
            permissions[class_name] = class_permissions #Permissions(**class_permissions)
            # print(permissions)
        roles[role_name] = Role(role_name, **permissions)
for user in users:
    user.role = roles[user_data["role"]]

for app in apps:
    app.role = roles[app_data["role"]]
# print(roles)
# new_user()
save_to_file(users, organisations)
