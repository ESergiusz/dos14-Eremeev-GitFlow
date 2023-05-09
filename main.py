import json
import yaml

roles = {}
organisations = []
users = []
apps = []
DB = {}

class Permissions:
    def __init__(self, create=False, read=False, update=False, delete=False):
        self._create = create
        self._read = read
        self._update = update
        self._delete = delete

    def to_dict(self):
        return {
            "create": self._create,
            "read": self._read,
            "update": self._update,
            "delete": self._delete,
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
    def __init__(self, name, permissions):
        self._name = name
        self._role = {k: Permissions(**v) for k, v in permissions.items()}
        # for key, values in permissions.items():
        #     self._role[key] = Permissions(**values)

    def to_dict(self):
        perm = {}
        for key, value in self._role.items():
            perm[key] = value.to_dict()
        return {"name": self._name, "permissions": perm}

    @property
    def name(self):
        return self._name

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
        return {
            "entity_id": self._entity_id,
            "first_name": self._first_name,
            "role": self._role.to_dict(),
            "last_name": self._last_name,
            "fathers_name": self._fathers_name,
            "date_of_birth": self._date_of_birth,
        }

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

    # @property
    # def age(birth, year=2023):
    #     result = year - birth
    #     return result

class Organisation(Entity):
    def __init__(self, entity_id, role, creation_date, unp, name):
        super().__init__(entity_id, role)
        self._creation_date = creation_date
        self._unp = unp
        self._name = name

    def to_dict(self):
        return {
            "entity_id": self._entity_id,
            "role": self._role.to_dict(),
            "creation_date": self._creation_date,
            "unp": self._unp,
            "name": self._name,
        }

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
    def __init__(self, entity_id, name, role):
        super().__init__(entity_id, role)
        self._name = name

    def to_dict(self):
        fields = {
            "entity_id": self._entity_id,
            "name": self._name,
            "role": self._role.to_dict(),
        }
        return fields

    @property
    def name(self):
        return self._name

# def age(birth, year=2023):
#     result = year - birth
#     return result

def new_user():
    first_name = input("Input first_name: ")
    last_name = input("Input last_name: ")
    fathers_name = input("Input fathers_name: ")
    date_of_birth = input("Input date_of_birth: ")
    # role_name = input("Input role_name: ")
    max_id = max([int(i.entity_id) for i in users])
    users.append(
        User(
            max_id + 1,
            first_name,
            last_name,
            fathers_name,
            date_of_birth,
            roles[user_data["role"]],
        )
    )
    with open("DataBase.json", "w") as convert_to_json:
        json.dump(DB, convert_to_json, ensure_ascii=False, indent=2)

def save_to_file(users, organisations):
    DB = {"users": [], "organisations": [], "apps": []}
    for user in users:
        DB["users"].append(user.to_dict())
    for organisation in organisations:
        DB["organisations"].append(organisation.to_dict())
    for app in apps:
        DB["apps"].append(app.to_dict())
    with open("DataBase.json", "w") as convert_to_json:
        json.dump(DB, convert_to_json, ensure_ascii=False, indent=4)

with open("roles.yaml", "r", encoding="utf8") as yamlfile:
    roles_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    for role_name, role_data in roles_data.items():
        roles[role_name] = Role(role_name, role_data)

with open("users.json", "r", encoding="utf8") as filejson:
    users_data = json.loads(filejson.read())["Users"]

    for user_data in users_data:
        user = User(
            int(user_data["entity_id"]),
            user_data["first_name"],
            user_data["last_name"],
            user_data["fathers_name"],
            user_data["date_of_birth"],
            roles[user_data["role"]],
        )
        users.append(user)

with open("users.json", "r", encoding="utf8") as filejson:
    organisations_data = json.loads(filejson.read())["Organisations"]

    for org_data in organisations_data:
        organization = Organisation(
            int(org_data["entity_id"]),
            roles[org_data["role"]],
            org_data["creation_date"],
            int(org_data["unp"]),
            org_data["name"],
        )
        organisations.append(organization)

with open("app.yaml", "r", encoding="utf8") as yamlfile:
    apps_data = yaml.load(yamlfile, Loader=yaml.FullLoader)["Apps"]

    for app_data in apps_data:
        app = App(int(app_data["entity_id"]), app_data["name"], roles[app_data["role"]])
        apps.append(app)

command = input(
    "What are you doing next? View DataBase (input view) "
    "or add new user and view DataBase (input add) ? For quit input quit: \n"
)
match command.split():
    case ["quit"]:
        print("Goodbye!")
    case ["view"]:
        save_to_file(users, organisations)
        with open('DataBase.json','r') as f:
            read_json = json.loads(f.read())
        print(read_json)
    case ["add"]:
        new_user()
        save_to_file(users, organisations)
        with open('DataBase.json','r') as f:
            read_json = json.loads(f.read())
        print(read_json)
    case _:
        print(f"Sorry, I couldn't understand {command}. Goodbye")